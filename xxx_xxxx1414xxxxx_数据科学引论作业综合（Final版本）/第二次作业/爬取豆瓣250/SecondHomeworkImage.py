import os
from urllib.request import urlretrieve

import requests
from lxml import etree

url_list = []


def get_url():
    for i in range(0, 226, 25):
        url_root = "https://movie.douban.com/top250?start=%d&filter=" % i
        url_list.append(url_root)


title_list = []
image_url_list = []


def get_title(url, headers):
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    title = html.xpath("//img/@alt")
    for i in range(0, len(title) - 1):
        title_list.append(title[i])


def get_image_url(url, headers):
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    img_url = html.xpath("//img/@src")
    for i in range(0, len(img_url) - 1):
        image_url_list.append(img_url[i])


def main():
    headers = {
        "Host": "movie.douban.com",
        "Referer": "https://movie.douban.com/top250?start=225&filter=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    }
    get_url()

    for url in url_list:
        get_title(url, headers)
        get_image_url(url, headers)

    movie_path = "movie_img"
    if movie_path not in os.listdir():
        os.makedirs(movie_path)

    for i in range(0, len(title_list)):
        for j in range(0, len(image_url_list)):
            if i == j:
                movie_name = title_list[j] + ".jpg"
                filename = movie_path + "/" + movie_name
                urlretrieve(url=image_url_list[i], filename=filename)


main()
