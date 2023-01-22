import json
import os
from collections import namedtuple


def caption_decode(caption_dict):
    return namedtuple('X', caption_dict.keys())(*caption_dict.values())


def read_caption(file):
    with open(file, 'r') as myfile:
        text =  myfile.read()
        return text


def check_for_caption(filepath):
    '''check if folder has json info'''
    print('checking for json file')
    base_dir = os.path.dirname(filepath)
    if os.path.exists(os.path.join(base_dir, 'caption.json')):
        print(f'caption file found, returning {os.path.join(base_dir, "caption.json")}')
        return os.path.join(base_dir, 'caption.json')
    return None


def generate_caption(filepath):
    results = read_caption(filepath)
    caption = json.loads(results, object_hook=caption_decode)
    tags = ''
    for tag in caption.tags:
        tags = f'{tags}\n#{tag}'
    return f'{caption.message}{tags}'


def get_caption(image_path):
    caption_file = check_for_caption(image_path)
    if caption_file:
        return generate_caption(caption_file)
    return f'#{os.path.basename(os.path.dirname(image_path))} #eddyizm | https://eddyizm.com'
    