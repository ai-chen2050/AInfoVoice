import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver 

def sina():
    task_q = [] # 本地存储新闻
    task_time = []
    
    data_list = getNews()

    task_q = data_list
    for data in data_list:
        print(data['n_time'],data['n_info'],'\n')
        # time.sleep(0.5)
        task_time.append(data['n_time'])
        

def getNews(): # 获取新闻函数
    news_list =[]
    base_url = 'http://live.sina.com.cn/zt/f/v/finance/globalnews1'
    browser = webdriver.PhantomJS()
    browser.get(base_url) 
    html = browser.page_source
    # browser.encoding = browser.apparent_encoding

    # f1 = open("cache.html",'a',encoding='utf8')
    # f1.write(html)
    # f1.close()

    # f1 = open("cache.html",'r+',encoding='utf8')
    # html = f1.read()
    # f1.close()

    html_bs4 = BeautifulSoup(html,'lxml') 
    info_list = html_bs4.find_all('div',class_='bd_i bd_i_og bd_i_focus clearfix')

    for info in info_list:  # 获取页面中自动刷新的新闻
        n_time = info.select('p[class="bd_i_time_c"]')[0].get_text()  # 新闻时间及内容
        n_info = info.select('p[class="bd_i_txt_c"]')[0].get_text()
        data = {
            'n_time': n_time,
            'n_info': n_info
        }
        news_list.append(data)
    return news_list[::-1] # 这里倒序，这样打印时才会先打印旧新闻，后打印新新闻



if __name__ == '__main__':
    sina()


'''
先得到页面的15条新闻
15条新闻放到列表并传递
每隔30秒请求一次页面，界面中时间与列表中的时间对照，不相同则读取
'''