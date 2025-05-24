import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 업로드(웹앱에서)
st.title("2024년 4월 연령별 인구 현황 시각화")
st.write("※ 데이터: 남녀구분, 합계 파일 활용")

uploaded_mf = st.file_uploader("남녀구분 인구 파일 업로드", type="csv", key="mf", help="202504_202504_연령별인구현황_월간_남녀구분.csv")
uploaded_sum = st.file_uploader("합계 인구 파일 업로드", type="csv", key="sum", help="202504_202504_연령별인구현황_월간_합계.csv")

if uploaded_mf is not None and uploaded_sum is not None:
    df_mf = pd.read_csv(uploaded_mf, encoding='cp949')
    df_sum = pd.read_csv(uploaded_sum, encoding='cp949')
    
    st.subheader("남녀구분 인구 데이터 예시")
    st.dataframe(df_mf.head())
    st.subheader("합계 인구 데이터 예시")
    st.dataframe(df_sum.head())

    # 예시1: 지역별, 연령별, 성별 인구 시각화 (bar chart)
    region_col = st.selectbox("지역(행정구역) 선택", df_mf['행정구역'].unique())
    filtered_df = df_mf[df_mf['행정구역'] == region_col]

    fig1 = px.bar(filtered_df, x='연령구간', y='값', color='성별',
                  barmode='group', title=f"{region_col} 연령별 남녀 인구분포")
    st.plotly_chart(fig1, use_container_width=True)

    # 예시2: 전체 연령대/성별 비중 파이차트
    total_by_gender = filtered_df.groupby('성별')['값'].sum().reset_index()
    fig2 = px.pie(total_by_gender, names='성별', values='값',
                  title=f"{region_col} 전체 남녀 비율")
    st.plotly_chart(fig2, use_container_width=True)

    # 예시3: 합계 데이터 활용 전체 인구 연령구간 라인차트
    region_col2 = st.selectbox("합계 데이터의 지역(행정구역) 선택", df_sum['행정구역'].unique())
    filtered_sum = df_sum[df_sum['행정구역'] == region_col2]
    fig3 = px.line(filtered_sum, x='연령구간', y='값',
                   title=f"{region_col2} 연령별 전체 인구 변화")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("좌측에 두 파일 모두 업로드해주세요.")

