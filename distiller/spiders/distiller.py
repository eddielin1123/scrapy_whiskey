import logging
import os
from distiller.items import DistillerItem, DistillerCommentItem, MomCommentItem
import scrapy
from bs4 import BeautifulSoup
import pandas as pd
import re
import pymongo

class MasterofmaltSpider(scrapy.Spider):

    name = "master_of_malt"

    def start_requests(self):
        df = pd.read_csv(r'masterofmalt_urls.csv')
        urls = df.iloc[:, 0].tolist()
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        basic_item = DistillerItem()
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            basic_item['name'] = soup.find('h1', {'id': 'ContentPlaceHolder1_pageH1'}).text.strip()
        except:
            basic_item['name'] = 'null'

        try:
            basic_item['official_content'] = soup.find('div', {'itemprop': 'description'}).text.strip().replace('"','').replace('\'', '').replace('#', '').replace('@', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('*', '').replace('\n', '').replace('\r', '').replace('\t', '')
        except:
            basic_item['official_content'] = 'null'

        try:
            basic_item['data_name'] = response.url.split('/')[-2]
        except:
            basic_item['data_name'] = 'null'

        try:
            basic_item['url'] = response.url
        except:
            basic_item['url'] = 'null'

        try:
            basic_item['image'] = 'https:' + soup.find('div',{'class':'productImageWrap'}).find('img')['src']
        except:
            basic_item['image'] = 'null'

        full_info = soup.find('div', {'class': 'expandContainer kv-list'})
        info = full_info.find_all('div', {'class': 'kv-row'})

        country = ''
        region = ''
        brand = ''
        year = ''
        type = ''
        abv = ''
        for i in info:

            if 'Country' in i.text:
                country += i.text.strip().split('Country')[1].replace('Whisky', '')

            elif 'Region' in i.text:
                region += i.text.strip().split('Region')[1].replace('Whisky', '')

            elif 'Distillery / Brand' in i.text:
                brand += i.text.strip().split('Distillery / Brand')[1]

            elif 'Age' in i.text:
                year += i.text.strip().split('Age')[1].replace('year old Whisky', '')

            elif 'Style' in i.text:
                type += i.text.strip().split('Style')[1].replace('Whisky', '')

            elif 'Alcohol' in i.text:
                abv += i.text.strip().split('Alcohol')[1]
        if country != '' or brand != '':
            basic_item['brand_country'] = brand + '//' + country
        else:
            basic_item['brand_country'] = 'null'
        if region != '':
            basic_item['region'] = region
        else:
            basic_item['region'] = 'null'
        if year != '':
            basic_item['year'] = year
        else:
            basic_item['year'] = 'null'
        if type != '':
            basic_item['type'] = type
        else:
            basic_item['type'] = 'null'
        if abv != '':
            basic_item['abv'] = abv
        else:
            basic_item['abv'] = 'null'

        taste = ''
        taste_box = soup.find_all('div', {'class': 'boxBgr'})
        for t in taste_box:
            try:
                if t.find('h3').text == 'Tasting Note by The Chaps at Master of Malt':
                    taste += t.find('h3').find_next_sibling().text
            except:
                continue

        if not taste == '':
            basic_item['taste_note'] = taste
        else:
            basic_item['taste_note'] = 'null'

        comments_block = soup.find_all('div', {'class': 'userReviewBlock'})
        comments = ''
        for c in comments_block:
            if c.find('meta', {'itemprop': 'ratingValue'}):
                score = c.find('meta', {'itemprop': 'ratingValue'}).find_next_sibling()['title'].split('(')[1].split(')')[0]
            user_comment = c.find('p').text.strip().replace('"', '')
            comments += user_comment

        basic_item['comment'] = comments

        yield basic_item


class DistillerSpider(scrapy.Spider):

    name = "distiller_basic"

    def start_requests(self):
        df = pd.read_csv(r'./all_urls.csv')
        urls = df.iloc[:,0].tolist()        

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        basic_item = DistillerItem()
        soup = BeautifulSoup(response.text,'lxml')
        try:
            basic_item['name'] = soup.find('h1',{'class':'long name secondary-headline'}).text.strip()
        except:
            try:
                basic_item['name'] = soup.find('h1', {'class': 'name secondary-headline'}).text.strip()
            except:
                try:
                    basic_item['name'] = soup.find('h1', {'class': 'name secondary-headline very-long'}).text.strip()
                except:
                    try:
                        basic_item['name'] = soup.find('h1', {'class': 'name secondary-headline super-long'}).text.strip()
                    except:
                        basic_item['name'] = 'null'
        basic_item['data_name'] = response.url.split('/')[5]
        basic_item['url'] = response.url

        try:
            basic_item['official_content'] = soup.find('p', {'class': 'description'}).text.strip()
        except:
            basic_item['official_content'] = 'null'
        
        try:
            if soup.find('li', {'class': 'detail age'}).find('div', {'class': 'value'}).text != '' or soup.find('li', {'class': 'detail age'}).find('div', {'class': 'value'}).text != 'NAS':
                basic_item['year'] = soup.find('li', {'class': 'detail age'}).find('div', {'class': 'value'}).text
            else:
                basic_item['year'] = 'null'
        except:
            basic_item['year'] = 'null'

        try:
            basic_item['abv'] = soup.find('li', {'class': 'detail abv'}).find('div', {'class': 'value'}).text
        except:
            basic_item['abv'] = 'null'

        try:
            basic_item['brand_country'] = soup.find('h2',{'class':'ultra-mini-headline location middleweight'}).text.strip()
        except:
            basic_item['brand_country'] = 'null'
        try:
            basic_item['type'] = soup.find('h2',{'class':'ultra-mini-headline type'}).text
        except:
            basic_item['type'] = 'null'
        # try:
        #     basic_item['origin'] = soup.find('h2', {'class': 'ultra-mini-headline location middleweight'}).text.split('//')[1]
        # except:
        #     basic_item['origin'] = 'null'
        try:
            basic_item['image'] = soup.find('div', {'class': 'desktop main-image official'})['style'].split('(')[1].split(')')[0]
        except:
            try:
                basic_item['image'] = soup.find('div', {'class': 'desktop main-image requested unofficial'})['style'].split('(')[1].split(')')[0]
            except:

                    basic_item['image'] = 'null'
        yield basic_item


class DistillerCommentSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 302, 404, 500, 520, 521]

    name = "distiller_comment"
    logger = logging.getLogger('CommentsLogger')

    def start_requests(self):
        df = pd.read_csv(r'./all_urls.csv')
        urls = df.iloc[:,0].tolist()        

        for url in urls:
            url = f'{url}/tastes'
            yield scrapy.Request(url=url, callback=self._page_handler)
        # test json
        #url = r'https://distiller.com//spirits/hibiki-21-year/tastes'
        #yield scrapy.Request(url=url, callback=self._page_handler)

    def _page_handler(self, response):
        LAST_PAGE = self._last_page_dealer(response)
        for page in range(1, int(LAST_PAGE)+1):
            url = f'{response.url}?page={page}'
            yield scrapy.Request(url=url, callback=self.comments_crawler)
    
    def comments_crawler(self, response):
        basic_item = DistillerCommentItem()
        
        if response.status == 200:            
            soup = BeautifulSoup(response.text, 'lxml')        
            comments = soup.find_all('div', {"class":"taste-content"})        
            name = response.url.split('/')[-2]       
            basic_item['whiskey_name'] = name
            if comments:
                #comment_dict = dict()
                for comment in comments:
                    user_name = comment.find('h3',{'class':"mini-headline name username truncate-line"})
                    content = comment.find('div',{'class':"body"})
                    star = comment.find('div',{'class':"rating-display__value"})
                    try:                        
                        basic_item['user_name'] = user_name.text.replace('\n','')
                    except:
                        self.logger.warning(f"There is no comment in {response.url}")
                    try:
                        basic_item['text'] = content.text.strip().replace('"','').replace('#','').replace('@','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('\n','').replace('\r','').replace('\t','')
                    except:
                        basic_item['text'] = 'null'
                    try:
                        basic_item['star'] = star.text
                    except:
                        basic_item['star'] = 'null'
                    yield basic_item
            else:
                # there is no commnet
                with open('logger.log', mode='a') as f:
                    f.write(f"There is no comment in {name}, Url:{response.url}\n")
                self.logger.warning(f"There is no comment in {response.url}")
        else:
            with open('logger.log', mode='a') as f:
                f.write(f"resopnse_status/{response.status}, {name}, url={response.url}\n")
            self.logger.error(f"resopnse_status/{response.status}, url={response.url}")

    def _last_page_dealer(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            page = soup.find('span',{'class':'last'}).a['href'][-2:]
            if page[0] == "=":
                LAST_PAGE = soup.find('span',{'class':'last'}).a['href'][-1]
            else:
                LAST_PAGE = soup.find('span',{'class':'last'}).a['href'][-2:]
            return LAST_PAGE
        except:
            return "1"

    def _dir_checker(self):
        if os.path.isdir(r'./comments') == False:
            os.mkdir(r'./comments')



# save csv version:
#                     temp_list = [star, content]
#                    df = pd.DataFrame([temp_list])
#                    if os.path.isfile(f"./comments/{name}.csv"):
#
#                        df.to_csv(f"./comments/{name}.csv", index=None, encoding='utf-8-sig', header=False, mode='a')
#                    else:
#                        df.to_csv(f"./comments/{name}.csv", index=None, encoding='utf-8-sig', header=['star', 'comment'])                           