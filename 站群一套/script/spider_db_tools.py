# -*- coding: utf-8 -*-
__author__ = 'yangxiaoyun'
#统计content中某个属性的字段值

import MySQLdb
import time
import datetime
import os,sys
import json
import types
import urllib
import urllib2
import pdb
from DBUtils.PooledDB import PooledDB

class DB():
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PWD, DB_NAME):
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PWD = DB_PWD
        self.DB_NAME = DB_NAME

        self.conn = self.getConnection()

    def getConnection(self):
       #pool = PooledDB(MySQLdb, 1, host=self.DB_HOST, user=self.DB_USER, passwd=self.DB_PWD, port=self.DB_PORT, db=self.DB_NAME, charset="utf8")
       #return pool.connection()
        return MySQLdb.Connect(
                           host=self.DB_HOST,
                           port=self.DB_PORT,
                           user=self.DB_USER,
                           passwd=self.DB_PWD,
                           db=self.DB_NAME,
                           charset='utf8'
                           )

    def query(self, sqlString):
        cursor=self.conn.cursor()
        cursor.execute(sqlString)
        returnData=cursor.fetchall()
        cursor.close()
       # self.conn.close()
        return returnData

    def update(self, sqlString):
        cursor=self.conn.cursor()
        cursor.execute(sqlString)
        self.conn.commit()
        cursor.close()


    def destroy(self):
        self.conn.close()

class DBOperation():
    def __init__(self):
        # self.db=DB('drdse7h0fv7cmp68.drds.aliyuncs.com',3306,'zhanqun','wdlPD40xjO5','zhanqun')
        self.db=DB('127.0.0.1', 3306,'root','123','resultdb')

    def tj(self, table, field):
        type_dict = {}

        sql = 'select result from %s' %(table)
        data = self.db.query(sql)
        cnt = 1
        for row in data:
            result = str(row[0])
            dataJson = json.loads(result)
            if dataJson.has_key(field):
                pass
            else:
                continue
            if type(dataJson[field]) is types.ListType:
                for key in dataJson[field]:
                    if len(key) == 0:
                        continue
                    if type_dict.has_key(key):
                        type_dict[key] = type_dict[key] + 1
                    else:
                        type_dict[key] = 1
            else:
                if len(dataJson[field]) == 0:
                    continue
                if type_dict.has_key(dataJson[field]):
                    type_dict[dataJson[field]] = type_dict[dataJson[field]] + 1
                else:
                    type_dict[dataJson[field]] = 1
        return type_dict

    def downloadData(self, table, output_file_path):
	file = open(output_file_path, 'w')
	sql = 'select taskid,result from %s' %(table)
	rows = self.db.query(sql)
	for row in rows:
	    file.write('%s$$$$$%s\n' %(row[0], json.dumps(row[1])))
	file.close()


    def loadSchemaInfo(self):
        #ins = urllib.urlopen('http://schema.baijiahulian.com/get_schema_attr/')
        #schema = ins.read()
	file = open('schema.dict')
	schema = file.read()
	file.close()
        schema_dict = eval(schema)
        info_dict = {}
        for id in schema_dict.keys():
            data_type_dict = {}
            is_must_dict = {}
            is_mul_dict = {}
            name_dict = {}
            attr_arr = schema_dict[id]
            for tmp in attr_arr:
                name = tmp['name']
                name_dict[name] = 1
                data_type_dict[name] = tmp['data_type']
                is_must_dict[name] = tmp['is_must']
                is_mul_dict[name] = tmp['is_mul']
            info_dict[id] = {}
            info_dict[id]['data_type_dict'] = data_type_dict
            info_dict[id]['is_must_dict'] = is_must_dict
            info_dict[id]['is_mul_dict'] = is_mul_dict
            info_dict[id]['name_dict'] = name_dict
        return info_dict

    def healty(self, table, node_id):
        #用node_id下的schema校验table中的数据健康
        info_dict = self.loadSchemaInfo()
        schema_attr_dict = info_dict.get(node_id)
       # sql = 'select result from %s limit 1' %(table)
       # data = self.db.query(sql)
       # for row in data:
	for line in open('./output/%s'%(table)):
	    line = line.strip()
	    f = line.split('$$$$$')
            content = json.loads(f[1])
	    dataJson = json.loads(content)
          #  dataJson = json.loads(result)
            #name验证
            for key in dataJson.keys():
                if schema_attr_dict['name_dict'].has_key(key):
                    pass
                else:
                    print 'attr:%s is not exist in schema system!' %(key)
                    return 1
            #单多值验证
                if dataJson[key] == None:
                    pass
                elif schema_attr_dict['is_mul_dict'].has_key(key):
                    if (schema_attr_dict['is_mul_dict'][key] == 1 and type(dataJson[key]) is types.ListType) \
                            or (schema_attr_dict['is_mul_dict'][key] == 0 and type(dataJson[key]) is not types.ListType):
                        pass
                    else:
                        print 'attr:%s\'s is_mul is not match to schema system!' %(key)
			return 1
                else:
                    print 'attr:%s\'s is_mul is  not exist in schema system!' %(key)
                    return 1
            #数据类型验证
                if schema_attr_dict['data_type_dict'].has_key(key):
                    real_type = 'unicode'
                    if type(dataJson[key]) is types.ListType:
                        if dataJson[key] == None:
                            real_type == 'unicode_dict'
                        else:
                            real_type = str(type(dataJson[key][0]))
                    else:
                        real_type = 'unicode'
                    if schema_attr_dict['data_type_dict'][key] == 1 and real_type.find('unicode') != -1 \
                        or schema_attr_dict['data_type_dict'][key] == 2 and real_type.find('dict') != -1:
			pass
		    else:
			print 'attr:%s data_type is not match!'%(key)
			return 1
		else:
		    print 'attr:%s data_type is not exist!'%(key)
		    return 1

	return 0

if __name__=="__main__":
 #   pdb.set_trace()
    opp_type = sys.argv[1]
    #统计result中的字段值的数量
    if opp_type == 'tj':
        #mysql的表名
        table = sys.argv[2]
        #result的json
        field = sys.argv[3]

        dbOP = DBOperation()
        result = dbOP.tj(table, field)
        print json.dumps(result, encoding="UTF-8", ensure_ascii=False)
    elif opp_type == 'health':
        #数据健康检测
        dbOP = DBOperation()
        table = sys.argv[2]
        node_id = sys.argv[3]
        ret = dbOP.healty(table, node_id)
	if ret == 1:
	    print 'data is not health'
	else:
	    print 'data is health'
    elif opp_type == 'download':
        dbOP = DBOperation()
        table = sys.argv[2]
	dbOP.downloadData(table,'../result/%s.res'%(table))
