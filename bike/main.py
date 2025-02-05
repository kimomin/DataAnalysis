import streamlit as st
import bike
import navernews

# 사이드바 화면
st.sidebar.title('사이드바')
user_id = st.sidebar.text_input('아이디 입력', value='python', max_chars=10)
user_pw = st.sidebar.text_input('패스워드 입력', value='', type='password')

if user_pw =='1234':
    st.sidebar.header('===김성민의 포트폴리오===')
    select_data = ['메뉴 선택','따릉이 분석','뉴스 분석']
    menu = st.sidebar.selectbox('',select_data,index=0)

    if menu == '따릉이 분석':
        st.write('따릉이 분석')
        bike.bike_main()
    elif menu == '따릉이 분석':
        st.write('따릉이 분석')
        bike.bike_main()
    elif menu == '뉴스 분석':
        st.write('뉴스 분석')
        df = navernews.data_create()
        st.dataframe(df)
        navernews.text_visualization(df)
    else:
        st.title('환영합니다')