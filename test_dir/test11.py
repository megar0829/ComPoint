import requests
import math
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def f1():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    base_url = f"https://m.jobkorea.co.kr/start/best1000/?schLocal=&schPart=10031&schMajor=&schEduLevel=5&schWork=&schCType=&schCareer=1&isSaved=1&LinkGubun=0&LinkNo=0&Page="

    # 페이지 수
    start_page = 1
    url = f"{base_url}{start_page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 현재 채용 중인 공고 개수 (ex. '(50)')
    post_cnt = int(soup.select_one('#TabIngCount').text.replace('(', '').replace(')', ''))
    end_page = math.ceil(post_cnt / 50)

    #페이지 번호 바꿔 가며 탐색
    for page_no in range(start_page, end_page + 1):
        url = f"{base_url}{page_no}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        companies = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.comp')
        titles = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.tit')
        urls = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a')
        images = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.logo > img')
        dates = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.desc > span:nth-of-type(3)')

        for i in range(post_cnt):
            b_tag = companies[i].find('b')
            if b_tag:
                b_tag.decompose()
                
            company = companies[i].text.strip()
            title = titles[i].text.strip()
            image = images[i]['src']
            date = dates[i].text
            no = urls[i]['linkurl'][17:25]
            # https://www.jobkorea.co.kr/Recruit/GI_Read/43133494
            # https://m.jobkorea.co.kr/Recruit/GIReadDetailContentIframe/43133494

            print(company)
            print(title)
            print(image)
            print(date)
            print(no)

def f2(no):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    url = f'https://www.jobkorea.co.kr/Recruit/GI_Read/{no}'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    apply = soup.select_one('#devApplyBtn > span').text
    apply_url = ''
    if apply == '홈페이지 지원':
        get_apply_url = soup.select_one('#devApplyBtn')['onclick']
        flag = False
        for i in get_apply_url:
            if flag is False and i == "/":
                flag = True
            
            if flag is True and i == "'":
                break
            
            if flag:
                apply_url += i
    else:
        apply_url = f'https://www.jobkorea.co.kr/Recruit/GI_Read/{no}'
    
    return apply_url

current = datetime.now()
date = (current + timedelta(days=1)).strftime("%Y-%m-%d")
print(date)
