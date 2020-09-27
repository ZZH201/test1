import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time

conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='ttttt', charset='utf8')
cursor = conn.cursor()

# 定义一个变量url，为需要爬取数据我网页网址
url = 'http://gangkou.00cha.net/'
# 获取这个网页的源代码，存放在req中，{}中为不同浏览器的不同User-Agent属性，针对不同浏览器可以自行百度
req = requests.get(url, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
req.encoding = 'gb2312'
# 生成一个Beautifulsoup对象，用以后边的查找工作
soup = BeautifulSoup(req.text, 'html.parser')

# 找到所有a标签中的内容并存放在xml这样一个类似于数组队列的对象中
xml = soup.find_all('a')
gj = []
# 查找国家港口的URL
for k in xml:
    if 'gj_' in k['href']:
        gj.append(k['href'])

for l in gj:
    urlgj = 'http://gangkou.00cha.net/' + l
    # 获取这个网页的源代码，存放在req中，{}中为不同浏览器的不同User-Agent属性，针对不同浏览器可以自行百度
    reqgj = requests.get(urlgj, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
    reqgj.encoding = 'gb2312'
    # 生成一个Beautifulsoup对象，用以后边的查找工作
    soupgj = BeautifulSoup(reqgj.text, 'html.parser')
    # 找到所有a标签中的内容并存放在xml这样一个类似于数组队列的对象中
    xmlgj = soupgj.find_all('a')
    # 查找国家港口的URL
    for kgj in xmlgj:
        if 'gk_' in kgj['href']:
            urlgk = 'http://gangkou.00cha.net/' + kgj['href']
            reqgk = requests.get(urlgk, {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
            reqgk.encoding = 'gb2312'
            soupgk = BeautifulSoup(reqgk.text, 'html.parser')
            # keylatlon1=soupgk.find(key1)
            trarry = []
            for tr in soupgk.find_all('tr'):
                tdarry = []
                for td in tr.find_all('td'):
                    text = td.text.replace('\u3000', '').replace('&nbsp;', ' ')
                    tdarry.append(text)
                trarry.append(tdarry)
            # tab2=[]
            # for tab in trarry:
            #    ctab2=[]
            #    for ctab in tab:
            #        ctab2.append(ctab.replace('\u3000',''))
            #    tab2.append(ctab2)
            keylonlat1 = 'LatLng'  # 设置经纬度关键字1
            keylonlat2 = ");"  # 设置经纬度关键字2
            plonlata = reqgk.text.find(keylonlat1)  # 找出关键字1的位置
            plonlatt = reqgk.text.find(keylonlat2, plonlata)  # 找出关键字2的位置(从字1后面开始查找)
            lonlat = reqgk.text[plonlata:plonlatt + 1]  # 得到关键字1与关键字2之间的内容(即想要的数据)
            lonlat = re.findall(r'[(](.*?)[)]', lonlat)
            introarry = []
            for introduce in soupgk.find_all('div', class_='bei lh'):
                if '港口介绍' in introduce.text:
                    introarry.append([introduce.text.replace('\ufffd', '').replace('\xe6', '').replace('&nbsp;', ' ')])
            try:
                if introarry[0][0].__len__() > 256:
                    introarry[0][0] = introarry[0][0][0:255]
            except:
                print(introarry)
            try:
                FCode = trarry[0][1]
            except:
                FCode = ''
            try:
                FCity = trarry[0][3]
            except:
                FCity = ''
            try:
                FCnName = trarry[1][1]
            except:
                FCnName = ''
            try:
                FEnName = trarry[1][3]
            except:
                FEnName = ''
            try:
                FCountry = trarry[2][1]
            except:
                FCountry = ''
            try:
                FArea = trarry[2][3]
            except:
                FArea = ''
            try:
                FCnRoute = trarry[3][1]
            except:
                FCnRoute = ''
            try:
                FEnRoute = trarry[3][3]
            except:
                FEnRoute = ''
            try:
                FAnchorage = trarry[4][1]
            except:
                FAnchorage = ''
            try:
                FType = trarry[4][3]
            except:
                FType = ''
            try:
                FLat = float(lonlat[0].split(',')[0])
            except:
                FLat = 0
            try:
                FLon = float(lonlat[0].split(',')[1])
            except:
                FLon = 0
            try:
                FIntroduction = introarry[0][0]
            except:
                FIntroduction = ''
            try:
                sql = "INSERT INTO T_AdminPorts(FCode,FCity,FCnName,FEnName,FCountry,FArea,FCnRoute,FEnRoute,FAnchorage,FType,FLat,FLon,FIntroduction)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                data = (
                FCode, FCity, FCnName, FEnName, FCountry, FArea, FCnRoute, FEnRoute, FAnchorage, FType, FLat, FLon,
                FIntroduction)
                cursor.execute(sql, data)
                # 如果没有指定autocommit属性为True的话就需要调用commit()方法
                conn.commit()
                print(FCity+':爬取一条港口信息数据，写库成功')
            except:
                print(FCity + ':写库失败！！！！！！！！！！！！')
            time.sleep(0.5)
