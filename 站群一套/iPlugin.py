#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-25 15:21
 # Filename      : iPlugin.py
 # Description   : 
###########################################################
import sys
import os
#coding:utf-8
import logging, os, time


class Plugin(object):
    """ 定义一个接口，其他 插件必须实现这个接口，name 属性必须赋值 """
    name = ''
    description = ''
    version = ''
    
    def __init__(self):
        pass

    """ 进程初始化，例如词典的初始化等等 """
    def processInit(self):
        pass

    """ 数据包初始化，例如变量清空等等 """
    def packetInit(self):
        pass
    
    """ 策略返回-1表示严重错误，数据丢弃；0表示数据正确；1表示策略异常，但不影响使用 """
    def run(self, pack):
        pass
