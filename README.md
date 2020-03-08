# insta_delete / insta_upload

* please see below for [insta_upload](#upload) details

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L01HI5A)

Selenium, BS4 powered script to delete old instagram posts.

Working with selenium can be challenging if you have no previous experience with it. Part of this project was for me to get more comfortable using selenium on an ever changing UI. 

## Updates  
Added a hard limit on profile posts to make sure it doesn't exceed a preferred minunum. Adjust the variable to make sure that quantity stays.   
```
post_counter = 500
```


## Prerequisites

Download ```chromedriver``` for your system [from here](https://sites.google.com/a/chromium.org/chromedriver/downloads). The script uses chromedriver after setting it in the path variables. Otherwise you can specify the specific location of the executable. 

If chromedriver is not specified in your environ, replace the code
```
browser = webdriver.Chrome()
```
with 
```
browser = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
```

See the getting started page for more help: http://chromedriver.chromium.org/getting-started


## Installation

    pip install -r requirements.txt

## Usage

I set up variables to store the URLS and account information. 

    log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
    logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"

These will need to be replaced with local paths for your system. 
The login.txt should be split into two lines:

    USERNAME
    PASSWORD

Other wise you can comment out the file open portion and replace the ```login[0]``` values with your credentials:

    #f = open (logintext, 'r')
    #login = f.read().splitlines()
    #f.close()
    insta_username = USERNAME
    insta_password = PASSWORD

### Scheduled Task / Cron Tab
On my windows machine I set up a scheduled task that fires off the script via a batch file set up to activate virtual environment and append output results to log file. Linux and Mac would be just as easy using crontab.

    REM ************************************************************
    REM Batch file to run python script
    REM ************************************************************

    @echo off
    cmd /k "cd /d C:\Users\eddyizm\Source\Repos\seleniumTesting\env\Scripts && activate && cd /d  C:\Users\eddyizm\Source\Repos\seleniumTesting && python insta_delete.py >> C:\Users\eddyizm\Source\Repos\seleniumTesting\env\log.txt"      

### Log File Output
Handy for debugging and keeping track of how long the scrolling takes and deleting progress. I tail this file to my dropbox or email to keep an eye on it.

    ----------------------------------------------------------------------------------------------------- 
    --------------------------------------- new session ------------------------------------------------- 
    2018-08-07 11:00:18
    ----------------------------------------------------------------------------------------------------- 
    file size: 0
    file empty, going to scroll
    2018-08-07 11:00:22
    scrolling profile to get more urls
    scrolled down: 617 times!
    2018-08-07 12:43:22
    logging in as mobile device to delete
    2018-08-07 12:43:28
    length of file: 30
    counter: 15
    DELETING POSTS!
    2018-08-07 12:43:59
    POST DELETED: https://www.instagram.com/p/NJM0L/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NLNSX/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NOkLl/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NO2KG/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NPJCZ/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NPSq-/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NPS6H/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NUlgG/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NUnRd/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NX6FM/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NYC8u/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NZL_R/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NcgTf/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NcqAb/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NdS2T/?taken-by=eddyizm
    POST DELETED: https://www.instagram.com/p/NdwvP/?taken-by=eddyizm
    while loop done and exited successfully
    2018-08-07 12:55:06
    ----------------------------------------------------------------------------------------------------- 
    2018-08-07 12:55:08
    --------------------------------------- end session ------------------------------------------------- 
    -----------------------------------------------------------------------------------------------------

## TODO
I'll be adding a few options to fine tune and make it a little more reliable.
1. Capture the date of the post in order to delete by date.
2. Get all the hyperlinks of the images in bulk, while scrolling and not the tail end.

<a name="upload"></a>
# insta_upload
