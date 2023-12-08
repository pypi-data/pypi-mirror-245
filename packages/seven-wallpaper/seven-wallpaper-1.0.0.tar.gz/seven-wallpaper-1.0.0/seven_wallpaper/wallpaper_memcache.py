# -*- coding: utf-8 -*-
"""
@Author: HuangWenBin
@Date: 2023-03-06 18:18:42
@LastEditTime: 2023-08-30 15:46:59
@LastEditors: 黄文彬 huangwenbin@gao7.com
@Description: 
"""
'''
description: memcached 帮助类
last_editors: HuangWenBin
'''
from seven_framework.memcached import *
from seven_framework import config
import hashlib

class WallpaperMemcacheHelper():
    def __init__(self,depan_key="",cache_key=""):    
        memcache_config=config.get_value("memcached")
        self.host_list=memcache_config["nodes"]
        self.node_num=memcache_config["node_num"]
        self.is_cache=memcache_config["is_cache"]
        self.is_debug=True
        if depan_key:
            self.md5_depan_key,node_index=self.__get_md5_key(key=depan_key)
            self.md5_key=hashlib.md5((depan_key+cache_key).encode("utf-8")).hexdigest()
            self.__mc= MemcachedHelper([self.host_list[node_index]],self.is_debug).memcached_client
        elif cache_key:
            self.md5_key,node_index=self.__get_md5_key(key=cache_key)
            self.__mc= MemcachedHelper([self.host_list[node_index]],self.is_debug).memcached_client
        else:
            self.__mc=None

        
    def m_set(self,value,time=60*30):
        '''
        description: 设置单个缓存
        param value 缓存值
        param time 过期时间(单位：秒)
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return
        self.__mc.set(key=self.md5_key,val=value,time=time)

    def m_get(self):
        '''
        description: 获取单个缓存
        return 缓存值
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return None
        return self.__mc.get(key=self.md5_key)

    def m_depan_set(self,value,time=60*30):
        '''
        description: 设置依赖缓存
        param value 缓存值
        param time 过期时间(单位：秒)
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return
        md5_key_in_depan_list=[]
        md5_depan_key_value= self.__mc.get(key=self.md5_depan_key)
        if md5_depan_key_value:
            md5_key_in_depan_list=list(md5_depan_key_value)
            md5_key_in_depan_list.append(self.md5_key)
            md5_key_in_depan_list=list(set(md5_key_in_depan_list))            
        else:
            md5_key_in_depan_list.append(self.md5_key)
        
        self.__mc.set(key=self.md5_depan_key,val=md5_key_in_depan_list,time=time)
        self.__mc.set(key=self.md5_key,val=value,time=time)

    def m_depan_get(self):
        '''
        description: 获取依赖缓存值
        return 缓存值
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return None
        return self.__mc.get(key=self.md5_key)

    def m_remove(self):
        '''
        description: 删除单个缓存
        return 删除缓存数量
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return 0
        return self.__mc.delete(self.md5_key)

    def m_depan_remove_one(self):
        '''
        description: 删除依赖键下所有缓存
        return 删除缓存数量
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return 0
        md5_key_in_depan_list=[]
        md5_depan_key_value= self.__mc.get(key=self.md5_depan_key)
        if md5_depan_key_value:
            md5_key_in_depan_list=list(md5_depan_key_value)
            if self.md5_key in md5_key_in_depan_list:
                md5_key_in_depan_list.remove(self.md5_key)
            self.__mc.set(key=self.md5_depan_key,val=md5_key_in_depan_list,time=1800)
            self.__mc.delete(key=self.md5_key)
            return 1
        
        return 0
    
    def m_depan_remove(self):
        '''
        description: 删除依赖键下所有缓存
        return 删除缓存数量
        last_editors: HuangWenBin
        '''
        if not self.is_cache:
            return 0
        md5_key_in_depan_list=[]
        md5_depan_key_value= self.__mc.get(key=self.md5_depan_key)
        if md5_depan_key_value:
            md5_key_in_depan_list=list(md5_depan_key_value)
            result=self.__mc.delete_multi(keys=md5_key_in_depan_list)
            if result:
                self.__mc.delete(key=self.md5_depan_key)
            return result
        
        return 0

    def __get_md5_key(self,key):
        '''
        description: 获取缓存键值名称16进制加密值以及缓存节点索引
        param key 缓存名称
        return 16进制加密值以及缓存节点索引
        last_editors: HuangWenBin
        '''
        md5_key=hashlib.md5(key.encode("utf-8")).hexdigest()
        long_md5_key=int(md5_key,16)
        node_index=long_md5_key%self.node_num
        return md5_key,node_index

