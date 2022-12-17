# -*- coding: UTF-8 -*-
import json
import logging as log

from bs4 import BeautifulSoup
from models import Settings

CONFIG = r"C:\Users\eddyizm\HP\config.json"


def dump_html_to_file(driver):
    ''' used this to debug and find html changes. '''
    checkhtml = BeautifulSoup(driver.page_source, "html.parser")
    with open('debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


def get_settings() -> Settings:
    ''' get settings and return populated model '''
    settings = get_keys()
    return Settings(settings['instagram']['login'],
        settings['instagram']['pass'],
        settings['windows']['log_path'],
        settings['windows']['app_log'],
        settings['windows']['firefox_path'],
        settings['windows']['profile_path'],
        settings['windows']['image_path']
        )


def get_keys():
    with open(CONFIG, 'r') as myfile:
        keys = myfile.read()
        return json.loads(keys)

Settings = get_settings()
handlers = [log.FileHandler(Settings.app_log), log.StreamHandler()]
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', handlers = handlers, level=log.INFO)
