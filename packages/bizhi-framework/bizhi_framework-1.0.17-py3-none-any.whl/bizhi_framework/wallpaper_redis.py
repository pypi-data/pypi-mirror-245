# -*- coding: utf-8 -*-
"""
@Author: HuangWenBin
@Date: 2023-04-07 09:51:48
@LastEditTime: 2023-04-27 13:45:11
@LastEditors: HuangWenBin
@Description: 
"""

from seven_framework import config
from seven_framework.redis import *

class WallpaperRedisHelper():
    def __init__(self,config_key="redis"):
        host = config.get_value(config_key)["host"]
        port = config.get_value(config_key)["port"]
        db = config.get_value(config_key)["db"]
        password = config.get_value(config_key)["password"]
        self.redis_cli = RedisHelper.redis_init(host, port, db, password)


    def get(self,key):
        value=self.redis_cli.get(key)
        if value:
            return value.decode("utf-8")
        return ""
    
    def mget(self,keys:list):
        value_list=self.redis_cli.mget(keys)        
        if value_list:
            return [v.decode("utf-8") for v in value_list]
        return []

    def hget(self,name,key):
        value=self.redis_cli.hget(name,key)
        if value:
            return value.decode("utf-8")
        
        return ""
    
    def hmget(self,keys:list):
        value_list=self.redis_cli.hmget(keys)        
        if value_list:
            return [v.decode("utf-8") for v in value_list]
        return []
    
    def hincrby(self,name,key,amount=1):
        return self.redis_cli.hincrby(name,key,amount)

    def hsetnx(self,name,key,value):
        return self.redis_cli.hsetnx(name,key,value)
    
    def lpop(self,name):
        return self.redis_cli.lpop(name).decode()
    
    def llen(self,name):
        return self.redis_cli.llen(name)
    
    def expireat(self, name, when, nx: bool = False, xx: bool = False, gt: bool = False, lt: bool = False):
        return self.redis_cli.expireat(name,when,nx,xx,gt,lt)
    

if __name__=="__main__":
    redis_cli=WallpaperRedisHelper()
    redis_cli.redis_cli.set("test","test")
    value=redis_cli.redis_cli.get("test")
    print(type(value))
    print(value)