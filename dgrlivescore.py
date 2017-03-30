from selenium import webdriver
from bs4 import BeautifulSoup
import requests as rq
import re

def livescore(html):
    """
    Finds all urls pointed to by all links inside
    'news' class div elements
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = [span for div in soup.find_all("div", attrs={"class": "row-gray"}) for span in div.find_all('span')]
    return links

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

if __name__ == '__main__':

    driver = webdriver.PhantomJS()
    url = "http://www.livescore.com/soccer/england/premier-league/"

    driver.get(url)


# This will get the initial html - before javascript
    html1 = driver.page_source

# This will get the html after on-load javascript
    html2 = driver.execute_script("return document.documentElement.innerHTML;")  
    rowdata = livescore(html2)
    i = 1
    message = ""
    listmatch = []
    for d in rowdata:

        data = cleanhtml(str(d))

        if not data.startswith('__') and data != "Limited coverage":
            message = message + " " + data

        if i % 7 == 0:
            if len(message.strip()) > 3 and "-" in message:
                listmatch.append(str(message.lstrip()))

            message = ""

        i += 1
    
    for l in sorted(listmatch, reverse=True):
        print(l)
