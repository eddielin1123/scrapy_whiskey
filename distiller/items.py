# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DistillerItem(scrapy.Item):
    
    name = scrapy.Field() # 酒名
    data_name = scrapy.Field() # url分解的酒名
    brand_country = scrapy.Field() # 酒廠/國家
    url = scrapy.Field() # URL
    abv = scrapy.Field() # 濃度
    year = scrapy.Field() # 年份
    type = scrapy.Field() # 類型
    region = scrapy.Field()  # 地域性 高地或低地
    taste_note = scrapy.Field()
    image = scrapy.Field() # 圖片
    official_content = scrapy.Field() # 官方內容
    # origin = scrapy.Field() # 產地
    comment = scrapy.Field() # 評論


class DistillerCommentItem(scrapy.Item):
    
    whiskey_name = scrapy.Field()  # 酒名
    user_name = scrapy.Field()  # 評論者
    star = scrapy.Field()  # 評分
    text = scrapy.Field()  # 評論

class MomCommentItem(scrapy.Item):
    data_name = scrapy.Field()
    whiskey_name = scrapy.Field()
    text = scrapy.Field()
    score = scrapy.Field()
"""       
{ 酒A:[
    {用戶1:評論},
    {用戶2:評論}
    ]
},
酒B:[{用戶1:評論}},{用戶2:評論}]}
"""