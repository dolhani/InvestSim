import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Ubuntu에서 NanumGothic 사용)
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # NanumGothic 폰트 경로
try:
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False  # 유니코드 마이너스 대신 ASCII 마이너스 사용
except:
    st.error("NanumGothic 폰트가 설치되어 있지 않습니다. 아래 명령어로 설치하세요:\n`sudo apt-get install -y fonts-nanum`")
    st.stop()

# Streamlit 페이지 설정
st.title("투자 시뮬레이션 그래프 (누적 변화, 로그 스케일)")
st.write("입력 값을 조정하고 '재실행' 버튼으로 시뮬레이션을 다시 실행하세요.")

# 입력 값 받기
success_prob = st.slider("성공 확률 (0~1)", 0.0, 1.0, 0.5, 0.01)
success_multiplier = st.slider("성공 배율 (예: 1.3 = 30% 수익)", 1.0, 2.0, 1.3, 0.01)
failure_multiplier = st.slider("실패 배율 (예: 0.7 = -30% 손실)", 0.0, 1.0, 0.7, 0.01)
leverage = st.slider("레버리지 배율 (0~1)", 0.0, 1.0, 1.0, 0.01)

# 초기 투자금 및 시도 횟수 설정
initial_investment = 1  # 초기 투자금 1로 설정
trials = 10000  # 10,000번 시뮬레이션

# 시뮬레이션 함수
def run_simulation(prob, success_mult, failure_mult, lev, trials, initial):
    balance = [initial]  # 투자금 변화 기록
    current_balance = initial

    # 시뮬레이션 실행
    for _ in range(trials):
        # 투자 금액 (레버리지 적용)
        investment = current_balance * lev

        # 성공/실패 랜덤 결정
        if np.random.random() < prob:
            # 성공 시
            profit = investment * (success_mult - 1)
            current_balance += profit
        else:
            # 실패 시
            loss = investment * (1 - failure_mult)
            current_balance -= loss

        # 결과 기록 (음수 방지)
        current_balance = max(0, current_balance)
        balance.append(current_balance)

    return balance

# 상태 관리: 버튼 클릭 여부 확인
if 'results' not in st.session_state:
    st.session_state.results = run_simulation(success_prob, success_multiplier, failure_multiplier, leverage, trials, initial_investment)

# 재실행 버튼 추가
if st.button("재실행"):
    st.session_state.results = run_simulation(success_prob, success_multiplier, failure_multiplier, leverage, trials, initial_investment)

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(st.session_state.results, label="투자금 변화 (누적)")
plt.axhline(y=initial_investment, color='r', linestyle='--', label="초기 투자금")
plt.yscale('log')  # y축을 로그 스케일로 설정
plt.title(f"10,000번 투자 시뮬레이션 (로그 스케일)\n성공 확률: {success_prob}, 성공 배율: {success_multiplier}, 실패 배율: {failure_multiplier}, 레버리지: {leverage}")
plt.xlabel("시도 횟수")
plt.ylabel("누적 투자금 (로그 스케일)")
plt.legend()
plt.grid(True, which="both", ls="--")  # 로그 스케일에 맞게 그리드 설정

# Streamlit에 그래프 표시
st.pyplot(plt)

# 결과 요약 출력
st.write(f"초기 투자금: {initial_investment}")
st.write(f"최종 투자금: {st.session_state.results[-1]:.2f}")
st.write(f"누적 수익률: {((st.session_state.results[-1] - initial_investment) / initial_investment * 100):.2f}%")
