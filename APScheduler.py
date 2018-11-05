import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def job1():
    print(datetime.datetime.now())
    print('job1 is runing...')

def job2(param,param2):
    print('param:' + param)
    print('param2:' + param2)
    print(datetime.datetime.now())
    print('job2 is runing...')

#创建调度器
print('--------1-------')
scheduler = BlockingScheduler()
# trigger:触发，有以下三个参数
# interval:循环触发间隔时间
# cron:定时任务
# date:具体时间的一次性任务
scheduler.add_job(func=job1,trigger='interval',seconds=3,id='job1')
scheduler.add_job(func=job2,args=['66666','77777'],trigger='interval',seconds=1,id='job2')
scheduler.start()
print('--------2-------')





