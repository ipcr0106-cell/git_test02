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

# --- CSS: 레버 애니메이션 및 티켓 스타일 ---
st.markdown("""
<style>
    /* 레버 본체와 손잡이 구성 */
    .lever-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    /* 레버 베이스 */
    .lever-base {
        width: 60px;
        height: 100px;
        background: #444;
        border-radius: 10px;
        position: relative;
    }

    /* 레버 막대와 손잡이 애니메이션 */
    @keyframes pull-lever {
        0% { transform: rotateX(0deg); }
        50% { transform: rotateX(60deg); }
        100% { transform: rotateX(0deg); }
    }

    .lever-active {
        animation: pull-lever 0.5s ease-in-out;
    }

    /* 티켓 스타일 */
    .ticket {
        background: white;
        border: 2px dashed #bbb;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        font-family: monospace;
    }
    .ticket-num {
        font-size: 1.4rem;
        font-weight: bold;
        color: #e63946;
    }

    /* 슬롯 숫자 스타일 */
    .slot-machine {
        background: #222;
        color: #f1c40f;
        font-size: 2.5rem;
        font-weight: bold;
        padding: 10px;
        border-radius: 10px;
        border: 4px solid #f39c12;
        text-align: center;
        margin-bottom: 20px;
        min-height: 80px;
    }
</style>
""", unsafe_allow_html=True)

# --- 오디오 재생 함수 ---
def play_audio():
    AUDIO_URL = "https://www.myinstants.com/media/sounds/jackpot.mp3"
    st.components.v1.html(f'<audio autoplay><source src="{AUDIO_URL}" type="audio/mp3"></audio>', height=0)

# --- 메인 화면 ---
st.title("🎰 REAL JACKPOT LOTTO")

# 세션 상태 초기화 (애니메이션 제어)
if 'playing' not in st.session_state:
    st.session_state.playing = False

# 슬롯 전광판
slot_placeholder = st.empty()
slot_placeholder.markdown('<div class="slot-machine">00 00 00 00 00 00</div>', unsafe_allow_html=True)

# 레버 구현 (진짜 레버처럼 보이게 하기 위해 버튼 스타일링)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # 레버 막대기를 형상화한 버튼
    st.write("🔽 PULL LEVER")
    if st.button("🔴", key="lever_btn"):
        st.session_state.playing = True
        play_audio()

# 잭팟 로직 실행
if st.session_state.playing:
    # 1. 숫자가 휘리릭 돌아가는 연출
    for _ in range(15):
        random_nums = " ".join([str(random.randint(1, 45)).zfill(2) for _ in range(6)])
        slot_placeholder.markdown(f'<div class="slot-machine">{random_nums}</div>', unsafe_allow_html=True)
        time.sleep(0.08)
    
    # 2. 결과값 확정
    final_numbers = sorted(random.sample(range(1, 46), 6))
    final_str = " ".join([str(n).zfill(2) for n in final_numbers])
    slot_placeholder.markdown(f'<div class="slot-machine" style="color:#ffffff;">{final_str}</div>', unsafe_allow_html=True)
    
    st.balloons()
    
    # 3. 6쌍의 영수증 티켓 출력
    st.markdown("### 🎟️ YOUR TICKETS")
    cols = st.columns(1) # 모바일 최적화를 위해 한 줄로
    for i in range(6):
        nums = sorted(random.sample(range(1, 46), 6))
        num_display = "  ".join([str(n).zfill(2) for n in nums])
        st.markdown(f"""
        <div class="ticket">
            <div style="font-size:0.8rem; color:gray;">LOTTO 6/45 - LUCKY NO.{i+1}</div>
            <div class="ticket-num">{num_display}</div>
            <div style="font-size:0.7rem; color:silver;">{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state.playing = False # 상태 초기화