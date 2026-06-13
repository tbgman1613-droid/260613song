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
# 스타일 (밝은 UI 유지 + 카드 강화)
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
    font-size:18px;
    color:#64748b;
}

.card{
    background:white;
    padding:18px;
    border-radius:18px;
    box-shadow:0px 4px 14px rgba(0,0,0,0.08);
    margin-bottom:12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 음악 데이터
# -----------------------------
music_db = {

    "발라드":[
        ("밤양갱","비비","감성"),
        ("사건의 지평선","윤하","희망"),
        ("Love Wins All","아이유","애절"),
        ("헤어지자 말해요","박재정","이별"),
        ("너의 모든 순간","성시경","고백"),
        ("좋니","윤종신","이별"),
        ("눈의 꽃","박효신","겨울"),
        ("취중고백","김민석","감성"),
        ("비가 오는 날엔","비스트","비"),
        ("어떻게 이별까지 사랑하겠어","AKMU","서정")
    ],

    "힙합":[
        ("METEOR","창모","강렬"),
        ("Counting Stars","BE'O","감성"),
        ("V","BIG Naughty","트렌디"),
        ("Achoo","미란이","에너지"),
        ("Selfmade Orange","창모","성공"),
        ("Freak","릴러말즈","힙합"),
        ("DNA Remix","릴보이","랩"),
        ("사이렌","호미들","트랩"),
        ("Buru Star","창모","비트"),
        ("Forever","ASH ISLAND","감성")
    ],

    "클래식":[
        ("Canon in D","Pachelbel","대표"),
        ("Moonlight Sonata","Beethoven","월광"),
        ("Für Elise","Beethoven","피아노"),
        ("Spring","Vivaldi","사계"),
        ("Clair de Lune","Debussy","달빛"),
        ("Nocturne","Chopin","야상곡"),
        ("Ave Maria","Schubert","성가"),
        ("Swan Lake","Tchaikovsky","발레"),
        ("Blue Danube","Strauss","왈츠"),
        ("Hungarian Dance","Brahms","활기")
    ],

    "록":[
        ("Bohemian Rhapsody","Queen","전설"),
        ("Numb","Linkin Park","강렬"),
        ("Believer","Imagine Dragons","에너지"),
        ("Zombie","The Cranberries","록"),
        ("It's My Life","Bon Jovi","동기부여"),
        ("나는 나비","YB","희망"),
        ("질풍가도","유정석","열정"),
        ("Lonely Night","부활","록발라드"),
        ("걱정말아요 그대","들국화","위로"),
        ("붉은 노을","이문세","감성")
    ],

    "재즈":[
        ("Fly Me To The Moon","Sinatra","대표"),
        ("Take Five","Brubeck","리듬"),
        ("Autumn Leaves","Bill Evans","감성"),
        ("What A Wonderful World","Louis Armstrong","따뜻"),
        ("So What","Miles Davis","모던"),
        ("Blue In Green","Miles Davis","잔잔"),
        ("Misty","Erroll Garner","피아노"),
        ("Summertime","Ella Fitzgerald","명곡"),
        ("All Of Me","Ella Fitzgerald","보컬"),
        ("My Funny Valentine","Chet Baker","감미")
    ]
}

# -----------------------------
# 제목
# -----------------------------
st.markdown("<div class='main-title'>🎵 AI 음악 추천 플랫폼</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>장르 + 분위기 + 상황 기반 음악 추천</div>", unsafe_allow_html=True)

st.write("")

# -----------------------------
# 오늘의 추천곡
# -----------------------------
all_songs = [song for g in music_db.values() for song in g]
today = random.choice(all_songs)

st.info(f"🎧 오늘의 추천곡: {today[0]} - {today[1]}")

# -----------------------------
# 선택 UI
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    genre = st.selectbox("🎵 장르", list(music_db.keys()))

with col2:
    mood = st.selectbox("😊 분위기", ["신남","감성","우울","행복","힐링","집중"])

with col3:
    situation = st.selectbox("🌈 상황", ["공부","운동","드라이브","산책","비 오는 날","잠들기 전"])

# -----------------------------
# 🎯 장르별 인기 TOP5 차트 (핵심 추가)
# -----------------------------
st.subheader("📊 장르별 인기 TOP 5")

popularity = {
    "발라드":[95,92,90,88,85],
    "힙합":[94,91,89,87,84],
    "클래식":[98,96,93,90,88],
    "록":[97,95,92,90,87],
    "재즈":[93,91,89,86,84]
}

top5_songs = [s[0] for s in music_db[genre][:5]]

chart_df = pd.DataFrame({
    "노래": top5_songs,
    "인기도": popularity[genre]
})

fig = px.bar(
    chart_df,
    x="노래",
    y="인기도",
    text="인기도",
    color="노래",
    title=f"🔥 {genre} TOP 5 인기곡"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 추천 버튼
# -----------------------------
if st.button("🤖 AI 추천받기", use_container_width=True):

    st.success(f"{mood} 분위기 + {genre} 추천 결과")

    for i, song in enumerate(music_db[genre], start=1):

        title, artist, desc = song

        st.markdown(f"""
        <div class='card'>
        <h3>🎵 {i}. {title}</h3>
        <b>아티스트:</b> {artist}<br><br>
        <b>설명:</b> {desc}<br><br>
        <b>추천 이유:</b> {mood} 분위기 + {situation} 상황에 적합
        </div>
        """, unsafe_allow_html=True)

    st.balloons()
