import streamlit as st
import numpy as np
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="Interactive Function Grapher", layout="wide")
st.title("Interactive Function Grapher")

# 설명 카드
st.markdown("""
<div style="background-color:#e0f7fa; padding:15px; border-radius:10px;">
<b>사용법 안내</b><br>
1. x 범위를 설정하세요.<br>
2. 함수 입력창에 수식을 직접 입력할 수 있습니다. (예: x**2 + 2*x + 1)<br>
3. 특수 함수 버튼 클릭 시 입력창에 자동 삽입됩니다.<br>
4. 필요 시 초기화 버튼으로 수식을 지우세요.<br>
5. '그래프 그리기' 버튼 클릭 → 그래프 확인.<br>
<br>
<b>특수 함수 버튼</b>: abs(x), np.exp(x), np.log(x)
</div>
""", unsafe_allow_html=True)

# x 범위 입력
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 수식 입력 및 특수 함수 삽입
func_input = st.text_input("함수 입력 (x 사용, 예: x**2 + 2*x + 1)", "x**2")

col_abs, col_exp, col_log, col_reset = st.columns(4)
if col_abs.button("abs(x)"):
    func_input += " + abs(x)"
if col_exp.button("exp(x)"):
    func_input += " + np.exp(x)"
if col_log.button("log(x)"):
    func_input += " + np.log(x)"
if col_reset.button("초기화"):
    func_input = ""

# 그래프 버튼
if st.button("그래프 그리기"):
    try:
        y = eval(func_input, {"__builtins__": {}}, {"x": x, "np": np, "abs": np.abs})
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