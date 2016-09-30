
killall pyspider
if [  $? -ne 0 ];then
	echo "kill spider failded!"
fi

kill -9 $(lsof -i:25555|tail -n 1 | awk  '{print $2}')
if [ $? -ne 0 ];then
	echo "kill phantomjs failed!"
fi
