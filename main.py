import streamlit as st
import pandas as pd
import plotly.express as px

st.title("연령별 인구 현황 시각화 (지역별 선택 가능)")

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

            # '지역' 또는 유사 컬럼명 자동 탐색
            region_col_candidates = [col for col in df_mf.columns if "지역" in col or "시도" in col or "시군구" in col]
            if region_col_candidates:
                region_col = region_col_candidates[0]
                regions = df_mf[region_col].unique().tolist()
                selected_region = st.selectbox("지역을 선택하세요", regions)
                filtered_df = df_mf[df_mf[region_col] == selected_region]
            else:
                st.warning("데이터에 '지역', '시도', '시군구' 컬럼이 없습니다. 전체 데이터를 사용합니다.")
                filtered_df = df_mf

            # 컬럼 자동 탐색
            col_age = [col for col in filtered_df.columns if "연령" in col or "나이" in col][0]
            col_male = [col for col in filtered_df.columns if "남자" in col]
            col_female = [col for col in filtered_df.columns if "여자" in col]
            y_cols = col_male + col_female

            if y_cols:
                fig = px.bar(
                    filtered_df,
                    x=col_age,
                    y=y_cols,
                    barmode='group',
                    labels={col_age: "연령", "value": "인구수"},
                    title=f"{selected_region if region_col_candidates else '전체'} 연령별 남녀 인구수"
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

            # '지역' 또는 유사 컬럼명 자동 탐색
            region_col_candidates = [col for col in df_total.columns if "지역" in col or "시도" in col or "시군구" in col]
            if region_col_candidates:
                region_col = region_col_candidates[0]
                regions = df_total[region_col].unique().tolist()
                selected_region = st.selectbox("지역을 선택하세요", regions, key="total_region")
                filtered_df = df_total[df_total[region_col] == selected_region]
            else:
                st.warning("데이터에 '지역', '시도', '시군구' 컬럼이 없습니다. 전체 데이터를 사용합니다.")
                filtered_df = df_total

            # 첫 번째와 두 번째 컬럼 자동 선택 (단, 지역 컬럼이 있을 땐 제외)
            filtered_columns = [col for col in filtered_df.columns if col not in region_col_candidates]
            if len(filtered_columns) >= 2:
                col_age = filtered_columns[0]
                col_total = filtered_columns[1]

                fig2 = px.line(
                    filtered_df,
                    x=col_age,
                    y=col_total,
                    markers=True,
                    labels={col_age: "연령", col_total: "인구수"},
                    title=f"{selected_region if region_col_candidates else '전체'} 연령별 전체 인구 변화"
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("파일에 최소 두 개의 컬럼이 필요합니다.")
