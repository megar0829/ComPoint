from pprint import pprint
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup as bs
from html_table_parser import parser_functions as parser 

# url = urlopen("https://ko.wikipedia.org/wiki/%ED%91%9C")
df = pd.read_html("https://ko.wikipedia.org/wiki/%ED%91%9C", converters={'no':str})
pprint(df)