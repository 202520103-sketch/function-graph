import streamlit as st
import numpy as np
import plotly.graph_objs as go
from scipy.optimize import fsolve

st.set_page_config(page_title="🎉 Click-to-Graph Function Grapher", layout="wide")
st.title("🎉 Click-to-Graph Function Grapher")

# 안내 카드
st.markdown("""
<div style="background: linear-gradient(90deg,#ffecd2,#fcb69f); padding:20px; border-radius:15px;">
<h3>📌 사용법 안내</h3>
<ol>
<li>🔢 x 최소/최대 범위를 설정하세요</li>
<li>🎯 아래 버튼을 클릭하면 선택한 함수의 그래프가 바로 표시됩니다</li>
<li>📈 필요 시 '역함수' 버튼을 클릭하면 수치 근사로 역함수 그래프 확인 가능</li>
<li>💡 함수 입력창은 자유롭게 수식을 실험하고 싶은 경우에만 사용</li>
</ol>
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 선택 버튼
st.markdown("### 🎁 함수 선택")
func = None
cols = st.columns(7)
buttons = [
    ("🟢 절댓값", lambda x: np.abs(x)),
    ("🟡 지수", lambda x: np.exp(x)),
    ("🟠 로그", lambda x: np.log(np.clip(x,1e-6,None))),
    ("🔵 sin", lambda x: np.sin(x)),
    ("🟣 cos", lambda x: np.cos(x)),
    ("🟤 tan", lambda x: np.tan(x)),
    ("💖 x**2", lambda x: x**2)
]
for i, (label, f) in enumerate(buttons):
    with cols[i]:
        if st.button(label):
            func = f

# 역함수 버튼
inverse = st.checkbox("🔄 역함수 보기 (수치 근사)")

# 그래프 그리기
if st.button("📈 그래프 그리기"):
    if func is None:
        st.warning("⚠️ 먼저 그래프를 그리고 싶은 함수를 선택하세요!")
    else:
        try:
            y = func(x)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
            
            # 역함수 계산 (근사)
            if inverse:
                y_vals = np.linspace(np.min(y), np.max(y), 500)
                x_inv = [fsolve(lambda t: func(t)-yv, 0)[0] for yv in y_vals]
                fig.add_trace(go.Scatter(x=x_inv, y=y_vals, mode='lines', name='f⁻¹(x)', line=dict(dash='dot', color='red')))
            
            fig.update_layout(title="함수 그래프", xaxis_title="x", yaxis_title="f(x)",
                              template="plotly_white", width=900, height=500)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ 오류: {e}")