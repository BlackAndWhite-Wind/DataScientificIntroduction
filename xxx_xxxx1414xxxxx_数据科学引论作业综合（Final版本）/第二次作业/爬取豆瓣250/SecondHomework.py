import bs4
import csv
import requests

csv_file = open('DoubanMovieTop250.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['电影排名', '国家', '电影名', '导演', '主演', '年份', '电影类型', '评分', '评语'])

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36'}

for x in range(10):
    url = 'https://movie.douban.com/top250?start=' + str(x * 25) + '&filter='
    res = requests.get(url, headers=headers)
    bs = bs4.BeautifulSoup(res.text, 'html.parser')
    bs = bs.find('ol', class_="grid_view")

    for elems in bs.find_all('li'):
        movie_number = elems.find('em', class_="").text
        movie_name = elems.find('span', class_="title").text
        movie_rating_number = elems.find('span', class_="rating_num").text
        otherThings = elems.find('div', class_='bd').find('p').text.strip('').split('\n')

        if '\xa0\xa0\xa0' in otherThings[1]:
            movie_directors = otherThings[1].strip('').split('\xa0\xa0\xa0')
            movie_director = movie_directors[0].strip(' ')
            movie_actors = movie_directors[1]
        else:
            movie_directors = otherThings[1].strip('').split('\xa0\xa0\xa0')
            movie_director = movie_directors[0].strip(' ')
            movie_actors = ''

        t = otherThings[2].strip('').split('\xa0/\xa0')
        movie_year = t[0].strip(' ')
        movie_country = t[1]
        movie_type = t[2]

        if elems.find('span', class_="inq") is not None:
            movie_recommendations = elems.find('span', class_="inq").text
            writer.writerow(
                [movie_number, movie_country, movie_name, movie_director, movie_actors, movie_year, movie_type,
                 movie_rating_number,
                 movie_recommendations])
        else:
            writer.writerow(
                [movie_number, movie_country, movie_name, movie_director, movie_actors, movie_year, movie_type,
                 movie_rating_number,
                 ''])

csv_file.close()
