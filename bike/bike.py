import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def data_preprocessing():
    bikes_temp={}
    # 데이터 불러오기
    for i in range(1,4): # i = 1,2,3
        bikes_temp[i] = pd.read_csv(f'files\서울특별시 공공자전거 대여이력 정보_240{i}.csv', encoding='cp949')

    bikes = pd.concat(bikes_temp, ignore_index=True)

    # 데이터 전처리
    # 월, 일자, 시간대 컬럼 추가
    bikes['대여일'] = pd.to_datetime(bikes['대여일시'])
    bikes['월'] = bikes['대여일'].dt.month
    bikes['일자'] = bikes['대여일'].dt.day
    bikes['시간대'] = bikes['대여일'].dt.hour
    # bikes['요일_n'] = bikes['대여일'].dt.weekday
    # 요일 컬럼 생성
    weekdays = {0:'월',1:'화',2:'수',3:'목',4:'금',5:'토',6:'일'}
    # bikes['요일'] = bikes['요일_n'].map(weekdays)
    bikes['요일'] = bikes['대여일'].dt.weekday.map(weekdays)
    # 주말 구분 열 생성
    # weekend = {'월':'평일','화':'평일','수':'평일','목':'평일','금':'평일','토':'주말','일':'주말'}
    # bikes['주말 구분'] = bikes['요일'].map(weekend)
    bikes['주말 구분'] = bikes['대여일'].dt.weekday.map(lambda x : '평일' if x <5 else '주말' )

    return bikes

def top50(bikes):
    bikes_weekend = bikes.groupby(['대여 대여소번호', '대여 대여소명', '주말 구분'])['자전거번호'].count().unstack()
    weekend50 = bikes_weekend.sort_values('주말',ascending=False).head(50).reset_index()
    bike_shop = pd.read_csv('files\공공자전거 대여소 정보.csv', encoding='cp949')
    bike_shop = bike_shop.rename(columns={'대여소\n번호':'대여소번호'})
    weekend50_total = pd.merge(weekend50,bike_shop,left_on='대여 대여소번호',right_on='대여소번호')

    map = folium.Map(location=[weekend50_total['위도'].mean(),weekend50_total['경도'].mean()],
            zoom_start=12, width=1000, height=700)

    marker_c = MarkerCluster().add_to(map)

    # folium marker 표시
    for i in weekend50_total.index:
        sub_lat = weekend50_total.loc[i,'위도']
        sub_lon = weekend50_total.loc[i,'경도']
        shop = [sub_lat,sub_lon]
        sub_name = weekend50_total.loc[i,'대여 대여소명']

        folium.Marker(location=shop, popup=sub_name, icon=folium.Icon(color='red',icon='star')).add_to(marker_c)
    
    components.html(map._repr_html_(),height=500)

def time_analyis(bikes):
    # 대여시간대별 따릉이 이용건수
    hourly_ride = bikes.groupby('시간대',as_index=False)[['자전거번호']].count()
    # 요일별 따릉이 인원수
    weekly_ride = bikes.groupby('요일',as_index=False)[['자전거번호']].count()
    
    fig, axes = plt.subplots(2,1,figsize=(5,9))

    sns.barplot(data=hourly_ride, x='시간대', y='자전거번호', ax=axes[0])
    sns.barplot(data=weekly_ride, x='요일', y='자전거번호', ax=axes[1])

    plt.tight_layout()
    st.pyplot(fig) # fig 있으면 plt.show()가 아니라 이거로 씀

def bike_main():
    tab1, tab2, tab3 = st.tabs(["데이터 보기","인기대여소50","시간대별 분석"])

    with tab1:
        data = data_preprocessing()
        st.dataframe(data.head(20))
    with tab2:
        top50(data)
    with tab3:
        time_analyis(data)

if __name__=='__main__':
    bike_main()