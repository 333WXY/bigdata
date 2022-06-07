# -*- coding:utf-8 -*-
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
    "cookie":'_T_WM=7233eb3af4519f17ef02c98c0fe9a83d; WEIBOCN_WM=3349; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhrO392wVX4U8IXeNZDvs5p5NHD95QfSo.ESonXSo.pWs4Dqcj8KfSZH.2t; SCF=Ai8AoA3GfkSyCEGZkLqgEhB1Ty-zk5rK8DDB0kSYCY-_pwxClC9B5Ffjt8Qov9WxPfTJHCuCMBGHvxfKbh4N40o.; SUB=_2A25PVjnsDeRhGeNI4lAX-CrKwj2IHXVsuUekrDV6PUJbktANLRnMkW1NSAzEknHBs5vnmr6uVz74pTfFonaY6Pm6; SSOLoginState=1649559996; MLOGIN=1; WEIBOCN_FROM=1110106030'
} 

id_list_num = collection.find({'num':1}).count()
id_list = collection.find({'num':1})
print(id_list_num)

session = requests.Session()
pbar = tqdm(total=id_list_num)
for i in id_list :
    pbar.update(1)
    id = i['id']
    print('正在获取 : ', id)
    url = f'https://weibo.cn/comment/{id}'
    print(url)
    page_detail = session.get(url=url,headers=headers).text.encode('utf-8')
    tree = etree.HTML(page_detail)
    text = tree.xpath('//span[@class="ctt"]//text()')
    text_del = []
    for i in text:
        if not i ==  '回复' and not i == "评论配图":
            text_del.append(i)
    print(id, '的文章+评论 : ' ,text_del)
    dic={'id':'detail'}
    dic['id'] = id
    dic['detail'] = text_del
    collection = db.detail_2
    insert = collection.insert_one(dic)

    sleep(random.randint(10, 20))
pbar.close()