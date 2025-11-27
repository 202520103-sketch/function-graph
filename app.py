import streamlit as st
import numpy as np
import plotly.graph_objs as go
import re
from scipy.optimize import fsolve

st.set_page_config(page_title="🌊 Easy Function Grapher", layout="wide")

# 페이지 스타일
st.markdown("""
<style>
.stApp { background-color: #e0f7fa; font-family: 'Segoe UI', sans-serif; }
.stButton>button { font-size:16px; padding:8px 12px; border-radius:8px; margin:5px; background:linear-gradient(90deg,#81d4fa,#29b6f6); color:#000; }
.stTextInput>div>div>input { font-size:16px; padding:5px; border-radius:5px; border:1px solid #29b6f6;}
</style>
""", unsafe_allow_html=True)

st.title("🌊 Easy Function Grapher")

# 안내 카드
st.markdown("""
<div style="background: linear-gradient(90deg,#b3e5fc,#81d4fa); padding:20px; border-radius:15px; color:#000;">
<h3>📌 사용법 안내</h3>
<ol>
<li>🔢 x 최소/최대 범위를 설정하세요.</li>
<li>✍️ 함수 입력창에 간단히 입력하세요 (예: sin(x), cos(x), tan(x), log(x+1), exp(x), abs(x-3), x**2, pi*x)</li>
<li>💡 함수 설명:
<ul>
<li><b>sin(x), cos(x), tan(x)</b>: 삼각함수, π 사용 가능 (예: sin(pi*x))</li>
<li><b>log(x)</b>: 자연로그 (x>0, 자동 안전 처리)</li>
<li><b>exp(x)</b>: e^x 지수 함수</li>
<li><b>abs(x)</b>: 절댓값</li>
</ul>
</li>
<li>📈 '그래프 그리기' 버튼 클릭 → 바로 그래프 확인</li>
<li>🔄 체크박스 선택 시 함수의 역함수 + y=x 대각선 표시</li>
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

# 역함수 표시 여부
show_inverse = st.checkbox("🔄 역함수 표시")

# 입력 변환 함수
def parse_func(s):
    s = s.replace("sin", "np.sin")
    s = s.replace("cos", "np.cos")
    s = s.replace("tan", "np.tan")
    s = s.replace("exp", "np.exp")
    s = s.replace("abs", "np.abs")
    s = s.replace("pi", "np.pi")
    pattern = r'log\((.*?)\)'
    s = re.sub(pattern, r'np.log(np.clip(\1,1e-6,None))', s)
    return s

parsed_input = parse_func(func_input)

# 그래프 그리기
if st.button("📈 그래프 그리기"):
    try:
        y = eval(parsed_input, {"__builtins__": {}}, {"x": x, "np": np})
        y = np.where(np.abs(y) > 1e6, np.nan, y)  # 이상치 처리
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)', line=dict(color="#0288d1", width=3)))
        
        if show_inverse:
            # 역함수 계산
            y_vals = np.linspace(np.nanmin(y), np.nanmax(y), 500)
            x_inv = []
            for yi in y_vals:
                try:
                    # 초기값을 y값 주변 + 0으로 다양화
                    root = fsolve(lambda t: eval(parsed_input, {"__builtins__": {}}, {"x": t, "np": np}) - yi, yi)
                    x_inv.append(root[0])
                except:
                    x_inv.append(np.nan)
            x_inv = np.array(x_inv)
            
            fig.add_trace(go.Scatter(x=y_vals, y=x_inv, mode='lines', name="f⁻¹(x)",
                                     line=dict(color="#d32f2f", width=3, dash='dash')))
            # y=x 대각선
            fig.add_trace(go.Scatter(x=y_vals, y=y_vals, mode='lines', name="y=x",
                                     line=dict(color="#388e3c", width=2, dash='dot')))
        
        # y 범위 자동 조절
        y_min = min(np.nanmin(y), np.nanmin(x_inv) if show_inverse else np.nan)
        y_max = max(np.nanmax(y), np.nanmax(x_inv) if show_inverse else np.nan)
        fig.update_layout(title=f"y = {func_input}",
                          xaxis_title="x",
                          yaxis_title="f(x)",
                          yaxis=dict(range=[y_min - 0.5, y_max + 0.5]),
                          template="plotly_white",
                          width=900, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"⚠️ 오류: {e}")