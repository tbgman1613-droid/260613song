import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="🎵 AI 음악 추천기",
    page_icon="🎵",
    layout="wide"
)

# -------------------
# CSS
# -------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.title{
    text-align:center;
    color:white;
    font-size:55px;
    font-weight:bold;
}

.card{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    color:white;
    border:1px solid #334155;
}

.genre{
    color:#38bdf8;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='title'>🎵 AI 음악 추천기</div>",
    unsafe_allow_html=True
)

st.write("")
st.write("")

# -------------------
# 음악 데이터
# -------------------

music_db = {

    "발라드":[
        ("밤양갱","비비","달콤하고 감성적인 발라드"),
        ("사건의 지평선","윤하","이별 후 성장 이야기"),
        ("헤어지자 말해요","박재정","애절한 감성"),
        ("취중고백","김민석","고백 감성"),
        ("너의 모든 순간","성시경","대표 고백송"),
        ("Love Wins All","아이유","감성 발라드"),
        ("눈의 꽃","박효신","겨울 감성"),
        ("좋니","윤종신","이별 명곡"),
        ("비가 오는 날엔","비스트","감성 자극"),
        ("어떻게 이별까지 사랑하겠어","AKMU","서정적 발라드")
    ],

    "힙합":[
        ("V","BIG Naughty","트렌디 힙합"),
        ("Counting Stars","BE'O","감성 랩"),
        ("DNA Remix","릴보이","강렬한 플로우"),
        ("호미들","사이렌","국내 대표 힙합"),
        ("Achoo","미란이","에너지 넘치는 곡"),
        ("Buru Star","창모","트랩 힙합"),
        ("METEOR","창모","국민 힙합곡"),
        ("Freak","릴러말즈","강한 비트"),
        ("쇼미더머니","Various","랩 경연 대표곡"),
        ("Selfmade Orange","창모","성공 스토리")
    ],

    "클래식":[
        ("Canon in D","파헬벨","세계적인 클래식"),
        ("Moonlight Sonata","베토벤","월광 소나타"),
        ("Für Elise","베토벤","엘리제를 위하여"),
        ("Spring","비발디","사계 중 봄"),
        ("Swan Lake","차이코프스키","백조의 호수"),
        ("The Blue Danube","요한 슈트라우스","아름다운 왈츠"),
        ("Clair de Lune","드뷔시","달빛"),
        ("Ave Maria","슈베르트","대표 성가"),
        ("Nocturne Op.9","쇼팽","야상곡"),
        ("Hungarian Dance No.5","브람스","활기찬 곡")
    ],

    "록":[
        ("질풍가도","유정석","국민 록"),
        ("걱정말아요 그대","들국화","명곡"),
        ("나는 나비","YB","희망 메시지"),
        ("붉은 노을","이문세","록 스타일 편곡 인기"),
        ("Lonely Night","부활","록 발라드"),
        ("It's My Life","Bon Jovi","세계적 록"),
        ("Numb","Linkin Park","록 명곡"),
        ("Zombie","The Cranberries","대표 록"),
        ("Believer","Imagine Dragons","강렬한 에너지"),
        ("Bohemian Rhapsody","Queen","전설적인 록")
    ],

    "재즈":[
        ("Fly Me To The Moon","Frank Sinatra","대표 재즈"),
        ("Take Five","Dave Brubeck","재즈 명곡"),
        ("Autumn Leaves","Bill Evans","감성 재즈"),
        ("My Funny Valentine","Chet Baker","재즈 스탠다드"),
        ("What A Wonderful World","Louis Armstrong","따뜻한 곡"),
        ("So What","Miles Davis","모던 재즈"),
        ("Blue In Green","Miles Davis","감성 재즈"),
        ("All Of Me","Ella Fitzgerald","재즈 보컬"),
        ("Misty","Erroll Garner","재즈 피아노"),
        ("Summertime","Ella Fitzgerald","대표 명곡")
    ]
}

# -------------------
# 장르 선택
# -------------------

genre = st.selectbox(
    "🎼 좋아하는 장르를 선택하세요",
    list(music_db.keys())
)

# -------------------
# 추천 버튼
# -------------------

if st.button("🤖 AI 추천받기", use_container_width=True):

    st.success(f"{genre} 장르 추천 결과")

    for idx, music in enumerate(music_db[genre], start=1):

        title, artist, desc = music

        st.markdown(
            f"""
            <div class="card">
            <h3>🎵 {idx}. {title}</h3>

            <p><b>가수/작곡가</b> : {artist}</p>

            <p><b>설명</b> : {desc}</p>

            <p class="genre">{genre}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.balloons()
