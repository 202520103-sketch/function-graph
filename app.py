import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="🌈 Easy Function Grapher", layout="wide")
st.title("🌈 Easy Function Grapher")

# 안내 카드
st.markdown("""
<div style="background: linear-gradient(90deg,#a1c4fd,#c2e9fb); padding:20px; border-radius:15px;">
<h3>📌 사용법 안내</h3>
<ol>
<li>🔢 x 범위를 설정하세요 (예: 최소 -10, 최대 10)</li>
<li>✍️ 함수 입력창에 수식을 입력하세요 (예: x**2 + 3*x + 2)</li>
<li>🎯 아래 추천 수식 버튼을 클릭하면 예시 수식과 입력 방법을 확인할 수 있습니다</li>
<li>📋 해당 예시를 참고하여 입력창에 붙여넣기 → '그래프 그리기' 클릭</li>
</ol>
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력창
func_input = st.text_input("함수 입력 ✍️", "x**2")

# 추천 수식 버튼 + 예시 표시
st.markdown("### 🎁 추천 수식 버튼 (클릭 → 예시 확인)")
buttons = [
    ("🟢 절댓값", "abs(x)", "예: abs(x-3)"),
    ("🟡 지수", "np.exp(x)", "예: np.exp(x)"),
    ("🟠 로그", "np.log(np.clip(x,1e-6,None))", "예: np.log(x+1)"),
    ("🔵 sin(x)", "np.sin(x)", "예: np.sin(x) or np.sin(np.pi*x)"),
    ("🟣 cos(x)", "np.cos(x)", "예: np.cos(x) or np.cos(np.pi*x)"),
    ("🟤 tan(x)", "np.tan(x)", "예: np.tan(x)"),
]
cols = st.columns(len(buttons))
for i, (label, code, example) in enumerate(buttons):
    with cols[i]:
        if st.button(label):
            st.code(code)
            st.caption(example)

# 그래프 그리기
if st.button("📈 그래프 그리기"):
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
        st.error(f"⚠️ 오류: {e}")