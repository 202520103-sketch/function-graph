import streamlit as st
import numpy as np
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="함수 그래프 플로터", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 8px 16px;
        border-radius: 5px;
    }
    .stNumberInput>div>div>input {
        padding: 5px;
        font-size: 16px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stSelectbox>div>div>div>select {
        font-size: 16px;
        padding: 5px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True
)

# 제목 및 설명
st.title("📊 예쁜 함수 그래프 플로터")
st.markdown("""
<div style="background-color:#e0f7fa; padding:15px; border-radius:10px;">
<b>사용법 안내</b><br>
1. x 범위를 설정합니다.<br>
2. 함수 유형을 선택하거나 직접 입력합니다.<br>
3. 필요하면 계수를 조정합니다.<br>
4. '그래프 그리기' 버튼을 클릭하면 결과 확인.<br>
<br>
<b>지원 함수</b>: 일차, 이차, 삼차, 지수(exp), 로그(log), 절댓값(abs), 직접 입력<br>
</div>
""", unsafe_allow_html=True)

# x 범위
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        x_min = st.number_input("x 최소값", value=-10.0)
    with col2:
        x_max = st.number_input("x 최대값", value=10.0)

x = np.linspace(x_min, x_max, 500)

# 함수 선택
func_type = st.selectbox("함수 선택", ["일차", "이차", "삼차", "지수", "로그", "절댓값", "직접 입력"])

y = np.zeros_like(x)

# 함수 정의
with st.container():
    if func_type == "일차":
        a = st.number_input("a (계수)", value=1.0)
        b = st.number_input("b (상수)", value=0.0)
        y = a*x + b
    elif func_type == "이차":
        a = st.number_input("a (2차)", value=1.0)
        b = st.number_input("b (1차)", value=0.0)
        c = st.number_input("c (상수)", value=0.0)
        y = a*x**2 + b*x + c
    elif func_type == "삼차":
        a = st.number_input("a (3차)", value=1.0)
        b = st.number_input("b (2차)", value=0.0)
        c = st.number_input("c (1차)", value=0.0)
        d = st.number_input("d (상수)", value=0.0)
        y = a*x**3 + b*x**2 + c*x + d
    elif func_type == "지수":
        a = st.number_input("지수 계수 a", value=1.0)
        y = np.exp(a*x)
    elif func_type == "로그":
        y = np.log(np.clip(x, 1e-6, None))
    elif func_type == "절댓값":
        y = np.abs(x)
    else:
        func_input = st.text_input("함수 입력 (예: x**2 + 2*x + 1, abs(x), np.exp(x), np.log(x))", "x**2")
        try:
            y = eval(func_input, {"__builtins__": {}}, {"x": x, "np": np, "abs": np.abs})
        except Exception as e:
            st.error(f"오류: {e}")
            y = np.zeros_like(x)

# 그래프 그리기
if st.button("그래프 그리기"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
    fig.update_layout(
        title=f"{func_type} 함수 그래프",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        width=900, height=500
    )
    st.plotly_chart(fig, use_container_width=True)