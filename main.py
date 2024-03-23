from data_clean import URLStatusChecker

checker = URLStatusChecker('test_accounts.csv')
checker.test_urls('url')
cleaned_df = checker.get_dataframe()

print(cleaned_df.head())