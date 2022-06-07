import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

import pymongo
from time import sleep
import random
from tqdm import tqdm

client = pymongo.MongoClient(host = 'localhost', port=27017)
db = client.yuanshe
collection = db.detail_1
id_list_num = collection.find({'Keywords':None}).count()
id_list = collection.find({'Keywords':None})
print(id_list_num)

pbar = tqdm(total=id_list_num)
for i in id_list :
    pbar.update(1)
    id = i['id']
    detail = i['detail']
    params_detail = {'Text':f'{detail}'}


    try:
        cred = credential.Credential("AKIDgBQP7YibEafU1HGyQbWAWcRzGH12nHUQ", "g5E7j36tOcaIkwrVt0qQkmX1D9oCJAk4")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.KeywordsExtractionRequest()
        params = params_detail        
        # params = {
        # 'Text':'[":【", "#张家口云顶霁雪美如画#", "】", "#河北爆料#", " 3月18日清晨，张家口市崇礼区云顶滑雪公园及周边群山迎来春雪暂停后的短暂日出，白雪覆盖下的崇山峻岭及雪道在阳光的照耀下绚丽多姿，美不胜收。（河北日报）", "#河北身边事#", " "]'

        # }
        req.from_json_string(json.dumps(params))

        resp = client.KeywordsExtraction(req)
        # print(resp.to_json_string())
        resp=json.loads(resp.to_json_string())
        print(resp)
        condition = {'id':f'{id}'}
        emo_upd = collection.find_one(condition)
        emo_upd['Keywords']=resp['Keywords']    
        result = collection.update_one(condition,{'$set':emo_upd})
    except TencentCloudSDKException as err:
        print(err)
