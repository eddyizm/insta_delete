# -*- coding: UTF-8 -*-
import json
CONFIG = r"C:\Users\eddyizm\HP\config.json"

def get_keys():
    with open(CONFIG, 'r') as myfile:
        keys = myfile.read()
        return json.loads(keys)