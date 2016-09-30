source /etc/profile
source ~/.bashrc
INPUT_DIR_INC=/ad/zhanqun/database/wenda_tiku/all/wenda/20160617
hls $INPUT_DIR_INC
if [ $? -ne 0 ];then
    echo 'error'
    exit 0
fi
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
    -files ./mapper1.py,./reducer1.py \
    -mapper ./mapper1.py \
    -reducer ./reducer1.py \
    -input $INPUT_DIR_INC/part-00001_dst_dst_dst \
    -output /ad/zhanqun/database/wenda_tiku/inc/test/output \
