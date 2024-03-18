from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
import requests
import pandas as pd
from html_table_parser import parser_functions as parser
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from datetime import date as datedate
import pytz
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from pprint import pprint
import math
from .models import Company, Finance, Article, Gongo, Report
from posts.models import Post, Comment
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


def find_corp_stockcode(find_name):
    for country in root.iter("list"):
        if country.findtext("stock_code") != ' ' and country.findtext("corp_name") == find_name :
            return country.findtext("stock_code")

tree = ET.parse('CORPCODE.xml')
root = tree.getroot()
company_name = ['삼성전자','삼성에스디에스', '케이티','SK텔레콤','국민은행','NAVER', '우리은행','카카오','LG전자','LG유플러스','신한은행']
company = {}
company_stockcode = {}


for name in company_name: 
    # 기업 고유 번호 - dart 기업 정보
    company[name] = find_corp_num(name)
    # 기업 종목 코드 - 뉴스 크롤링
    company_stockcode[name] = find_corp_stockcode(name)
# =================================================================================================================
# =================================================================================================================

    # 직원 수
def load_data_employee(**kwargs):
    crtfc_key = 'b913de0ec72741e320cafa8e5fa18ac030699e38'
    corp_code = kwargs['corp_code']

    if kwargs['request'] == 'company':
         url = 'https://opendart.fss.or.kr/api/empSttus.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code+'&bsns_year=2022&reprt_code=11011'

    r = requests.get(url)
    company_data = r.json()

    return company_data


    # 부채, 자산
def load_data_financial(**kwargs):
    crtfc_key = 'b913de0ec72741e320cafa8e5fa18ac030699e38'
    corp_code = kwargs['corp_code']

    if kwargs['request'] == 'company':
         url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code+'&bsns_year=2022&reprt_code=11011'

    r = requests.get(url)
    company_data = r.json()
    
    return company_data
# =================================================================================================================

def newsCrawler(company_code, page_num):
    url = 'https://finance.naver.com/item/news_news.naver?code='+company_code+'&page='+page_num
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='cp949')
    time.sleep(random.randint(1, 4))
    title_td = soup.find_all("td", 'title')
    titles = []
    links = []
    # 제목, url
    for t in title_td:
        titles.append(t.get_text().strip('\n'))
        # /item/news_read.naver?article_id=0005082784&amp;office_id=014&amp;code=005930&amp;page=1&amp;sm=
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
    
    
    news_data = zip(titles, links, press, date)
    
    return news_data
# =================================================================================================================


    
# 프로젝트 메인페이지 랜더링
def main_page(request):
    companies = Company.objects.all()
    gongos = Gongo.objects.all().order_by('dday')[:12]
    articles = Article.objects.all().order_by('-date')[:10]

    context = {
        'companies': companies,
        'gongos': gongos,
        'articles': articles,
    }
    return render(request, 'index.html', context)

# 채용공고 메인페이지 랜더링
def gongos(request):
    return render(request, 'informations/gongo_index.html')

# 기업정보 메인페이지 랜더링
def index(request):
    if request.method ==  'POST':   
        # dart api 데이터 정리 및 저장
        for company_name, company_code in company.items():
            # 직원수        
            employee = load_data_employee(request = 'company', corp_code = company_code)
            sum_sm = 0
            sum_avrg = 0
            year_cnt = 0
            if employee and employee.get('list'):
                if len(employee.get('list')) > 2:
                    for list in employee.get('list'):
                        if list['fo_bbm'] == '성별합계':
                            sm = list['sm'].split(',')
                            sum_sm = ''
                            for s_str in sm:
                                sum_sm += s_str
                            sum_sm = int(sum_sm)
                            avrg_cnwk_sdytrn = list['avrg_cnwk_sdytrn']
                            year_cnt += 1
                            if '.' in avrg_cnwk_sdytrn:
                                sum_avrg += float(avrg_cnwk_sdytrn)
                            else:
                                save_year = ''
                                save_month = ''
                                year_flag = True
                                month_flag = True
                                for text in avrg_cnwk_sdytrn:
                                    if text.isdigit():
                                        if year_flag:
                                            save_year += text
                                        elif month_flag:
                                            save_month += text
                                    else:
                                        if text == '년':
                                            year_flag = False
                                        if text == '개':
                                            month_flag = False
                                if not save_year:
                                    save_year = 0
                                if not save_month:
                                    save_month = 0
                                sum_avrg += round(int(save_year) + float(int(save_month) / 12), 1)
                                        
                                    
                elif len(employee.get('list')) == 2:
                    for list in employee.get('list'):
                        sm = list['sm'].split(',')
                        sum_sm = ''
                        for s_str in sm:
                            sum_sm += s_str
                        sum_sm = int(sum_sm)
                        avrg_cnwk_sdytrn = list['avrg_cnwk_sdytrn']
                        year_cnt += 1
                        if '.' in avrg_cnwk_sdytrn:
                            sum_avrg += float(avrg_cnwk_sdytrn)
                        else:
                            save_year = ''
                            save_month = ''
                            year_flag = True
                            month_flag = True
                            for text in avrg_cnwk_sdytrn:
                                if text.isdigit():
                                    if year_flag:
                                        save_year += text
                                    elif month_flag:
                                        save_month += text
                                else:
                                    if text == '년':
                                        year_flag = False
                                    if text == '개':
                                        month_flag = False
                            if not save_year:
                                save_year = 0
                            if not save_month:
                                save_month = 0
                            sum_avrg += round(int(save_year) + float(int(save_month) / 12), 1)
            if year_cnt:
                sum_avrg = round(sum_avrg / year_cnt, 1)
            
            # 매출액, 당기순이익, 부채비율

            idx = 0
            financial = load_data_financial(request = 'company', corp_code = company_code)
            if financial and financial.get('list'):
                save_money = [0] * 3
                year = int(financial['list'][0].get('bsns_year'))
                capital = []
                data = {
                    year - 2: [0, 0, 0],
                    year - 1: [0, 0, 0],
                    year: [0, 0, 0],
                }
                for list in financial['list']:
                    if (list['account_nm'] == "매출액" or list['account_nm'] == "당기순이익") \
                        and list['fs_nm'] == "재무제표":
                        s_bfefrm = list['bfefrmtrm_amount'].split(',')
                        save_val = ''
                        for bfe_data in s_bfefrm:
                            save_val += bfe_data
                        data[year - 2][idx] = save_val[:7]
                        s_frmtrm = list['frmtrm_amount'].split(',')
                        save_val2 = ''
                        for ftm_data in s_frmtrm:
                            save_val2 += ftm_data
                        data[year - 1][idx] = save_val2[:7]
                        s_thstrm = list['thstrm_amount'].split(',')
                        save_val3 = ''
                        for ths_data in s_thstrm:
                            save_val3 += ths_data
                        data[year][idx] = save_val3[:7] 
                        idx += 1
                    if list['fs_nm'] == '연결재무제표':
                        if list['account_nm'] == '부채총계':
                            s1 = list['bfefrmtrm_amount'].split(',')
                            save_s1 = ''
                            for s1_data in s1:
                                save_s1 += s1_data
                            s2 = list['frmtrm_amount'].split(',')
                            save_s2 = ''
                            for s2_data in s2:
                                save_s2 += s2_data
                            s3 = list['thstrm_amount'].split(',')
                            save_s3 = ''
                            for s3_data in s3:
                                save_s3 += s3_data
                            save_money[0] = int(save_s1)
                            save_money[1] = int(save_s2)
                            save_money[2] = int(save_s3)
            
                        if list['account_nm'] == '자본총계':
                            # 20년도
                            s1 = list['bfefrmtrm_amount'].split(',')
                            save_s1 = ''
                            for s1_data in s1:
                                save_s1 += s1_data
                            # 21년도
                            s2 = list['frmtrm_amount'].split(',')
                            save_s2 = ''
                            for s2_data in s2:
                                save_s2 += s2_data
                            # 22년도
                            s3 = list['thstrm_amount'].split(',')
                            save_s3 = ''
                            for s3_data in s3:
                                save_s3 += s3_data

                            save_money[0] /= int(save_s1)
                            save_money[1] /= int(save_s2)
                            save_money[2] /= int(save_s3)
                            
                        if list['account_nm'] == '자본금':
                            s1 = list['bfefrmtrm_amount'].split(',')
                            save_s1 = ''
                            for s1_data in s1:
                                save_s1 += s1_data
                            s2 = list['frmtrm_amount'].split(',')
                            save_s2 = ''
                            for s2_data in s2:
                                save_s2 += s2_data
                            s3 = list['thstrm_amount'].split(',')
                            save_s3 = ''
                            for s3_data in s3:
                                save_s3 += s3_data
                            capital.append(int(save_s1[:7]))
                            capital.append(int(save_s2[:7]))
                            capital.append(int(save_s3[:7]))

                            
                        s_bfefrmtrm_3 = str(save_money[0])
                        data[year - 2][idx] = s_bfefrmtrm_3[2:4] + '.' + s_bfefrmtrm_3[4:6] + ' %'
                        s_frmtrm_3 = str(save_money[0])
                        data[year - 1][idx] = s_frmtrm_3[2:4] + '.' + s_frmtrm_3[4:6] + ' %'
                        s_thstrm_3 = str(save_money[0])
                        data[year][idx] = s_thstrm_3[2:4] + '.' + s_thstrm_3[4:6] + ' %'             
            
    # =================================================================================================================
        #  Company model : name(기업명), description(사업개요), logo, employee, work_year(근속년수) 
        #  Finance model : company(기업명), capital(자본금), revenue(매출액), profit(영업이익), dept(부채비율), year(년도) 
        #  Article model : company(기업명), title(기사제목), url(기사URL), press(신문사), date(기사날짜)
        #  Report model : company, title, url, date, author
    # =================================================================================================================
        
            logo_path = f"../../../static/img/{company_name}.png"
        
            comp = Company()
            comp.name = company_name
            comp.employee = sum_sm
            comp.work_year = sum_avrg
            comp.logo_path = logo_path
            comp.save()
            
            # 매출액, 당기순이익, 부채비율, capital
            idx = 0
            for data_year, data_value in data.items():
                if Finance.objects.filter(year=data_year).exists():
                    continue
                else :
                    finance = Finance()
                    finance.company = comp
                    finance.revenue = data_value[0]
                    finance.profit = data_value[1]
                    finance.debt = data_value[2]
                    finance.capital = capital[idx]
                    finance.year = data_year
                    finance.save()
                idx += 1

            # 뉴스 - 제목, url, 신문사, 날짜
            stockcode = company_stockcode[company_name]
            news_data = newsCrawler(stockcode, '1') # [titles, links, press, date]
            # news_data = newsCrawler('005930', '1') # 기업종목코드, 페이지번호
            for title, url, press, date in news_data:
                if Article.objects.filter(title=title).exists():
                    continue
                else :
                    article = Article()
                    article.title = title
                    article.url = url
                    article.press = press
                    dt = datetime.strptime(date, ' %Y.%m.%d %H:%M').replace(tzinfo=pytz.UTC)
                    article.date = dt
                    article.company = comp
                    article.save()
            
            
            # 증권사 리포트
            # url에 들어갈 회사이름 인코딩 : 삼성전자 -> %EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90
            new_name = parse.quote(company_name)
            url_h = f"https://consensus.hankyung.com/analysis/list?sdate=2018-10-01&edate=2023-10-01&now_page=1&search_value=&report_type=&pagenum=20&search_text={new_name}&business_code="
            html_h = requests.get(url_h, headers={'User-Agent':'Gils'}).content
            soup_h = BeautifulSoup(html_h, 'lxml')
            time.sleep(random.randint(1, 4))
            
            temp_body = soup_h.find('div', {"class":"table_style01"}).find('tbody')
            # 검색결과 없는 경우
            searchResulExists = True
            if temp_body.find('tr', {'class':'listNone'}):
                searchResulExists = False
            if searchResulExists :
                temp_body_tr = soup_h.find('div', {"class":"table_style01"}).find('tbody').find_all('tr')        
                for tmp_tr in temp_body_tr :
                    tmp_td = tmp_tr.find_all('td')
                    # https://consensus.hankyung.com/analysis/downpdf?report_idx=623493
                    r_title = tmp_td[2].find('a').get_text()
                    if Report.objects.filter(title=r_title).exists():
                        continue
                    else: 
                        r_url = 'https://consensus.hankyung.com' + tmp_td[2].find('a')['href']
                        r_date = tmp_td[0].get_text()
                        dt = datetime.strptime(r_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
                        r_author = tmp_td[3].get_text()
                        r_firm = tmp_td[4].get_text() # 추가하면 좋을듯
                    
                        report = Report()
                        report.title = r_title
                        report.url = r_url
                        report.date = dt
                        report.author = r_author
                        report.firm = r_firm
                        report.company = comp
                        report.save()
# =================================================================================================================

    # companies = get_list_or_404(Company)
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    
    return render(request, 'informations/index.html', context)


# =================================================================================================================



def detail(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    finances = company.finance_set.all()
    articles = company.article_set.all()
    reports = company.report_set.all()
    context = {
        'company': company,
        'finances': finances,
        'articles': articles,
        'reports': reports,
        # 'gongos': gongos,
        
        
    }
    return render(request, 'informations/detail.html', context)


# ==================================================================================================================
def gongos(request):
    current = datetime.now()
    if request.method ==  'POST':
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
        base_url = f"https://m.jobkorea.co.kr/start/best1000/?schLocal=&schPart=10031&schMajor=&schEduLevel=5&schWork=&schCType=&schCareer=1&isSaved=1&LinkGubun=0&LinkNo=0&Page="
        
        # 페이지 수
        start_page = 1
        url = f"{base_url}{start_page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.randint(1, 4))
        # 현재 채용 중인 공고 개수 (ex. '(50)')
        post_cnt = soup.select_one('#TabIngCount').text.replace('(', '').replace(')', '')
        end_page = math.ceil(int(post_cnt) / 50)
        

        #페이지 번호 바꿔 가며 탐색
        for page_no in range(start_page, end_page + 1):
            url = f"{base_url}{page_no}"
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(random.randint(1, 4))
            
            names = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.comp')
            titles = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.tit')
            urls = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a')
            images = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.logo > img')
            dates = soup.select('#devStarterForm > article > div.filterListWrap > ul > li > div.item.devListLink > a > span.desc > span:nth-of-type(3)')

            for i in range(len(names)):
                # 기업명에 b태그가 포함되어 있다면 삭제
                b_tag = names[i].find('b')
                if b_tag:
                    b_tag.decompose()
                    
                name = names[i].text.strip()
                title = titles[i].text.strip()
                image = images[i]['src']
                no = urls[i]['linkurl'][17:25]
                apply_url = get_url(no)
                date = dates[i].text

                if '내일' in date:
                    date = (current + timedelta(days=1)).strftime("%Y-%m-%d")
                elif '오늘' in date:
                    date = current.strftime("%Y-%m-%d")
                else:
                    month = day = ''
                    flag = True
                    for i in date:
                        if flag and i.isdigit():
                            month += i
                        elif i.isdigit():
                            day += i
                        elif i == "/":
                            flag = False
                        elif i == "(":
                            break
                    if int(month) < int(current.strftime("%m")):
                        year = int(current.strftime("%Y")) + 1
                        date = f'{year}-{month}-{day}'
                    else:
                        year = int(current.strftime("%Y"))
                        date = f'{year}-{month}-{day}'
                
                dday = str(datedate(int(year), int(month), int(day)) - datedate.today())
                dday, *_ = dday.split(' ')
                dday = int(dday)
                if name in company_name:
                    comp = Company.objects.get(name=name)
                    if not Gongo.objects.filter(name=name, title=title).exists():
                        gongo = Gongo(company=comp, name=name, title=title, no=no, url=apply_url, image=image, date=date, dday=dday)
                        gongo.save()
                else:
                    if not Gongo.objects.filter(name=name, title=title).exists():
                        gongo = Gongo(name=name, title=title, no=no, url=apply_url, image=image, date=date, dday=dday)
                        gongo.save()

    gongos = Gongo.objects.all()
    # 채용 마감일이 어제라면 삭제
    for gongo in gongos:
        if gongo.date == (current - timedelta(days=1)).strftime("%Y-%m-%d"):
            gongo.delete()

    gongos = Gongo.objects.all()
    context = {
        'gongos': gongos
    }
    return render(request, 'informations/gongo_index.html', context)


def get_url(no):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    url = f'https://www.jobkorea.co.kr/Recruit/GI_Read/{no}'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(random.randint(1, 4))
    apply = soup.select_one('#devApplyBtn > span').text
    apply_url = ''
    if apply == '홈페이지 지원':
        get_apply_url = soup.select_one('#devApplyBtn')['onclick']
        flag = False
        for i in get_apply_url:
            if flag is False and i == "/":
                flag = True
                continue
            
            if flag is True and i == "'":
                break
            
            if flag:
                apply_url += i
    else:
        apply_url = f'Recruit/GI_Read/{no}'
    
    return apply_url


def gongo_detail(request, gongo_pk):
    gongo = Gongo.objects.get(pk=gongo_pk)
    context = {
        'gongo': gongo,
    }
    return render(request, 'informations/gongo_detail.html', context)


def bookmark(request, gongo_pk):
    gongo = Gongo.objects.get(pk=gongo_pk)

    if request.user in gongo.bookmark_users.all():
        gongo.bookmark_users.remove(request.user)
        is_liked = False
    else:
        gongo.bookmark_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
    }
    return JsonResponse(context)


def search(request):
    keyword = request.GET.get('q')
    # 기업 정보 검색
    companys = Company.objects.all()
    search_companys = []
    company_name = []
    for company in companys :
        if keyword in company.name :
            if company.name not in company_name:
                search_companys.append(company)
                company_name.append(company.name)

    # 공고 정보 검색
    gongos = Gongo.objects.all()
    search_gongos = []
    for gongo in gongos:
        if keyword in gongo.title or keyword in gongo.name:
            search_gongos.append(gongo)

    # 커뮤니티 글 검색
    posts = Post.objects.all()
    search_posts = []
    for post in posts:
        if keyword in post.title or keyword in post.content:
            search_posts.append(post)
            
    context = {
        'keyword' : keyword,
        'search_companys': search_companys,
        'search_gongos': search_gongos,
        'search_posts': search_posts,
    }
    
    
    return render(request, 'informations/search.html', context)