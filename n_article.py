# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import requests
# from pprint import pprint

# # url = 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20230307000542'

# # 사업의 개요
# url = 'https://finance.naver.com/item/news.naver?code=005930'

# # 주요 제품 및 서비스
# # url = 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230307000542&dcmNo=9040011&eleId=11&offset=142076&length=4215&dtd=dart3.xsd'

# html = urlopen(url).read()
# soup = BeautifulSoup(html, 'html.parser')
# contents = soup.select('body')
# pprint(contents)
# # business = contents[0].get_text()
# # pprint(contents[0])
# # print(type(contents))
# # print(business)