1.启动pyspider(rd用户)
cd /apps/home/rd/hexing/pyspider-master && sh start.sh
2.杀掉pyspider(rd用户)
cd /apps/home/rd/hexing/pyspider-master && sh kill.sh
3.启动pyspider的配置文件
/apps/home/rd/hexing/pyspider-master/config.json (默认连上本机的redis的标号1的库作为消息队列)
4.pyspider流程：
scheduler调度项目对应的内存任务队列---->scheduler2fetcher----->fetcher2processor---->(processor2resultwork,newtask_queue,statusqueue)
scheduler取newtask_queue里的任务,判断其是不是新任务： 1)是新任务,则加入数据库并且放到对应的项目内存队列,等待scheduler调度给scheduler2fetcher; 2).是旧任务，则判断其有没有过期(age)，过期了则更新该任务的在数据库里的状态为active并且再次加入对应的项目内存队列,等待scheduler调度给scheduler2fetcher，若没过期，则过滤掉不做操作。
scheduler取statusqueue里的任务,判断其有没有执行成功： 1).执行ok,则更新数据库该任务的状态为success; 2)执行error,则默认会重试4次，在不同的间隔直到这4次爬取成功，若4次都不成功，则不会在运行。 这里可以设置auto_recrawl和age改变这里的运行逻辑，让其不管执行成功和失败都固定重复运行，具体见下面的auto_recrawl解析。
5.pyspider注意点：
itag,auto_recrawl,force_update,age字段含义
1).建议inc任务的list_page和detail_page都设置age,且age都为1
2).设置force_update属性(force_update=True,默认没有设置该属性)，意味着该项目的不会对url去重，任务会不停止的运行，适用于需要实时爬取的任务
3).itag的用处,当你想重新跑某个项目的情况下，你可以给项目加个itag(加之前先stop掉该项目运行)，用处在于能再次跑数据库里已经跑过的task
4).auto_recrawl和age一般连用,连用的情况下一般是指在指定时间间隔再次运行对应task，对于运行的成功的task下次运行时间是当前时间＋age，失败的task，下次运行时间由多个因素决定，且对于失败的任务默认会再次运行四次，分别间隔30s,1h,6h,12h,1d DEFAULT_RETRY_DELAY = { 0: 30, 1: 1*60*60, 2: 6*60*60, 3: 12*60*60, '': 24*60*60 }
总结：如果同时设置auto_recrawl和age,对于成功的task,会自动不停的跑，每次重新开始时间是当前时间+age,若是失败的task，则也会不停止的跑，下次执行时间是多个因素决定，但是重点都是同时设置auto_recrawl和age的前提下，不管失败或者成功，都是循环跑，只是间隔时间不同
5)对于redis的五个队列，默认启动的时候不给队列长度大小的情况下，默认为100，意味着每个消息队列最多存100条消息，在机器内存大的情况下，可以设置--queue-maxsize属性，加大默认值，这样可以加快爬虫运行速度
6)对于redis5个队列中的newtask_queue每条消息实际最多存1000个task(其他4个redis队列都是一条消息存1个task)，意味着在默认情况下(queue-maxsize=100),newtask_queue最多可以存1000*100=10w个task