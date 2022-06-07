import pymongo
from time import sleep
import random
from tqdm import tqdm
import json
import ast
client = pymongo.MongoClient(host = 'localhost', port=27017)
db = client.yuanshe
collection = db.detail_2
id_list_num = collection.find().count()
id_list = collection.find()
print(id_list_num)
pbar = tqdm(total=id_list_num)
for i in id_list:
    key = i['Keywords']
    list = ast.literal_eval(key)

    # print(list)
    id = i['id']
    print(id)
    if list:
        for n in list:
            collection = db.word_2
            word = n['Word']
            score =n['Score']
            text = {
                'id':id,
                'word':word,
                'score':score
            }

            result = collection.insert_one(text)

    pbar.update(1)
        
