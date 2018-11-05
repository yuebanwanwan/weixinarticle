import time
import logging

import wechatsogou
from lxml import etree
from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler


import html_class

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(executable_path='/usr/local/chromedriver', options=chrome_options)

logging.basicConfig(filename='/Users/mac/Desktop/Python-Scrapy/weixinarticle/urlLogging.txt',level=logging.INFO)


def resolution_article_page(response_text):
    """
    :param response_text:str 页面的源代码
    :return:
    """
    # article = {'article_word':[],'article_img_url':[],'article_video_url':[]}
    article = []
    response = etree.HTML(response_text)
    all_item = response.xpath('//div[@id="js_content"]//p')
    assert len(all_item) > 0,'all_item为空'
    for item in all_item:
        if len(item.xpath('.//img')) > 0:
            assert len(item.xpath('.//img/@data-src')) > 0, 'img is null'
            img = item.xpath('.//img/@data-src')[0]
            logging.info(img)
            article.append({'article_img_url':img})
        elif len(item.xpath('.//iframe')) > 0:
            assert len(item.xpath('.//iframe')) > 0,'iframe is null'
            video = item.xpath('.//iframe/@src')[0]
            logging.info(video)
            article.append({'article_video_url':video})
        elif len(item.xpath('.//span//text()')) > 0:
            assert len(item.xpath('.//span')) > 0,'span is null'
            word = ''.join(item.xpath('.//span//text()')).strip()
            logging.info(word)
            article.append({'article_word':word})
        elif len(item.xpath('.//mpvoice')) > 0:
            assert len(item.xpath('.//mpvoice')) > 0,'voice is null'
            voice = item.xpath('.//mpvoice/@src')[0]
            logging.info(voice)
            article.append({'article_voice':voice})
        else:
            pass
    return article

def request_article(article):
    """
    根据文章的url属性返回文章的内容
    :param article:
    :return: 文章内容(每段文字，图片，视频按出现顺序排列)
    """
    browser.get(article['content_url'])
    # result = etree.HTML(browser.page_source)
    # article_content = ''.join(result.xpath('//div[@id="js_content"]//span//text()')).strip()
    # article_content = browser.page_source
    article_content = resolution_article_page(browser.page_source)
    return article_content

def get_article_content(gzh):
    """
    该函数接受公众号参数返回该公众号最新的10篇文章以及这些文章中最新的时间戳
    :param gzh: 公众号
    :return: 最新的更新时间以及新的文章列表
    数据结构 = {
    'gzh': {
        'wechat_name': '',  # 名称
        'wechat_id': '',  # 微信id
        'introduction': '',  # 简介
        'authentication': '',  # 认证
        'headimage': ''  # 头像
    },
    'article': [
        {
            'datetime': int,  # 群发datatime 10位时间戳
            'title': '',  # 文章标题
            'abstract': '',  # 摘要
            'content_url': '',  # 文章链接
            'cover': '',  # 封面图
            'author': '',  # 作者
            'copyright_stat': int,  # 文章类型
        },
        ...
      ]
    }
    """
    ws_api = wechatsogou.WechatSogouAPI()
    result = ws_api.get_gzh_article_by_history(gzh)
    # print(result)
    articles = result.get('article')
    new_articles = []
    latest_time = 0
    latest_time_in_file = ''
    with open('/Users/mac/Desktop/Python-Scrapy/weixinarticle/latest_time.txt', 'r') as f:
        latest_time_in_file = f.read()
    for article in articles:
        # 如果不是第一次则处理更新的文章
        if len(latest_time_in_file) > 0 and article['datetime'] > int(latest_time_in_file):
            article['article_content'] = request_article(article)
            new_articles.append(article)
        # 第一次获取公众号最近的10篇文章
        elif len(latest_time_in_file) == 0:
            article['article_content'] = request_article(article)
            new_articles.append(article)
        if article['datetime'] > latest_time:
            latest_time = article['datetime']
    return {'latest_time':latest_time,'articles':new_articles}

def begin_test(gzh):
    """
    以公众号及其设置的循环测试时间为列表元素，循环测试每个公众号，对文章进行增删改查
    gzh_list: [{'gzh':'smcode2016','cycle_time':300},{'gzh':'gh_018e1a6f90ea','cycle_time':600}]
    gzh: 公众号
    :return:
    """
    result = get_article_content(gzh)
    latest_time = str(result['latest_time'])
    articles = result['articles']
    for article in articles:
        print('新增了文章')
        print(article)
        html_class.article_to_html(article)
    latest_time_in_file = ''
    with open('/Users/mac/Desktop/Python-Scrapy/weixinarticle/latest_time.txt', 'r') as f:
        latest_time_in_file = f.read()
    if len(latest_time_in_file) == 0:
        with open('/Users/mac/Desktop/Python-Scrapy/weixinarticle/latest_time.txt', 'w') as f:
            f.write(latest_time)
    else:
        """文件中的最新时间大于最新10篇文章中的最新时间"""
        if int(latest_time_in_file) > int(latest_time):
            """判断此时该公众号删除了文章，此时应该删除数据库中所有大于最新10篇文章中最新时间的文章"""
            for article in articles:
                pass
        elif int(latest_time_in_file) < int(latest_time):
            with open('/Users/mac/Desktop/Python-Scrapy/weixinarticle/latest_time.txt', 'w') as f:
                """更新最新时间戳"""
                f.write(latest_time)
        else:
            print('未进行文章的增删!')

def scheduler(gzh_list):
    """
    以一个公众号+循环测试时间为单位，添加到调度任务
    :param gzh_list:[{'gzh':'smcode2016','cycle_time':300},{'gzh':'gh_018e1a6f90ea','cycle_time':600}]
    :return:
    """
    schedu = BlockingScheduler()
    for each_gzh in gzh_list:
        schedu.add_job(func=begin_test,trigger='interval',seconds=each_gzh['cycle_time'],id=str(time.time()),args=[each_gzh['gzh']])
    schedu.start()

if __name__ == '__main__':
    gzh_list = [{'gzh': 'smcode2016', 'cycle_time':20}]
    scheduler(gzh_list)
# X = 1540891534
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(X)))
# 2018-10-30 17:25:34