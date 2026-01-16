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

# --- CSS: 입체적인 3D 버튼 및 애니메이션 ---
st.markdown("""
<style>
    /* 3D 스타트 버튼 디자인 */
    .stButton>button {
        background: radial-gradient(circle at 30% 30%, #ff4b4b, #b30000);
        color: white;
        border-radius: 50%; /* 완전 원형 */
        width: 120px !important;
        height: 120px !important;
        border: 6px solid #333;
        font-size: 20px !important;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        box-shadow: 0px 10px 0px 0px #800000, 0px 15px 25px rgba(0,0,0,0.4);
        transition: all 0.1s;
        margin: 20px auto;
        display: block;
    }

    /* 버튼 클릭 시 (레버를 내리는 물리적 효과) */
    .stButton>button:active {
        transform: translateY(8px);
        box-shadow: 0px 2px 0px 0px #800000, 0px 5px 10px rgba(0,0,0,0.4);
    }

    /* 슬롯 전광판 스타일 */
    .slot-machine {
        background: #000;
        color: #00ff00; /* 레트로 터미널 느낌의 초록색 또는 황금색 */
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.5rem;
        padding: 20px;
        border-radius: 15px;
        border: 5px double #555;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: inset 0px 0px 20px rgba(0,255,0,0.2);
    }

    /* 티켓 스타일 */
    .ticket {
        background: #fffef0;
        border-left: 10px solid #ff4b4b;
        border-right: 2px solid #ddd;
        border-top: 2px solid #ddd;
        border-bottom: 2px solid #ddd;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0 10px 10px 0;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- 오디오 재생 함수 ---
def play_audio():
    # 잭팟/코인 투입 소리 등
    AUDIO_URL = "https://www.myinstants.com/media/sounds/jackpot.mp3"
    st.components.v1.html(f'<audio autoplay><source src="{AUDIO_URL}" type="audio/mp3"></audio>', height=0)

# --- 메인 화면 ---
st.title("🎰 LUCKY SLOT MACHINE")
st.write("<p style='text-align:center;'>행운의 버튼을 꾹 눌러주세요!</p>", unsafe_allow_html=True)

# 세션 상태 초기화
if 'playing' not in st.session_state:
    st.session_state.playing = False

# 슬롯 표시 (placeholder)
slot_placeholder = st.empty()
slot_placeholder.markdown('<div class="slot-machine">?? ?? ?? ?? ?? ??</div>', unsafe_allow_html=True)

# 버튼 배치
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # 텍스트를 버튼 안에 넣기 위해 label을 "PUSH"로 설정
    if st.button("PUSH"):
        st.session_state.playing = True
        play_audio()

# 잭팟 실행 로직
if st.session_state.playing:
    # 1. 롤링 애니메이션
    for _ in range(12):
        temp_nums = " ".join([str(random.randint(1, 45)).zfill(2) for _ in range(6)])
        slot_placeholder.markdown(f'<div class="slot-machine">{temp_nums}</div>', unsafe_allow_html=True)
        time.sleep(0.1)
    
    # 2. 결과 확정
    final_numbers = sorted(random.sample(range(1, 46), 6))
    final_str = " ".join([str(n).zfill(2) for n in final_numbers])
    slot_placeholder.markdown(f'<div class="slot-machine" style="color:#ffd700; border-color:#ffd700;">{final_str}</div>', unsafe_allow_html=True)
    
    st.balloons()

    # 3. 티켓 출력
    st.markdown("### 🎟️ 오늘의 행운 번호")
    for i in range(6):
        set_nums = sorted(random.sample(range(1, 46), 6))
        num_display = " ".join([str(n).zfill(2) for n in set_nums])
        st.markdown(f"""
            <div class="ticket">
                <small>GAME {i+1}</small><br>
                <strong style="font-size: 1.5rem; color: #333;">{num_display}</strong><br>
                <small style="color: #999;">{datetime.datetime.now().strftime('%Y/%m/%d %H:%M')}</small>
            </div>
        """, unsafe_allow_html=True)
    
    st.session_state.playing = False