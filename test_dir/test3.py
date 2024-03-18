import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
from html_table_parser import parser_functions as parser

url = "https://consensus.hankyung.com/analysis/list?sdate=2018-10-01&edate=2023-10-01&now_page=1&search_value=&report_type=&pagenum=20&search_text=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&business_code="
html = requests.get(url, headers={'User-Agent':'Gils'}).content
soup = BeautifulSoup(html, 'lxml')
# pprint(soup)
# table = soup.find('div', {"class":"table_style01"}).find('table')
temp = soup.find('div', {"class":"table_style01"}).find('table')
# pprint(temp)
# # pprint(table)
# first = table.find("tr", {"class":"first"})
# date = first.find("td", {"class":"first txt_number"})
# title = first.find("td", {"class":"text_l"})
# author = first.find("td")
# ref = first.find("td")
# report_url = 'https://consensus.hankyung.com' + first.find("a")["href"]
# print(report_url)

p = parser.make2d(temp)
for t in p:
    print(*t)
# pprint(p)
df = pd.DataFrame(p[:], columns=p[0])
# print(df)

# print(date.text)
# print(title.text.split('\n')[1])
# print(first.text.split('\n')[-7])
# print(first.text.split('\n')[-6])
