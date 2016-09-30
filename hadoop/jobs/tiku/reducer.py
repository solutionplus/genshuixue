#!/usr/bin/env python
#!coding: utf-8

import os,sys
import json
import re
import time
reload(sys)
sys.setdefaultencoding("utf-8")


def writeBck(record):
    id = record['id']
    cls = record['class']
    content = record['content']
    source = record['source']
    update_time = record['update_time']
    taskid = record['taskid']
    print '%s%s%s%s%s%s' %(id, cls, json.dumps(content), source, update_time, taskid)

def parseLine(line):
    try:
        line = line.strip()
        f = line.split('')
        if len(f) != 6:
            return None
        id = f[0]
        cls = f[1]
        content = json.loads(f[2])
        source = f[3]
        update_time = f[4]
        taskid = f[5]
        record = {}
        record['id'] = id
        record['class'] = cls
        record['content'] = content
        record['source'] = source
        record['update_time'] = update_time
        record['taskid'] = taskid
        return record
    except:
        traceback.print_exc(sys.stdin)
        return None


best_record = {}
old_key = '0'
best_time = time.strptime('2012-02-17 12:49:04', '%Y-%m-%d %H:%M:%S')
if __name__=='__main__':
    for line in sys.stdin:
        try:
            line = line.strip()
            f = line.split('\t')
            new_key = f[0]
            line = line.replace('%s\t'%(f[0]), '')
            record = parseLine(line)
            str = record['update_time']
            time_f = str.split('.')
            record['update_time']= time_f[0]
            record_update_time = time.strptime(record['update_time'], '%Y-%m-%d %H:%M:%S')
            if old_key == '0':
                best_record = record
                best_time = record_update_time
                old_key = new_key
                continue
            else:
                if old_key == new_key:
                    if record_update_time > best_time:
                        best_record = record
                        best_time = record_update_time
                    continue
                else:
                    writeBck(best_record)
                    best_record = record
                    old_key = new_key
                    best_time = record_update_time
        except:
            continue
    writeBck(best_record)
