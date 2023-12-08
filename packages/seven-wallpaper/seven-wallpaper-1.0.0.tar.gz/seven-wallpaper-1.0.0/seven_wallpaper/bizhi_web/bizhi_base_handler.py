
from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_wallpaper.app_encrypt import *
from seven_wallpaper.useranget import *

class WallpaperBaseHandler(BaseApiHandler):
    def __init__(self, *argc, **argkw):
        """
        :Description: 初始化
        :last_editors: ChenXiaolei
        """
        super(BaseApiHandler, self).__init__(*argc, **argkw)

    def get_useragent(self):
        """
        @description:获取app客户端头部信息
        @return：返回头部信息
        @last_editors: HuangWenBin
        """
        user_agent= UserAgentInfo()
        dic_header=self.request.headers
        if "User-Agent1" not in dic_header:
            return user_agent
        user_agent1=dic_header._dict["User-Agent1"]
        if user_agent1.startswith("2"):
            user_agent1=user_agent1[1:]
        #dict_useragent={}
        decrypt=app_des_encrypt()
        user_agent1=decrypt.des_decrypt(user_agent1)
        list_str = str.split(CodingHelper.url_decode(user_agent1.decode("unicode_escape")), "&")

        for item in list_str:
                key,value=item.split("=",1)
                if hasattr(user_agent, key):
                    if key in["pid","pt","ch","ver","adolescent","login"]:
                        if value:
                            setattr(user_agent, key, int(value))
                        else:
                            setattr(user_agent, key, 0)
                    else:
                        if value:
                            setattr(user_agent, key, value)
                        else:
                            setattr(user_agent, key, "")

        user_agent.userip=self.get_remote_ip()
        return user_agent

    def get_request_param(self, param_name, default=""):
        if not param_name in self.request_params:
            return default
        param_ret=self.request_params[param_name]
        return param_ret
    
    def get_request_param_int(self, param_name, default=0):
        param_ret=self.get_request_param(param_name,"0")
        if not param_ret or param_ret == "0":
            param_ret = default
        return int(param_ret)
    
    def get_param_int(self,param_name,default=0):
        param_value= self.get_param(param_name)
        if param_value:
            return default
        return int(param_value)

    def get_url_param(self,url,param_name):
        url=CodingHelper.url_decode(url)
        list_str = str.split(url,"&")
        for item in list_str:
            kv=item.split("=")
            if len(kv)==2 and kv[0]==param_name:
                return kv[1]        
        return ""



