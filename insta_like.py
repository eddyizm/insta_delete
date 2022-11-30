# -*- coding: UTF-8 -*-
''' writing a script to like posts in my thread '''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.file_detector import UselessFileDetector
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pyautogui
import pickle
from insta_upload import  login_to_site, return_randomtime
from insta_delete import get_keys


def main():
    settings = get_keys()
    driver = login_to_site()


if __name__ == "__main__":
    main()
