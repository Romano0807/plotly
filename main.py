import streamlit as st
import pandas as pd
import plotly.express as px

st.title("연령별 인구 현황 시각화")

# 파일 업로드
tab1, tab2 = st.tabs(["남녀구분", "합계"])

with tab1:
    st.header("남녀 구분 연령별 인구")
    uploaded_file_mf = st.file_uploader("남녀구분 CSV 업로드", type="csv", key="mf")
    if uploaded_file_mf is not None:
        df_mf = pd.read_csv(uploaded_file_mf)
        st.dataframe(df_mf.head())

        # 연령대별 남녀 인구수 막대그래프
        fig = px.bar(
            df_mf, 
            x=df_mf.columns[0],  # 연령
            y=[col for col in df_mf.columns if "남자" in col or "여자" in col],
            barmode='group',
            labels={df_mf.columns[0]: "연령", "value": "인구수"},
            title="연령별 남녀 인구수"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("합계 연령별 인구")
    uploaded_file_total = st.file_uploader("합계 CSV 업로드", type="csv", key="total")
    if uploaded_file_total is not None:
        df_total = pd.read_csv(uploaded_file_total)
        st.dataframe(df_total.head())

        # 연령별 전체 인구 꺾은선 그래프
        fig2 = px.line(
            df_total, 
            x=df_total.columns[0], 
            y=df_total.columns[1],
            markers=True,
            labels={df_total.columns[0]: "연령", df_total.columns[1]: "인구수"},
            title="연령별 전체 인구 변화"
        )
        st.plotly_chart(fig2, use_container_width=True)
