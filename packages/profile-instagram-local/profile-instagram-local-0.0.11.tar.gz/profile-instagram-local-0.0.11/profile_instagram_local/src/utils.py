import requests
import shutil

import os
from dotenv import load_dotenv
from .constants_instagram_graphql import ConstantsInstagramAPI
load_dotenv()

from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE)


class Utils:

    @staticmethod
    def download_image(image_url, local_file_name, path_to_save):
        logger.start(object={'image_url': image_url, 'local_file_name': local_file_name, 'path_to_save': path_to_save})
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