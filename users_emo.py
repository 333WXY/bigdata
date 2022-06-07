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
collection = db.detail_2
id_list_num = collection.find({'Positive':None}).count()
id_list = collection.find({'Positive':None})
print(id_list_num)

pbar = tqdm(total=id_list_num)
for i in id_list :
    pbar.update(1)
    id = i['id']
    detail = i['detail']
    params_detail = {'Text':f'{detail}'}
    try:
        cred = credential.Credential("AKIDgBQP7YibEafU1HGyQbWAWcRzGH12nHUQ", 
                                    "g5E7j36tOcaIkwrVt0qQkmX1D9oCJAk4")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.SentimentAnalysisRequest()
        params = params_detail
        # params = {
        #    'Text':'[":", "#冬奥风吹春色新#", " 这是张家口崇礼区云顶滑雪公园的景色。 "]'
        # }
        req.from_json_string(json.dumps(params))

        resp = client.SentimentAnalysis(req)    
        
        
    
        resp=json.loads(resp.to_json_string())
        print(resp)
        condition = {'id':f'{id}'}
        emo_upd = collection.find_one(condition)
        emo_upd['Positive']=resp['Positive']
        emo_upd['Neutral']=resp['Neutral']
        emo_upd['Negative']=resp['Negative']
        emo_upd['Sentiment']=resp['Sentiment']

        result = collection.update_one(condition,{'$set':emo_upd})



    except TencentCloudSDKException as err:
        print(err)

