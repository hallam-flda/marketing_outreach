
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

sample_url = "https://vantage-mortgages.co.uk/"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

sample_html = driver.get(sample_url)
driver.implicitly_wait(4)  # wait for 4 seconds for the page to load
web_page = driver.page_source

soup = BeautifulSoup(web_page, 'html.parser')

def social_media_links(page_soup):

    social_media_sites = ["facebook","instagram","twitter"]
    social_dict = {}

    for item in social_media_sites:
        try:
            web_element = soup.find(name="a", href=lambda href: href and f"{item}.com" in href)
            web_element_link = web_element['href']
            social_dict[item] = web_element_link
        except:
            social_dict[item] = "no link found"

    return social_dict

def page_links(page_soup):

test = social_media_links(soup)
print(test)


