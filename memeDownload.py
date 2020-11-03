import requests
import os
import time
import threading
from bs4 import BeautifulSoup


def download_page(url):
    '''
    download page we want
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8' 
    return r.text


def get_pic_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_area = soup.find_all('div', class_='sensitive-content')
    for i in pic_area:
        pic_link = i.find('a').find('img')
        text = i.find_parents('div').find_parents('div').find('b').get_text()
        get_pic(pic_link, text)
        time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封

def get_pic(pic_link, text):
    '''
    获取当前页面的图片,并保存
    '''
    print('TEST')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    create_dir('pic')
    pic_link = i.get('src')  # 拿到图片的具体 url
    r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
    with open('pic/{}'.format(text), 'wb') as f:
        f.write(r.content)


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html)


def main():
    create_dir('pic')
    queue = [i for i in range(1, 5)]   # 构造 url 链接 页码。
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and len(queue) > 0:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            url = 'https://memes.tw/wtf?contest=53&page={}'.format(cur_page)
            thread = threading.Thread(target=execute, args=(url,))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下載{}頁'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()
