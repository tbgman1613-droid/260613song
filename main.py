import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# ----------------------------
# 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="🎵 AI 음악 장르 분석기",
    page_icon="🎵",
    layout="wide"
)

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.title {
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:white;
}

.subtitle {
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
}

.genre-box {
    background:#334155;
    padding:15px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:20px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# 제목
# ----------------------------
st.markdown(
    "<div class='title'>🎵 AI 음악 장르 분석기</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>텍스트 속 음악 성향을 분석해보세요</div>",
    unsafe_allow_html=True
)

st.write("")

# ----------------------------
# 장르 소개
# ----------------------------
col1,col2,col3,col4,col5 = st.columns(5)

genres = [
    ("🎤","힙합"),
    ("🎼","발라드"),
    ("🎻","클래식"),
    ("🎸","록"),
    ("🎷","재즈")
]

for col, (emoji, genre) in zip([col1,col2,col3,col4,col5], genres):
    with col:
        st.markdown(
            f"""
            <div class='genre-box'>
            {emoji}<br>{genre}
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")
st.write("")

# ----------------------------
# 장르 키워드
# ----------------------------
genre_keywords = {
    "힙합": [
        "랩","비트","플로우","래퍼",
        "힙합","스웨그","트랩","드릴"
    ],

    "발라드": [
        "사랑","이별","감성",
        "눈물","추억","목소리"
    ],

    "클래식": [
        "오케스트라","교향곡",
        "피아노","바이올린",
        "첼로","클래식"
    ],

    "록": [
        "록","rock",
        "기타","드럼",
        "밴드","헤비메탈"
    ],

    "재즈": [
        "재즈","색소폰",
        "블루스","스윙",
        "즉흥연주"
    ]
}

# ----------------------------
# 입력 방식
# ----------------------------
st.subheader("📝 텍스트 입력")

text = st.text_area(
    "노래 설명, 가사 느낌, 감상문 등을 입력하세요",
    height=250
)

# ----------------------------
# 분석 함수
# ----------------------------
def analyze_text(text):

    scores = {
        "힙합":0,
        "발라드":0,
        "클래식":0,
        "록":0,
        "재즈":0
    }

    lower = text.lower()

    for genre, keywords in genre_keywords.items():

        for keyword in keywords:

            if keyword.lower() in lower:
                scores[genre] += 1

    return scores

# ----------------------------
# 워드클라우드
# ----------------------------
def draw_wordcloud(text):

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="black"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)

# ----------------------------
# 분석
# ----------------------------
if st.button("🚀 분석 시작", use_container_width=True):

    if len(text.strip()) == 0:
        st.warning("텍스트를 입력해주세요.")
        st.stop()

    result = analyze_text(text)

    df = pd.DataFrame({
        "장르": result.keys(),
        "점수": result.values()
    })

    st.subheader("📊 장르 분석 결과")

    fig = px.bar(
        df,
        x="장르",
        y="점수",
        color="장르",
        text="점수"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    winner = max(result, key=result.get)

    st.success(
        f"🎯 가장 높은 성향은 '{winner}' 입니다!"
    )

    st.subheader("📈 점수 비율")

    pie = px.pie(
        df,
        names="장르",
        values="점수"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    st.subheader("☁️ 워드클라우드")

    cleaned = re.sub(
        r"[^가-힣a-zA-Z ]",
        "",
        text
    )

    draw_wordcloud(cleaned)

    st.subheader("🔥 TOP 단어")

    words = cleaned.split()

    top_words = Counter(words).most_common(10)

    top_df = pd.DataFrame(
        top_words,
        columns=["단어","횟수"]
    )

    st.dataframe(
        top_df,
        use_container_width=True
    )

    st.balloons()
