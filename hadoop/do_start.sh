day=`date -d "now" +%Y%m%d`
#INPUT_DIR=/ad/zhanqun/database/corpora/all/$day
source /etc/profile
source ~/.bashrc
export HADOOP_HOME=/apps/srv/hadoop
INPUT_DIR=/ad/zhanqun/database/corpora/all/$day
echo $INPUT_DIR
OUTPUT_DIR=/ad/zhanqun/database/corpora/temp/article_num2
hls ${OUTPUT_DIR}
if [ $? -eq 0 ];then
        hrmr ${OUTPUT_DIR}
fi

#$HADOOP_HOME/bin/hadoop fs -rm -r $OUTPUT_DIR
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
    -input $INPUT_DIR \
    -output $OUTPUT_DIR \
    -mapper mapper.py \
    -file mapper.py  \
    -reducer reducer.py \
    -file reducer.py

#yesterday=`date -d "yesterday" +%Y%m%d`
#DST_FILE=/apps3/rd/xuzhihao/article/$yesterday.res
#hget $OUTPUT_DIR/part-00000 $DST_FILE