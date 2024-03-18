from urllib.request import urlopen
from bs4 import BeautifulSoup

# 뉴스 페이지 링크 - 번호는 기업코드

def newsCrawler(company_code, page_num):
    url = 'https://finance.naver.com/item/news_news.naver?code='+company_code+'&page='+page_num
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='cp949')
    title_td = soup.find_all("td", 'title')
    titles = []
    links = []
    
    for t in title_td:
        # 제목
        titles.append(t.get_text().strip('\n'))
        # /item/news_read.naver?article_id=0005082784&amp;office_id=014&amp;code=005930&amp;page=1&amp;sm=
        # 기사 url 
        a = t.find('a', 'tit')['href'] 
        article_id = a[33:43]
        office_id = a[54:57]
        # print(article_id, office_id)
        link = 'https://n.news.naver.com/mnews/article/'+office_id+'/'+article_id
        links.append(link)
    # 신문사
    press = []
    press_td = soup.find_all('td', 'info')
    for p in press_td :
        press.append(p.get_text())
    # 발행일 
    date = []
    date_td = soup.find_all('td', 'date')
    for d in date_td :
        date.append(d.get_text())
    
    for i in range(len(titles)):
        print(titles[i], links[i], press[i], date[i])
        
    

newsCrawler('005930', '1')

