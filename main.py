import streamlit as st
import pandas as pd
import plotly.express as px

st.title("연령별 인구 현황 시각화")

# 탭 구성
tab1, tab2 = st.tabs(["남녀구분", "합계"])

with tab1:
    st.header("남녀 구분 연령별 인구")
    uploaded_file_mf = st.file_uploader("남녀구분 CSV 업로드", type="csv", key="mf")
    if uploaded_file_mf is not None:
        try:
            df_mf = pd.read_csv(uploaded_file_mf, encoding='cp949')
        except UnicodeDecodeError:
            st.error("인코딩 오류: 파일이 cp949 형식이 아닙니다. 파일을 확인해 주세요.")
        else:
            st.dataframe(df_mf.head())

            # 연령대별 남녀 인구수 막대그래프
            # 남자 또는 여자라는 단어가 포함된 컬럼 자동 추출
            col_age = df_mf.columns[0]
            col_male = [col for col in df_mf.columns if "남자" in col]
            col_female = [col for col in df_mf.columns if "여자" in col]
            y_cols = col_male + col_female

            if y_cols:
                fig = px.bar(
                    df_mf,
                    x=col_age,
                    y=y_cols,
                    barmode='group',
                    labels={col_age: "연령", "value": "인구수"},
                    title="연령별 남녀 인구수"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("남자 또는 여자 컬럼이 없습니다. 파일 구조를 확인하세요.")

with tab2:
    st.header("합계 연령별 인구")
    uploaded_file_total = st.file_uploader("합계 CSV 업로드", type="csv", key="total")
    if uploaded_file_total is not None:
        try:
            df_total = pd.read_csv(uploaded_file_total, encoding='cp949')
        except UnicodeDecodeError:
            st.error("인코딩 오류: 파일이 cp949 형식이 아닙니다. 파일을 확인해 주세요.")
        else:
            st.dataframe(df_total.head())

            # 첫 번째와 두 번째 컬럼을 자동 선택
            if len(df_total.columns) >= 2:
                col_age = df_total.columns[0]
                col_total = df_total.columns[1]

                fig2 = px.line(
                    df_total,
                    x=col_age,
                    y=col_total,
                    markers=True,
                    labels={col_age: "연령", col_total: "인구수"},
                    title="연령별 전체 인구 변화"
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("파일에 최소 두 개의 컬럼이 필요합니다.")

