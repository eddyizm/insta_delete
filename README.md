# insta_delete / insta_upload

* please see below for [insta_upload](#upload) details
  
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L01HI5A)

 Short demo on [youtube](https://youtu.be/3YaTVtTsMgY).

Selenium, BS4 powered script to delete old instagram posts.

Working with selenium can be challenging if you have no previous experience with it. Part of this project was for me to get more comfortable using selenium on an ever changing UI. 

## Updates  
Added a hard limit on profile posts to make sure it doesn't exceed a preferred minunum. Adjust the variable to make sure that quantity stays.   
```
post_counter = 500
```


## Prerequisites

Download `geckodriver` for your system [here](https://github.com/mozilla/geckodriver/releases). The script uses geckodriver after setting it in the path variables. Otherwise you can specify the specific location of the executable. 


```
browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefoxPath)
```

For more help: https://github.com/mozilla/geckodriver


## Installation

    pip install -r requirements.txt

## Usage

I updated all the environment specific stuff to a json file and a function to read the file. All I need to pass in is the file location

    CONFIG = r"/path/to/file/config.json"
    logintext = "/path/to/file/login.txt"

Config file format

    {
        "instagram": {
            "login": "<YOUR_LOGIN",
            "pass": "<YOUR_PASSWORD>"
        },
        "windows": {
            "image_path": "/path/to/files/images",
            "log_path" : "/path/to/files/media_urls.txt",
            "app_log" : "/path/to/files/insta_delete.log",
            "firefoxPath" : "/path/to/files/geckodriver.exe"
        }
    }

### Scheduled Task / Cron Tab
On my windows machine I set up a scheduled task that fires off the script via a batch file set up to activate virtual environment and append output results to log file. Linux and Mac would be just as easy using crontab.

    REM ************************************************************
    REM Batch file to run python insta_delete script
    REM ************************************************************

    @echo off
    cmd /k "cd /d /path/to/files/insta_delete/env/Scripts && activate && cd /d  /path/to/files/insta_delete/ && python insta_delete.py     

### Log File Output
Handy for debugging and keeping track of how long the scrolling takes and deleting progress. I tail this file to my dropbox or email to keep an eye on it.

    2022-08-21 13:31:58,860 | INFO | ----------------------------------------------------------------------------------------------------- 
    2022-08-21 13:31:58,861 | INFO | --------------------------------------- new session ------------------------------------------------- 
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
    2022-08-21 13:36:40,474 | INFO | --------------------------------------- end session ------------------------------------------------- 
    2022-08-21 13:36:40,474 | INFO | ----------------------------------------------------------------------------------------------------- 


## TODO
I'll be adding a few options to fine tune and make it a little more reliable.
1. Capture the date of the post in order to delete by date.
2. Get all the hyperlinks of the images in bulk, while scrolling and not the tail end.

<a name="upload"></a>
# insta_upload
