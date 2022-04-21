import re
import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re, os
from urllib.request import urlretrieve
'''
遇到不懂的问题？Python学习交流群：1136201545满足你的需求，资料都已经上传群文件，可以自行下载！
'''


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        #判断请求是否成功
        return response.text
    else:
        return None


def parse_html(html):
    #进行页面数据提取
    soup = BeautifulSoup(html, 'html.parser')
    movies = soup.select('tbody tr')
    for movie in movies:
        poster = movie.select_one('.posterColumn')
        score = poster.select_one('span[name="ir"]')['data-value']
        #U[X,Y]\d{2}_CR\d{1},0,45,67_AL_
        poster_image = poster.select_one('a').select_one('img')['src']
        movie_link = movie.select_one('.titleColumn').select_one('a')['href']
        #电影详情链接
        year_str = movie.select_one('.titleColumn').select_one(
            'span').get_text()
        year_pattern = re.compile('\d{4}')
        year = int(year_pattern.search(year_str).group())
        id_pattern = re.compile(r'(?<=tt)\d+(?=/?)')
        movie_id = int(id_pattern.search(movie_link).group())
        #movie_id不使用默认生成的，从数据提取唯一的ID
        movie_name = movie.select_one('.titleColumn').select_one('a').string
        #使用yield生成器，生成每一条电影信息
        yield {
            'movie_id': movie_id,
            'movie_name': movie_name,
            'year': year,
            'movie_link': movie_link,
            'movie_rate': float(score),
            'poster_image': poster_image
        }


def write_file(content):
    with open('movie2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    url = 'https://www.imdb.com/chart/top'
    html = get_html(url)
    #https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThlMGVjNzE1OGViXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_UY67_CR0,0,45,67_AL_.jpg
    #U[X,Y]\d{2}_CR\d{1},0,45,67_AL_
    #re.sub(pattern, repl, 'string', count=0, flags=0)
    #print(re.sub('U[X,Y]\d{2}_CR\d{1},0,45,67_AL_', '', 'https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThlMGVjNzE1OGViXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_UY67_CR0,0,45,67_AL_.jpg'))
    for item in parse_html(html):
        urlretrieve(
            re.sub('U[X,Y]\d{2}_CR\d{1},0,45,67_AL_', '',
                   item['poster_image']), str(item['movie_id']) + '.jpg')
        write_file(item)
        #print(item['poster_image'])


if __name__ == '__main__':
    main()
