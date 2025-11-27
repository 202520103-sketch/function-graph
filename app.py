import streamlit as st
import numpy as np
import plotly.graph_objs as go
import re
from scipy.optimize import fsolve
import itertools

st.set_page_config(page_title="🌊 Multi Function Grapher", layout="wide")

# 스타일
st.markdown("""
<style>
.stApp { background-color: #e0f7fa; font-family: 'Segoe UI', sans-serif; }
.stButton>button { font-size:16px; padding:8px 12px; border-radius:8px; margin:5px; background:linear-gradient(90deg,#81d4fa,#29b6f6); color:#000; }
.stTextInput>div>div>input { font-size:16px; padding:5px; border-radius:5px; border:1px solid #29b6f6;}
</style>
""", unsafe_allow_html=True)

st.title("🌊 Multi Function Grapher")

# 안내 카드
st.markdown("""
<div style="background: linear-gradient(90deg,#b3e5fc,#81d4fa); padding:20px; border-radius:15px; color:#000;">
<h3>📌 사용법 안내</h3>
<ol>
<li>🔢 x 최소/최대 범위를 설정하세요.</li>
<li>✍️ 함수 입력창에 쉼표(,)로 여러 함수를 입력하세요 (예: x**2, sin(x), exp(x), (x+1)**x)</li>
<li>💡 함수 설명:
<ul>
<li><b>삼각함수</b>: sin(x), cos(x), tan(x), π 사용 가능 (예: sin(pi*x))</li>
<li><b>로그</b>: log(x), x>0 안전 처리</li>
<li><b>지수함수</b>: exp(x) 또는 base**exp, 밑과 지수 모두 수식 가능, 밑>0 자동 처리</li>
<li><b>절댓값</b>: abs(x)</li>
</ul>
</li>
<li>📈 '그래프 그리기' 버튼 클릭 → 바로 그래프 확인</li>
<li>🔄 체크박스 선택 시 함수별 역함수 + y=x 대각선 표시</li>
</ol>
</div>
""", unsafe_allow_html=True)

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력
func_inputs = st.text_input("함수 입력 ✍️ (쉼표로 구분)", "x**2, sin(x), exp(x)")
func_list = [f.strip() for f in func_inputs.split(",")]

# 역함수 표시 여부
show_inverse = st.checkbox("🔄 역함수 표시")

# 함수 변환
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

# 색상 순서
colors = itertools.cycle(["#0288d1","#d32f2f","#388e3c","#fbc02d","#7b1fa2","#f57c00","#0097a7","#c2185b"])

# 그래프 그리기
if st.button("📈 그래프 그리기"):
    fig = go.Figure()
    y_min_all, y_max_all = np.inf, -np.inf
    
    for func_input in func_list:
        parsed_input = parse_func(func_input)
        try:
            y = np.array([eval(parsed_input, {"__builtins__": {}}, {"x": xi, "np": np}) for xi in x])
            y = np.where(np.isfinite(y) & (np.abs(y)<1e6), y, np.nan)
            
            color = next(colors)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f"{func_input}", line=dict(color=color, width=3)))
            
            y_min_all = min(y_min_all, np.nanmin(y))
            y_max_all = max(y_max_all, np.nanmax(y))
            
            # 역함수
            if show_inverse:
                y_vals = np.linspace(np.nanmin(y), np.nanmax(y), 500)
                x_inv = []
                for yi in y_vals:
                    try:
                        root = fsolve(lambda t: eval(parsed_input, {"__builtins__": {}}, {"x": t, "np": np}) - yi, yi)
                        x_inv.append(root[0])
                    except:
                        x_inv.append(np.nan)
                x_inv = np.array(x_inv)
                fig.add_trace(go.Scatter(x=y_vals, y=x_inv, mode='lines', name=f"{func_input}⁻¹(x)",
                                         line=dict(color=color, width=3, dash='dash')))
                fig.add_trace(go.Scatter(x=y_vals, y=y_vals, mode='lines', name=f"y=x",
                                         line=dict(color="#000000", width=2, dash='dot')))
                
                y_min_all = min(y_min_all, np.nanmin(x_inv))
                y_max_all = max(y_max_all, np.nanmax(x_inv))
                
        except Exception as e:
            st.warning(f"⚠️ {func_input} 계산 중 오류: {e}")
    
    fig.update_layout(title="여러 함수 그래프",
                      xaxis_title="x",
                      yaxis_title="f(x)",
                      yaxis=dict(range=[y_min_all - 0.5, y_max_all + 0.5]),
                      template="plotly_white",
                      width=900, height=500)
    st.plotly_chart(fig, use_container_width=True)
st.markdown("""
<div style="background-color:#b3e5fc; padding:10px; border-radius:10px; margin-top:10px;">
📌 그래프 안내: 
<ul>
<li>💡 원하는 영역을 드래그하면 확대할 수 있습니다.</li>
<li>📱 모바일: 오른쪽 위 <b>집 모양 버튼</b> 클릭 시 원래 크기로 돌아갑니다.</li>
<li>🖱️ PC: 마우스 오른쪽 클릭 → <b>Reset axes</b> 선택 시 원래 크기로 돌아갑니다.</li>
</ul>
</div>
""", unsafe_allow_html=True)