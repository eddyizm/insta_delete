from bs4 import BeautifulSoup, SoupStrainer
from subprocess import call, CalledProcessError
# import urllib.request
import httplib2
# import parseUrl

# variables
output = " -o \"F:/%(title)s.%(ext)s\""
downloadedFileName = "download.html"
command = 'C:/Users/eddyizm/Documents/Apps/youtube-dl/youtube-dl.exe --download-archive C:/Users/eddyizm/Documents/Apps/youtube-dl/downloaded.txt '
video = 'https://www.youtube.com'
log_path = 'C:/Users/eddyizm/Source/Repos/WebScraping/env/slogin.txt'
archive  = 'C:/Users/eddyizm/Source/Repos/WebScraping/env/archive.txt'
http = httplib2.Http()
nFile = []

status, response = http.request('https://www.youtube.com')


def writeToLog(log):
    with open(log, 'w') as g:
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                #t = parseUrl.CheckUrl(link['href'])
                if t is not None:
                    g.write(t +'\n')

def DownloadVideo(videoUrl, ytcommand):
    try:
        runYT = ytcommand+videoUrl+output
        print(runYT)
        call(runYT, shell=False)    
    except CalledProcessError as e:
        print (e)

def OpenLog():
    with open(log_path, 'r') as g:
        lines = g.read()
        count = len(lines)
        return (lines, count)

def WriteToArchive(log, data):
     with open(log, 'w') as f:
         for d in data:
             f.write(d+'\n')


# process 25
# writeToLog(log_path)  

names = OpenLog()
if x.startswith("https://www.youtube.com"):
       DownloadVideo(x, command)
    

# p = count-25
#  n = open(archive,'a')
# while count > p:
#     x = lines[count-1]
#     if x.startswith("https://www.youtube.com"):
#         DownloadVideo(x, command)
#     count = count-1
#     n.write(x+'\n')    
# n.close()    
    
              
