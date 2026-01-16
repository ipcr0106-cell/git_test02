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

st.set_page_config(page_title="리얼 잭팟 머신", page_icon="🎰", layout="centered")

# --- CSS: 머신 본체 명암 및 레버 애니메이션 ---
st.markdown("""
<style>
    /* 배경: 금속 느낌의 회색 질감 */
    .stApp {
        background: radial-gradient(circle, #4a4a4a 0%, #1a1a1a 100%);
    }

    /* 잭팟 머신 본체 프레임 */
    .machine-body {
        background: linear-gradient(145deg, #8e8e8e, #4a4a4a);
        border: 10px solid #222;
        border-radius: 30px;
        padding: 40px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.8), inset 0 0 20px rgba(255,255,255,0.2);
        position: relative;
        margin-top: 20px;
    }

    /* 타이틀 배너: 입체감 강화 */
    .title-banner {
        background: linear-gradient(to bottom, #d30000, #800000);
        border: 4px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5), inset 0 0 15px rgba(255,215,0,0.3);
        position: relative;
        margin-bottom: 30px;
    }

    /* 금색 입체 텍스트 */
    .title-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(to bottom, #fff3ad 0%, #ffcc00 50%, #b38600 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(3px 5px 2px rgba(0,0,0,0.8));
    }

    .bulb {
        position: absolute; width: 10px; height: 10px;
        background-color: #fff; border-radius: 50%; z-index: 10;
        animation: bulb-flash 0.5s infinite alternate;
    }
    @keyframes bulb-flash {
        0% { background-color: #444; box-shadow: none; }
        100% { background-color: #ffcc00; box-shadow: 0 0 15px #ffcc00; }
    }

    /* 전광판: 깊이감 있는 블랙 홀 */
    .slot-container {
        background-color: #000 !important;
        border: 8px solid #333 !important;
        border-radius: 15px !important;
        padding: 40px 10px !important;
        display: flex !important;
        box-shadow: inset 0 15px 30px rgba(0,0,0,1), 0 5px 15px rgba(255,255,255,0.1) !important;
    }
    .slot-box {
        flex: 1; text-align: center; font-size: 4rem; font-weight: bold;
        color: #ffcc00; text-shadow: 0 0 20px #ffcc00; font-family: 'Courier New', monospace;
    }

    /* --- 레버(Lever) 디자인 및 애니메이션 --- */
    .lever-container {
        position: absolute;
        right: -80px; top: 150px;
        width: 60px; height: 200px;
        cursor: pointer;
    }
    .lever-base {
        width: 20px; height: 120px; background: #333;
        margin: 0 auto; border-radius: 10px; position: relative;
        transform-origin: bottom center;
        transition: transform 0.3s cubic-bezier(.47,1.64,.41,.8);
    }
    .lever-knob {
        width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #ff4b4b, #800000);
        border-radius: 50%; border: 4px solid #ffd700;
        position: absolute; top: -40px; left: -15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .click-label {
        position: absolute; top: -70px; left: -10px;
        color: #fff; font-size: 0.8rem; font-weight: bold;
        animation: bounce 1s infinite;
    }
    @keyframes bounce { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-5px);} }

    /* 클릭 시 레버가 내려가는 효과 */
    .lever-container:active .lever-base {
        transform: rotateX(60deg) scaleY(0.5);
    }

    /* 티켓 디자인 */
    .ticket {
        background: #fff; border: 2px dashed #999; padding: 20px;
        margin-top: 20px; text-align: center; border-radius: 5px;
        font-family: monospace; box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'playing' not in st.session_state:
    st.session_state.playing = False

# --- 머신 렌더링 ---
st.write("") # 상단 여백
st.markdown('<div class="machine-body">', unsafe_allow_html=True)

# 1. 타이틀 전광판
bulbs_html = "".join([f'<div class="bulb" style="top:-5px; left:{i}%;"></div>' for i in range(0, 101, 8)])
bulbs_html += "".join([f'<div class="bulb" style="bottom:-5px; left:{i}%;"></div>' for i in range(0, 101, 8)])
st.markdown(f"""
    <div class="title-banner">
        {bulbs_html}
        <p class="title-text">LUCKY JACKPOT</p>
    </div>
""", unsafe_allow_html=True)

# 2. 숫자 전광판
slot_placeholder = st.empty()
initial_slots = "".join(['<div class="slot-box">?</div>' for _ in range(6)])
slot_placeholder.markdown(f'<div class="slot-container">{initial_slots}</div>', unsafe_allow_html=True)

# 3. 레버 (HTML/CSS 레버) - 클릭 시 버튼 이벤트를 트리거하기 위해 hidden button 사용
if not st.session_state.playing:
    st.markdown("""
        <div class="lever-container">
            <div class="click-label">CLICK!</div>
            <div class="lever-base">
                <div class="lever-knob"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 레버를 누르는 것과 동일한 효과를 위해 투명 버튼 배치
    if st.button("레버 당기기", use_container_width=True):
        st.session_state.playing = True
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True) # 머신 바디 끝

# --- 실행 로직 ---
if st.session_state.playing:
    # 1. 롤링 애니메이션
    for i in range(20):
        temp_nums = [str(random.randint(0, 9)) for _ in range(6)]
        slots_html = "".join([f'<div class="slot-box">{n}</div>' for n in temp_nums])
        slot_placeholder.markdown(f'<div class="slot-container">{slots_html}</div>', unsafe_allow_html=True)
        time.sleep(0.05 + (i * 0.01)) # 점점 느려지게
    
    # 2. 777777 잭팟 확정 연출
    st.components.v1.html('<audio autoplay><source src="https://www.myinstants.com/media/sounds/jackpot.mp3"></audio>', height=0)
    final_slots_html = "".join(['<div class="slot-box" style="color:#ff0000; font-size:5rem;">7</div>' for _ in range(6)])
    slot_placeholder.markdown(f'<div class="slot-container">{final_slots_html}</div>', unsafe_allow_html=True)
    
    st.balloons()
    st.snow()
    
    # 3. 결과 티켓 출력
    st.markdown("<h2 style='text-align:center; color:white; margin-top:50px;'>🎉 JACKPOT TICKETS 🎉</h2>", unsafe_allow_html=True)
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    cols = st.columns(2)
    for i in range(6):
        nums = sorted(random.sample(range(1, 46), 6))
        num_str = " ".join([str(n).zfill(2) for n in nums])
        with cols[i % 2]:
            st.markdown(f"""
            <div class="ticket">
                <div style="color:#800000; font-weight:bold; border-bottom:1px solid #ccc;">777 LUCKY TICKET</div>
                <div style="font-size:1.5rem; color:#d30000; padding:10px 0;">{num_str}</div>
                <div style="font-size:0.7rem; color:#666;">DATE: {now}</div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("RESET MACHINE"):
        st.session_state.playing = False
        st.rerun()