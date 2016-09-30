#!/usr/bin/env python
#!coding: utf-8
import sys

count = 0
for line in sys.stdin:  # 遍历读入数据的每一行
    count += 1
print count  # 将行尾行首的空格去除
    
