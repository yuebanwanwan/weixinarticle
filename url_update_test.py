import time
import logging

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(filename='/Users/mac/Desktop/Python-Scrapy/weixinarticle/urlLogging.txt',level=logging.WARNING)
def gzh_mainpage_test(url):
    response = requests.get(url=url)
    if response.status_code == 200:
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        logging.warning(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # print('公众号主页链接:' + url + '有效!')
        logging.warning('公众号主页链接:' + url + '有效!')
    else:
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        logging.error(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # print('公众号主页链接:' + url + '无效!')
        logging.error('公众号主页链接:' + url + '无效!')

def gzh_article_test(url):
    response = requests.get(url=url)
    if response.status_code == 200:
        logging.warning(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        logging.warning('公众号主页链接:' + url + '有效!')
    else:
        logging.error(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        logging.error('公众号主页链接:' + url + '无效!')

def scheduler(url):
    schedu = BlockingScheduler()
    schedu.add_job(func=gzh_mainpage_test,trigger='interval',seconds=1000,id=str(time.time()),args=[url['main_page_url']])
    schedu.add_job(func=gzh_article_test, trigger='interval', seconds=1200, id=str(time.time()),
                   args=[url['main_article_url']])
    schedu.start()

if __name__ == '__main__':
    url = {'main_page_url':'http://mp.weixin.qq.com/profile?src=3&timestamp=1541054936&ver=1&signature=e*oeynerSAcgZfln1J8e*vCHKV2jg3oZqqAQwFIiE1z4ql4E7spI4U2kjtJDiG1oTZZf7oblb-*9aQA==',
           'main_article_url':'https://mp.weixin.qq.com/s?timestamp=1541064848&src=3&ver=1&signature=BIt8eYPNqCqJGkoy53O-Vgj5RLAjuO*pjbIWw2IZc1PVs0O9vL1mwsOt9gSyIJkq16in*osX9oLc5jo83uA0bYBtDVu6RbsUdEy5pH*ZGbGteILWBw2dgwf*2C1a2pLsNd45Cc*xu0FVLJIDibUlWRnWflTEWQbjPjjBotn1m94='
           }
    scheduler(url)








