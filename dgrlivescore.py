from selenium import webdriver
from bs4 import BeautifulSoup
import requests as rq

def livescore(html):
    """
    Finds all urls pointed to by all links inside
    'news' class div elements
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = [span for div in soup.find_all("div", attrs={"class": "row-gray"}) for span in div.find_all('span')]
    return links


if __name__ == '__main__':

    driver = webdriver.PhantomJS()
    url = "http://www.livescore.com/"

    driver.get(url)


# This will get the initial html - before javascript
    html1 = driver.page_source

# This will get the html after on-load javascript
    html2 = driver.execute_script("return document.documentElement.innerHTML;")

    print(livescore(html2))
