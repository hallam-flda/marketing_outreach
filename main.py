from data_clean import URLStatusChecker
from web_elements import WebScraper

checker = URLStatusChecker('test_accounts.csv',n_rows=10)
checker.test_urls('url')
full_df = checker.get_dataframe()

full_df_2 = full_df.copy()
okay_link_df = full_df_2[full_df_2["status"] != 'broken website']

web_scraper = WebScraper(okay_link_df)
scraped_data = web_scraper.scrape_data()
print(scraped_data.info())  # or save this DataFrame to a file


# copy_table = cleaned_df.copy()
# good_links = copy_table[copy_table["status"] != "broken website"]
# urls = good_links["url_clean"]
#
#
# print(cleaned_df.head())
#
#
#
# from openpyxl import Workbook
# from openpyxl.utils.dataframe import dataframe_to_rows
# from openpyxl.styles import Font
#
# # Assuming another_new_df is your final DataFrame
#
# # Define your output Excel file
# output_file = 'test_output.xlsx'
#
# # Create an Excel writer using openpyxl
# writer = pd.ExcelWriter(output_file, engine='openpyxl')
#
# # Write your DataFrame to an Excel file
# another_new_df.to_excel(writer, index=False, sheet_name='Sheet1')
#
# # Load the workbook and select the first sheet
# workbook = writer.book
# worksheet = writer.sheets['Sheet1']
#
# # Iterate over the rows and format the last 5 columns as hyperlinks
# for row in worksheet.iter_rows(min_row=2, max_col=worksheet.max_column, max_row=worksheet.max_row):
#     selected_cells = [row[4]] + list(row[-5:])
#     for cell in selected_cells:
#         if cell.value != 'no link found':
#             cell.value = f'=HYPERLINK("{cell.value}", "{cell.value}")'
#             cell.font = Font(color='0000FF', underline='single')
#
# # Save the workbook
# writer.close()
