import os
import requests
import http
from .constants_instagram_graphql import ConstantsInstagramAPI
from dotenv import load_dotenv  # noqa: E402
load_dotenv()                   # noqa: E402

from user_context_remote.user_context import UserContext  # noqa: E402
from user_external_local.external_user import ExternalUser                      # noqa: E402
from logger_local.Logger import Logger  # noqa: E402


FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v17.0/"


INSTAGRAM_GRAPH_IMPORT_API_COMPONENT_ID = 158

logger = Logger.create_logger(object=ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE)

user_context = UserContext().login_using_user_identification_and_password()

# Imports data from Businesses and Creators on Instagram.


class InstagramAPI:

    def __init__(self, circlez_username: str = None, system_id: int = None):
        logger.start(object={"circlez_username": circlez_username, "system_id": system_id})
        if circlez_username is not None and system_id is not None:
            access_token_tuple = ExternalUser.get_access_token_by_username_and_system_id(
                circlez_username, system_id)
            self.access_token = access_token_tuple[0]
        else:
            self.access_token = os.getenv("INSTAGRAM_GRAPH_IMPORT_API_ACCESS_TOKEN_LONG_TERM")

    # requires permission from our user
    # doesn't require permission from the user for discovery
    def get_data_by_instagram_username(self, circlez_user_id, instagram_username_for_discovery):
        logger.start(object={"circlez_user_id": circlez_user_id,
                     "instagram_username_for_discovery": instagram_username_for_discovery})
        url = (FACEBOOK_GRAPH_URL + circlez_user_id +
               "?fields=business_discovery.username(" + instagram_username_for_discovery + ")" +
               '{' + "id,username,name,biography,website,follows_count,followers_count,media_count,profile_picture_url" + '}' +
               "&access_token=" + self.access_token)
        headers = {'Content-Type': 'application/json'}
        api_response = requests.get(url=url, headers=headers)
        result = self.__process_response(api_response, True)
        logger.end({"result": result})
        return result

    # generates a long-lived access token
    def get_long_lived_access_token(self, access_token: str) -> str:
        url = FACEBOOK_GRAPH_URL + "oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": os.getenv("INSTAGRAM_APP_ID"),
            "client_secret": os.getenv("INSTAGRAM_APP_SECRET"),
            "fb_exchange_token": access_token
        }

        response = requests.get(url, params=params)
        long_lived_token = response.json()['access_token']
        return long_lived_token

    # requires user's permission
    def get_data_by_instagram_user_id(self, user_id):
        logger.start(object={"user_id": user_id})
        url = (FACEBOOK_GRAPH_URL + user_id +
               f"?fields=id,username,name,biography,website,follows_count,followers_count,media_count,"
               f"profile_picture_url"
               f"&access_token={self.access_token}")
        headers = {'Content-Type': 'application/json'}
        api_response = requests.get(url=url, headers=headers)
        result = self.__process_response(api_response, False)
        logger.end({"result": result})
        return result

    # requires user's permission'
    def get_data_by_facebook_page_id(self, page_id):
        logger.start(object={"page_id": page_id})
        url = FACEBOOK_GRAPH_URL + page_id + f"?fields=instagram_business_account&access_token={self.access_token}"
        headers = {'Content-Type': 'application/json'}
        api_response = requests.get(url=url, headers=headers)
        if api_response.status_code == http.HTTPStatus.OK:
            page_data = api_response.json()
            instagram_id = page_data['instagram_business_account']['id']
            logger.info(object={'instagram_id': instagram_id})
            result = self.get_data_by_instagram_user_id(instagram_id)
            logger.end(object={"result": result})
            return result
        else:
            logger.error("Error occurred while fetching page data from Instagram Graph")
            return None

    def __process_response(self, api_response, is_business_discovery):
        if api_response.status_code == requests.codes.ok:
            user_data = api_response.json()
            if is_business_discovery:
                result = user_data['business_discovery']
            else:
                result = user_data
            return result
        else:
            logger.error("Error occurred while fetching user data from Instagram Graph")
            return None
