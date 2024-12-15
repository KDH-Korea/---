import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 데이터 불러오기
data = pd.read_excel('복사본 동해의 차 만족도.xlsx')

# 페이지 제목 설정
st.set_page_config(page_title="차 만족도 대시보드", layout="wide")
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5em;
        color: #ff7f50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
    }
    .car-card {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: black;
    }
    .car-card h4 {
        margin: 0;
        color: #007bff;
    }
    .car-card p {
        color: black;
    }
    </style>
    <div class="main-title">🚗 차 만족도 대시보드 🚗</div>
    """,
    unsafe_allow_html=True,
)

# 사이드바 필터
st.sidebar.header("🔍 필터")
st.sidebar.markdown("필터를 사용하여 원하는 차량 데이터를 탐색하세요.")
brands = st.sidebar.multiselect("브랜드 선택", options=data["브랜드"].unique(), default=data["브랜드"].unique())
satisfaction_range = st.sidebar.slider("만족도 범위 선택", min_value=0, max_value=10, value=(0, 10))

# 사용자 입력에 따라 데이터 필터링
filtered_data = data[
    (data["브랜드"].isin(brands)) &
    (data["총 만족도+ 감성점수(10점만점)"].between(satisfaction_range[0], satisfaction_range[1]))
]

# 필터링된 데이터 표시
tab1, tab2, tab3 = st.tabs(["📊 데이터 테이블", "📈 만족도 차트", "🚘 차량별 링크"])

with tab1:
    st.markdown("<h3 style='text-align: center; color: #4caf50;'>필터링된 데이터</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_data, use_container_width=True)

    # 필터링된 데이터 다운로드 허용
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 필터링된 데이터 다운로드",
        data=csv,
        file_name='filtered_car_satisfaction.csv',
        mime='text/csv',
    )

with tab2:
    st.markdown("<h3 style='text-align: center; color: #4caf50;'>차종별 만족도 점수</h3>", unsafe_allow_html=True)

    # 만족도 누적 막대 그래프
    satisfaction_columns = ["외관 만족도", "내부 만족도", "총 만족도+ 감성점수(10점만점)"]
    stacked_data = filtered_data.melt(
        id_vars=["브랜드", "차종"],
        value_vars=satisfaction_columns,
        var_name="만족도 유형",
        value_name="만족도 점수"
    )
    fig = px.bar(
        stacked_data,
        x="차종",
        y="만족도 점수",
        color="만족도 유형",
        barmode="stack",
        title="차종별 만족도 누적 막대 그래프",
        labels={"만족도 점수": "점수", "차종": "차량"},
        hover_data=["브랜드"],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("<h3 style='text-align: center; color: #4caf50;'>🚘 차량별 구매 링크</h3>", unsafe_allow_html=True)
    for i, row in filtered_data.iterrows():
        st.markdown(
            f"""
            <div class="car-card">
                <h4>{row['브랜드']} {row['차종']}</h4>
                <p><b>KB 차차차 - 저가 링크:</b> 신뢰할 수 있는 중고차 거래 플랫폼 KB 차차차에서 제공하는 저가 옵션입니다. <a href="{row['KB 차차차        저가 링크']}" target="_blank">여기</a></p>
                <p><b>SK 엔카 - 고가 링크:</b> SK 엔카에서 제공하는 고가 옵션으로 차량 상태가 더 좋을 가능성이 높습니다. <a href="{row['SK 엔카                  고가 링크']}" target="_blank">여기</a></p>
                <p><b>대전 중고차 링크:</b> 대전 지역의 중고차 거래를 위한 추천 링크입니다. <a href="{row['대전 중고차 링크']}" target="_blank">여기</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )

# 추가적인 스타일 적용
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-size: 1.2em;
    }
    .stButton > button:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
