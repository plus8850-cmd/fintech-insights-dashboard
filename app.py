import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="핀테크 광고 데이터 — 10가지 핵심 인사이트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 UI 숨김 (헤더·푸터·패딩 제거)
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden; height: 0;}
.block-container {padding: 0 !important; max-width: 100% !important;}
[data-testid="stAppViewContainer"] {background: #0d0f14;}
[data-testid="stVerticalBlock"] {gap: 0 !important;}
</style>
""", unsafe_allow_html=True)

html = Path(__file__).parent / "dashboard.html"
components.html(html.read_text(encoding="utf-8"), height=5800, scrolling=False)
