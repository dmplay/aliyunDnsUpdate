from datetime import datetime
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler

import update
import logging


def checkDomain():
    update.checkDomain()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    logging.basicConfig(level=logging.INFO,  # 配置logging配置
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log1.txt',  # 指定日志打印到的文件
                        filemode='a')  # 文件的打开方式

    # 间隔3秒钟执行一次
    scheduler.add_job(checkDomain, 'interval', seconds=10)
    # 这里的调度任务是独立的一个线程
    g = scheduler.start()
    try:
        # 其他任务是独立的线程执行
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')