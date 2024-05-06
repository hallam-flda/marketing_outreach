import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import pgeocode
import openpyxl

# The purpose of this class is to take a website and return all the elements that may be of interest.
# If it cannot find this element, it should return nothing
# I will try and use proper error handling
# This will only work with valid URLs which should be checked in another function


sample_urls = ['https://leedsmoneyman.com/',"https://reach4mortgages.com/","https://www.themortgagecentres.co.uk/","https://imbonline.co.uk/"]

class WebsiteInfoCrawler:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.driver = self._init_webdriver()
        self.facebook_url = None
        self.twitter_url = None
        self.instagram_url = None
        self.calculator_url = None
        self.insight_url = None
        self.about_us_url = None
        self.about_us_text = None
        self.contact_us_url = None
        self.company_postcode = None
        self.company_place_name = None
        self.company_county_name = None


    def _init_webdriver(self):
        """
        initialise the webdriver
        :return: driver for browsing website
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def obtain_url_soup(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(4)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def obtain_social_media_links(self):

        social_media_sites = ["facebook", "twitter", "instagram"]
        social_dict = {}

        for social in social_media_sites:
            try:
                page_soup = self.soup
                # For some reason you cannot call self.soup.find all in one go
                # Look up the reason for this but reverting to naming it first worked
                element = page_soup.find(name="a", href=lambda href: href and f"{social}.com" in href)
                page_soup_link = element['href']
                social_dict[social] = page_soup_link
            except Exception as e:
                social_dict[social] = None
                print(e)

        self.facebook_url = social_dict["facebook"]
        self.twitter_url = social_dict["twitter"]
        self.instagram_url = social_dict["instagram"]

    def obtain_additional_links(self):

        additional_sites = ["calculator","insight"]
        additional_dict = {}

        for site in additional_sites:

                page_soup = self.soup
                element = page_soup.find(name="a", href=lambda href: href and f"{site}" in href)
                if element is None:
                    additional_dict[site] = None
                else:
                    page_soup_link = element['href']

                    if not page_soup_link.startswith("https://"):
                        additional_dict[site] = self.url + page_soup_link
                    else:
                        additional_dict[site] = page_soup_link

        self.calculator_url = additional_dict["calculator"]
        self.insight_url = additional_dict["insight"]

    def obtain_about_us_link(self):
        about_phrases = ["meet-the-team", "the-team", "our-team", "our-people", "meet-us", "who-we-are","about-us","about"]

        for phrase in about_phrases:
            try:
                page_soup = self.soup
                element = page_soup.find(name="a", href=lambda href: href and f"{phrase}" in href)
                page_soup_link = element['href']
                # checking for relative url paths
                if not page_soup_link.startswith("https://"):
                    self.about_us_url = self.url[:-1] + page_soup_link
                else:
                    self.about_us_url = page_soup_link
                break
            except:
                self.about_us_url = None


    def obtain_about_us_text(self):
        if self.about_us_url:
            about_us_link = self.about_us_url
            self.driver.get(about_us_link)
            self.driver.implicitly_wait(4)
            about_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            paragraphs = about_soup.find_all('p')
            p_texts = []
            for p in paragraphs:
                paragraph_text = p.get_text()
                p_texts.append(paragraph_text)
            full_text = ' '.join(p_texts[:5])
            self.about_us_text = full_text
        else:
            self.about_us_text = None


    def obtain_contact_us_url(self):
        contact_phrases = ["contact-us", "contact"]

        for phrase in contact_phrases:
            try:
                page_soup = self.soup
                element = page_soup.find(name="a", href=lambda href: href and f"{phrase}" in href)
                page_soup_link = element['href']
                # checking for relative url paths
                if not page_soup_link.startswith("https://"):
                    self.contact_us_url = self.url[:-1] + page_soup_link
                else:
                    self.contact_us_url = page_soup_link
                break
            except:
                self.contact_us_url = None

    def obtain_company_address(self):

        # Postcode setting
        if self.contact_us_url:
            contact_us_link = self.contact_us_url
            self.driver.get(contact_us_link)
            self.driver.implicitly_wait(4)
            contact_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            s = contact_soup.get_text()
            postcode_list = re.findall(r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}', s)
            if postcode_list:
                postcode = max(set(postcode_list), key=postcode_list.count)
                self.company_postcode = postcode
            else:
                self.company_postcode = None
        else:
            self.company_postcode = None

        # Address finding from postcode
        if self.company_postcode:
            nomi = pgeocode.Nominatim('gb')
            self.company_place_name = nomi.query_postal_code(self.company_postcode).place_name
            self.company_county_name = nomi.query_postal_code(self.company_postcode).county_name





    def close(self):
        """
        Close the WebDriver to release resources.
        """
        self.driver.quit()


detail_list = []

for url in sample_urls:
    crawler = WebsiteInfoCrawler(url)
    crawler.obtain_url_soup()
    crawler.obtain_social_media_links()
    crawler.obtain_additional_links()
    crawler.obtain_about_us_link()
    crawler.obtain_about_us_text()
    crawler.obtain_contact_us_url()
    crawler.obtain_company_address()
    # print(crawler.twitter_url)
    # print(crawler.facebook_url)
    # print(crawler.instagram_url)
    # print(crawler.calculator_url)
    # print(crawler.insight_url)
    # print(crawler.about_us_url)
    # print(crawler.about_us_text)
    # print(crawler.contact_us_url)
    # print(crawler.company_postcode)
    # print(crawler.company_place_name)
    # print(crawler.company_county_name)
    new_dict = {
        "url": crawler.url,
        "twitter_url": crawler.twitter_url,
        "facebook_url": crawler.facebook_url,
        "instagram_url": crawler.instagram_url,
        "calculator_url": crawler.calculator_url,
        "insight_url": crawler.insight_url,
        "about_us_url": crawler.about_us_url,
        "about_us_text": crawler.about_us_text,
        "company_postcode": crawler.company_postcode,
        "company_place_name": crawler.company_place_name,
        "company_county_name": crawler.company_county_name
    }
    crawler.close()
    detail_list.append(new_dict)

df = pd.DataFrame(detail_list)

web_element_file = 'web_element_revised_test.xlsx'
writer = pd.ExcelWriter(web_element_file, engine='openpyxl')
df.to_excel(writer, index=False, sheet_name='Sheet1')
workbook = writer.book
worksheet = writer.sheets['Sheet1']
writer.close()





