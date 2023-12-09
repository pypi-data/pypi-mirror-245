import requests
import http
from .constants_instagram_graphql import ConstantsInstagramAPI
from dotenv import load_dotenv  # noqa: E402
load_dotenv()                   # noqa: E402

from logger_local.Logger import Logger  # noqa: E402


FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v17.0/"

# Temporary access token for testing purposes
INSTAGRAM_GRAPH_IMPORT_API_ACCESS_TOKEN = (
    "EAAUdpG5aRPYBO4jP4hwuKcM1ZA2vrEsL1yZBaNB4CXaFrRsEFZCbW0vElS5Gs28FgU" +
    "XvbO1smSEvMTPqg8DDkmyezsAn5Mrbdb0F5DQKrj5UmZCUZAWLFUnf99IPHOjdogK19" +
    "UfSmk85VGrmhNhdJZCe4rhDBjpz7qYLFZAtZBKR82OJZCqDIDZBEZB8ju4YwCnSCl2T" +
    "ZBnAyXCZAVAswr4hIHqP1TJwY9lPDqrK5l8tKy1gA8vMZD"
)

# NOTE: Remember to replace all the above variables with your actual values
# before moving to a production environment. Never commit or expose your
# sensitive data (like access_token, appSecret) in your version control system.

INSTAGRAM_GRAPH_IMPORT_API_COMPONENT_ID = 158

obj = ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE


logger = Logger.create_logger(object=ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE)

# Imports data from Businesses and Creators on Instagram.


class InstagramAPI:

    def __init__(self):
        # TODO: Get access token from environment variable
        # self.access_token = os.getenv("INSTAGRAM_GRAPH_IMPORT_API_ACCESS_TOKEN")
        self.access_token = INSTAGRAM_GRAPH_IMPORT_API_ACCESS_TOKEN

    # requires permission from our user
    # doesn't require permission from the user for discovery
    def get_data_by_instagram_username(self, circlez_user_id, instagram_username_for_discovery):
        logger.start({"circlez_user_id": circlez_user_id,
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
