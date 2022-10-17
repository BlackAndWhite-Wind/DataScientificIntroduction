import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

data = pd.read_excel('DoubanMovieTop250.xlsx')

year_counts = data['年份'].value_counts()
year_counts.columns = ['年份', '数量']
year_counts = year_counts.sort_index()
c = (
    Bar()
        .add_xaxis(list(year_counts.index))
        .add_yaxis('上映数量', year_counts.values.tolist())
        .set_global_opts(
        title_opts=opts.TitleOpts(title='各年份上映电影数量'),
        yaxis_opts=opts.AxisOpts(name='上映数量'),
        xaxis_opts=opts.AxisOpts(name='上映年份'),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')], )
        .render('各年份上映电影数量.html')
)

