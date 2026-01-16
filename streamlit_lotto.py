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

# --- CSS: 배경색 및 버튼 중앙 정렬 수정 ---
st.markdown("""
<style>
    /* 전체 배경을 어둡게 설정 */
    .stApp {
        background-color: #0e1117;
    }

    /* 1. 타이틀: 리얼 전구 전광판 스타일 */
    .title-banner {
        background: linear-gradient(to right, #b30000, #ff0000);
        border: 6px solid #444; 
        border-radius: 20px;
        padding: 25px 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        position: relative;
        overflow: visible;
    }

    /* 전구 공통 스타일 */
    .bulb {
        position: absolute;
        width: 12px;
        height: 12px;
        background-color: #fff;
        border-radius: 50%;
        z-index: 10;
        animation: bulb-flash 0.8s infinite alternate;
    }

    @keyframes bulb-flash {
        0% { background-color: #444; box-shadow: none; }
        100% { background-color: #ffcc00; box-shadow: 0 0 15px #ffcc00, 0 0 25px #ffcc00; }
    }

    /* 금색 그라데이션 및 금속 느낌의 텍스트 디자인 */
    .title-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.8rem;
        font-weight: bold;
        margin: 0;
        letter-spacing: 2px;
        background: linear-gradient(to bottom, #fff3ad 0%, #ffcc00 45%, #b38600 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.5));
    }

    /* 2. 전광판: 둥근 검정 사각형 + 노란색 네온 숫자 */
    .slot-container {
        background-color: #111111 !important;
        border-radius: 30px !important;
        padding: 30px 10px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: inset 0px 0px 30px rgba(0,0,0,1) !important;
        margin: 30px 0px !important;
        border: 2px solid #333 !important;
    }
    .slot-box {
        flex: 1 !important;
        text-align: center !important;
        font-family: 'Arial Black', sans-serif !important;
        font-size: 2.8rem !important;
        color: #f6e05e !important;
        text-shadow: 0 0 15px rgba(246, 224, 94, 1) !important;
        border-right: 2px solid #222 !important;
    }
    .slot-box:last-child { border-right: none !important; }

    /* 3. 레버 버튼: 입체적인 붉은 버튼 및 중앙 정렬 */
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton>button {
        background: radial-gradient(circle at 30% 30%, #ff4b4b, #800000) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 120px !important;
        height: 120px !important;
        border: 8px solid #ffd700 !important;
        box-shadow: 0px 10px 0px 0px #500000, 0px 15px 30px rgba(0,0,0,0.5) !important;
        transition: all 0.1s !important;
        margin: 20px auto !important;
    }
    .stButton>button:active {
        transform: translateY(8px) !important;
        box-shadow: 0px 2px 0px 0px #500000 !important;
    }

    /* 4. 티켓 디자인 */
    .ticket {
        background-color: #ffffff;
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        color: #333; /* 어두운 배경에서 글씨가 잘 보이게 설정 */
    }
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 구성 ---

# 타이틀 전구 배치를 위한 HTML 생성
bulbs_html = ""
for i in range(0, 101, 6):
    bulbs_html += f'<div class="bulb" style="top: -6px; left: {i}%;"></div>'
    bulbs_html += f'<div class="bulb" style="bottom: -6px; left: {i}%;"></div>'
for i in range(15, 86, 20):
    bulbs_html += f'<div class="bulb" style="left: -6px; top: {i}%;"></div>'
    bulbs_html += f'<div class="bulb" style="right: -6px; top: {i}%;"></div>'

# 상단 타이틀 배너 출력
st.markdown(f"""
    <div class="title-banner">
        {bulbs_html}
        <p class="title-text">🎰 LUCKY JACKPOT</p>
    </div>
    <p style="text-align:center; color:#ccc; font-size:1.1rem; font-weight:bold;">WINNER WINNER CHICKEN DINNER!</p>
    """, unsafe_allow_html=True)

if 'playing' not in st.session_state:
    st.session_state.playing = False

# 전광판 플레이스홀더
slot_placeholder = st.empty()
initial_slots = "".join([f'<div class="slot-box">??</div>' for _ in range(6)])
slot_placeholder.markdown(f'<div class="slot-container">{initial_slots}</div>', unsafe_allow_html=True)

# 레버 버튼 (가운데 정렬은 CSS에서 처리됨)
if st.button("PUSH"):
    st.session_state.playing = True

if st.session_state.playing:
    # 잭팟 효과음
    st.components.v1.html('<audio autoplay><source src="https://www.myinstants.com/media/sounds/jackpot.mp3"></audio>', height=0)

    # 1. 롤링 애니메이션
    for _ in range(15):
        temp_nums = [str(random.randint(1, 45)).zfill(2) for _ in range(6)]
        slots_html = "".join([f'<div class="slot-box">{n}</div>' for n in temp_nums])
        slot_placeholder.markdown(f'<div class="slot-container">{slots_html}</div>', unsafe_allow_html=True)
        time.sleep(0.08)
    
    # 2. 결과 확정
    final_numbers = sorted(random.sample(range(1, 46), 6))
    final_slots_html = "".join([f'<div class="slot-box">{str(n).zfill(2)}</div>' for n in final_numbers])
    slot_placeholder.markdown(f'<div class="slot-container">{final_slots_html}</div>', unsafe_allow_html=True)
    
    st.balloons()
    
    # 3. 티켓 6쌍 출력
    st.markdown("<h3 style='text-align:center; color:white;'>🎟️ 당신의 행운 티켓</h3>", unsafe_allow_html=True)
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    for i in range(6):
        nums = sorted(random.sample(range(1, 46), 6))
        num_str = " ".join([str(n).zfill(2) for n in nums])
        st.markdown(f"""
        <div class="ticket">
            <div style="font-weight:bold; border-bottom:1px solid #eee; margin-bottom:10px;">LOTTO LUCKY TICKET #{i+1}</div>
            <div style="font-size:1.6rem; color:#ff4b4b; font-weight:bold; letter-spacing:3px;">{num_str}</div>
            <div style="font-size:0.8rem; color:#999; margin-top:10px;">ISSUED: {now}</div>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.playing = False