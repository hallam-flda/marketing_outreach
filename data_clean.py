import pandas as pd
import requests

class URLStatusChecker:
    def __init__(self, csv_file, n_rows=30):
        """ Default at 30 rows for testing"""
        # Required to not return 403 errors, where the website refuses to acknowledge requests without a user agent
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        self.dataframe = pd.read_csv(csv_file, nrows=n_rows)
        self.dataframe.dropna(axis=1, inplace=True)


    def test_urls(self, url_column_name):
        """ args: dataframe and the name of the column that contains the url"""
        status_list = []
        clean_url_list = []
        for url in self.dataframe[url_column_name]:
            url_clean = "http://"+url
            try:
                response = requests.get(url = url_clean, headers=self.headers, timeout=10)
                status_list.append("working" if response.ok else "broken website")
                clean_url_list.append(url_clean)
            except:
                response = "broken website"
                status_list.append(response)
                clean_url_list.append(url_clean)
        status_df = pd.DataFrame({url_column_name: self.dataframe[url_column_name], "status": status_list, "url_clean": clean_url_list})
        self.dataframe = pd.merge(self.dataframe, status_df, on=url_column_name)

    def get_dataframe(self):
        return self.dataframe




