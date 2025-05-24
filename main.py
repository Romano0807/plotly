import streamlit as st
import pandas as pd
import plotly.express as px

st.title("2024년 4월 연령별 인구 현황 시각화")
st.write("※ 데이터: 남녀구분, 합계 파일 활용")

uploaded_mf = st.file_uploader("남녀구분 인구 파일 업로드", type="csv", key="mf", help="202504_202504_연령별인구현황_월간_남녀구분.csv")
uploaded_sum = st.file_uploader("합계 인구 파일 업로드", type="csv", key="sum", help="202504_202504_연령별인구현황_월간_합계.csv")

if uploaded_mf is not None and uploaded_sum is not None:
    # 데이터 불러오기
    try:
        df_mf = pd.read_csv(uploaded_mf, encoding='cp949')
        df_sum = pd.read_csv(uploaded_sum, encoding='cp949')
    except Exception as e:
        st.error(f"파일을 불러오는 중 에러가 발생했습니다: {e}")
        st.stop()
    
    st.subheader("남녀구분 인구 데이터 예시 (상위 5개)")
    st.dataframe(df_mf.head())
    st.write("남녀구분 데이터 컬럼명:", df_mf.columns.tolist())
    
    st.subheader("합계 인구 데이터 예시 (상위 5개)")
    st.dataframe(df_sum.head())
    st.write("합계 인구 데이터 컬럼명:", df_sum.columns.tolist())

    # 컬럼명 자동 선택
    with st.expander("① 남녀구분 인구 데이터에서 그래프용 컬럼 선택"):
        col_region_mf = st.selectbox("지역(행정구역) 컬럼", df_mf.columns, key="region_mf")
        col_age_mf = st.selectbox("연령구간 컬럼", df_mf.columns, key="age_mf")
        col_sex_mf = st.selectbox("성별 컬럼", df_mf.columns, key="sex_mf")
        col_value_mf = st.selectbox("인구수(값) 컬럼", df_mf.columns, key="value_mf")

    region_list = df_mf[col_region_mf].unique()
    region_col = st.selectbox("시각화할 지역(행정구역) 선택", region_list)
    filtered_df = df_mf[df_mf[col_region_mf] == region_col]

    # Bar Chart (남녀별 연령구간 인구)
    fig1 = px.bar(filtered_df, x=col_age_mf, y=col_value_mf, color=col_sex_mf,
                  barmode='group', title=f"{region_col} 연령별 남녀 인구분포")
    st.plotly_chart(fig1, use_container_width=True)

    # Pie Chart (전체 남녀 비율)
    total_by_gender = filtered_df.groupby(col_sex_mf)[col_value_mf].sum().reset_index()
    fig2 = px.pie(total_by_gender, names=col_sex_mf, values=col_value_mf,
                  title=f"{region_col} 전체 남녀 비율")
    st.plotly_chart(fig2, use_container_width=True)

    # 합계 데이터용 컬럼 선택
    with st.expander("② 합계 인구 데이터에서 그래프용 컬럼 선택"):
        col_region_sum = st.selectbox("지역(행정구역) 컬럼(합계)", df_sum.columns, key="region_sum")
        col_age_sum = st.selectbox("연령구간 컬럼(합계)", df_sum.columns, key="age_sum")
        col_value_sum = st.selectbox("인구수(값) 컬럼(합계)", df_sum.columns, key="value_sum")

    region_list2 = df_sum[col_region_sum].unique()
    region_col2 = st.selectbox("시각화할 지역(행정구역) 선택(합계)", region_list2)
    filtered_sum = df_sum[df_sum[col_region_sum] == region_col2]

    # Line Chart (전체 인구 연령구간)
    fig3 = px.line(filtered_sum, x=col_age_sum, y=col_value_sum,
                   title=f"{region_col2} 연령별 전체 인구 변화")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("좌측에 두 파일 모두 업로드해주세요.")

