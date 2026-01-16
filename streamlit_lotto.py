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

# --- CSS: 모든 요소의 너비 통일 및 사각형 버튼 디자인 ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }

    /* 모든 주요 요소의 너비를 동일하게 고정 (너비 100%) */
    .title-banner, .slot-container, .stButton > button, .ticket {
        max-width: 500px; /* 적절한 가로폭 제한 */
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* 1. 타이틀 전광판 */
    .title-banner {
        background: linear-gradient(to right, #b30000, #ff0000);
        border: 4px solid #444; 
        border-radius: 20px;
        padding: 25px 10px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
        position: relative;
    }
    .bulb {
        position: absolute; width: 10px; height: 10px;
        background-color: #fff; border-radius: 50%;
        animation: bulb-flash 0.8s infinite alternate;
    }
    @keyframes bulb-flash {
        0% { background-color: #444; box-shadow: none; }
        100% { background-color: #ffcc00; box-shadow: 0 0 15px #ffcc00; }
    }
    .title-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.2rem; font-weight: bold; margin: 0;
        background: linear-gradient(to bottom, #fff3ad 0%, #ffcc00 45%, #b38600 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.5));
    }

    /* 2. 전광판 슬롯 */
    .slot-container {
        background-color: #111111 !important;
        border-radius: 20px !important;
        padding: 30px 10px !important;
        display: flex !important;
        justify-content: center !important;
        box-shadow: inset 0px 0px 30px rgba(0,0,0,1) !important;
        margin-top: 25px !important;
        margin-bottom: 25px !important;
        border: 2px solid #333 !important;
    }
    .slot-box {
        flex: 1; text-align: center; font-family: 'Arial Black', sans-serif;
        font-size: 2.5rem; color: #f6e05e;
        text-shadow: 0 0 15px rgba(246, 224, 94, 1);
        border-right: 2px solid #222;
    }
    .slot-box:last-child { border-right: none; }

    /* 3. PUSH 버튼: 모서리가 둥근 사각형 + 너비 통일 */
    div.stButton {
        display: flex;
        justify-content: center;
    }
    div.stButton > button {
        width: 100% !important; /* 위 요소들과 너비 동일하게 */
        height: 70px !important; /* 높이는 적절하게 조정 */
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important;
        border-radius: 15px !important; /* 다른 요소들과 비슷한 곡률 */
        border: 4px solid #ffd700 !important;
        box-shadow: 0px 6px 0px 0px #500000, 0px 10px 20px rgba(0,0,0,0.5) !important;
        font-family: 'Arial Black', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
        transition: all 0.1s !important;
    }
    div.stButton > button:active {
        transform: translateY(4px) !important;
        box-shadow: 0px 2px 0px 0px #500000 !important;
    }

    /* 4. 티켓 디자인 */
    .ticket {
        background-color: #ffffff;
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
        text-align: center;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 구성 ---

# 타이틀 전구 배치
bulbs_html = "".join([f'<div class="bulb" style="top:-6px; left:{i}%;"></div>' for i in range(0, 101, 8)])
bulbs_html += "".join([f'<div class="bulb" style="bottom:-6px; left:{i}%;"></div>' for i in range(0, 101, 8)])

st.markdown(f"""
    <div class="title-banner">
        {bulbs_html}
        <p class="title-text">🎰 LUCKY JACKPOT</p>
    </div>
    """, unsafe_allow_html=True)

if 'playing' not in st.session_state:
    st.session_state.playing = False

# 전광판 플레이스홀더
slot_placeholder = st.empty()
initial_slots = "".join([f'<div class="slot-box">??</div>' for _ in range(6)])
slot_placeholder.markdown(f'<div class="slot-container">{initial_slots}</div>', unsafe_allow_html=True)

# PUSH 버튼 (사각형 디자인)
if st.button("PUSH"):
    st.session_state.playing = True

if st.session_state.playing:
    st.components.v1.html('<audio autoplay><source src="https://www.myinstants.com/media/sounds/jackpot.mp3"></audio>', height=0)
    for _ in range(15):
        temp_nums = [str(random.randint(1, 45)).zfill(2) for _ in range(6)]
        slots_html = "".join([f'<div class="slot-box">{n}</div>' for n in temp_nums])
        slot_placeholder.markdown(f'<div class="slot-container">{slots_html}</div>', unsafe_allow_html=True)
        time.sleep(0.08)
    
    final_numbers = sorted(random.sample(range(1, 46), 6))
    final_slots_html = "".join([f'<div class="slot-box">{str(n).zfill(2)}</div>' for n in final_numbers])
    slot_placeholder.markdown(f'<div class="slot-container">{final_slots_html}</div>', unsafe_allow_html=True)
    st.balloons()
    
    st.markdown("<h3 style='text-align:center; color:white; margin-top:30px;'>🎟️ 행운의 티켓 (5장)</h3>", unsafe_allow_html=True)
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    for i in range(5):
        nums = sorted(random.sample(range(1, 46), 6))
        num_str = " ".join([str(n).zfill(2) for n in nums])
        st.markdown(f"""
        <div class="ticket">
            <div style="font-weight:bold; border-bottom:1px solid #eee; margin-bottom:8px; color:#666;">LUCKY TICKET #{i+1}</div>
            <div style="font-size:1.6rem; color:#ff4b4b; font-weight:bold; letter-spacing:2px;">{num_str}</div>
            <div style="font-size:0.7rem; color:#999; margin-top:5px;">{now} 발행</div>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.playing = False
