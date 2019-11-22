from bs4 import BeautifulSoup as bs
import os
import urllib.request
image_url = ""
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}

request=urllib.request.Request(image_url, None,headers)
response = urllib.request.urlopen(request)
data = response.read()
content = bs(data, "html.parser")
print(content)
