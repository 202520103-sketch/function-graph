import streamlit as st
import numpy as np
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="Smart Function Grapher", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background-color: #f5f7fa; font-family: 'Segoe UI', sans-serif;}
    .stButton>button { background-color: #4CAF50; color:white; font-size:16px; padding:8px 16px; border-radius:5px; margin:3px;}
    .stTextInput>div>div>input { font-size:16px; padding:5px; border-radius:5px; border:1px solid #ccc;}
    </style>
    """, unsafe_allow_html=True
)

# 제목
st.title("Smart Function Grapher")
st.markdown("""
<div style="background-color:#e0f7fa; padding:15px; border-radius:10px;">
<b>사용법:</b><br>
1. x 범위를 설정하세요.<br>
2. 함수 입력창에 기본 수식을 입력하거나, 버튼 클릭으로 특수 함수를 추가하세요.<br>
3. '그래프 그리기' 버튼 클릭 → 그래프 확인.<br>
<br>
<b>특수 함수 버튼</b>: 절댓값, 지수, 로그, 사인, 코사인, 탄젠트 등
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력
func_input = st.text_input("함수 입력 (예: x**2 + 2*x + 1)", "x**2")

# 특수 함수 버튼
col_abs, col_exp, col_log, col_sin, col_cos, col_tan, col_reset = st.columns(7)
if col_abs.button("abs()"): func_input += " + abs(x)"
if col_exp.button("exp()"): func_input += " + np.exp(x)"
if col_log.button("log()"): func_input += " + np.log(np.clip(x, 1e-6, None))"
if col_sin.button("sin()"): func_input += " + np.sin(x)"
if col_cos.button("cos()"): func_input += " + np.cos(x)"
if col_tan.button("tan()"): func_input += " + np.tan(x)"
if col_reset.button("초기화"): func_input = ""

# 그래프 그리기
if st.button("그래프 그리기"):
    try:
        y = eval(func_input, {"__builtins__": {}}, {"x": x, "np": np, "abs": np.abs, "sin": np.sin, "cos": np.cos, "tan": np.tan})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
        fig.update_layout(
            title=f"y = {func_input}",
            xaxis_title="x",
            yaxis_title="f(x)",
            template="plotly_white",
            width=900, height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"오류: {e}")