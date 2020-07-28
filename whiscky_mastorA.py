import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime

Alcohol_name = []
Alcohol_winery = []
Alcohol_url = []
Alcohol_years = []
Alcohol_style = []
Alcohol_loct = []
Alcohol_ABV = []
Alcohol_content = []
Alcohol_contect = []
Alcohol_price = []
Alcohol_img = []

for page in range(1, 105):
    url = ('https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/'.format(page))
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Referer": "https://www.masterofmalt.com/country/scotch-whisky/"
               }
    resfirst_url = requests.get(url , headers=headers)
    soupfirst_url = BeautifulSoup(resfirst_url.text , 'html.parser')

    alcohol_url = soupfirst_url.select('div[class="col-md-12"]>div>h3>a')

    for alcohol in alcohol_url:

        name = alcohol.text
        URL = str(alcohol).split('"')[1]
        res_url = requests.get(URL , headers=headers)
        soup_url = BeautifulSoup(res_url.text , 'html.parser')
        Detail = str(soup_url.select('span[class="kv-val"]'))
        try:
            Years = str(re.search(r'\w\w year old', Detail , re.M | re.I)).split('\'')[1]
        except IndexError as e:
            Years = 'None'
        try:
            Style = soup_url.select('div[id="ContentPlaceHolder1_ctl00_ctl00_wdStyle"]>span[class="kv-val"]')[0].text.split('Whisky')[0]
        except IndexError as e:
            Style = 'None'
        try:
            Content = soup_url.select('div[itemprop="description"]>p')[0].text
        except IndexError as e:
            Content = 'None'
        Contect =  soup_url.select('div[class="h-gutter row"]>div>div>div>div>div>p[itemprop="reviewBody"]')
        if Contect :
            for i in Contect:
                Contectlist = i.text.replace('\n', ' ')
        else:
            Contectlist = 'None'
        try:
            Price = str(soup_url.select('div[class="product-price gold"]>div')[0]).split('<span>')[-1].split('</span>')[0]
        except IndexError as e:
            Price = 'NT$'
        try:
            IMG = 'https:' + soup_url.select('div[class="productImageWrap"]>img')[0]['src']
        except IndexError as e:
            IMG = 'None'
        res = r'<span class="kv-val".*?>(.*?%)</span>'
        mm = re.findall(res, Detail, re.S | re.M)
        for item in mm:
            Location = item.split(',')[0].split('>')[1].split('<')[0]
            Brand = item.split(',')[1].split('>')[2].split('<')[0]
            ABV = item.split(',')[-1].split('>')[1]

            Alcohol_name.append(name)
            Alcohol_winery.append(Brand)
            Alcohol_url.append(URL)
            Alcohol_style.append(Style)
            Alcohol_years.append(Years)
            Alcohol_loct.append(Location)
            Alcohol_ABV.append(ABV)
            Alcohol_content.append(Content)
            Alcohol_price.append(Price)
            Alcohol_img.append(IMG)
            Alcohol_contect.append(Contectlist)

            pd.set_option('display.max_rows', 500)
            pd.set_option('display.max_columns', 500)
            pd.set_option('display.width', 1000)

            df = pd.DataFrame({'酒名':Alcohol_name ,'酒廠':Alcohol_winery,'網址':Alcohol_url,'風味':Alcohol_style, '年分':Alcohol_years,'產地':Alcohol_loct,'酒精度':Alcohol_ABV,'評論':Alcohol_contect,'價格':Alcohol_price,'照片':Alcohol_img,'內容':Alcohol_content})

            df.to_csv("whisckytest.csv", index=False, sep='*')








