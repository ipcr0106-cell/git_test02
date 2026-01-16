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

# --- CSS: 명암과 체이싱 애니메이션 강화 ---
st.markdown("""
<style>
    /* 전체 배경색 조정 */
    .stApp {
        background-color: #0e1117;
    }

    /* 1. 타이틀 전광판 본체: 입체감 있는 명암 추가 */
    .casino-marquee {
        background: linear-gradient(145deg, #d20000, #8b0000); /* 입체적인 레드 그라데이션 */
        border: 4px solid #222; 
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        /* 외부 그림자와 내부 광원 효과로 입체감 부여 */
        box-shadow: 
            0 20px 50px rgba(0,0,0,0.8), 
            inset 5px 5px 15px rgba(255,255,255,0.2), 
            inset -5px -5px 15px rgba(0,0,0,0.5);
        position: relative;
        margin-bottom: 40px;
    }

    /* 전구 스타일: 전구 소켓 느낌 추가 */
    .bulb {
        position: absolute;
        width: 14px;
        height: 14px;
        background-color: #333;
        border-radius: 50%;
        z-index: 10;
        border: 1px solid #111;
    }

    /* 엇갈림 깜빡임 (Chasing) 애니메이션 */
    /* 홀수 전구: 켜진 상태로 시작 */
    .bulb:nth-child(odd) { 
        animation: chase-1 0.8s infinite step-end; 
    }
    /* 짝수 전구: 꺼진 상태로 시작 (0.4초 뒤에 켜짐) */
    .bulb:nth-child(even) { 
        animation: chase-2 0.8s infinite step-end; 
    }

    @keyframes chase-1 {
        0%, 100% { background-color: #ffcc00; box-shadow: 0 0 20px #ffcc00, 0 0 35px #ff9900; }
        50% { background-color: #444; box-shadow: none; }
    }

    @keyframes chase-2 {
        0%, 100% { background-color: #444; box-shadow: none; }
        50% { background-color: #ffcc00; box-shadow: 0 0 20px #ffcc00, 0 0 35px #ff9900; }
    }

    /* 글씨 디자인: 금색 메탈릭 + 네온 효과 */
    .title-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(to bottom, #fff3ad 0%, #ffcc00 50%, #b38600 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 10px rgba(255, 204, 0, 0.5));
        text-transform: uppercase;
        letter-spacing: -1px;
    }

    /* 2. 전광판 숫자 박스 (기존 디자인 유지 및 명암 강화) */
    .slot-container {
        background: #000 !important;
        border-radius: 20px !important;
        padding: 30px 10px !important;
        display: flex !important;
        box-shadow: inset 0 0 20px #000, 0 5px 15px rgba(255,255,255,0.05) !important;
        margin-bottom: 30px !important;
    }
    .slot-box {
        flex: 1 !important;
        color: #f6e05e !important;
        font-size: 3rem !important;
        font-weight: bold !important;
        text-shadow: 0 0 20px #f6e05e !important;
        border-right: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 구성 ---

# 전구 위치 계산 루프 (더 촘촘하게 배치)
bulbs_html = ""
# 상단/하단
for i in range(0, 101, 6):
    bulbs_html += f'<div class="bulb" style="top: 8px; left: {i}%;"></div>'
    bulbs_html += f'<div class="bulb" style="bottom: 8px; left: {i}%;"></div>'
# 좌측/우측
for i in range(12, 89, 15):
    bulbs_html += f'<div class="bulb" style="left: 8px; top: {i}%;"></div>'
    bulbs_html += f'<div class="bulb" style="right: 8px; top: {i}%;"></div>'

st.markdown(f"""
    <div class="casino-marquee">
        {bulbs_html}
        <h1 class="title-text">LUCKY JACKPOT</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 로직 (기존 기능 통합) ---
if 'playing' not in st.session_state:
    st.session_state.playing = False

slot_placeholder = st.empty()
initial_slots = "".join([f'<div class="slot-box">??</div>' for _ in range(6)])
slot_placeholder.markdown(f'<div class="slot-container">{initial_slots}</div>', unsafe_allow_html=True)

if st.button("🎰 SPIN THE LEVER"):
    st.session_state.playing = True

if st.session_state.playing:
    # 롤링 애니메이션
    for _ in range(15):
        temp_nums = [str(random.randint(1, 45)).zfill(2) for _ in range(6)]
        slots_html = "".join([f'<div class="slot-box">{n}</div>' for n in temp_nums])
        slot_placeholder.markdown(f'<div class="slot-container">{slots_html}</div>', unsafe_allow_html=True)
        time.sleep(0.08)
    
    final_numbers = sorted(random.sample(range(1, 46), 6))
    final_slots_html = "".join([f'<div class="slot-box">{str(n).zfill(2)}</div>' for n in final_numbers])
    slot_placeholder.markdown(f'<div class="slot-container">{final_slots_html}</div>', unsafe_allow_html=True)
    st.balloons()
    st.session_state.playing = False