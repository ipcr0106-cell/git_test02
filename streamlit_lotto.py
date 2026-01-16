# # 로또 번호를 대쉬보드에 띄우기
# from numpy import number
# import streamlit as st
# import random # 랜덤 숫자 생성 라이브러리
# st.title("로또 번호 생성기") # 대쉬보드 제목 설정
# st.markdown("버튼을 클릭하면 로또 번호 6개가 생성됩니다.")

# # 로또 번호 생성 함수
# def generate_lotto_numbers():
#     numbers = set() # 중복 없는 숫자 생성을 위해 집합 사용
#     while len(numbers) < 6: # 6개의 숫자가 모일 때까지 반복
#         numbers.add(random.randrange(1, 46)) # 1부터 45까지의 숫자 중 랜덤 선택
#     return numbers # 생성된 숫자 집합 반환

# import datetime
# # 버튼 클릭 시 로또 번호 생성
# botton=st.button("로또 번호 생성")
# if botton:
#     for i in range(1, 6):
#         st.subheader(f"{i}번째 추천 로또 번호:{generate_lotto_numbers()}")
#         # 5세트의 로또 번호 생성
#         st.write(f"생성된 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") # 생성된 시각 표시


# # gt hub에 올려서 bridge로 연결 -> streamlit cloud에 배포 -> URL 복사 -> 노션에 임베드



import streamlit as st
import random
import time
import datetime

st.set_page_config(page_title="럭키 잭팟 로또", page_icon="🎰", layout="centered")

# --- 커스텀 스타일 (레버 애니메이션 및 티켓 디자인) ---
st.markdown("""
<style>
    /* 잭팟 레버 디자인 */
    .stButton>button {
        background: linear-gradient(145deg, #ff4b4b, #cc0000);
        color: white;
        border-radius: 50px;
        height: 80px;
        width: 80px;
        font-size: 30px;
        border: 4px solid #ffd700;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .stButton>button:active {
        transform: translateY(20px); /* 레버가 눌리는 느낌 */
        background: #990000;
    }

    /* 티켓 디자인 */
    .ticket {
        background-color: #ffffff;
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        font-family: 'Courier New', Courier, monospace;
        color: #333;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .ticket-title {
        font-size: 1.2rem;
        font-weight: bold;
        border-bottom: 1px solid #eee;
        margin-bottom: 10px;
        padding-bottom: 5px;
    }
    .lotto-numbers {
        font-size: 1.5rem;
        letter-spacing: 5px;
        color: #ff4b4b;
        font-weight: bold;
    }
    .ticket-footer {
        font-size: 0.8rem;
        color: #888;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 오디오 재생 함수 (자바스크립트) ---
# 실제 잭팟 사운드 파일 URL로 변경해주세요!
# 예시: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
# 짧고 효과음 같은 파일을 쓰는게 좋습니다.
AUDIO_URL = "https://www.myinstants.com/media/sounds/jackpot.mp3" # 잭팟 사운드 예시

def play_audio():
    st.components.v1.html(
        f"""
        <audio autoplay="true" src="{AUDIO_URL}"></audio>
        """,
        height=0,
        width=0,
    )

# --- 메인 화면 ---
st.title("🎰 LUCKY JACKPOT")
st.write("아래 버튼(레버)을 눌러 행운을 잡으세요!")

# 중앙 정렬을 위한 컬럼 배치
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    handle_clicked = st.button("🕹️")

if handle_clicked:
    play_audio() # 버튼 클릭 시 오디오 재생

    # 1. 휘리릭 돌아가는 애니메이션 효과
    with st.empty():
        for _ in range(10):
            random_nums = " ".join([str(random.randint(1, 45)).zfill(2) for _ in range(6)])
            st.markdown(f"<h1 style='text-align: center; color: #ffd700;'>{random_nums}</h1>", unsafe_allow_html=True)
            time.sleep(0.1)
        st.write("") # 지우기

    st.balloons()

    # 2. 6쌍의 티켓 생성
    st.subheader("🎟️ 당신의 행운 티켓")
    
    for i in range(6):
        numbers = sorted(random.sample(range(1, 46), 6))
        num_str = "  ".join([str(n).zfill(2) for n in numbers])
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        # 티켓 HTML 출력
        st.markdown(f"""
        <div class="ticket">
            <div class="ticket-title">LOTTO LUCKY TICKET #{i+1}</div>
            <div class="lotto-numbers">{num_str}</div>
            <div class="ticket-footer">
                ISSUED: {now}<br>
                <b>GOOD LUCK TO YOU!</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # 초기 화면 안내
    st.info("레버를 당기면 6개의 티켓이 발행됩니다!")