
import requests
import re
from bs4 import BeautifulSoup
url='http://www.cntour.cn/'
strhtml=requests.get(url)
soup=BeautifulSoup(strhtml.text,'html.parser', from_encoding='utf-8')
data = soup.select('#main>div>div.mtop.firstMod.clearfix>div.centerBox>ul.newsList>li>a ')
#将数据
print(data)
#数据清洗和组织数据
for item in data:
#明确提取的数据为标题和链接
    result={
#提取标签正文
    'title': item.get_text(),
#提取标签中的href属性
    'link': item.get('href'),
#提取链接中的id
    'id':re.findall('\d+', item.get('href'))   }
print(result)