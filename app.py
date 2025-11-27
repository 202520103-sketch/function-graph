import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Simple & Easy Function Grapher", layout="wide")
st.title("🎨 Simple & Easy Function Grapher")

# 안내
st.markdown("""
📌 **사용법**
1. x 범위를 설정하세요.
2. 함수 입력창에 간단히 입력하세요.
   - 예시: `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`, `log(x+1)`, `abs(x-3)`, `x**2`, `pi*x`
3. '그래프 그리기' 버튼 클릭
""")

# x 범위
col1, col2 = st.columns(2)
x_min = col1.number_input("x 최소값", value=-10.0)
x_max = col2.number_input("x 최대값", value=10.0)
x = np.linspace(x_min, x_max, 500)

# 함수 입력
func_input = st.text_input("함수 입력 ✍️", "x**2")

# 입력 변환 함수
def parse_func(s):
    s = s.replace("sin", "np.sin")
    s = s.replace("cos", "np.cos")
    s = s.replace("tan", "np.tan")
    s = s.replace("exp", "np.exp")
    s = s.replace("log", "np.log(np.clip")
    s = s.replace("abs", "np.abs")
    s = s.replace("pi", "np.pi")
    # log 함수 괄호 닫기
    if "np.log(np.clip" in s:
        s = s.replace("np.log(np.clip", "np.log(np.clip") + ",1e-6,None))"
    return s

parsed_input = parse_func(func_input)

# 그래프 그리기
if st.button("📈 그래프 그리기"):
    try:
        y = eval(parsed_input, {"__builtins__": {}}, {"x": x, "np": np})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)'))
        fig.update_layout(title=f"y = {func_input}", xaxis_title="x", yaxis_title="f(x)",
                          template="plotly_white", width=900, height=500)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ 오류: {e}")