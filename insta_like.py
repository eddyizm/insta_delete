# -*- coding: UTF-8 -*-
''' writing a script to like posts in my thread '''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.file_detector import UselessFileDetector
from bs4 import BeautifulSoup
from datetime import datetime
import insta_base as ib
import insta_upload as iu

import logging

log = logging.getLogger(__name__)


def main():
    log.info(f'file directory: {ib.BASE_DIR}')
    # iu.main()
    file, tag = iu.get_images(ib.Settings.image_path)
    log.info(file)
    log.info(tag)

if __name__ == "__main__":
    main()
