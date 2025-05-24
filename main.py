import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("연령별 인구 피라미드 시각화 (지역별 선택 가능)")

uploaded_file = st.file_uploader("남녀구분 CSV 업로드", type="csv")
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        st.error("인코딩 오류: 파일이 cp949 형식이 아닙니다. 파일을 확인해 주세요.")
    else:
        st.dataframe(df.head())

        # 행정구역, 연령구간 컬럼 찾기
        region_col_candidates = [col for col in df.columns if "행정구역" in col or "지역" in col or "시도" in col or "시군구" in col]
        age_col_candidates = [col for col in df.columns if "연령" in col or "나이" in col or "연령구간" in col]

        if region_col_candidates and age_col_candidates:
            region_col = region_col_candidates[0]
            age_col = age_col_candidates[0]
            # 모든 행정구역 이름 추출(중복제거)
            regions = df[region_col].unique().tolist()
            selected_region = st.selectbox("지역을 선택하세요", regions)
            filtered_df = df[df[region_col] == selected_region]

            # 선택 지역의 연령 구간 종류 확인
            if filtered_df[age_col].nunique() < 2:
                st.warning(f"선택한 지역({selected_region})은 연령별 데이터가 1개(혹은 없음)입니다. 인구 피라미드를 그릴 수 없습니다.")
            else:
                # 남/여 인구 컬럼 찾기
                col_male_candidates = [col for col in filtered_df.columns if "남" in col and "인구" in col]
                col_female_candidates = [col for col in filtered_df.columns if "여" in col and "인구" in col]
                # 우선순위 추출 함수
                def get_priority(col_list):
                    for kw in ["연령구간인구수", "총인구수", "인구수"]:
                        filtered = [col for col in col_list if kw in col]
                        if filtered:
                            return filtered[0]
                    return col_list[0] if col_list else None
                col_male = get_priority(col_male_candidates)
                col_female = get_priority(col_female_candidates)

                if col_male and col_female:
                    # 수치형 변환 (콤마 제거)
                    filtered_df[col_male] = pd.to_numeric(filtered_df[col_male].astype(str).str.replace(",", ""), errors='coerce')
                    filtered_df[col_female] = pd.to_numeric(filtered_df[col_female].astype(str).str.replace(",", ""), errors='coerce')
                    # 연령 구간 정렬(필요시 정렬방식 맞춰보세요)
                    filtered_df = filtered_df.sort_values(by=age_col, ascending=False)

                    filtered_df["남성(음수)"] = -filtered_df[col_male]
                    filtered_df["여성(양수)"] = filtered_df[col_female]

                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        y=filtered_df[age_col].astype(str),
                        x=filtered_df["남성(음수)"],
                        name="남자",
                        orientation='h',
                        marker_color='lightblue'
                    ))
                    fig.add_trace(go.Bar(
                        y=filtered_df[age_col].astype(str),
                        x=filtered_df["여성(양수)"],
                        name="여자",
                        orientation='h',
                        marker_color='lightpink'
                    ))

                    fig.update_layout(
                        title=f"{selected_region} 연령별 인구 피라미드",
                        xaxis=dict(title="인구수", tickvals=[-2000000, -1000000, 0, 1000000, 2000000],
                                   ticktext=[f"{abs(val):,}" for val in [-2000000, -1000000, 0, 1000000, 2000000]]),
                        yaxis=dict(title="연령"),
                        barmode='relative',
                        bargap=0.05,
                        plot_bgcolor="white"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("남성과 여성 인구 컬럼을 찾을 수 없습니다. 파일 구조를 확인해 주세요.")
        else:
            st.warning("데이터에 '행정구역' 및 '연령' 컬럼이 모두 필요합니다. 파일 구조를 확인하세요.")
