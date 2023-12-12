from datetime import datetime, timedelta
import requests
import shutil
import os
from dotenv import load_dotenv
from .constants_instagram_graphql import ConstantsInstagramAPI                  # noqa: E402
load_dotenv()

from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE)

INVALID_PROFILE_ID = -1


class Utils:

    @staticmethod
    def get_expiry() -> str:
        logger.start()
        # Get the current date
        current_date = datetime.now()

        # Calculate the date 59 days ahead (the actual expiry date is 60 days ahead)
        future_date = current_date + timedelta(days=59)

        # Convert the future date to a string in the desired format
        expiry = future_date.strftime("%Y-%m-%d")
        logger.end(object={'expiry': expiry})
        return expiry

    @staticmethod
    def download_image(image_url, local_file_name, path_to_save):
        logger.start(object={'image_url': image_url,
                     'local_file_name': local_file_name, 'path_to_save': path_to_save})
        response = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if response.status_code == requests.codes.ok:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            response.raw.decode_content = True

            file_path = os.path.join(path_to_save, local_file_name)

            # Open a local file with wb ( write binary ) permission.
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

            logger.end(object={'Image successfully downloaded: ': local_file_name})
        else:
            logger.error('Image couldn\'t be retrieved')
