import os
import re
import time
from multiprocessing import Process
from multiprocessing import Queue
from time import sleep

import requests
from bs4 import BeautifulSoup


def task_delegator(taskQueue: Queue, urlsQueue: Queue):
    # 为每个进程初始化一个任务
    #关键是委派者利用Queue对象来为各个进程分工
    visited = ['/wiki.Kevin_Bacon', 'Wiki/Month_Python']
    taskQueue.put('/wiki/Kevin_Bacon')
    taskQueue.put('/wiki/Month_Python')
    while 1:
        # 检查urlsQueue中是否存在新链接需要处理
        if not urlsQueue.empty():
            links = [link for link in urlsQueue.get() if link not in visited]
            for link in links:
                # 向taskQueue中添加新链接
                taskQueue.put(link)


def get_Links(bs: BeautifulSoup):
    links = bs.find('div', attrs={'id': 'bodyContent'}).find_all \
        ('a', attrs={'href': re.compile('^(/wiki/)((?!:).)*$')})
    return [link.attrs['href'] for link in links]


def scrape_article(taskQueue: Queue, urlsQueue: Queue):
    while 1:
        while taskQueue.empty():
            # 如果任务队列为空,休息100毫秒
            # 这种情况应该极少发生
            sleep(.1)
        path = taskQueue.get()
        html = requests.get("http://en.wikipedia.org{}".format(path))
        time.sleep(5)
        bs = BeautifulSoup(html, 'html.parser')
        title = bs.find('h1').get_text()
        print('Scraping{} in process {}'.format(title, os.getpid()))
        links = get_Links(bs)
        urlsQueue.put(links)


if __name__ == '__main__':
    process = []
    taskQueue = Queue()
    urlsQueue = Queue()
    process.append(Process(target=task_delegator, args=(taskQueue, urlsQueue)))
    process.append(Process(target=scrape_article, args=(taskQueue, urlsQueue)))
    process.append(Process(target=scrape_article, args=(taskQueue, urlsQueue)))
    # 开启进程
    for p in process:
        p.start()
