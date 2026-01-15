# 로또 번호를 대쉬보드에 띄우기
from numpy import number
import streamlit as st
import random # 랜덤 숫자 생성 라이브러리
st.title("로또 번호 생성기") # 대쉬보드 제목 설정
st.markdown("버튼을 클릭하면 로또 번호 6개가 생성됩니다.")

# 로또 번호 생성 함수
def generate_lotto_numbers():
    numbers = set() # 중복 없는 숫자 생성을 위해 집합 사용
    while len(numbers) < 6: # 6개의 숫자가 모일 때까지 반복
        numbers.add(random.randrange(1, 46)) # 1부터 45까지의 숫자 중 랜덤 선택
    return numbers # 생성된 숫자 집합 반환

import datetime
# 버튼 클릭 시 로또 번호 생성
botton=st.button("로또 번호 생성")
if botton:
    for i in range(1, 6):
        st.subheader(f"{i}번째 추천 로또 번호:{generate_lotto_numbers()}")
        # 5세트의 로또 번호 생성
        st.write(f"생성된 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") # 생성된 시각 표시