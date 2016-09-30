#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-26 11:47
 # Filename      : invokePluginMain.py
 # Description   : 
###########################################################
from pluginManager import DirectoryPluginManager
import os,sys

import logging
import logging.config
import codecs

logging.config.fileConfig("./conf/logging.conf")
logger = logging.getLogger('data_compute')

if __name__=='__main__':
    result_file_name = sys.argv[1]
    plugin_manager = DirectoryPluginManager()
    plugin_manager.loadPlugins()
    plugin_names = []
    #数据解析
    plugin_names.append('dataParsePlugin')
    #数据健康检查
    plugin_names.append('dataHealthPlugin')
    #唯一id生成
    plugin_names.append('idGeneratePlugin')
    #充图策略
    plugin_names.append('picFillPlugin')
    #数据指纹计算
    plugin_names.append('fingerPrintPlugin')
    #组包策略
    plugin_names.append('summaryPlugin')
    strategy_arr = []
    for e in plugin_names:
        s = plugin_manager.getPlugins(e)[0]
        strategy_arr.append(s)
    #进程初始化
    for e in strategy_arr:
        flag = e.processInit()
        if flag != 0:
            logger.error('%s processInit fail.'%(e.name))
            sys.exit(-1)
        else:
            logger.info('%s processInit succ.'%(e.name))
    f = codecs.open('./result/' + result_file_name, 'w', 'utf-8')
    #f = open('./result/' + result_file_name, 'w')
    for line in sys.stdin:
        try:
            pack = {}
            pack['origin_data'] = line.strip()
            """ 策略返回-1表示严重错误，数据丢弃；0表示数据正确；1表示策略异常，但不影响使用 """
            flag = 0
            for e in strategy_arr:
#                logger.info('strategy:%s begin.'%(e.name))
                flag = e.run(pack)
                if flag == -1:
                    logger.error('task_id:%s, strategy:%s run fail.'%(pack['task_id'], e.name))
                    break
                elif flag == 1:
                    logger.warn('task_id:%s, strategy:%s run exception.' %(pack['task_id'], e.name))
                elif flag == 0:
                    logger.info('task_id:%s, strategy:%s run succ.' %(pack['task_id'], e.name))
            if flag != -1:
                result = pack['result']
                f.write(result)
                f.write('\n')
        except:
            logger.error('unkown exception line: %s'%(line))
            continue
    f.close()
