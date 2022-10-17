import pandas as pd

csv = pd.read_csv('DoubanMovieTop250.csv', encoding='utf-8')
csv.to_excel('DoubanMovieTop250.xlsx', sheet_name='data')