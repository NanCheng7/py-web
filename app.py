import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import re
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Line  
from pyecharts import options as opts 
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Funnel
import streamlit.components.v1 as comps
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud

# 数据限制
def limitNum(count):
    if len(count) > 20:
        return dict(sorted(count.items(), key=lambda item: item[1], reverse=True)[:20]) 
    else :
        return count
# 获取页面信息
def requestPage(url) :
    page = requests.get(url)
    page.raise_for_status()
    page.encoding = page.apparent_encoding
    soup = BeautifulSoup(page.text,'html.parser')
    body_contain = soup.find("body")

    content = f'{body_contain}'
    return content
# 数据分析
def dataAnalysis(page):
    # 去除标签
    page = re.sub('<[^<]+?>','',page)    
    # 去除中文符号
    page = re.sub('[^a-zA-Z0-9\u4e00-\u9fa5]','',page)
    # 对文本分词
    words = jieba.lcut(page)
    words_count = Counter(words)

    data  = dict(words_count)
    data = {key: value for key, value in data.items() if len(key) > 1}  
    data = dict(sorted(data.items(),key=lambda item: item[1],reverse=True))
    return limitNum(data)

#绘图
def painting(bar):
    html_page = bar.render_embed()
    comps.html(html_page,height=600,width=900)
    


# 柱状图
def zhu_map(data):
    bar = (
        Bar()
        .add_xaxis(list(data.keys()))
        .add_yaxis("词频",list(data.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频统计"),
            xaxis_opts=opts.AxisOpts(name_textstyle_opts=opts.TextStyleOpts(font_size=1))
        )
    )
    painting(bar)

# 阶梯图
def jieti_map(data):
    jieti = (
        Line()
        .add_xaxis(list(data.keys()))
        .add_yaxis("词频", data.values(), is_step=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="词频-阶梯图"))
    )
    painting(jieti)

#虚折线图
def xvzhexian_map(data):
    xvzhexian =(
        Line()
        .add_xaxis(list(data.keys()))
        .add_yaxis(
            series_name='词频-曲线',
            y_axis=list(data.values()),
            symbol="triangle",
            symbol_size=20,
            linestyle_opts=opts.LineStyleOpts(color="green", width=4, type_="dashed"),
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=3, border_color="yellow", color="blue"
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
    )
    painting(xvzhexian)

# 面积图
def mianji_map(data):
    mianji = (
         Funnel()
        .add(
            "词频-漏斗图",
            [list(z) for z in zip(list(data.keys()), list(data.values()))],
            label_opts=opts.LabelOpts(position="inside"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Funnel-Label（inside)"))
    )
    painting(mianji)

# 象形柱图
def xiangxing_map(data):
    xiangxing = (
        PictorialBar()
        .add_xaxis(list(data.keys()))
        .add_yaxis(
            "",
            list(data.values()),
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT,
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频-象形柱图"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=9)
                )
            )
        )
    )
    painting(xiangxing)

# 数据集
def bin_map(data):
    bin = (
         Funnel()
        .add(
        "词频-数据集",
        [list(z) for z in zip(list(data.keys()), list(data.values()))],
        label_opts=opts.LabelOpts(position="inside"),
         )
    )
    painting(bin)

#   词云图
def ciyun_map(data):
    ciyun = (
        WordCloud()
        .add(series_name='词频-云图',data_pair=list(data.items()),word_size_range=[50,300])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="词频-云图", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    painting(ciyun)

#  网站骨架
st.title('这是一个爬取网站:blue[源码页面] ')
st.subheader('并且进行:blue[词频分析]的小破站:sunglasses:',divider='rainbow')
st.markdown(':cherry_blossom:  Writen by :rainbow[_NanCheng_] ')
st.markdown(':rose: if you have any issue please email :blue[_nanchengqj@gmail.com_]')
st.markdown('\n')
st.markdown('\n')
st.markdown('\n')
st.markdown('\n')

# 变量
urlIsEmpty = True
data = {}
buttonPress = False
with st.sidebar:
    goal_website = st.text_input('请在此输入目标网站的网址：')
    option = st.selectbox(
        '请选择图型筛选',
        ('柱状图','阶梯图','虚折线图','面积图','象形柱图','数据集','词云图')
    )
    st.write('您选择的图型是:',option)
    if st.button('开始分析') :
        buttonPress = True
        if goal_website != '' :
            urlIsEmpty = False
            data = dataAnalysis(requestPage(goal_website))
if buttonPress:
    if urlIsEmpty :
        st.markdown("!!!:red[请您输入待分析网站的网址后再点击]:blue[开始分析]")
    else :
        if option == '柱状图' :
            zhu_map(data)
        elif option == '阶梯图':
            jieti_map(data)
        elif option == '虚折线图':
            xvzhexian_map(data)
        elif option == '面积图':
            mianji_map(data)
        elif option == '象形柱图':
            xiangxing_map(data)
        elif option == '数据集':
            bin_map(data)
        elif option == '词云图':
            ciyun_map(data)

