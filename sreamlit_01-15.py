# venv: 개발자들이 주로 사용하는 가상 환경 도구

import streamlit as st # streamlit 라이브러리 임포트하여 st라는 별칭으로 사용
# 외부로 띄울 수 있게 대쉬보드를 만듦
# pip install --upgrade streamlit  #streamlit 업그레이드 명령어

# flask는 대쉬보드 만들기 어려움
# streamlit은 대쉬보드 쉽게 만들 수 있음

import numpy as np # 숫자 계산
import pandas as pd # 그래프 그리기 # 엑셀 자료를 잘 다룸
from datetime import datetime as dt# 날짜와 시간 다루기
import datetime

st.title("이것은 타이틀") # 대쉬보드 제목 설정
# 대쉬보드 실행할 때는 python 파일명.py가 아닌 streamlit run 파일명.py로 실행해야 함
st.title("스마일: 😀")
st.caption("그림에 대한 설명 캡션을 한번 넣어봤음")
st.markdown("**이성은** *이성은* ~~이성은~~") # 마크다운 문법 사용 가능
st.markdown("**Streamlit**은 한마디로 말하면 **파이썬 코드만으로 웹 앱을 아주 빠르게 만드는 도구**입니다.")
st.markdown(":green[$\sqrt{x^2 + y^2} = 1$] 와 같은 수식도 표현 가능") #$\ 루트표시
st.latex(r'''\sqrt{x^2 + y^2} = 1''') # LaTeX 수식 표현 가능


# 코드 자체를 표시
sample_code = '''
def hello():
    print("Hello, Streamlit!")
'''
st.code(sample_code, language='python') #sample code를 가지고 올 거고 언어는 파이썬

# 마크다운 문법 지원
st.markdown("텍스트의 색상을 :green[초록색]으로, 그리고 **:blue[파란색 볼드체]** 를 설정할 수 있다")

# 수식 표시
st.title("데이터프레임 출력하기")
# dataframe 생성
dataframe = pd.DataFrame(
    {"first column": [1, 2, 3, 4],
    "second column": [10, 20, 30, 40]
    }) #이 데이터로 그래프를 그리겠다
# dataframe 출력
st.dataframe(dataframe) # 대쉬보드에 '데이터프레임'으로 출력하기 # sorting 가능 # 유동적으로 조절 가능
# table 출력
st.table(dataframe) # 대쉬보드에 '테이블'으로 출력하기 # 고정값으로 누구도 고치지 못하게 # sorting 불가능
# metric 출력
st.metric(label="온도", value="25 °C", delta="1.2 °C") # 대쉬보드에 '메트릭'으로 출력하기 # delta는 변화량
st.metric(label="삼성전자", value="140,000원", delta="+100%") # 대쉬보드에 '메트릭'으로 출력하기
# write 출력
st.write(dataframe) # 대쉬보드에 '라이트'로 출력하기

# 컬럼으로 영역 나누어 표기
col1, col2, col3 = st.columns(3) # 3개의 컬럼으로 나누기
col1.metric(label="달러", value="1471원", delta="4.5원") # 첫 번째 컬럼에 메트릭 출력
col2.metric(label="유로", value="1623원", delta="2.3원") # 두 번째 컬럼에 메트릭 출력
col3.metric(label="엔화", value="11원", delta="-0.1원") # 세 번째 컬럼에 메트릭 출력

# 버튼 클릭
button = st.button("현재 시간 표시") # 버튼 생성
if button: # 버튼이 클릭되었을 때
    st.write(":blue[버튼]이 클릭되었습니다!") # 버튼 클릭 메시지 출력
    st.write("현재 시간:", dt.now().strftime("%Y-%m-%d %H:%M:%S")) # 현재 시간 출력

# 체크박스
agree=st.checkbox("체크박스를 눌러주세요") # 체크박스 생성 # 옵션 여러 개 선택 가능
if agree: # 체크박스가 선택되었을 때
    st.write("체크박스가 선택되었습니다!") # 체크박스 선택 메시지 출력

# 라디오 버튼
mbti=st.radio("당신의 MBTI는 무엇인가요?", ("INFP", "INTJ", "ENTJ")  , index=1) # 라디오 버튼 생성 # 옵션 중 하나 선택 가능 # index=1은 체크기본값을 INTJ로 설정
if mbti=="INFP": # INFP가 선택되었을 때
    st.write("당신은 이상주의자입니다!") # INFP 메시지 출력
elif mbti=="INTJ": # INTJ가 선택되었을 때
    st.write("당신은 전략가입니다!") # INTJ 메시지 출력
else: # ENTJ가 선택되었을 때
    st.write("당신은 리더입니다!") # ENTJ 메시지 출력

# 셀렉트 박스
option = st.selectbox("좋아하는 과일을 선택하세요", ("사과", "바나나", "체리")) # 셀렉트 박스 생성
st.write(f"당신이 선택한 과일은: :red[{option}]") # 선택한 과일

# 멀티 셀렉트 박스
options = st.multiselect("좋아하는 색상을 선택하세요", ["빨강", "파랑", "초록", "노랑"]) # 멀티 셀렉트 박스 생성 # 옵션 여러 개 선택 가능
st.write("당신이 선택한 색상은:", options) # 선택한 색상

# 슬라이더
age = st.slider("당신의 나이는?", 0, 120, 25) # 슬라이더 생성 # 최소값 0, 최대값 120, 기본값 25
st.write(f"당신의 나이는: :orange[{age}]세") # 선택한 나이

# 범위 슬라이드
value=st.slider("범위의 값을 다음과 같은 범위로 설정하세요", 0.0, 100.0, (25.0,75.0)) # 슬라이더 생성 # 최소값 0.0, 최대값 100.0, 기본값 (25.0,75.0) 범위
st.write(f"선택한 범위는: :purple[{value}]") # 선택한 범위


# 날짜 선택
date = st.slider("언제 약속을 잡는 것이 좋을까요?", 
                min_value=dt(2026, 1, 1,0,0), 
                max_value=dt(2026, 1, 31,0,0), 
                value=dt(2026, 1, 15,0,0),
                step= datetime.timedelta(hours=1),
                format="YYYY-MM-DD HH:mm")
# 날짜 슬라이더 생성 # 최소값 2026-01-01, 최대값 2026-01-31, 기본값 2026-01-15, step은 하루/시간 단위, format은 날짜 형식
st.write(f"선택한 날짜는: :red[{date}]") # 선택한 날짜


# 텍스트 입력
title=st.text_input(label="가고 싶은 여행지가 있나요?",
                    placeholder="예: 도쿄, 뉴욕, 파리", #예시 미리보기
                    ) # 텍스트 입력 생성
st.write(f"당신이 가고 싶은 여행지는 :green[{title}] 입니다.") # 입력한 여행지

# 숫자 +-입력 버튼
number=st.number_input(label="당신이 좋아하는 숫자는 무엇인가요?",
                        min_value=0,
                        max_value=100,
                        value=50,
                        step=2
                        )
st.write(f"당신이 좋아하는 숫자는 :blue[{number}] 입니다.") # 입력한 숫자

# 파일 다운로드 버튼
st.download_button(
    label="샘플 CSV 파일 다운로드",
    data=dataframe.to_csv(index=False).encode('utf-8'), # dataframe을 CSV로 변환하여 utf-8(유니코드 종류)로 인코딩
    file_name="sample_data.csv", # 다운로드 파일명
    mime="text/csv" # 파일 형식: 텍스트를 CSV로 바꾸기
)