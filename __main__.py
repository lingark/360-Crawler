import requests as rq
from lxml import etree
import linecache
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    # 设置请求头("反反爬虫")
    }
def get_html(url,headers=None):
    ret=rq.get(url,headers=headers) # 发送请求
    response=ret.content.decode(errors='ignore') # 获得响应内容(utf-8编码)
    return response # 返回响应内容

def download_file(url,headers=None,filename=None):
    ret=rq.get(url,headers=headers)
    response=ret.content
    with open(filename,'wb') as f:
        f.write(response) # 保存文

def save_to_file(filename,data):
    with open(filename,'a+',encoding='utf-8') as f:
        f.write(data+'\n')

def douban_top250():
    for i in range(4):
        if i==0:
            download_file("http://movie.douban.com/top250/",headers=headers,filename='0.html')
            html = open(str(i)+'.html', encoding='utf-8').read()
            selector=etree.HTML(html)
            movie_list=selector.xpath('//div[@class="item"]')
            for movie in movie_list:
                title=movie.xpath('.//span[@class="title"]/text()')
                score=movie.xpath('.//span[@class="rating_num"]/text()')
                print(title[0],score[0])
                save_to_file('douban.txt',title[0]+':'+score[0])
        else:
            download_file('http://movie.douban.com/top250/?'+"start="+str(i*25)+'&filter=',headers=headers,filename=str(i)+'.html')
            html = open(str(i)+'.html', encoding='utf-8').read()
            selector=etree.HTML(html)
            movie_list=selector.xpath('//div[@class="item"]')
            for movie in movie_list:
                title=movie.xpath('.//span[@class="title"]/text()')
                score=movie.xpath('.//span[@class="rating_num"]/text()')
                print(title[0],score[0])
                save_to_file('douban·.txt',title[0]+':'+score[0])
def news163(headers=None):
    url='http://news.163.com/'
    response=get_html(url,headers=headers)
    selector=etree.HTML(response)
    news_list=selector.xpath('//li[@class="newsdata_item"]')
    for news in news_list:
        title=news.xpath('.//div//a/text()')
        href=news.xpath('.//div//a/@href')
        for i in range(len(title)):
            save_to_file('news163.txt',title[i]+':'+href[i])
    return open('news163.txt','r',encoding='utf-8').readlines()
def news_163news(headers=None):
    try:
        num=int(input("请输入要读取的行数"))
    except:
        print("请输入阿拉伯数字")
    file=linecache.getline('news163.txt',num)
    url = file[file.find(":")+1:]
    response=get_html(url=url,headers=headers)
    selector=etree.HTML(response)
    post_main=selector.xpath('//div[@class="post_main"]')
    for news in post_main:
        title=news.xpath('.//h1/text()')
        content=news.xpath('.//div[@class="post_body"]/p/text()')
    save_to_file('news163_title.txt',title[0])
    for i in range(len(content)):
        save_to_file(title[0]+'.txt',content[i])
if __name__ == '__main__':
    news163(headers=headers) # 爬取网易新闻
    print(news163(headers=headers))
    news_163news(headers=headers) # 爬取网易新闻文章
    douban_top250() # 爬取豆瓣电影排行榜
