import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Settings:
    def __init__(self):
        self.insta_username = os.getenv('USERNAME')
        self.insta_password = os.getenv('PASSWORD')
        self.log_path = os.getenv('LOG_PATH')
        self.app_log = os.getenv('APP_LOG')
        self.firefox_path = os.getenv('FIREFOX_PATH')
        self.profile_path = os.getenv('PROFILE_PATH')
        self.image_path = os.getenv('IMAGE_PATH')
        self.BYPASS_NOTIFICATION_CHECKED = False
