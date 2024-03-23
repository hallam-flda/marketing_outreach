import pandas as pd
import requests

# Required to not return 403 errors, where the website refuses to acknowledge requests without a user agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# import the file
a = pd.read_csv("test_accounts.csv", nrows=30)

# drop the null columns in the column axis
a.dropna(axis=1, inplace=True)
a.info()


def test_urls(dataframe, url_column_name):
    """ args: dataframe and the name of the column that contains the url"""
    status_list = []
    for url in dataframe[url_column_name]:
        url_clean = "http://"+url
        try:
            response = requests.get(url = url_clean, headers=headers, timeout=10)
            status_list.append("working" if response.ok else "broken website")
        except:
            response = "broken website"
            status_list.append(response)
    status_df = pd.DataFrame({url_column_name: dataframe[url_column_name], "status": status_list})
    return status_df


url_status_df = test_urls(a, "url")
a_status = pd.merge(a, url_status_df, on = "url")

print(a_status.head())





