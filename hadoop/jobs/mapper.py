#!/usr/bin/env python
#!coding: utf-8
import sys

for line in sys.stdin:  # 遍历读入数据的每一行
    
    line = line.strip()  # 将行尾行首的空格去除
    words = line.split()  #按空格将句子分割成单个单词
    for word in words:
        print '%s\t%s' %(word, 1)
