import concurrent.futures

import requests
from bs4 import BeautifulSoup


def crawl(url):
    resp = requests.get(url)
    return resp.text


def parse(html):
    bs = BeautifulSoup(html,'html.parser')
    links = bs.findAll('a', attrs={'class': 'post-item-title'})
    return [(link.attrs['href'], link.get_text()) for link in links]


if __name__ == '__main__':
    urls = [f"https://www.cnblogs.com/#p{page}" for page in range(1, 51)]
    with concurrent.futures.ThreadPoolExecutor() as pool:
        htmls = pool.map(crawl, urls)
        htmls = list(zip(urls, htmls))
        for url, html in htmls:
            print(url, len(html))
    print("crawl end")
    with concurrent.futures.ThreadPoolExecutor() as pool:
        futures = {}
        for url, html in htmls:
            future = pool.submit(parse, html)
            futures[url] = future
        for url, future in futures.items():
            print(url, future.result())
    print("end")
