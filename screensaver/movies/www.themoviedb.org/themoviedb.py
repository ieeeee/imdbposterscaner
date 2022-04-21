import re
import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re, os
from urllib.request import urlretrieve
import time
'''
遇到不懂的问题？Python学习交流群：1136201545满足你的需求，资料都已经上传群文件，可以自行下载！
'''


def get_html(page):
    cookies = {
        'tmdb.prefs':
        '%7B%22adult%22%3Afalse%2C%22i18n_fallback_language%22%3A%22en-US%22%2C%22locale%22%3A%22zh-CN%22%2C%22country_code%22%3A%22US%22%2C%22timezone%22%3A%22America%2FChicago%22%7D',
        '_ga': 'GA1.2.927731318.1650546440',
        '_gid': 'GA1.2.1479632103.1650546440',
        '_dc_gtm_UA-2087971-10': '1',
        'tmdb.session':
        'AUGwOncpFIOe2FBOqnUzCxKdEVHCyYjd_n7cGVq4BzWrme92eX8OfOmuiEWp5D4ObXXdEmz_sj9DiIdCbVUMfk7eTwLijP94xYoe93mcgPpfPDZ3sIfbxhrmii_rLnqpe_x9OS_HP3W92V_44_pL90_Xc--MBLXedkerzYYuMWw8Ox7DAU9QxM-78fvVn8Dwyj5O7-AzCMRJC4k3E9BxU871xTJQTUOBnfN3LH6VTKFx',
        '_gali': 'pagination_page_1',
    }
    headers = {
        'authority': 'www.themoviedb.org',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'tmdb.prefs=%7B%22adult%22%3Afalse%2C%22i18n_fallback_language%22%3A%22en-US%22%2C%22locale%22%3A%22zh-CN%22%2C%22country_code%22%3A%22US%22%2C%22timezone%22%3A%22America%2FChicago%22%7D; _ga=GA1.2.927731318.1650546440; _gid=GA1.2.1479632103.1650546440; _dc_gtm_UA-2087971-10=1; tmdb.session=AUGwOncpFIOe2FBOqnUzCxKdEVHCyYjd_n7cGVq4BzWrme92eX8OfOmuiEWp5D4ObXXdEmz_sj9DiIdCbVUMfk7eTwLijP94xYoe93mcgPpfPDZ3sIfbxhrmii_rLnqpe_x9OS_HP3W92V_44_pL90_Xc--MBLXedkerzYYuMWw8Ox7DAU9QxM-78fvVn8Dwyj5O7-AzCMRJC4k3E9BxU871xTJQTUOBnfN3LH6VTKFx; _gali=pagination_page_1',
        'origin': 'https://www.themoviedb.org',
        'referer': 'https://www.themoviedb.org/movie',
        'sec-ch-ua':
        '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'air_date.gte': '',
        'air_date.lte': '2022-10-21',
        'certification': '',
        'certification_country': 'US',
        'debug': '',
        'first_air_date.gte': '',
        'first_air_date.lte': '',
        'ott_region': 'HK',
        'page': '' + str(page) + '',
        'primary_release_date.gte': '',
        'primary_release_date.lte': '',
        'region': '',
        'release_date.gte': '',
        'release_date.lte': '2022-10-21',
        'show_me': '0',
        'sort_by': 'popularity.desc',
        'vote_average.gte': '0',
        'vote_average.lte': '10',
        'vote_count.gte': '0',
        'with_genres': '',
        'with_keywords': '',
        'with_networks': '',
        'with_origin_country': '',
        'with_original_language': 'zh',
        'with_ott_monetization_types': '',
        'with_ott_providers': '',
        'with_release_type': '',
        'with_runtime.gte': '0',
        'with_runtime.lte': '400',
    }

    response = requests.post('https://www.themoviedb.org/discover/movie/items',
                             headers=headers,
                             cookies=cookies,
                             data=data)

    if response.status_code == 200:
        #判断请求是否成功
        return response.text
    else:
        return None


def parse_html(html):
    #进行页面数据提取
    soup = BeautifulSoup(html, 'html.parser')
    movies = soup.select('.wrapper')
    for movie in movies:
        movie_name = movie.select_one('a')['title']
        poster_image = movie.select_one('a').select_one('img')['src']

        movie_link = movie.select_one('a')['href']
        id_pattern = re.compile(r'\d+(?=/?)')
        movie_id = int(id_pattern.search(movie_link).group())

        #使用yield生成器，生成每一条电影信息
        yield {
            'movie_id': movie_id,
            'movie_name': movie_name,
            'movie_link': movie_link,
            'poster_image': 'https://www.themoviedb.org' + poster_image
        }


def write_file(content):
    with open('movie2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    dir = os.path.abspath('.')

    count = 2
    while (count <= 10):
        html = get_html(count)
        print(html)
        #https://www.themoviedb.org/t/p/w220_and_h330_face/3sSxRcX3DQvP4p5bAUcLVY5Mhv0.jpg
        #w220_and_h330_face
        #w440_and_h660_face
        #w600_and_h900_bestv2

        for item in parse_html(html):
            write_file(item)
            work_path = os.path.join(dir, 'images',
                                     str(item['movie_id']) + '.jpg')

            urlretrieve(
                re.sub('w\d{3}_and_h\d{3}_face', 'w600_and_h900_bestv2',
                       item['poster_image']), work_path)
        
        count = count + 1
        time.sleep(2)


if __name__ == '__main__':
    main()
