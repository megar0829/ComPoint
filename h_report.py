from bs4 import BeautifulSoup
import requests
import pandas as pd
from html_table_parser import parser_functions as parser
from pprint import pprint

# 한경 컨센서스 레포트 가져오기
url_h = "https://consensus.hankyung.com/analysis/list?sdate=2018-10-01&edate=2023-10-01&now_page=1&search_value=&report_type=&pagenum=20&search_text=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&business_code="
html_h = requests.get(url_h, headers={'User-Agent':'Gils'}).content
soup_h = BeautifulSoup(html_h, 'lxml')

temp_head = soup_h.find('div', {"class":"table_style01"}).find('thead').get_text().strip('\n').split('\n')
temp_body = soup_h.find('div', {"class":"table_style01"}).find('tbody').get_text().strip('\n').split('\n')

report_body = [[]]
cnt = 0
for body in temp_body:
    if body != '' and body != ' ':
        report_body[cnt].append(body)
        if body[-2:] == '증권':
            cnt += 1
            report_body.append([])
report_body.pop()

body_len = len(report_body)
for idx in range(body_len):
    report_body[idx].pop(2)
    report_body[idx][3:-2]
    # print('작성일 : ', report_body[idx][0])
    # print('분류 : ', report_body[idx][1])
    # print('제목 : ', report_body[idx][2])
    # print('소제목 : ', report_body[idx][3:-2])
    # print('작성자 : ', report_body[idx][-2])
    # print('제공출처 : ', report_body[idx][-1])
    # print('--------------------------------')
    
    

# for i in temp_body:
#     print(i)
# pprint(df)
# print()
# pprint(p1)
# print()
# pprint(df1)