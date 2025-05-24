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

            # 행정구역 또는 유사 컬럼 찾기
            region_col_candidates = [col for col in df_mf.columns if "행정구역" in col or "지역" in col or "시도" in col or "시군구" in col]
            if region_col_candidates:
                region_col = region_col_candidates[0]
                regions = df_mf[region_col].unique().tolist()
                selected_region = st.selectbox("지역을 선택하세요", regions)
                filtered_df = df_mf[df_mf[region_col] == selected_region]
            else:
                st.warning("데이터에 '행정구역', '지역', '시도', '시군구' 컬럼이 없습니다. 전체 데이터를 사용합니다.")
                filtered_df = df_mf

            # '남' 또는 '여' 포함된 컬럼 자동 추출
            col_male = [col for col in filtered_df.columns if "남" in col]
            col_female = [col for col in filtered_df.columns if "여" in col]
            y_cols = col_male + col_female

            # 연령 컬럼 추출: '연령', '나이', '연령구간' 등 자동 탐색
            age_col_candidates = [col for col in filtered_df.columns if "연령" in col or "나이" in col]
            if age_col_candidates:
                col_age = age_col_candidates[0]
            else:
                # 없으면 두 번째 컬럼을 연령으로 가정 (실제 파일 구조에 맞게 조정)
                col_age = filtered_df.columns[1]

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
                st.info("남 또는 여 컬럼이 없습니다. 파일 구조를 확인하세요.")

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

            region_col_candidates = [col for col in df_total.columns if "행정구역" in col or "지역" in col or "시도" in col or "시군구" in col]
            if region_col_candidates:
                region_col = region_col_candidates[0]
                regions = df_total[region_col].unique().tolist()
                selected_region = st.selectbox("지역을 선택하세요", regions, key="total_region")
                filtered_df = df_total[df_total[region_col] == selected_region]
            else:
                st.warning("데이터에 '행정구역', '지역', '시도', '시군구' 컬럼이 없습니다. 전체 데이터를 사용합니다.")
                filtered_df = df_total

            # 연령 컬럼 찾기
            age_col_candidates = [col for col in filtered_df.columns if "연령" in col or "나이" in col]
            if age_col_candidates:
                col_age = age_col_candidates[0]
            else:
                col_age = filtered_df.columns[1]
            # 인구수 컬럼 (합계 등) 자동 선택
            value_col_candidates = [col for col in filtered_df.columns if "총인구수" in col or "합계" in col or "인구수" in col]
            if value_col_candidates:
                col_total = value_col_candidates[0]
            else:
                # 두 번째 또는 세 번째 컬럼을 기본값으로
                col_total = filtered_df.columns[2]

            fig2 = px.line(
                filtered_df,
                x=col_age,
                y=col_total,
                markers=True,
                labels={col_age: "연령", col_total: "인구수"},
                title=f"{selected_region if region_col_candidates else '전체'} 연령별 전체 인구 변화"
            )
            st.plotly_chart(fig2, use_container_width=True)
