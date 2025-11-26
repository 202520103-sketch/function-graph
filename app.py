# streamlit_function_plotter.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="함수 그래프 그리기", layout="centered")

st.title("📈 함수 그래프 그리기")
st.markdown("""
원하는 함수를 입력하면 그래프로 그려줍니다.  
예시 입력:  
- 일차 함수: 2*x + 3  
- 이차 함수: x**2 - 4*x + 5  
- 삼차 함수: x**3 - 6*x**2 + 11*x - 6
""")

# 사용자 입력
func_input = st.text_input("함수 입력 (x 변수 사용)", "x**2")
x_min = st.number_input("x 최소값", value=-10.0)
x_max = st.number_input("x 최대값", value=10.0)

if st.button("그래프 그리기"):
    try:
        x = np.linspace(x_min, x_max, 500)
        # 안전하게 eval 사용: locals()에 x만 제공
        y = eval(func_input, {"__builtins__": {}}, {"x": x, "np": np})
        
        # 그래프 그리기
        plt.figure(figsize=(8,5))
        plt.plot(x, y, label=f"y = {func_input}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("함수 그래프")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"오류 발생: {e}")
