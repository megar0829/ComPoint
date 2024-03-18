import requests
from pprint import pprint
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
crtfc_key = 'b913de0ec72741e320cafa8e5fa18ac030699e38'

### 회사고유번호 데이터 불러오기
# url = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=' + crtfc_key
# with urlopen(url) as zipresp:
#     with ZipFile(BytesIO(zipresp.read())) as zfile:
#         zfile.extractall('corp_num')
        
# import xml.etree.ElementTree as ET

# ### 압축파일 안의 xml 파일 읽기
# tree = ET.parse('CORPCODE.xml')
# root = tree.getroot()
# company = ['삼성전자','케이티','에스케이티','국민은행','NAVER', '우리은행','카카오','LG전자','LG유플러스','신한은행']
# def find_corp_num(find_name):
#     for country in root.iter("list"):
#         if country.findtext("corp_name") == find_name:
#             return country.findtext("corp_code")
# for c in company: 
#     print(c, ':', find_corp_num(c))


# 사업 내용
# url = 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20230307000542'

# 사업의 개요
url = 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230307000542&dcmNo=9040011&eleId=10&offset=139666&length=2406&dtd=dart3.xsd'

# 주요 제품 및 서비스
# url = 'https://dart.fss.or.kr/report/viewer.do?rcpNo=20230307000542&dcmNo=9040011&eleId=11&offset=142076&length=4215&dtd=dart3.xsd'

html = urlopen(url).read()
soup = bs(html, 'html.parser')
contents = soup.select('body')
business = contents[0].get_text().split('\n')

pprint(business)