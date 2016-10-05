#!/usr/bin/python
# coding: utf-8

# 豆瓣电影Top250收录了至今为止，大家最喜欢的250部电影。
# 该列表呈现了每部电影的评分，年份等基本信息。
# 这题的答案很简单，就是这个榜单的前166部电影的评分总和。
# 举例：
# 目前排第一的《肖申克的救赎》是9.6分，第二的《这个杀手不太冷》是9.4分，第三的《阿甘正传》是9.4分。
# 那么前3部电影的总分为9.6+9.4+9.4=28.4。

# 方法一: 将这几个合起来就是 ./23_7560...sh
# curl https://movie.douban.com/top250 | grep --col rating_num | awk -F '[<|>]' '{a+=$3}END{print a}'
# curl https://movie.douban.com/top250\?start\=25 | grep --col rating_num | awk -F '[<|>]' '{a+=$3}END{print a}'
# curl https://movie.douban.com/top250\?start\=50 | grep --col rating_num | awk -F '[<|>]' '{a+=$3}END{print a}'
# curl https://movie.douban.com/top250\?start\=75 | grep --col rating_num | awk -F '[<|>]' '{a+=$3}END{print a}'
# curl https://movie.douban.com/top250\?start\=100 | grep --col rating_num | awk -F '[<|>]' '{a+=$3}END{print a}'
# curl https://movie.douban.com/top250\?start\=125 | grep --col rating_num | awk -F '[<|>]' '{a+=$3}END{print a}'
# curl https://movie.douban.com/top250\?start\=150 | grep --col rating_num | head -16 | awk -F '[<|>]' '{a+=$3}END{print a}'

# 方法二: urlib.request, 好像不能用了, 豆瓣 403 了
import requests
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250?start={}"
counter = 0
film_counter = 0
my_headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip, deflate, sdch'}
# 很尴尬, 豆瓣的反扒机制号厉害啊

while film_counter < 166:
    r = requests.get(url.format(film_counter), headers = my_headers)
    print(r.content)
    soup = BeautifulSoup(r.content, "html.parser")
    for rate in soup.find_all(class_="rating_num"):
        counter += float(rate.string)
        film_counter += 1
        if film_counter>=166:
            break

print(counter)

# 方法三: python 自动化测试框架selenium+beautifulSoup搞定爬虫 简化规则
