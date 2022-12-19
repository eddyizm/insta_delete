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
    result = ib.get_working_directory(__file__)
    log.info(f'file directory: {result}')
    
if __name__ == "__main__":
    main()
