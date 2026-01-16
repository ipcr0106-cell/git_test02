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

# --- CSS: 전구 반짝임 애니메이션 추가 ---
st.markdown("""
<style>
    /* 1. 타이틀 배너: 애니메이션 테두리 */
    .title-banner {
        background: linear-gradient(to right, #b30000, #ff0000);
        border: 6px solid #ffd700;
        border-radius: 50px;
        padding: 20px 30px;
        text-align: center;
        box-shadow: 0 0 20px #ff0000;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    /* 전구 효과를 위한 가상 요소 (점선 테두리가 반짝이는 느낌) */
    .title-banner::before {
        content: '';
        position: absolute;
        top: -10px; left: -10px; right: -10px; bottom: -10px;
        border: 8px dotted #fff; /* 전구 모양을 점선으로 표현 */
        border-radius: 60px;
        opacity: 0.8;
        animation: blink 0.8s infinite; /* 0.8초마다 반짝임 */
    }

    @keyframes blink {
        0% { opacity: 0.2; filter: drop-shadow(0 0 2px #ffd700); }
        50% { opacity: 1; filter: drop-shadow(0 0 15px #fff) drop-shadow(0 0 25px #ffd700); }
        100% { opacity: 0.2; filter: drop-shadow(0 0 2px #ffd700); }
    }

    .title-text {
        color: #ffffff;
        font-family: 'Arial Black', sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.7);
        margin: 0;
        position: relative; /* 전구 위로 텍스트가 오게 설정 */
        z-index: 1;
    }

    /* 2. 전광판 디자인 (기존 유지) */
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
    }

    /* 3. 버튼 디자인 (기존 유지) */
    .stButton>button {
        background: radial-gradient(circle at 30% 30%, #ff4b4b, #800000) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 120px !important;
        height: 120px !important;
        border: 8px solid #ffd700 !important;
        box-shadow: 0px 10px 0px 0px #500000, 0px 15px 30px rgba(0,0,0,0.5) !important;
        display: block !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 구성 ---
st.markdown("""
    <div class="title-banner">
        <p class="title-text">✨ LUCKY JACKPOT ✨</p>
    </div>
    <p style="text-align:center; color:#ddd; font-weight:bold;">WINNER WINNER CHICKEN DINNER!</p>
    """, unsafe_allow_html=True)

# ... (이후 버튼 및 로또 로직은 동일하게 사용하시면 됩니다)

# 전광판 플레이스홀더
slot_placeholder = st.empty()
initial_slots = "".join([f'<div class="slot-box">??</div>' for _ in range(6)])
slot_placeholder.markdown(f'<div class="slot-container">{initial_slots}</div>', unsafe_allow_html=True)

# 레버 버튼
if st.button("PUSH"):
    st.session_state.playing = True

if st.session_state.playing:
    # 잭팟 효과음 (웹 오디오)
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
    st.markdown("<h3 style='text-align:center;'>🎟️ 당신의 행운 티켓</h3>", unsafe_allow_html=True)
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