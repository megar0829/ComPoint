from urllib import parse
from bs4 import BeautifulSoup
import requests
# x = parse.quote('KT')
# print(x)
# 은행의 경우 증권사 리포트가 없는 경우도 있다. 신한은행은 하나 정도
# KB금융, 신한지주로 찾으면 더 잘나옴
# models.py에 출처도 포함시키는게 좋을 것 같다!
# company_name = ['삼성전자','케이티','SK텔레콤','국민은행','NAVER', '우리은행','카카오','LG전자','LG유플러스','신한은행']
company_name=['국민은행']
for corp_name in company_name:
    # url에 들어갈 회사이름 인코딩 : 삼성전자 -> %EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90
    new_name = parse.quote(corp_name)
    url_h = f"https://consensus.hankyung.com/analysis/list?sdate=2018-10-01&edate=2023-10-01&now_page=1&search_value=&report_type=&pagenum=20&search_text={new_name}&business_code="
    html_h = requests.get(url_h, headers={'User-Agent':'Gils'}).content
    soup_h = BeautifulSoup(html_h, 'lxml')

    temp_body = soup_h.find('div', {"class":"table_style01"}).find('tbody').find_all('tr')
    print(temp_body[0])
    temp_test_body = soup_h.find('div', {"class":"table_style01"}).find('tbody')
    if temp_test_body.find('tr', {'class':'listNone'}):
        print("asdfasdfasdfasdfasdfasdfaas")
    
    
    print(temp_body[0].find('td'))
    # print(temp_body)
    if temp_body[0].find('td').get_text() == '결과가 없습니다.':
        print('Rmx')
    else :
        print('adsfasd')
    # for tmp_tr in temp_body :
    #     print(type(tmp_tr))
    #     tmp_td = tmp_tr.find_all('td')
        
    #     # https://consensus.hankyung.com/analysis/downpdf?report_idx=623493
    #     url = 'https://consensus.hankyung.com' + tmp_td[2].find('a')['href']
    #     title = tmp_td[2].find('a').get_text()
    #     date = tmp_td[0].get_text()
    #     author = tmp_td[3].get_text()
    #     firm = tmp_td[4].get_text()


