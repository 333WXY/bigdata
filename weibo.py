import requests
import lxml
from lxml import etree
import re
import pymongo
from time import sleep
import random
from tqdm import tqdm
client = pymongo.MongoClient(host = 'localhost', port=27017)
db = client.yuanshe
collection = db.id_2
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "cookie":'_s_tentry=passport.weibo.com; Apache=2250516130380.3887.1649560162745; SINAGLOBAL=2250516130380.3887.1649560162745; ULV=1649560162755:1:1:1:2250516130380.3887.1649560162745:; crossidccode=CODE-yf-1NDnXf-41hWOG-R3JyfkmSX4iiv7Ge19e8f; SSOLoginState=1649560176; SUB=_2A25PVjogDeRhGeNI4lAX-CrKwj2IHXVsuUZorDV8PUJbkNANLXTwkW1NSAzEknUJoSpTh3W5coQ0niwVDHY1fEYW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhrO392wVX4U8IXeNZDvs5p5NHD95QfSo.ESonXSo.pWs4Dqcj8KfSZH.2t; wvr=6; wb_view_log_5692684691=1707*9601.5; webim_unReadCount=%7B%22time%22%3A1649560210693%2C%22dm_pub_total%22%3A13%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A13%2C%22msgbox%22%3A0%7D'
} 



url_to = []
for page_num in tqdm(range(1, 32), desc=u'列表爬取进度') :
    # 崇礼冬奥
    # url = f'https://s.weibo.com/weibo?q=%E5%B4%87%E7%A4%BC%E5%86%AC%E5%A5%A5&page={page_num}' 
    # 云顶滑雪
    url = f'https://s.weibo.com/weibo?q=%E4%BA%91%E9%A1%B6%E6%BB%91%E9%9B%AA&Refer=SWeibo_box&page={page_num}'

    page_text = requests.get(url=url,headers=headers).text

    tree = etree.HTML(page_text)
    result = re.findall('<a href="//\w{5}\W\w{3}/\d{10}/(\D.{8})', page_text, re.S)
    url = list(set(result))
    url.sort(key=result.index)
    # for u in url:
    #     url_to.append(u)
    for i in url:
        dic = {'num':'id'}
        dic['num'] = 1
        dic['id'] = i
        print(dic)
        insert = collection.insert_one(dic)
    sleep(random.randint(3, 10))



