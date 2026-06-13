import streamlit as st
import pandas as pd
import plotly.express as px
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI 음악 추천 플랫폼",
    page_icon="🎵",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background-color:#f8fafc;
}

.main-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#0f172a;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:#64748b;
}

.card{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.genre-box{
    background:white;
    border-radius:15px;
    padding:15px;
    text-align:center;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 데이터
# -----------------------------
music_db = {

    "발라드":[
        ("밤양갱","비비","달콤한 감성"),
        ("사건의 지평선","윤하","희망적인 감성"),
        ("Love Wins All","아이유","애절한 사랑"),
        ("헤어지자 말해요","박재정","이별 감성"),
        ("너의 모든 순간","성시경","고백 명곡"),
        ("좋니","윤종신","이별 명곡"),
        ("눈의 꽃","박효신","겨울 감성"),
        ("취중고백","김민석","고백 노래"),
        ("비가 오는 날엔","비스트","비 오는 날"),
        ("어떻게 이별까지 사랑하겠어","AKMU","감성 발라드")
    ],

    "힙합":[
        ("METEOR","창모","강렬한 비트"),
        ("Counting Stars","BE'O","감성 힙합"),
        ("V","BIG Naughty","트렌디"),
        ("DNA Remix","릴보이","랩 퍼포먼스"),
        ("Achoo","미란이","에너지 폭발"),
        ("Selfmade Orange","창모","성공 스토리"),
        ("Freak","릴러말즈","힙한 분위기"),
        ("Buru Star","창모","트랩 스타일"),
        ("사이렌","호미들","강한 중독성"),
        ("Forever","ASH ISLAND","감성 랩")
    ],

    "클래식":[
        ("Canon in D","파헬벨","대표 클래식"),
        ("Moonlight Sonata","베토벤","월광 소나타"),
        ("Für Elise","베토벤","피아노 명곡"),
        ("Spring","비발디","사계"),
        ("Clair de Lune","드뷔시","달빛"),
        ("Nocturne Op.9","쇼팽","야상곡"),
        ("Ave Maria","슈베르트","성가"),
        ("Hungarian Dance No.5","브람스","활기찬"),
        ("Swan Lake","차이코프스키","발레곡"),
        ("Blue Danube","슈트라우스","왈츠")
    ],

    "록":[
        ("나는 나비","YB","희망 메시지"),
        ("질풍가도","유정석","열정"),
        ("Lonely Night","부활","록 발라드"),
        ("Numb","Linkin Park","강렬함"),
        ("Believer","Imagine Dragons","에너지"),
        ("Zombie","The Cranberries","대표 록"),
        ("Bohemian Rhapsody","Queen","전설"),
        ("걱정말아요 그대","들국화","위로"),
        ("붉은 노을","이문세","신나는 록"),
        ("It's My Life","Bon Jovi","동기부여")
    ],

    "재즈":[
        ("Fly Me To The Moon","Frank Sinatra","대표 재즈"),
        ("Take Five","Dave Brubeck","재즈 명곡"),
        ("Autumn Leaves","Bill Evans","감성"),
        ("What A Wonderful World","Louis Armstrong","따뜻함"),
        ("So What","Miles Davis","모던 재즈"),
        ("Blue In Green","Miles Davis","잔잔함"),
        ("Misty","Erroll Garner","재즈 피아노"),
        ("Summertime","Ella Fitzgerald","대표곡"),
        ("All Of Me","Ella Fitzgerald","보컬 재즈"),
        ("My Funny Valentine","Chet Baker","감미로운")
    ]
}

# -----------------------------
# 제목
# -----------------------------
st.markdown(
    "<div class='main-title'>🎵 AI 음악 추천 플랫폼</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>장르 · 분위기 · 상황을 선택하고 음악을 추천받아보세요</div>",
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# 오늘의 추천곡
# -----------------------------
all_songs = []

for genre in music_db:
    all_songs.extend(music_db[genre])

today_song = random.choice(all_songs)

st.info(
    f"🎧 오늘의 추천곡 : {today_song[0]} - {today_song[1]}"
)

# -----------------------------
# 음악 성향 테스트
# -----------------------------
st.subheader("🧠 음악 성향 테스트")

q1 = st.radio(
    "가사를 중요하게 생각하나요?",
    ["예","아니오"]
)

q2 = st.radio(
    "비트가 중요하나요?",
    ["예","아니오"]
)

q3 = st.radio(
    "잔잔한 음악을 좋아하나요?",
    ["예","아니오"]
)

if st.button("성향 분석"):

    if q1 == "예" and q3 == "예":
        st.success("🎼 당신은 감성 발라드형입니다!")

    elif q2 == "예":
        st.success("🎤 당신은 힙합/록형입니다!")

    else:
        st.success("🎻 당신은 클래식/재즈형입니다!")

st.divider()

# -----------------------------
# 선택
# -----------------------------
col1,col2,col3 = st.columns(3)

with col1:
    genre = st.selectbox(
        "🎵 장르",
        list(music_db.keys())
    )

with col2:
    mood = st.selectbox(
        "😊 분위기",
        [
            "신나는",
            "감성적인",
            "행복한",
            "우울한",
            "힐링",
            "집중"
        ]
    )

with col3:
    situation = st.selectbox(
        "🌈 상황",
        [
            "공부",
            "운동",
            "산책",
            "드라이브",
            "비 오는 날",
            "잠들기 전",
            "혼자 있을 때"
        ]
    )

# -----------------------------
# 인기 차트
# -----------------------------
st.subheader("📊 장르 인기 비율")

chart_df = pd.DataFrame({
    "장르":["발라드","힙합","록","재즈","클래식"],
    "비율":[35,25,18,12,10]
})

fig = px.pie(
    chart_df,
    names="장르",
    values="비율"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# 추천
# -----------------------------
if st.button("🤖 AI 추천받기", use_container_width=True):

    st.success(
        f"{mood} 분위기의 {genre} 음악을 추천합니다!"
    )

    for i, song in enumerate(music_db[genre], start=1):

        title, artist, desc = song

        st.markdown(f"""
        <div class='card'>

        <h3>🎵 {i}. {title}</h3>

        <b>아티스트</b> : {artist}<br><br>

        <b>곡 설명</b> : {desc}<br><br>

        <b>추천 이유</b> :
        {mood} 분위기와 '{situation}' 상황에 잘 어울리는 곡

        </div>
        """, unsafe_allow_html=True)

    rating = st.slider(
        "⭐ 추천 만족도",
        1,
        5,
        3
    )

    st.write(f"당신의 평가 : {rating}점")

    st.balloons()
