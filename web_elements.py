
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
class WebScraper:
    def __init__(self, cleaned_df):
        self.cleaned_df = cleaned_df
        self.driver = self._init_webdriver()

    def _init_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_soup(self, url):
        print(f"{url} is the URL being tried for get_soup")
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(4)  # Adjust time as needed
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except:
            return "Unable to find an about page"


    def social_media_links(self, page_soup):

        social_media_sites = ["facebook","instagram","twitter"]
        social_dict = {}

        for item in social_media_sites:
            try:
                web_element = page_soup.find(name="a", href=lambda href: href and f"{item}.com" in href)
                web_element_link = web_element['href']
                social_dict[item] = web_element_link
            except:
                social_dict[item] = "no link found"

        return social_dict


    def about_us_page(self, page_soup, base_url):
        # Separate the keywords related to "team" and others for prioritization
        team_keywords = ["meet-the-team", "meet-team", "our-people", "team"]
        other_keywords = ["about", "our-story", "our-process"]

        # Combine the keywords for a single iteration
        combined_keywords = team_keywords + other_keywords

        for keyword in combined_keywords:
            try:
                link = page_soup.find('a', href=lambda href: href and keyword.lower() in href.lower())
                if link and link['href']:
                    about_link = link['href']
                    # Check if the link is relative
                    if not about_link.startswith('http'):
                        if not about_link.startswith('/'):
                            about_link = base_url + '/' + about_link
                        else:# Construct the full URL
                            about_link = base_url + about_link
                    return about_link
            except:
                continue

        return "no link found"


    def calculator_page(self, page_soup, base_url):
        # Separate the keywords related to "team" and others for prioritization
        keyword = "calculator"
        try:
            web_element = page_soup.find(name="a", href=lambda href: href and f"{keyword}" in href)
            if web_element and web_element['href']:
                web_element_link = web_element['href']
                # Check if the link is relative
                if not web_element.startswith('http'):
                    # Construct the full URL
                    web_element_link = base_url + web_element_link
                return web_element_link
        except:
            return "no link found"

    def insight_page(self, page_soup, base_url):
        # Separate the keywords related to "team" and others for prioritization
        keywords = ["insight","blog","news"]
        for keyword in keywords:
            try:
                web_element = page_soup.find(name="a", href=lambda href: href and f"{keyword}" in href)
                if web_element and web_element['href']:
                    web_element_link = web_element['href']
                    # Check if the link is relative
                    if not web_element.startswith('http'):
                        # Construct the full URL
                        web_element_link = base_url + web_element_link
                    return web_element_link
            except:
                continue
        return "no link found"

    def scrape_data(self):
        entries = []
        for url in self.cleaned_df['url_clean']:
            print(f"trying URL: {url}")
            try:
                page_soup = self.get_soup(url=url)
                socials = self.social_media_links(page_soup=page_soup)
                abouts = self.about_us_page(page_soup=page_soup, base_url=url)
                calc = self.calculator_page(page_soup=page_soup, base_url=url)
                insight = self.insight_page(page_soup=page_soup, base_url=url)
                socials["about"] = abouts
                socials["calculator"] = calc
                socials["insight"] = insight
                socials["url_clean"] = url
                entries.append(socials)
            except:
                new_dict = {
                    "facebook": None,
                    "instagram": None,
                    "twitter":None,
                    "about": "go crazy write whatever you want",
                    "calculator": None,
                    "insight": None,
                    "url_clean": url
                }
                entries.append(new_dict)

        return pd.DataFrame(entries)







