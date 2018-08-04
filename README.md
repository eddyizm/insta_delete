# insta_delete
Selenium, BS4 powered script to delete old instagram posts.

Working with selenium can be challenging if you have no previous experience with it. Part of this project

## Prerequisites

Make sure you have chromedriver installed. The script uses chromedriver after setting it in the path variables. Otherwise you can specify the specific location of the executable. 

If chromedriver is not specified in your environ, replace the code
```
browser = webdriver.Chrome()
```
with 
```
brwoser = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
```

See the getting started page for more help: http://chromedriver.chromium.org/getting-started


## Installation

    pip install -r requirements.txt
