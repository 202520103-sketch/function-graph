import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Smart Function Grapher", layout="wide")
st.title("Smart Function Grapher")

st.markdown("""
<div style="background-color:#e0f7fa; padding:10px; border-radius:10px;">
<b>사용법:</b><br>
- x 범위 설정 → 수식 입력 → '그래프 그리기' 클릭<br>
- 버튼 클릭 → 추천 수식 표시 → 필요하면 복사해서 입력창에 붙여넣기
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력
func_input = st.text_input("함수 입력", "x**2")

# 추천 수식 버튼
st.markdown("**추천 수식 버튼 (클릭 → 복사해서 입력)**")
buttons = [("절댓값", "abs(x)"), ("지수", "np.exp(x)"), ("로그", "np.log(np.clip(x,1e-6,None))"),
           ("sin", "np.sin(x)"), ("cos", "np.cos(x)"), ("tan", "np.tan(x)")]
cols = st.columns(len(buttons))

for i, (label, val) in enumerate(buttons):
    if cols[i].button(label):
        st.code(val)

# 그래프 그리기
if st.button("그래프 그리기"):
    try:
        y = eval(func_input, {"__builtins__": {}}, {"x": x, "np": np, "abs": np.abs, "sin": np.sin, "cos": np.cos, "tan": np.tan})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
        fig.update_layout(title=f"y = {func_input}", xaxis_title="x", yaxis_title="f(x)", template="plotly_white", width=900, height=500)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"오류: {e}")