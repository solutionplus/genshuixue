#INPUT_DIR_INC=/ad/zhanqun/database/corpora/inc/*
#INPUT_DIR_ALL=/ad/zhanqun/database/wenda_tiku/all/tiku/20160617
INPUT_DIR_ALL=/ad/zhanqun/database/wenda_tiku/all/tiku/20160617/21cnjy.res
OUTPUT_DIR=/ad/zhanqun/database/corpora/temp/tiku_all
$HADOOP_HOME/bin/hadoop fs -rmr $OUTPUT_DIR
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
    -input $INPUT_DIR_ALL \
    -output $OUTPUT_DIR \
    -mapper ./mapper.py \
    -file ./mapper.py
