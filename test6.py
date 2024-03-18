from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd
from html_table_parser import parser_functions as parser
import xml.etree.ElementTree as ET
from datetime import datetime
from django.utils.dateparse import parse_datetime
from pprint import pprint
import json
import xmltodict

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


def find_corp_stockcode(find_name):
    for country in root.iter("list"):
        if country.findtext("stock_code") != ' ' and country.findtext("corp_name") == find_name :
            return country.findtext("stock_code")

tree = ET.parse('CORPCODE.xml')
root = tree.getroot()
company_name = ['삼성전자','케이티','SK텔레콤','국민은행','NAVER', '우리은행','카카오','LG전자','LG유플러스','신한은행']
company = {}
company_stockcode = {}
for name in company_name: 
    # 기업 고유 번호 - dart 기업 정보
    company[name] = find_corp_num(name)
    # 기업 종목 코드 - 뉴스 크롤링
    company_stockcode[name] = find_corp_stockcode(name)
# =================================================================================================================
    


    # 직원 수
def load_data_employee(**kwargs):
    crtfc_key = 'b913de0ec72741e320cafa8e5fa18ac030699e38'
    corp_code = kwargs['corp_code']

    if kwargs['request'] == 'company':
         url = 'https://opendart.fss.or.kr/api/empSttus.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code+'&bsns_year=2022&reprt_code=11011'

    r = requests.get(url)
    company_data = r.json()
    with open(f'./{kwargs["name"]}_employee.json','w') as f:
        json.dump(company_data, f, ensure_ascii=False, indent=4)    

    return company_data


    # 부채, 자산
def load_data_financial(**kwargs):
    crtfc_key = 'b913de0ec72741e320cafa8e5fa18ac030699e38'
    corp_code = kwargs['corp_code']

    url = f'https://opendart.fss.or.kr/api/list.json?crtfc_key={crtfc_key}&corp_code={corp_code}&bgn_de=20181019&pblntf_detail_ty=A001&date'

    r = requests.get(url)
    company_data = r.json()
    # with open(f'./{kwargs["name"]}_financial.json','w') as f:
    #     json.dump(company_data, f, ensure_ascii=False, indent=4)    
    report_code = company_data.get('list')[0]['rcept_no']
        
    url = f'https://opendart.fss.or.kr/api/fnlttXbrl.xml?crtfc_key={crtfc_key}&rcept_no={report_code}&reprt_code=11011'
    


# for company_name, company_code in company.items():
#             # 직원수        
#             employee = load_data_employee(name = company_name, request = 'company', corp_code = company_code)
#             financial = load_data_financial(name = company_name, request = 'company', corp_code = company_code)
            
#             pprint(financial)

# print(company)
# for company_name, company_code in company.items():
financial = load_data_financial(name = '삼성전자', corp_code = '00126380')
pprint(financial)

# employee = load_data_employee(name = company_name, request = 'company', corp_code = company_code)
# financial = load_data_financial(name = '우리은행', request = 'company', corp_code = '00254045')

# pprint(financial)