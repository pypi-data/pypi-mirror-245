# -*- coding: utf-8 -*-
"""
@Author: HuangWenBin
@Date: 2023-04-18 17:02:04
@LastEditTime: 2023-08-21 14:55:56
@LastEditors: 黄文彬 huangwenbin@gao7.com
@Description: 
"""
import io
import os
import uuid

from seven_framework.file import COSHelper
from seven_framework import config

class FileUploadHelper():
    def __init__(self,upload_config):
        config_value=config.get_value(upload_config)
        self.access_key_id=config_value["access_key_id"]
        self.secret_access_key=config_value["secret_access_key"]
        self.region="ap-beijing"

    def upload_pic(self,pic_file,file_name="",pic_bucket="bizhi-pic-1319258424",pic_domain="https://p1-bos.532106.com/"):
        """
        :description: 上传图片
        :param: 图片文件
        :return url,code-success|faile
        :last_editors: HuangWenBin
        """
        if not file_name:
            file_name=str(uuid.uuid4()).replace("-","") + ".jpg"
        cos_helper=COSHelper(secret_id=self.access_key_id,secret_key=self.secret_access_key,region=self.region)
        result = cos_helper.put_file(bucket_name=pic_bucket,object_name=file_name,source_file_object=pic_file["body"])
        if result:
            url=pic_domain+file_name
            return url,"success"
        else:
            return "","faile"
        
    
        
    def upload_video(self,media_file,file_name="",media_bucket="bizhi-media-1319258424",media_domain="https://m1-bos.532106.com/"):
        file_stream=io.BytesIO(media_file["body"])
        if not file_name:
            file_name=str(uuid.uuid4()).replace("-","")+ ".MOV"
        content_length = file_stream.getbuffer().nbytes
        data=file_stream.read(content_length)
        cos_helper=COSHelper(secret_id=self.access_key_id,secret_key=self.secret_access_key,region=self.region)
        result= cos_helper.put_file(bucket_name=media_bucket,object_name=file_name,source_file_object=data)
        if result:
            url=media_domain+file_name
            return url,"success"
        else:
            return "","faile"
        
    def upload_file(self,file,file_name="",file_bucket="bizhi-file-1319258424",file_domain="https://f1-bos.532106.com/"):
        file_stream=io.BytesIO(file["body"])   
        if not file_name:     
            file_ext = os.path.splitext(file["filename"])[1]
            file_name=str(uuid.uuid4()).replace("-","")+file_ext
        content_length = file_stream.getbuffer().nbytes
        data=file_stream.read(content_length)
        cos_helper=COSHelper(secret_id=self.access_key_id,secret_key=self.secret_access_key,region=self.region)
        result= cos_helper.put_file(bucket_name=file_bucket,object_name=file_name,source_file_object=data)
        if result:
            url=file_domain+file_name
            return url,"success"
        else:
            return "","faile"
        
    
    def upload_file_from_stream(self,file_stream,file_name="",file_bucket="bizhi-file-1319258424",pic_domain="https://f1-bos.532106.com/"):
        """
        :description: 上传文件
        :return url,code-success|faile
        :last_editors: HuangWenBin
        """
        content_length = file_stream.getbuffer().nbytes
        data=file_stream.read(content_length)
        cos_helper=COSHelper(secret_id=self.access_key_id,secret_key=self.secret_access_key,region=self.region)
        result= cos_helper.put_file(bucket_name=file_bucket,object_name=file_name,source_file_object=data)
        if result:
            url=pic_domain+file_name
            return url,"success"
        else:
            return "","faile"