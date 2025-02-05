import pandas as pd
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
import streamlit as st

def req_url(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res) # 파싱

    return(soup)

def data_create():
    url = 'https://news.naver.com/breakingnews/section/101/259'
    soup = req_url(url)
    temp = soup.select_one('ul.sa_list').select('li',limit=5)

    news_list=[]
    for li in temp:
        new_info = {'title':li.select_one('strong.sa_text_strong').text,
                    'date':li.select_one('div.sa_text_datetime.is_recent').text,
                    'news_url':li.select_one('a')['href']}
        # print(new_info)
        news_list.append(new_info)

    # 뉴스 본문 가져오기
    for news in news_list:
        news_url = news['news_url']
        # res = requests.get(news_url).text
        # soup = BeautifulSoup(res)
        soup = req_url(news_url)
        # print(soup)

        body = soup.select_one('article.go_trans._article_content')
        news_content = body.text.replace('\n','').strip()
        # print(news_content)
        news['news_content'] = news_content

    df = pd.DataFrame(news_list)

    return df

def text_visualization(df):
    # 워드 클라우드 시각화
    okt = Okt()
    clist = []
    for word in df['news_content']:
        token = okt.pos(word)
        for word,tag in token:
            if tag in ['Noun','Adjective']:
                clist.append(word)
    counts = collections.Counter(clist)
    tag = counts.most_common(50)

    s_words=STOPWORDS.union({'있다','이','것'})

    fpath = 'C:\Windows\Fonts\malgunbd.ttf'
    wc = WordCloud(font_path=fpath, background_color='white',stopwords=s_words)
    cloud = wc.generate_from_frequencies(dict(tag))

    fig = plt.figure(figsize=(10,8))
    plt.axis('off') # 축 안 보이게 함
    plt.imshow(cloud)
    plt.show()

    st.pyplot(fig)

if __name__ == '__main__':
    df = data_create()
    st.dataframe(df)
    text_visualization(df)