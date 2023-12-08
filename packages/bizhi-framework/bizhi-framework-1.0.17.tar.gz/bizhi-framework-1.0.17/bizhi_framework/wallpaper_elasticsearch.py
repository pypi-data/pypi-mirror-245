from elasticsearch import Elasticsearch
from seven_framework import config
import json

class WallpaperElasticSearch():
    def __init__(self,index_name):
        """
        :description: es_client初始化
        :param index_name 索引名称
        :last_editors: HuangWenBin
        """
        hostAddress=config.get_value("es")["host"]
        self.index_name=index_name
        self.doc_type_name="_doc"
        self.es=Elasticsearch(hostAddress,sniffer_timeout=600)

    def es_index_init(self,es_model_config_path):   
        """
        :description: 索引映射初始化
        :param es_model_config_path 索引model文件路径
        :return 
        :last_editors: HuangWenBin
        """
        with open(es_model_config_path) as json_file:
            es_body=json.load(json_file)
        if es_body:
            result= self.es.indices.create(self.index_name,body=es_body)
            return result
        else:
            result={"code":"error","msg":"es_body is empty"}

    def es_querypage(self,param_body,param_size,param_from_):
        """
        :description: 读取分页数据
        :param param_body 查询语句
        :param param_size 读取数量
        :param param_from_ 读取起始位置
        :return dic_list 字段列表 count 数量 is_last_page 是否最后一页
        :last_editors: HuangWenBin
        """
        data= self.es.search(index=self.index_name,doc_type=self.doc_type_name, body=param_body,size=param_size,from_=param_from_)
        dic_list=[]
        count=0
        for item in data['hits']['hits']:
            dic_list.append(item['_source'])
        count=data['hits']['total']['value']
        isLastPage=True
        if int(count)>param_from_+param_size:
            isLastPage=False
        
        return {"dic_list":dic_list,"count":count,"is_last_page":isLastPage}

    def es_querycount(self,param_body):
        """
        :description: 根据条件查询文档数量
        :param {*} param_body 查询语句
        :return {*}count 数量
        :last_editors: HuangWenBin
        """
        count= self.es.count(body=param_body,index=self.index_name,doc_type=self.doc_type_name)
        #print(count)
        return count
    
    def es_queryrecord(self,key_name,key_value):
        """
        :description: 
        :param key_name 字段名
        :param key_value 字段值
        :return dict实体
        :last_editors: HuangWenBin
        """
        es_body={"query":{"term":{str(key_name):key_value}}}
        data= self.es.search(index=self.index_name,doc_type=self.doc_type_name,body=es_body,size=1,from_=0)
        dic_list=[]
        for item in data['hits']['hits']:
            dic_list.append(item['_source'])
        if len(dic_list)>0:
            return dic_list[0]
        return ""

    def es_update(self,key_id,**param_dict):
        """
        @description: 根据id更新数据
        @param key_id:主键id
        @param param_dict: 更新字段，字典传值
        @return: 更新成功即为True 失败则为False
        @last_editors: HuangWenBin
        """
        es_body={"doc":param_dict}
        result= self.es.update(id=key_id, index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        return result

    def es_update_by_query(self,es_body):
        """
        :description: 根据条件更新数据表
        :param es_body 更新语句
        :return :更新成功即为True 失败则为False
        :last_editors: HuangWenBin
        """
        result= self.es.update_by_query(index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        return result

    def es_add(self,id,es_body):
        """
        :description: 添加文档
        :param id 主键id
        :param es_body 文档内容
        :return 
        :last_editors: HuangWenBin
        """
        result=self.es.create(index=self.index_name,doc_type=self.doc_type_name,id=id,body=es_body)
        return result
    
    def es_delete_by_query(self,es_body):
        """
        :description: 根据条件删除数据表
        :param es_body 删除语句
        :return 成功即为True 失败则为False
        :last_editors: HuangWenBin
        """
        result= self.es.delete_by_query(index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        return result
        
    def es_delete_by_id(self,id):
        """
        :description: 根据主键id删除记录
        :param 主键id
        :return 成功即为True 失败则为False
        :last_editors: HuangWenBin
        """
        result= self.es.delete(id)
        return result
