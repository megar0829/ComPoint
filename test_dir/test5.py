# 크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 뉴스 양이 너무 작을 경우 여러 페이지에서 가져올 것
# # 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
# # 입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
# def makePgNum(num):
#     if num == 1:
#         return num
#     elif num == 0:
#         return num + 1
#     else:
#         return num + 9 * (num - 1)

# # 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
# def makeUrl(search, start_pg, end_pg):
#     if start_pg == end_pg:
#         start_page = makePgNum(start_pg)
#         url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + search + "&start=" + str(
#             start_page)
#         print("생성url: ", url)
#         return url
#     else:
#         urls = []
#         for i in range(start_pg, end_pg + 1):
#             page = makePgNum(i)
#             url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
#             urls.append(url)
#         print("생성url: ", urls)
#         return urls



# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
def makeUrl(search):
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + search + "&start=1" 
    # print("생성url: ", url)
    return url
   
# 검색어 입력
search = input("기업 이름 작성:") # 해당 페이지의 기업 이름 변수로 대체

# naver url 생성
search_urls = makeUrl(search)

## selenium으로 navernews만 뽑아오기##

# 버전에 상관 없이 os에 설치된 크롬 브라우저 사용
# 옵션 생성
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)



# selenium으로 검색 페이지 불러오기 #

naver_urls = []

driver.get(search_urls)
time.sleep(1)  # 대기시간 변경 가능

# 네이버 기사 눌러서 제목 및 본문 가져오기#
# 네이버 기사가 있는 기사 css selector 모아오기
a = driver.find_elements(By.CSS_SELECTOR, 'a.info')
#print(a)

# 위에서 생성한 css selector list 하나씩 클릭하여 본문 url얻기
for i in a :
    url = i.get_attribute("href")

    if "news.naver.com" in url:
        naver_urls.append(url)

    else:
        pass

print(naver_urls)

###naver 기사 제목과 url 가져오기###

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

titles = []
results = []
for i in naver_urls:
    original_html = requests.get(i, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    # 검색결과확인시
    # print(html)

    # 뉴스 제목 가져오기
    title = html.select("div#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
    # list합치기
    title = ''.join(str(title))
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1, repl='', string=title)
    titles.append(title)
    results.append([i, title])

    # 신문사
    newspaper = html.select('')
    
    # 사진



# print(titles)
for url, title in results :
    print(url, title)
