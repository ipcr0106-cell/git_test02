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

# --- CSS (디자인 유지, 정렬은 건드리지 않음) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }

    .stButton > button {
        background: radial-gradient(circle at 30% 30%, #ff4b4b, #800000) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 120px !important;
        height: 120px !important;
        border: 8px solid #ffd700 !important;
        box-shadow: 0px 10px 0px 0px #500000,
                    0px 15px 30px rgba(0,0,0,0.5) !important;
        transition: all 0.1s !important;
    }

    .stButton > button:active {
        transform: translateY(8px) !important;
        box-shadow: 0px 2px 0px 0px #500000 !important;
    }

    .title-banner {
        background: linear-gradient(to right, #b30000, #ff0000);
        border: 6px solid #444;
        border-radius: 20px;
        padding: 25px 30px;
        text-align: center;
        margin-bottom: 25px;
        position: relative;
    }

    .title-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.5rem;
        background: linear-gradient(to bottom, #fff3ad, #ffcc00, #b38600);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .slot-container {
        background-color: #111;
        border-radius: 30px;
        padding: 30px 10px;
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }

    .slot-box {
        flex: 1;
        text-align: center;
        font-family: 'Arial Black';
        font-size: 2.8rem;
        color: #f6e05e;
        border-right: 2px solid #222;
    }

    .slot-box:last-child { border-right: none; }

    .ticket {
        background-color: #fff;
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        font-family: 'Courier New';
        text-align: center;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 타이틀 ---
st.markdown("""
<div class="title-banner">
    <p class="title-text">🎰 LUCKY JACKPOT</p>
</div>
<p style="text-align:center; color:#ccc; font-weight:bold;">
WINNER WINNER CHICKEN DINNER!
</p>
""", unsafe_allow_html=True)

# --- 슬롯 ---
if "playing" not in st.session_state:
    st.session_state.playing = False

slot_placeholder = st.empty()
slot_placeholder.markdown(
    '<div class="slot-container">' +
    ''.join('<div class="slot-box">??</div>' for _ in range(6)) +
    '</div>',
    unsafe_allow_html=True
)

# ===============================
# ✅ PUSH 버튼 (타이틀 영향 없음)
# ===============================
with st.container():
    left, center, right = st.columns([3, 2, 3])
    with center:
        if st.button("PUSH"):
            st.session_state.playing = True

# --- 게임 로직 ---
if st.session_state.playing:
    for _ in range(15):
        nums = [str(random.randint(1, 45)).zfill(2) for _ in range(6)]
        slot_placeholder.markdown(
            '<div class="slot-container">' +
            ''.join(f'<div class="slot-box">{n}</div>' for n in nums) +
            '</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.08)

    final = sorted(random.sample(range(1, 46), 6))
    slot_placeholder.markdown(
        '<div class="slot-container">' +
        ''.join(f'<div class="slot-box">{str(n).zfill(2)}</div>' for n in final) +
        '</div>',
        unsafe_allow_html=True
    )

    st.balloons()

    st.markdown("<h3 style='text-align:center;color:white;'>🎟️ 당신의 행운 티켓</h3>",
                unsafe_allow_html=True)

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    for i in range(5):
        nums = sorted(random.sample(range(1, 46), 6))
        st.markdown(f"""
        <div class="ticket">
            <b>LUCKY TICKET #{i+1}</b><br><br>
            <span style="font-size:1.6rem; color:#ff4b4b;">
                {' '.join(str(n).zfill(2) for n in nums)}
            </span><br>
            <small>{now}</small>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.playing = False

