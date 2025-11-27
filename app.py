# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="함수 그래프 그리기", layout="centered")

# 페이지 스타일
st.markdown("""
<style>
    .title-box {
        background: linear-gradient(to right, #6C63FF, #968BFF);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 25px;
    }
    .section-box {
        background: #F4F4FF;
        padding: 18px;
        border-radius: 10px;
        margin-top: 20px;
        border-left: 6px solid #6C63FF;
    }
    .result-box {
        background: #F0FFF0;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 제목 박스
st.markdown('<div class="title-box">📈 범용 함수 그래프 그리기</div>', unsafe_allow_html=True)

# 설명 구역
st.markdown("""
<div class="section-box">
    <h4>📘 사용 방법</h4>
    이 웹사이트는 다양한 함수를 입력하면 자동으로 그래프를 그려주는 도구입니다.<br><br>

    <b>✔ 입력 가능한 함수 예시</b><br>
    • 일차: <code>2*x + 3</code><br>
    • 이차: <code>x**2 - 4*x + 1</code><br>
    • 삼차: <code>x**3 - 3*x</code><br>
    • 절댓값: <code>abs(x)</code><br>
    • 지수함수: <code>np.exp(x)</code><br>
    • 로그함수: <code>np.log(x)</code><br>
    • 삼각함수: <code>np.sin(x)</code>, <code>np.cos(x)</code><br>
    • 루트: <code>np.sqrt(x)</code><br><br>

    <b>⚠ 주의</b><br>
    • 로그는 음수에서 정의되지 않으니 <code>x > 0</code> 구간으로 그래프 범위를 설정하세요.<br>
    • <code>x</code>만 변수로 사용해야 합니다.<br>
    • 곱하기는 반드시 <code>*</code> 필요 (예: 2x ❌ → 2*x ⭕)
</div>
""", unsafe_allow_html=True)

# 입력 구역
st.markdown("### ✏ 함수 입력")

func_input = st.text_input("함수식 입력 (x 사용)", "x**2 - 3*x + 2")

col1, col2 = st.columns(2)
with col1:
    x_min = st.number_input("x 최소값", value=-10.0)
with col2:
    x_max = st.number_input("x 최대값", value=10.0)

# 버튼
if st.button("그래프 그리기"):
    try:
        x = np.linspace(x_min, x_max, 500)
        allowed = {
            "x": x,
            "np": np,
            "abs": abs
        }
        y = eval(func_input, {"__builtins__": {}}, allowed)

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"y = {func_input}")

        # 결과 박스
        st.markdown('<div class="result-box"><b>✨ 그래프가 생성되었습니다!</b></div>', unsafe_allow_html=True)
        st.pyplot(plt)

    except Exception as e:
        st.error(f"오류 발생: {e}")