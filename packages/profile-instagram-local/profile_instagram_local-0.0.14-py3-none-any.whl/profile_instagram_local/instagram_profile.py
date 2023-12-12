import os
from typing import Dict
import json

from dotenv import load_dotenv      # noqa: E402
load_dotenv()                       # noqa: E402

from .constants_instagram_graphql import ConstantsInstagramAPI                  # noqa: E402
from .utils import Utils                                                        # noqa: E402
from profile_local.comprehensive_profile import ComprehensiveProfilesLocal      # noqa: E402
from profile_metrics_local.profile_metrics_local import ProfileMetricsLocal     # noqa: E402
from profile_url_local.profile_url_local import UrlProfilesLocal                # noqa: E402
from user_external_local.external_user import ExternalUser                      # noqa: E402

from logger_local.Logger import Logger  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402

user_context = UserContext()
user_context.login_using_user_identification_and_password()

logger = Logger.create_logger(object=ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE)

DEFAULT_GENDER_ID = 1
DEFAULT_STARS = 0
DEFAULT_LAST_DIALOG_WORKFLOW_STATE_ID = 1

LANG_CODE_EN = user_context.get_effective_profile_preferred_lang_code()

# TODO: add method "get_profile_metrics_type_ml_id_by_name" to ProfileMetricsLocal and use it here
FOLLOWERS_COUNT_PROFILE_METRICS_TYPE_ML_ID = 2
FOLLOWS_COUNT_PROFILE_METRICS_TYPE_ML_ID = 3
MEDIA_COUNT_PROFILE_METRICS_TYPE_ML_ID = 4

# TODO: find out what is this constant for
URL_TYPE_ID = 1001
SYSTEM_ID = 3


class InstagramProfile:

    def __init__(self, instagram_profile_json: Dict[str, any]):
        self.username = instagram_profile_json['username']
        self.id = instagram_profile_json['id']
        self.name = instagram_profile_json['name']
        self.biography = instagram_profile_json['biography']
        self.website = instagram_profile_json['website']
        self.follows_count = instagram_profile_json['follows_count']
        self.followers_count = instagram_profile_json['followers_count']
        self.media_count = instagram_profile_json['media_count']
        self.profile_picture_url = instagram_profile_json['profile_picture_url']

    def insert_to_database(self):
        logger.start(object={"username": self.username, "id": self.id, "name": self.name, "biography": self.biography,
                             "website": self.website, "follows_count": self.follows_count,
                             "followers_count": self.followers_count, "media_count": self.media_count,
                             "profile_picture_url": self.profile_picture_url})

        profile_json = {
            'profile': {
                'name': self.name,
                'name_approved': True,
                'lang_code': LANG_CODE_EN,
                'user_id': None,
                'is_main': None,
                'visibility_id': True,
                'is_approved': True,
                'profile_type_id': None,
                'preferred_lang_code': None,
                'experience_years_min': None,
                'main_phone_id': None,
                'rip': None,
                'gender_id': DEFAULT_GENDER_ID,
                'stars': DEFAULT_STARS,
                'last_dialog_workflow_state_id': DEFAULT_LAST_DIALOG_WORKFLOW_STATE_ID
            },
            'storage': {
                "url": self.profile_picture_url,
                "filename": self.username + '.jpg',
                "file_type": "Profile Image"
            }
            # TODO: add biography to profile_ml_table, username to user_table
            # TODO: add id, website
        }
        profile_json_str = json.dumps(profile_json)

        profile_id = ComprehensiveProfilesLocal.insert(profile_json_str, LANG_CODE_EN)
        access_token = os.getenv("INSTAGRAM_GRAPH_IMPORT_API_ACCESS_TOKEN_LONG_TERM")
        expiry = Utils.get_expiry()
        ExternalUser.insert_or_update_user_external_access_token(self.username, profile_id, SYSTEM_ID, access_token,
                                                                 expiry=expiry)

        # TODO: add ProfileMetricsLocal.insert to ComprehensiveProfilesLocal.insert
        profile_metrics_object = ProfileMetricsLocal()
        profile_metrics_object.insert(profile_id, FOLLOWERS_COUNT_PROFILE_METRICS_TYPE_ML_ID, self.followers_count)
        profile_metrics_object.insert(profile_id, FOLLOWS_COUNT_PROFILE_METRICS_TYPE_ML_ID, self.follows_count)
        profile_metrics_object.insert(profile_id, MEDIA_COUNT_PROFILE_METRICS_TYPE_ML_ID, self.media_count)

        # TODO: add UrlProfilesLocal.insert to ComprehensiveProfilesLocal.insert
        url_profiles_object = UrlProfilesLocal()
        url_profiles_object.insert(self.website, URL_TYPE_ID, profile_id)

        logger.end()
