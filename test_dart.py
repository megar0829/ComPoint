import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
from html_table_parser import parser_functions as parser
import xml.etree.ElementTree as ET

from requests_html import HTMLSession
from urllib.parse import urlparse
import time
import random


# =================================================================================================================
# 기업 이름 : 기업 고유 번호 저장  => company : dictionary
def find_corp_num(find_name):
    new_date = 0
    result_corp_code = ''
    for country in root.iter("list"):
        if country.findtext("stock_code") != ' ' and country.findtext("corp_name") == find_name :
            if int(country.findtext("modify_date")) > new_date:
                new_date = int(country.findtext("modify_date"))
                result_corp_code = country.findtext("corp_code")
    return result_corp_code


tree = ET.parse('CORPCODE.xml')
root = tree.getroot()
company_name = ['삼성전자','케이티','SK텔레콤','국민은행','NAVER', '우리은행','카카오','LG전자','LG유플러스','신한은행']
company = {}
for name in company_name: 
    # 기업 고유 번호 - dart 기업 정보
    company[name] = find_corp_num(name)
# =================================================================================================================


    # 부채, 자산
def load_data_financial(**kwargs):

    # dart api를 이용해서 각 기업의 가장 최신 사업보고서 rcpNo를 가져오기
    crtfc_key = 'b913de0ec72741e320cafa8e5fa18ac030699e38'
    corp_code = kwargs['corp_code']

    url_corp = f'https://opendart.fss.or.kr/api/list.json?crtfc_key={crtfc_key}&corp_code={corp_code}&bgn_de=20181019&pblntf_detail_ty=A001&date'

    read_corp = requests.get(url_corp, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})
    time.sleep(random.randint(1, 4))

    company_data = read_corp.json()

    rcpNo = company_data.get('list')[0]['rcept_no']
    
    # rcpNo를 합친 주소를 이용해서 사업보고서를 불러오고 그 안에서 
    
    url_report = f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcpNo}'
    url_dart = "https://dart.fss.or.kr{}"
    
    session = HTMLSession()
    response = session.get(url_report)
    
    response.html.render()

    src = response.html.lxml.get_element_by_id("ifrm").attrib.get("src")
    # url_detail: eleId 를 조정하며 찾게될 사업보고서의 각각의 detail 페이지
    url_detail = url_dart.format(src)
    session.close()
    url_dict = get_url(url_detail)
    
    # # 사업의 개요 parsing
    # url_1 = url_dict['사업의 개요']
    # html_1 = requests.get(url_1).content
    # soup_1 = BeautifulSoup(html_1, 'lxml')
    # content_1 = soup_1.find_all('p')
    # # 결과 출력
    # # for c in content_1:
    # #     print(c.text)
    # #     print()
            
    # # 요약재무정보 parsing
    # url_2 = url_dict['요약재무정보']
    # html_2 = requests.get(url_2).content
    # soup_2 = BeautifulSoup(html_2, 'lxml')            
            
    session.close()
    return url_dict

# =================================================================================================================

def get_url(url_detail):
    url_parsed = urlparse(url_detail)
    
    queries = url_parsed.query.split('&')
    queries_split = [x.split('=') for x in queries]
    queries_dict = {}
    for q in queries_split:
        queries_dict[q[0]] = q[1]
    
    title_number = {
        '사업의 개요': '',
        '요약재무정보': '',
        '임원 및 직원 등의 현황': ''
    }
    for num in range(9, 50):
        queries_dict['eleId'] = num
        queries = '&'.join([f'{x[0]}={x[1]}' for x in queries_dict.items()])
        url_parsed = url_parsed._replace(query=queries)
        url_page = url_parsed.geturl()
    
        html = requests.get(url_page, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}).content
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(random.randint(1, 4))

        # title_number: 보고서의 세부 항목들의 eleId 값 찾아서 저장
        if soup.find('p', {"class":"section-2"}):
            title = soup.find('p', {"class":"section-2"}).find('a').text[3:]
            
            if title == '사업의 개요' or title == '(제조서비스업)사업의 개요':
                if title_number['사업의 개요'] == '':
                    title_number['사업의 개요'] = url_page
            elif title == '요약재무정보':
                if title_number['요약재무정보'] == '':
                    title_number['요약재무정보'] = url_page
            elif title == '임원 및 직원 등의 현황':
                if title_number['임원 및 직원 등의 현황'] == '':
                    title_number['임원 및 직원 등의 현황'] = url_page
                return title_number
    
    return title_number

for name, corp_code in company.items():
    for title, url in load_data_financial(corp_code = corp_code).items(): 
        print(f'{title} : {url}')


# {'삼성전자': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230307000542&dcmNo=9040011&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  '케이티': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230323001449&dcmNo=9099288&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''(제조서비스업)사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  'SK텔레콤': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230320000235&dcmNo=9073286&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  '국민은행': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230316001101&dcmNo=9065710&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  'NAVER': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230314001049&dcmNo=9055077&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  '우리은행': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230316001052&dcmNo=9065521&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  '카카오': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230320001096&dcmNo=9077903&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''(제조서비스업)사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  'LG전자': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230317000955&dcmNo=9071929&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  'LG유플러스': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230302000615&dcmNo=9034279&eleId=1&offset=0&length=0&dtd=dart3.xsd', 
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  '신한은행': 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230315001124&dcmNo=9060124&eleId=1&offset=0&length=0&dtd=dart3.xsd'
'''사업의 개요, 요약재무정보, 임원 및 직원 등의 현황'''
#  }


# url = "https://consensus.hankyung.com/analysis/list?sdate=2018-10-01&edate=2023-10-01&now_page=1&search_value=&report_type=&pagenum=20&search_text=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&business_code="
# html = requests.get(url, headers={'User-Agent':'Gils'}).content
# soup = BeautifulSoup(html, 'lxml')
# pprint(soup)
# table = soup.find('div', {"class":"table_style01"}).find('table')
# temp = soup.find('div', {"class":"table_style01"}).find('table')