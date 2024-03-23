
from openai import OpenAI
import os


sample_about = '''
Gulf Coast Finance was established in 2016 by current CEO. Having worked in the finance industry in the UK and Dubai he had a desire to break out in order to offer simplicity, honesty, and integrity amongst the complexities of the rapid growth and expansion in the region. From its birth Gulf Coast Finance was designed to put the client at the center. It was to be the service of choice and grew from one good recommendation to the next. Personalization and transparency are at the heart of everything we do.

Having established a loyal client base in the Middle East, Gulf Coast Finance recognized the needs of those clients were evolving and grew connections with established partners to build a base in Africa. Our second office lies in the hub of economic growth and development in Lagos to serve the needs of those wishing to finance on the continent. Following that we went back to our roots to put our firm footing in the bustling and new powerhouse of the UK, Manchester. Our office is in the center of the exciting expansion and vibrant rejuvenation of this iconic UK city. With these solid bases to service our diverse clientele we are in a unique and advantageous position to become the best in our field.

From humble beginnings of offering straightforward mortgage advice to now meeting the needs of a myriad of client needs including project finance, investment, UK visas, and international business solutions. Whether you need to finance in Africa, the Middle East, or the UK we have the network, the expertise, and the knowledge to find what works for you. We will guarantee that we will offer you our undivided attention and to ensure you get a professional service we offer you a dedicated consultant who will work your case from start to completion. We work closely with you, the lenders, developers, and legal teams to ensure trust and confidence in the process. We look forward to building our relationship with you
'''

CHAT_GPT_INSTRUCTION = '''
You are a master content reviewer, your job is to write a compliment about the text you receive and return a one line comment followed by a question that elicits a response. 
When referring to the company in the text you should refer to the business as 'you' and 'your' rather than a separate entity. Do not return a line break in any response.
Try to not be too verbose, shorter comments are preferred
'''


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system",
         "content":  f"{CHAT_GPT_INSTRUCTION}"},
        {"role": "user", "content": f"{sample_about}"}
    ],
    temperature=0,
)

print(response.choices[0].message.content)

