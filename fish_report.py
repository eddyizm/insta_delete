from bs4 import BeautifulSoup, SoupStrainer
from subprocess import call, CalledProcessError
# import urllib.request
import httplib2
# import parseUrl

# variables
#downloadedFileName = "download.html"
#command = 'C:/Users/eddyizm/Documents/Apps/youtube-dl/youtube-dl.exe --download-archive C:/Users/eddyizm/Documents/Apps/youtube-dl/downloaded.txt '
video = 'http://www.22ndstreet.com/fishcounts.php'
log_path = 'C:/Users/ecervantes/source/repos/pyVirtual/venv/log.txt'
#archive  = 'C:/Users/eddyizm/Source/Repos/WebScraping/env/archive.txt'
http = httplib2.Http()
nHeaders = []
nContent = []

status, response = http.request('http://www.22ndstreet.com/fishcounts.php')

def write_header(log, title):
    with open(log, 'w+') as g:
      for h in title:
        g.write(h+'\n')
      
def write_header(log, headers, title):
    counter = 0
    with open(log, 'w+') as g:
      for t in title:
        g.write(t.text+'\n')
      for h in headers:
        if len(h) < 20 and counter < 4:
          g.write(h+' | ')
          counter +=1
      g.write('\n')

def write_data(log, data):
    with open(log, 'a+') as g:
      counter = 0
      for d in data:
        if (not d.isspace()):
          if counter >= 3:
            g.write(d+' | '+'\n')          
            counter = 0
          else:
            g.write(d+' | ')
            counter += 1

soup =  BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('tr'))

t = soup.findAll("td", {"class": "scale-title"})
h = soup.findAll("td", {"class": "scale-head"})
d = soup.findAll("td", {"class": "scale-data"})

# for title in t:
#   print (title.text)

for head in h:
  nHeaders.append(head.text)
  
for cont in d:
  nContent.append(cont.text)

write_header(log_path, nHeaders, t)
write_data(log_path, nContent)

#print (nHeaders)
#print (nContent)