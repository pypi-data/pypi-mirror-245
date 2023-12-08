# -*- coding: utf-8 -*-
"""
@Author: HuangWenBin
@Date: 2023-05-06 09:29:53
@LastEditTime: 2023-05-06 10:11:22
@LastEditors: HuangWenBin
@Description: 
"""
import urllib.parse
import requests
import json
from wallpaper_redis import *

class BDCensorHelper():
    def __init__(self,app_id=23990383) -> None:
        self.__app_id=app_id        
        self.__set_api_key()
        self.__token=self.get_token()

    def __set_api_key(self):
        if self.__app_id==23990383:
            self.__api_key="k3Wl1uk4GueLO6N7LqviYqL9"
            self.__secret_key="o8drefKGeP2AdLkRW3HtfxaCaGiFIRqn"
        elif self.__app_id==24019798:
            self.__api_key="a5aZCkokYnCIeyEpEPaQ9mIy"
            self.__secret_key="WBUaIylvHqOIyX5xQUU716PQV4lPk39d"

    def get_token(self):
        redis_key="BDAIToken:{0}".format(self.__app_id)
        redis_cli=WallpaperRedisHelper()
        token= redis_cli.get(redis_key)
        if token:
            return token
        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(self.__api_key,self.__secret_key)  
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code==200:
            result_dict=json.loads(response.text)
            token=result_dict["access_token"]
            expires_in=int(result_dict["expires_in"])-60
            if token:
                redis_cli.redis_cli.set(redis_key,token,ex=expires_in)
        
        return token
        
    def img_censor(self,image_url):
        code=0
        message=""
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + self.__token
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
            }
        params="imgUrl={0}&imgType=0".format(image_url)
        response = requests.post(request_url, data=params, headers=headers)
        if response.status_code==200:
            result_dict=json.loads(response.text)
            if not result_dict or not result_dict["conclusion"]=="合规":
                code=0
                message="违规图片"
                if result_dict["data"]:
                    msg_list=[m.get("msg") for m in result_dict["data"]]
                    message=",".join(msg_list)
            else:
                code=1
        else:
            code=0
            message="接口请求失败"
        
        return code,message
    
    def txt_censor(self,word):
        code=0
        message=""
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + self.__token
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
            }
        params="text={0}".format(urllib.parse.quote(word))
        response = requests.post(request_url, data=params, headers=headers)
        if response.status_code==200:
            result_dict=json.loads(response.text)
            if not result_dict or not result_dict["conclusion"]=="合规":
                code=0
                message="违规内容"
                if result_dict["data"]:
                    msg_list=[m.get("msg") for m in result_dict["data"]]
                    message=",".join(msg_list)
            else:
                code=1
        else:
            code=0
            message="接口请求失败"
        
        return code,message

    def video_censor(self,video_url,video_id,video_name):
        code=0
        message=""
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + self.__token
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
            }
        params="name={0}&extId={1}&videoUrl={2}".format(video_name,video_id,video_url)
        response = requests.post(request_url, data=params, headers=headers)
        if response.status_code==200:
            result_dict=json.loads(response.text)
            if not result_dict or not result_dict["conclusion"]=="合规":
                code=0
                message="违规图片"
                if result_dict["data"]:
                    msg_list=[m.get("msg") for m in result_dict["data"]]
                    message=",".join(msg_list)
            else:
                code=1
        else:
            code=0
            message="接口请求失败"
        
        return code,message
