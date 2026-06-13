import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(
    page_title="🎵 AI 유튜브 댓글 음악 분석기",
    page_icon="🎵",
    layout="wide"
)

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.big-title {
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:white;
}

.genre-card {
    background:#1e293b;
    padding:15px;
    border-radius:15px;
    text-align:center;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# API 입력
# -----------------------
st.markdown(
    "<div class='big-title'>🎵 AI 유튜브 댓글 음악 분석기</div>",
    unsafe_allow_html=True
)

st.write("")

api_key = st.text_input(
    "YouTube API Key 입력",
    type="password"
)

video_id = st.text_input(
    "유튜브 Video ID 입력"
)

# -----------------------
# 장르 설명
# -----------------------

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class='genre-card'>
    🎤<br>
    힙합
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='genre-card'>
    🎼<br>
    발라드
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='genre-card'>
    🎻<br>
    클래식
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='genre-card'>
    🎸<br>
    록
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class='genre-card'>
    🎷<br>
    재즈
    </div>
    """, unsafe_allow_html=True)

# -----------------------
# 장르 키워드
# -----------------------

genre_keywords = {
    "힙합": [
        "랩","flow","비트","swag","힙합",
        "래퍼","드릴","트랩"
    ],

    "발라드": [
        "감성","눈물","사랑","이별",
        "목소리","발라드"
    ],

    "클래식": [
        "오케스트라","피아노","바이올린",
        "클래식","교향곡"
    ],

    "록": [
        "기타","밴드","록",
        "rock","드럼","헤비"
    ],

    "재즈": [
        "재즈","sax","색소폰",
        "스윙","블루스"
    ]
}

# -----------------------
# 댓글 가져오기
# -----------------------

def get_comments(api_key, video_id):

    youtube = build(
        "youtube",
        "v3",
        developerKey=api_key
    )

    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    response = request.execute()

    while request:

        for item in response["items"]:

            text = item["snippet"]\
                ["topLevelComment"]\
                ["snippet"]\
                ["textDisplay"]

            comments.append(text)

        request = youtube.commentThreads().list_next(
            request,
            response
        )

        if request:
            response = request.execute()

    return comments

# -----------------------
# 장르 분석
# -----------------------

def analyze_genre(comments):

    result = {
        "힙합":0,
        "발라드":0,
        "클래식":0,
        "록":0,
        "재즈":0
    }

    for comment in comments:

        lower = comment.lower()

        for genre, keywords in genre_keywords.items():

            for keyword in keywords:

                if keyword.lower() in lower:
                    result[genre]+=1

    return result

# -----------------------
# 워드클라우드
# -----------------------

def make_wordcloud(text):

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="black"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12,5))

    ax.imshow(wc)
    ax.axis("off")

    st.pyplot(fig)

# -----------------------
# 분석 버튼
# -----------------------

if st.button("🚀 분석 시작"):

    if api_key == "" or video_id == "":
        st.warning("API Key와 Video ID를 입력하세요.")
        st.stop()

    with st.spinner("댓글 분석 중..."):

        comments = get_comments(
            api_key,
            video_id
        )

    st.success(f"{len(comments)}개의 댓글 분석 완료!")

    # -------------------
    # 장르 분석
    # -------------------

    genre_result = analyze_genre(comments)

    df = pd.DataFrame({
        "장르":genre_result.keys(),
        "언급수":genre_result.values()
    })

    fig = px.bar(
        df,
        x="장르",
        y="언급수",
        color="장르",
        title="🎵 음악 장르 반응 분석"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------
    # 댓글 목록
    # -------------------

    st.subheader("💬 댓글 샘플")

    for c in comments[:20]:
        st.write("•", c)

    # -------------------
    # 워드클라우드
    # -------------------

    st.subheader("🔥 인기 키워드")

    text = " ".join(comments)

    text = re.sub(
        r"[^가-힣a-zA-Z ]",
        "",
        text
    )

    make_wordcloud(text)

    # -------------------
    # TOP 단어
    # -------------------

    words = text.split()

    top_words = Counter(words).most_common(15)

    word_df = pd.DataFrame(
        top_words,
        columns=["단어","빈도"]
    )

    fig2 = px.pie(
        word_df,
        names="단어",
        values="빈도",
        title="🏆 TOP 단어"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # -------------------
    # 결과
    # -------------------

    best_genre = max(
        genre_result,
        key=genre_result.get
    )

    st.markdown(f"""
    ## 🎯 AI 판정 결과

    현재 댓글 반응은
    **{best_genre}**
    장르 성향이 가장 강합니다.
    """)
