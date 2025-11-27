import streamlit as st
import numpy as np
import plotly.graph_objs as go
import re

st.set_page_config(page_title="🎨 Simple & Fun Grapher", layout="wide")

# 페이지 스타일
st.markdown("""
<style>
.stApp { background-color: #f0f8ff; font-family: 'Segoe UI', sans-serif; }
.stButton>button { font-size:16px; padding:8px 12px; border-radius:8px; margin:5px; background:linear-gradient(90deg,#a1c4fd,#c2e9fb); color:#000; }
.stTextInput>div>div>input { font-size:16px; padding:5px; border-radius:5px; border:1px solid #ccc;}
</style>
""", unsafe_allow_html=True)

st.title("🎨 Simple & Fun Function Grapher")

# 안내 카드
st.markdown("""
<div style="background: linear-gradient(90deg,#ffecd2,#fcb69f); padding:20px; border-radius:15px;">
<h3>📌 사용법 안내</h3>
<ol>
<li>🔢 x 최소/최대 범위를 설정하세요.</li>
<li>✍️ 함수 입력창에 간단히 입력하세요 (예: sin(x), log(x+1), exp(x), abs(x-3), x**2, pi*x)</li>
<li>📈 '그래프 그리기' 버튼 클릭 → 바로 함수 그래프 확인</li>
<li>💡 삼각함수, 지수, 로그, 절댓값, π 모두 지원</li>
</ol>
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력
func_input = st.text_input("함수 입력 ✍️", "x**2")

# 입력 변환 함수 (π, 삼각함수, 로그, 지수, 절댓값)
def parse_func(s):
    s = s.replace("sin", "np.sin")
    s = s.replace("cos", "np.cos")
    s = s.replace("tan", "np.tan")
    s = s.replace("exp", "np.exp")
    s = s.replace("abs", "np.abs")
    s = s.replace("pi", "np.pi")
    # log(x) -> np.log(np.clip(x,1e-6,None))
    pattern = r'log\((.*?)\)'
    s = re.sub(pattern, r'np.log(np.clip(\1,1e-6,None))', s)
    return s

parsed_input = parse_func(func_input)

# 그래프 그리기
if st.button("📈 그래프 그리기"):
    try:
        y = eval(parsed_input, {"__builtins__": {}}, {"x": x, "np": np})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)', line=dict(color="#FF5733", width=3)))
        fig.update_layout(title=f"y = {func_input}",
                          xaxis_title="x",
                          yaxis_title="f(x)",
                          template="plotly_white",
                          width=900, height=500)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ 오류: {e}")