
from openai import OpenAI
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

from bs4 import BeautifulSoup
import requests

df = pd.read_csv("test_output.csv")
new_df = df.copy().dropna()

new_df = new_df[(new_df["about"] != 'no link found') & (new_df["about"] != '')]
print(new_df['about'][0:5])

url_list = list(new_df["about"])

print(url_list)



def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def find_paragraphs_with_keyword(soup, keywords, limit=3):
    paragraphs = soup.find_all('p')
    matched_paragraphs = []
    for paragraph in paragraphs:
        if any(keyword.lower() in paragraph.text.lower() for keyword in keywords):
            matched_paragraphs.append(paragraph.text)
            if len(matched_paragraphs) == limit:  # Stop after finding 'limit' number of paragraphs
                break
    return ' '.join(matched_paragraphs) if matched_paragraphs else "Keyword not found in any <p> tag."

# Example usage

keywords = ["founded","since","family","experience","run","established","years"]
about_texts = []

for url in url_list:
    soup = get_soup(url)
    founded_text = find_paragraphs_with_keyword(soup, keywords, limit=5)
    about_texts.append(founded_text)
    print(f"for {url}: {founded_text}")



CHAT_GPT_INSTRUCTION = '''
compliment the business and make specific mention to some of the topics they mention in the text. 
Use a casual tone, you are british so don't use american phrases or terminology. 
If a place name is mentioned, say you visited a few years ago and loved the area, make specific reference to a venue or location in the place.
 Keep your response to two sentences and ask a question that encourages a response. Do not use people's names in your response:
'''



client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"
response_data = []

for url in url_list:
    soup = get_soup(url)
    founded_text = find_paragraphs_with_keyword(soup, keywords, limit=5)
    print(f"trying{url}")
    if founded_text != "Keyword not found in any <p> tag.":
        # Replace the next line with your actual API call
        chatgpt_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CHAT_GPT_INSTRUCTION},
                {"role": "user", "content": founded_text}
            ],
            temperature=1,
        )
        chatgpt_text = chatgpt_response.choices[0].message.content
    else:
        chatgpt_text = ''

    print(chatgpt_text)

    # Append a dictionary with the URL, the text found, and the ChatGPT text
    response_data.append({
        'url': url,
        'founded_text': founded_text,
        'chatgpt_text': chatgpt_text
    })


response_df = pd.DataFrame(response_data)
response_df = response_df.rename(columns={'url': 'about'})
merged_df = pd.merge(new_df, response_df, on='about', how='left')
merged_df.to_csv("chatgpt4_test_2.csv")