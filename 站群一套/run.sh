#!/bin/bash
source ~/.bashrc


WORK_DIR=`pwd`
DATA_DIR=${WORK_DIR}/../spider_data
CONF_DIR=${WORK_DIR}/conf
RES_DIR=${WORK_DIR}/result
PROJECT_NAME=$1
file_path=${DATA_DIR}/${PROJECT_NAME}.res
DT=`date +'%Y%m%d'`
HADOOP_DEST_DIR=/ad/zhanqun/database/corpora/inc/$DT
export JAVA_HOME=/apps/srv/jdk
echo '##################################################'
#1.获取配置文件
cd $CONF_DIR
wget http://schema.baijiahulian.com/get_schema_attr/
if [ $? -ne 0 ];then
    echo ${PROJECT_NAME} 'wget schema fail'
    exit 1
fi
mv index.html schema.dict

#2.获取工程数据文件
cd $WORK_DIR
sh fetch_data.sh $PROJECT_NAME $DATA_DIR
if [ $? -ne 0 ];then
    echo ${PROJECT_NAME} 'fetch_data fail'
    exit 2
fi
#3.数据计算＋充图
cat ${DATA_DIR}/${PROJECT_NAME}.res | /usr/local/bin/python2.7 invokePluginMain.py ${PROJECT_NAME} 
if [ $? -ne 0 ];then
    echo ${PROJECT_NAME} 'invokePluginMain fail'
    exit 3
fi

/apps/srv/hadoop/bin/hadoop fs -ls $HADOOP_DEST_DIR
if [ $? -ne 0 ];then
    /apps/srv/hadoop/bin/hadoop fs -mkdir $HADOOP_DEST_DIR
fi
#将充图后的数据put到hdfs上
/apps/srv/hadoop/bin/hadoop fs -put ${RES_DIR}/${PROJECT_NAME}  $HADOOP_DEST_DIR
