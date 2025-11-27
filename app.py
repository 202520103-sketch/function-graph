import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Smart Function Grapher", layout="wide")
st.title("Smart Function Grapher")

# 설명 카드
st.markdown("""
<div style="background-color:#e0f7fa; padding:10px; border-radius:10px;">
<b>사용법:</b> 수식을 입력하고 버튼을 눌러 특수 함수 추가 후 '그래프 그리기' 클릭.
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# Session state 초기화
if "func_input" not in st.session_state:
    st.session_state.func_input = "x**2"

# 함수 입력
st.text_input("함수 입력", key="func_input")

# 특수 함수 버튼 가로 정렬
buttons = ["abs()", "exp()", "log()", "sin()", "cos()", "tan()", "초기화"]
cols = st.columns(len(buttons))
for i, btn in enumerate(buttons):
    if cols[i].button(btn):
        if btn == "abs()":
            st.session_state.func_input += " + abs(x)"
        elif btn == "exp()":
            st.session_state.func_input += " + np.exp(x)"
        elif btn == "log()":
            st.session_state.func_input += " + np.log(np.clip(x,1e-6,None))"
        elif btn == "sin()":
            st.session_state.func_input += " + np.sin(x)"
        elif btn == "cos()":
            st.session_state.func_input += " + np.cos(x)"
        elif btn == "tan()":
            st.session_state.func_input += " + np.tan(x)"
        elif btn == "초기화":
            st.session_state.func_input = ""

# 그래프 그리기
if st.button("그래프 그리기"):
    try:
        y = eval(st.session_state.func_input, {"__builtins__": {}}, {"x": x, "np": np, "abs": np.abs, "sin": np.sin, "cos": np.cos, "tan": np.tan})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
        fig.update_layout(title=f"y = {st.session_state.func_input}", xaxis_title="x", yaxis_title="f(x)", template="plotly_white", width=900, height=500)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"오류: {e}")