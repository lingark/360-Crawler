import requests as rq 
from lxml import etree 
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
if __name__=='__main__':
    douban_top250() # 爬取豆瓣电影top250
