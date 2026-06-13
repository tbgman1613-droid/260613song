import streamlit as st
from youtube_comment_downloader import YoutubeCommentDownloader
from collections import Counter
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import re

st.set_page_config(
    page_title="🎵 Music Comment Analyzer",
    page_icon="🎵",
    layout="wide"
)

# ----------------------------
# 디자인
# ----------------------------

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.big-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    background: linear-gradient(90deg,#00d4ff,#ff00ff);
    -webkit-background-clip:text;
    color:transparent;
}

.sub{
    text-align:center;
    color:#bbbbbb;
    font-size:20px;
}

.card{
    background:#1e1e1e;
    padding:20px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="big-title">🎵 Music Comment Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">유튜브 댓글만으로 음악 장르를 분석해보세요</div>',
    unsafe_allow_html=True
)

st.divider()

# ----------------------------
# 장르 키워드
# ----------------------------

genre_keywords = {
    "힙합": [
        "랩","비트","플로우","스웩","힙합",
        "라임","드릴","트랩","가사"
    ],

    "발라드": [
        "감성","눈물","사랑","추억","이별",
        "발라드","슬프다","울컥","감동"
    ],

    "클래식": [
        "오케스트라","피아노","바이올린",
        "클래식","교향곡","연주","베토벤"
    ],

    "록": [
        "록","기타","밴드","헤드뱅잉",
        "락","드럼","에너지","강렬"
    ],

    "재즈": [
        "재즈","스윙","색소폰","즉흥",
        "블루스","그루브","재지"
    ]
}

# ----------------------------
# 댓글 수집
# ----------------------------

url = st.text_input(
    "🎬 유튜브 URL 입력",
    placeholder="https://youtube.com/watch?v=..."
)

if st.button("분석 시작 🚀"):

    if not url:
        st.warning("URL을 입력해주세요.")
        st.stop()

    with st.spinner("댓글 수집 중..."):

        downloader = YoutubeCommentDownloader()

        comments = []

        try:
            for comment in downloader.get_comments_from_url(url):
                comments.append(comment["text"])

                if len(comments) >= 500:
                    break

        except:
            st.error("댓글 수집 실패")
            st.stop()

    if len(comments) == 0:
        st.error("댓글 없음")
        st.stop()

    text = " ".join(comments)

    # ----------------------------
    # 장르 점수
    # ----------------------------

    scores = {}

    for genre, words in genre_keywords.items():

        score = 0

        for word in words:
            score += text.count(word)

        scores[genre] = score

    total = sum(scores.values())

    if total == 0:
        total = 1

    genre_df = pd.DataFrame({
        "장르": list(scores.keys()),
        "확률": [round(v/total*100,2)
                 for v in scores.values()]
    })

    # ----------------------------
    # 감성분석
    # ----------------------------

    sentiments = []

    for c in comments[:300]:

        try:
            polarity = TextBlob(c).sentiment.polarity
            sentiments.append(polarity)
        except:
            pass

    avg_sentiment = round(sum(sentiments)/len(sentiments),2)

    # ----------------------------
    # 결과
    # ----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎼 장르 확률")

        fig = px.bar(
            genre_df,
            x="장르",
            y="확률",
            text="확률",
            color="장르"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("😊 댓글 감정 점수")

        st.metric(
            "평균 감정",
            avg_sentiment
        )

        if avg_sentiment > 0.3:
            st.success("긍정적인 반응")
        elif avg_sentiment < -0.3:
            st.error("부정적인 반응")
        else:
            st.info("중립적인 반응")

    # ----------------------------
    # 워드클라우드
    # ----------------------------

    st.subheader("☁️ 워드클라우드")

    wordcloud = WordCloud(
        width=1200,
        height=500,
        background_color="black"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(15,5))

    ax.imshow(wordcloud)
    ax.axis("off")

    st.pyplot(fig)

    # ----------------------------
    # AI 해설
    # ----------------------------

    best_genre = genre_df.sort_values(
        "확률",
        ascending=False
    ).iloc[0]["장르"]

    st.subheader("🤖 AI 분석")

    st.markdown(f"""
### 분석 결과

가장 높은 확률의 장르는 **{best_genre}** 입니다.

댓글에서 해당 장르를 연상시키는 표현이
가장 많이 발견되었습니다.

이 영상의 청취자들은 해당 음악을
{best_genre} 특유의 분위기로
인식하고 있는 것으로 보입니다.

댓글 수: **{len(comments)}개**
""")

    st.success("분석 완료 🎉")
