import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Smart Function Grapher", layout="wide")
st.title("Smart Function Grapher")

# 설명 카드
st.markdown("""
<div style="background-color:#e0f7fa; padding:10px; border-radius:10px;">
<b>사용법:</b><br>
1. x 범위를 설정하세요.<br>
2. 수식을 입력하거나 버튼 클릭으로 특수 함수 추가.<br>
3. '그래프 그리기' 클릭 → 그래프 확인.<br>
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# Session State 초기화
if "func_input" not in st.session_state:
    st.session_state["func_input"] = "x**2"

# 수식 입력
st.session_state["func_input"] = st.text_input("함수 입력", st.session_state["func_input"])

# 버튼 클릭 시 함수 삽입
def add_func(fstr):
    current = st.session_state["func_input"]
    st.session_state["func_input"] = current + " + " + fstr

# 버튼 가로 정렬
buttons = [("abs()", "abs(x)"), ("exp()", "np.exp(x)"), ("log()", "np.log(np.clip(x,1e-6,None))"),
           ("sin()", "np.sin(x)"), ("cos()", "np.cos(x)"), ("tan()", "np.tan(x)"), ("초기화", "RESET")]

cols = st.columns(len(buttons))
for i, (label, fstr) in enumerate(buttons):
    if cols[i].button(label):
        if fstr == "RESET":
            st.session_state["func_input"] = ""
        else:
            add_func(fstr)

# 그래프 그리기
if st.button("그래프 그리기"):
    try:
        y = eval(
            st.session_state["func_input"],
            {"__builtins__": {}},
            {"x": x, "np": np, "abs": np.abs, "sin": np.sin, "cos": np.cos, "tan": np.tan}
        )
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
        fig.update_layout(
            title=f"y = {st.session_state['func_input']}",
            xaxis_title="x",
            yaxis_title="f(x)",
            template="plotly_white",
            width=900, height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"오류: {e}")