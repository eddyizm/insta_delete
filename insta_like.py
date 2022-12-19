# -*- coding: UTF-8 -*-
''' writing a script to like posts in my thread '''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.file_detector import UselessFileDetector
from bs4 import BeautifulSoup
from datetime import datetime

import os
import logging
import pyautogui
import pickle

import insta_base as ib

log = logging.getLogger(__name__)

def main():
    log.info(f'file directory: {ib.BASE_DIR}')


if __name__ == "__main__":
    main()
