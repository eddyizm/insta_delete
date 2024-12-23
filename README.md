# insta_delete / insta_upload / insta_like

insta_delete status: working | 12/27/2022  

* please see below for  
> [insta_upload](#upload)  
> [insta_like](#like) 
  
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L01HI5A)

 Short demo on [youtube](https://youtu.be/3YaTVtTsMgY).

Selenium, BS4 powered script to delete old instagram posts, upload new images, and like posts in my feed.

Working with selenium can be challenging if you have no previous experience with it. Part of this project was for me to get more comfortable using selenium on an ever changing UI. 

## Prerequisites

Download `geckodriver` for your system [here](https://github.com/mozilla/geckodriver/releases). The script uses geckodriver after setting it in the path variables. Otherwise you can specify the specific location of the executable. You also need firefox installed unless you are going to be using chromedriver, in which case you will probably need a chrome based browser eg. Brave, Edge or Chrome. 

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz

# Replace v0.35.0 with the actual Geckodriver version you need.
tar -xvzf  geckodriver-v0.35.0-linux-aarch64.tar.gz

chmod +x geckodriver 

sudo mv geckodriver /usr/local/bin/ 

geckodriver --version
```

```
browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefox_path)
```

For more help: https://github.com/mozilla/geckodriver


## Installation

This guide assumes you already have python 3 and git installed.  

Clone repository  

    git clone https://github.com/eddyizm/insta_delete.git  

Create a virtual environment  

    cd <newly cloned git repo>
    python -m venv env

Activate virtual environment and install requirements

    # using git bash
    source env/Scripts/activate  
    pip install -r requirements.txt

## Config

~~I updated all the environment specific stuff to a json file and a function to read the file. All I need to pass in is the file location~~

Swapped in `python-dotenv` to remove the json path and use `.env`
in your root directory


env file. Fill out your settings here. This file does not get checked in. New `config.py` file loads the settings from the environment.

```
USERNAME=
PASSWORD=
LOG_PATH=
APP_LOG=
FIREFOX_PATH=/path_to_driver/env/geckodriver.exe
PROFILE_PATH=/path_to/AppData/Roaming/Mozilla/Firefox/Profiles/1gzgq8je.default-release
IMAGE_PATH=
OS=
```

### Scheduled Task / Cron Tab
On my windows machine I set up a scheduled task that fires off the script via a batch file set up to activate virtual environment using git bash. 

    #!/bin/bash

    # calling insta scripts via shell file. 
    source <PATH TO CODE>/insta_delete/env/Scripts/activate
    python <PATH TO CODE>/insta_delete/<script name> # eg insta_upload.py

### Logs
For debugging and keeping track of progress. All the scripts share the same log and are delinated with their filename as a sesion. Note that the scripts can run concurrently on separate threads and log to the same file. That is interesting and not intended. 

    2022-08-21 13:31:58,860 | INFO | ----------------------------------------------------------------------------------------------------- 
    2022-08-21 13:31:58,861 | INFO | start insta_delete.py session -------------------
    2022-08-21 13:31:58,862 | INFO | ----------------------------------------------------------------------------------------------------- 
    2022-08-21 13:31:58,862 | INFO | file size: 3131
    2022-08-21 13:31:58,862 | INFO | logging in as mobile device to delete
    2022-08-21 13:32:15,469 | INFO | found username element: <selenium.webdriver.remote.webelement.WebElement (session="2bcb2e52-f7de-4343-a9b9-bc477e63bb9d", element="2eb1be44-2dd4-4533-bc80-3f7a7a727491")>
    2022-08-21 13:32:41,432 | INFO | length of file: 45
    2022-08-21 13:32:41,432 | INFO | counter: 10
    2022-08-21 13:32:41,432 | INFO | DELETING POSTS!
    2022-08-21 13:32:41,433 | INFO | getting new url: https://www.instagram.com/p/CZw-ODmpXjL/
    2022-08-21 13:33:03,334 | INFO | POST DELETED: https://www.instagram.com/p/CZw-ODmpXjL/
    2022-08-21 13:33:03,334 | INFO | getting new url: https://www.instagram.com/p/CZzQdEHFT00/
    2022-08-21 13:33:25,290 | INFO | POST DELETED: https://www.instagram.com/p/CZzQdEHFT00/
    2022-08-21 13:33:25,290 | INFO | getting new url: https://www.instagram.com/p/CZ10sjyFgMV/
    2022-08-21 13:33:46,994 | INFO | POST DELETED: https://www.instagram.com/p/CZ10sjyFgMV/
    2022-08-21 13:33:46,995 | INFO | getting new url: https://www.instagram.com/p/CZ4aUIVFSnN/
    2022-08-21 13:34:08,289 | INFO | POST DELETED: https://www.instagram.com/p/CZ4aUIVFSnN/
    2022-08-21 13:34:08,289 | INFO | getting new url: https://www.instagram.com/p/CZ6-z_FFile/
    2022-08-21 13:34:29,830 | INFO | POST DELETED: https://www.instagram.com/p/CZ6-z_FFile/
    2022-08-21 13:34:29,831 | INFO | getting new url: https://www.instagram.com/p/CZ9fNDclq1o/
    2022-08-21 13:34:51,532 | INFO | POST DELETED: https://www.instagram.com/p/CZ9fNDclq1o/
    2022-08-21 13:34:51,533 | INFO | getting new url: https://www.instagram.com/p/CaAIwjiFHx7/
    2022-08-21 13:35:12,983 | INFO | POST DELETED: https://www.instagram.com/p/CaAIwjiFHx7/
    2022-08-21 13:35:12,984 | INFO | getting new url: https://www.instagram.com/p/CaCs5lClleg/
    2022-08-21 13:35:34,654 | INFO | POST DELETED: https://www.instagram.com/p/CaCs5lClleg/
    2022-08-21 13:35:34,654 | INFO | getting new url: https://www.instagram.com/p/CaFSDqvlBOA/
    2022-08-21 13:35:56,133 | INFO | POST DELETED: https://www.instagram.com/p/CaFSDqvlBOA/
    2022-08-21 13:35:56,133 | INFO | getting new url: https://www.instagram.com/p/CaH16QZl89n/
    2022-08-21 13:36:17,632 | INFO | POST DELETED: https://www.instagram.com/p/CaH16QZl89n/
    2022-08-21 13:36:17,632 | INFO | getting new url: https://www.instagram.com/p/CaM788KFQag/
    2022-08-21 13:36:39,084 | INFO | POST DELETED: https://www.instagram.com/p/CaM788KFQag/
    2022-08-21 13:36:39,085 | INFO | while loop done and exited successfully
    2022-08-21 13:36:39,086 | INFO | 2022-08-21 13:36:39
    2022-08-21 13:36:40,473 | INFO | ----------------------------------------------------------------------------------------------------- 
    2022-08-21 13:36:40,474 | INFO | end insta_delete.py session -------------------
    2022-08-21 13:36:40,474 | INFO | ----------------------------------------------------------------------------------------------------- 


<a name="upload"></a>
# insta_upload

Status: working | 12/27/2022

<a name="like"></a>
# insta_like

Status: working |  01/02/2023. finally got a loop working, tested 4 likes. 

join me on discord (eddyizm#3389) to discuss features/todos or open an issue...

## TODO
I'll be adding a few options to fine tune and make it a little more reliable.
* Capture the date of the post in order to delete by date.
* Add a hard limit on profile posts to make sure it doesn't exceed a preferred mininum. Adjust the variable to make sure that quantity stays.  
* Get all the hyperlinks of the images in bulk, while scrolling and not the tail end.
* Create a cli entry point to control and call the 3 different automations, possibly mixing them up and passing variables.  