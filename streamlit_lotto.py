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

# --- CSS: 디자인 스타일 시트 ---
st.markdown("""
<style>
    /* 1. 슬롯 전광판 배경 (이미지 재현) */
    .slot-container {
        background-color: #1a1a1a !important;
        border-radius: 20px !important;
        padding: 20px 10px !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        align-items: center !important;
        border: 3px solid #333 !important;
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.8) !important;
        margin: 20px 0px !important;
        width: 100% !important;
    }

    /* 2. 개별 숫자 박스 및 구분선 */
    .slot-box {
        flex: 1 !important;
        text-align: center !important;
        font-family: 'Arial Black', sans-serif !important;
        font-size: 2.2rem !important;
        color: #f6e05e !important; /* 이미지의 노란색 */
        text-shadow: 0 0 10px rgba(246, 224, 94, 0.9), 0 0 20px rgba(246, 224, 94, 0.4) !important;
        border-right: 1px solid #444 !important;
    }

    .slot-box:last-child {
        border-right: none !important;
    }

    /* 3. 3D 푸시 버튼 */
    .stButton>button {
        background: radial-gradient(circle at 30% 30%, #ff4b4b, #b30000) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 100px !important;
        height: 100px !important;
        border: 4px solid #333 !important;
        font-weight: bold !important;
        box-shadow: 0px 8px 0px 0px #800000, 0px 10px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.1s !important;
        display: block !important;
        margin: 0 auto !important;
    }

    .stButton>button:active {
        transform: translateY(6px) !important;
        box-shadow: 0px 2px 0px 0px #800000, 0px 5px 10px rgba(0,0,0,0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 로직 ---
st.title("🎰 LUCKY JACKPOT")

if 'playing' not in st.session_state:
    st.session_state.playing = False

# 초기 전광판 모습
slot_placeholder = st.empty()
initial_slots = "".join([f'<div class="slot-box">??</div>' for _ in range(6)])
slot_placeholder.markdown(f'<div class="slot-container">{initial_slots}</div>', unsafe_allow_html=True)

# 버튼 (레버)
if st.button("PUSH"):
    st.session_state.playing = True

if st.session_state.playing:
    # 잭팟 효과음 재생 (선택사항)
    # st.components.v1.html('<audio autoplay><source src="https://www.myinstants.com/media/sounds/jackpot.mp3"></audio>', height=0)

    # 1. 숫자가 휘리릭 돌아가는 연출
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
    
    # 3. 티켓 출력 로직 (생략되지 않도록 유지)
    st.markdown("### 🎟️ YOUR TICKETS")
    for i in range(6):
        nums = sorted(random.sample(range(1, 46), 6))
        num_str = " ".join([str(n).zfill(2) for n in nums])
        st.markdown(f'<div style="background:#fff; border:1px dashed #ccc; padding:15px; margin-bottom:10px; border-radius:10px; text-align:center; font-family:monospace;"><b>TICKET #{i+1}</b><br><span style="font-size:1.5rem; color:#ff4b4b;">{num_str}</span></div>', unsafe_allow_html=True)

    st.session_state.playing = False