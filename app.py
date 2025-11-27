import streamlit as st
import numpy as np
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="🎨 Easy & Fun Function Grapher", layout="wide")
st.markdown("""
<style>
.stApp { background-color: #f0f8ff; font-family: 'Segoe UI', sans-serif; }
.stButton>button { font-size:16px; padding:8px 12px; border-radius:8px; margin:3px; }
.stTextInput>div>div>input { font-size:16px; padding:5px; border-radius:5px; border:1px solid #ccc;}
</style>
""", unsafe_allow_html=True)

st.title("🎨 Easy & Fun Function Grapher")

# 안내 카드
st.markdown("""
<div style="background: linear-gradient(90deg, #a1c4fd, #c2e9fb); padding:20px; border-radius:15px; color:#000;">
<h3>📌 사용법 안내</h3>
<ol>
<li>🔢 x 범위를 설정하세요 (예: 최소 -10, 최대 10)</li>
<li>✍️ 함수 입력창에 원하는 수식을 입력하세요 (예: x**2 + 3*x + 2)</li>
<li>🎯 아래 추천 수식 버튼을 클릭하면 예시 수식이 표시됩니다</li>
<li>📋 필요하면 '복사' 버튼 클릭 → 입력창에 붙여넣기</li>
<li>📈 '그래프 그리기' 클릭 → 함수 그래프 확인</li>
</ol>
</div>
""", unsafe_allow_html=True)

# x 범위 입력
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력
func_input = st.text_input("함수 입력 ✍️", "x**2")

# 추천 수식 버튼 + 컬러/이모티콘
st.markdown("### 🎁 추천 수식 버튼 (클릭 → 아래 코드 확인 → 복사 가능)")
buttons = [
    ("🟢 절댓값", "abs(x)"),
    ("🟡 지수", "np.exp(x)"),
    ("🟠 로그", "np.log(np.clip(x,1e-6,None))"),
    ("🔵 sin(x)", "np.sin(x)"),
    ("🟣 cos(x)", "np.cos(x)"),
    ("🟤 tan(x)", "np.tan(x)"),
    ("🌟 sin(pi/2 예시)", "np.sin(np.pi/2)")
]
cols = st.columns(len(buttons))
for i, (label, code) in enumerate(buttons):
    with cols[i]:
        st.write(label)
        st.code(code)
        # Streamlit 복사 기능 없음 → 사용자가 직접 복사 가능하도록 안내
        st.caption("📋 코드 복사 → 입력창에 붙여넣기")

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