#!/usr/bin/env python
#!coding: utf-8

from operator import itemgetter
import sys

current_word = None  # 为当前单词
current_count = 0  # 当前单词频数
word = None
count = 0
for line in sys.stdin:
    count += int(line.strip())  # 去除字符串首尾的空白字符
    
print count
