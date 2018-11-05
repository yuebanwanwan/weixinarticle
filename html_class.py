import logging


from bs4 import BeautifulSoup

logging.basicConfig(filename='/Users/mac/Desktop/Python-Scrapy/weixinarticle/urlLogging.txt',level=logging.INFO)


class Html(object):
    """
    html类，表示一个html页面源码
    """
    def __init__(self,html=None):
        """
        初始化html变量，若为空则初始化为空list
        :param html:type list
        """
        self.html = [] if html is None else html
        self.html.append('<!DOCTYPE html>')
        self.html.append('')

    def _addTitle(self,value):
        """
        添加标题标签
        :param value:type:str
        :return:
        """
        assert isinstance(value,str),'value must be a str class!'
        Element = '<head>\n<meta charset="UTF-8">\n<meta name="referrer" content="never">\n<title>' + value + '</title>\n</head>'
        logging.info('title:' + Element)
        self.html.append(Element)

    def _addImg(self,value):
        """
        添加图片链接标签
        :param value:type:str
        :return:
        """
        assert isinstance(value,str),'value must be a str class!'
        Element = '<img src="' + value + '"/>'
        logging.info('img:' + Element)
        self.html.append(Element)

    def _addWord(self,value):
        """
        添加文本标签
        :param value:type:str
        :return:
        """
        assert isinstance(value,str),'value must be a str class!'
        Element = '<span>' + value + '</span>'
        logging.info('word:' + Element)
        self.html.append(Element)

    def _addVideo(self,value):
        """
        添加视频链接标签
        :param value:type:str
        :return:
        """
        assert isinstance(value,str),'value must be a str class!'
        Element = '<iframe src="' + value + '"/>'
        Element = '<video width="320" height="240" controls="controls">\n<source src="' + value +'" type="video/ogg">\n<source src="' + value + '" type="video/mp4">\nYour browser does not support the video tag.\n</video>'
        logging.info('video:' + Element)
        self.html.append(Element)

    def __str__(self):
        return '\n'.join(self.html)


if __name__ == '__main__':
    title = 'Hello world!'
    word = 'Hello word!'
    img = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1541335954390&di=54bf3c40bd45201cf749307670cf64d2&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F6c224f4a20a44623639e57469222720e0cf3d7ba.jpg'
    video = 'http://baishi.baidu.com/watch/06212930388548252356.html?&page=videoMultiNeed'
    html = Html()
    html._addTitle(title)
    html._addWord(word)
    html._addImg(img)
    html._addVideo(video)
    logging.info(html)
    html = str(html)
    soup = str(BeautifulSoup(html,"html5lib"))
    print(soup)
    with open('/Users/mac/Desktop/Python-Scrapy/weixinarticle/test_HTML.html', 'w') as f:
        f.write(soup)

def article_to_html(article):
    """
    文章和HTML对接
    :param article:type:dict
    :return:
    """
    content = article['article_content']
    title = article['title']
    html = Html()
    html._addTitle(title)
    for item in content:
        if item.get('article_word',None) is not None:
            html._addWord(item.get('article_word',None))
        elif item.get('article_img_url',None) is not None:
            html._addImg(item.get('article_img_url',None))
        elif item.get('article_video_url',None) is not None:
            html._addVideo(item.get('article_video_url',None))
    html = str(html)
    soup = str(BeautifulSoup(html, "html5lib"))
    print(soup)
    with open('/Users/mac/Desktop/Python-Scrapy/weixinarticle/HTML/' + str(article['datetime']) + '.html', 'w') as f:
        f.write(soup)
