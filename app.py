import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="핀테크 광고 데이터 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  .metric-card {
    background: #13161f;
    border: 1px solid #1e2130;
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
  }
  .metric-card h3 { font-size: 11px; color: #6b7280; font-weight: 400; margin-bottom: 6px; letter-spacing: 0.02em; }
  .metric-card .val { font-size: 28px; font-weight: 700; letter-spacing: -1px; color: #f0f2f8; margin: 0; }
  .metric-card .sub { font-size: 12px; color: #6b7280; margin-top: 6px; }
  .badge { display:inline-block; font-size:11px; font-weight:600; padding:2px 8px; border-radius:6px; margin-left:6px; vertical-align:middle; }
  .badge-up   { background:#0f2a1a; color:#34d399; }
  .badge-down { background:#2a0f0f; color:#f87171; }
  .badge-warn { background:#2a1e0f; color:#fbbf24; }
  .badge-info { background:#0f1a2a; color:#60a5fa; }
  .section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: #4b5268;
    margin: 32px 0 12px;
    display: flex; align-items: center; gap: 10px;
  }
  .insight-item { display:flex; gap:14px; padding:12px 0; border-bottom:1px solid #1a1e2a; align-items:flex-start; }
  .insight-item:last-child { border-bottom:none; }
  .insight-num { width:28px; height:28px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0; }
  .insight-title { font-size:13px; font-weight:600; color:#d0d4e0; margin-bottom:4px; }
  .insight-desc { font-size:12px; color:#6b7280; line-height:1.6; }
  .tag { display:inline-block; font-size:10px; font-weight:600; padding:1px 6px; border-radius:4px; margin-right:4px; vertical-align:middle; }
  .funnel-row { display:flex; align-items:center; padding:8px 0; border-bottom:1px solid #1a1e2a; gap:12px; }
  .funnel-row:last-child { border-bottom:none; }
</style>
""", unsafe_allow_html=True)

COLORS = {
    "google": "#3b82f6",
    "googleL": "#93c5fd",
    "naver": "#10b981",
    "naverL": "#6ee7b7",
    "facebook": "#ec4899",
    "facebookL": "#f9a8d4",
    "video": "#8b5cf6",
    "image": "#06b6d4",
    "retarget": "#10b981",
    "nontarget": "#6b7280",
    "grid": "rgba(255,255,255,0.05)",
    "text": "#8b93a8",
    "bg": "#13161f",
    "paper": "#0f1117",
}

PLOT_LAYOUT = dict(
    paper_bgcolor=COLORS["paper"],
    plot_bgcolor=COLORS["bg"],
    font=dict(color=COLORS["text"], size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=COLORS["grid"], tickfont=dict(color=COLORS["text"], size=10)),
    yaxis=dict(gridcolor=COLORS["grid"], tickfont=dict(color=COLORS["text"], size=10)),
    showlegend=True,
    legend=dict(font=dict(color=COLORS["text"], size=11), bgcolor="rgba(0,0,0,0)"),
)


def plot(**kw):
    d = dict(PLOT_LAYOUT)
    d.update(kw)
    return d


# ── Header ──────────────────────────────────────────────
st.markdown("""
<div style="border-bottom:1px solid #1e2130; padding-bottom:16px; margin-bottom:4px;">
  <h1 style="font-size:20px; font-weight:600; color:#f0f2f8; margin:0; letter-spacing:-0.3px;">핀테크 광고 데이터 분석</h1>
  <p style="font-size:13px; color:#6b7280; margin:4px 0 10px;">2025년 1월 ~ 12월 · 109,500행 · 3개 채널 · 총 광고비 ₩273억</p>
  <span style="background:#1a2744; border:1px solid #2d4a8a; border-radius:20px; padding:3px 12px; font-size:12px; color:#6ea6ff; margin-right:6px;">구글</span>
  <span style="background:#1a2744; border:1px solid #2d4a8a; border-radius:20px; padding:3px 12px; font-size:12px; color:#6ea6ff; margin-right:6px;">페이스북</span>
  <span style="background:#1a2744; border:1px solid #2d4a8a; border-radius:20px; padding:3px 12px; font-size:12px; color:#6ea6ff; margin-right:6px;">네이버검색</span>
  <span style="background:#1e2130; border:1px solid #2a2f45; border-radius:20px; padding:3px 12px; font-size:12px; color:#8b93a8;">10가지 인사이트</span>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ───────────────────────────────────────────
st.markdown('<div class="section-label">핵심 지표 요약</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
kpis = [
    (c1, "#2563eb", "최저 CPI 채널", "₩626", "구글 앱설치당 비용", "구글", "badge-info"),
    (c2, "#0f766e", "리타겟 CPA 절감", "23%↓", "₩2,255 → ₩1,737", "리타겟 우위", "badge-up"),
    (c3, "#b45309", "최대 퍼널 병목", "51.2%", "계좌개설 → 첫거래", "개선 필요", "badge-warn"),
    (c4, "#be185d", "자동이체 설정률", "3.8%", "전 채널 동일", "제품 UX 이슈", "badge-down"),
]
for col, color, title, val, sub, badge, badge_cls in kpis:
    col.markdown(f"""
    <div class="metric-card" style="border-top:2px solid {color};">
      <h3>{title}</h3>
      <div class="val">{val}</div>
      <div class="sub">{sub} <span class="badge {badge_cls}">{badge}</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 인사이트 1·2: 채널 효율 ────────────────────────────
st.markdown('<div class="section-label">채널 효율 분석</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**인사이트 1 — 광고비 비중 vs 계좌개설 비중**")
    st.caption("구글은 예산 25%로 계좌개설의 41.2%를 창출. 페이스북은 42% 투입 대비 44% 성과로 균형적, 네이버는 33% 투입에 14.8% 성과로 최저 효율.")
    channels = ["구글", "페이스북", "네이버검색"]
    fig1 = go.Figure()
    fig1.add_bar(name="광고비 비중", x=channels, y=[24.9, 42.4, 32.6],
                 marker_color=[f"rgba(59,130,246,0.4)", "rgba(236,72,153,0.4)", "rgba(16,185,129,0.4)"],
                 marker_line_color=[COLORS["google"], COLORS["facebook"], COLORS["naver"]], marker_line_width=2)
    fig1.add_bar(name="계좌개설 비중", x=channels, y=[41.2, 44.0, 14.8],
                 marker_color=[COLORS["google"], COLORS["facebook"], COLORS["naver"]])
    fig1.update_layout(**plot(barmode="group", yaxis=dict(gridcolor=COLORS["grid"], ticksuffix="%", tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor=COLORS["grid"], tickfont=dict(color=COLORS["text"], size=10)), height=260))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown("**인사이트 2 — 채널 × 포맷별 CPI**")
    st.caption("구글 영상(₩600)이 전체 최저. 네이버 일반키워드(₩2,690)는 구글 영상 대비 4.5배 비쌈. 동일 채널 내 영상이 이미지보다 일관되게 낮음.")
    labels = ["구글\n영상", "구글\n이미지", "페이스북\n영상", "페이스북\n이미지", "네이버\n브랜드KW", "네이버\n일반KW"]
    values = [600, 660, 954, 1048, 2071, 2690]
    bar_colors = [COLORS["google"], COLORS["googleL"], COLORS["facebook"], COLORS["facebookL"], COLORS["naver"], COLORS["naverL"]]
    fig2 = go.Figure(go.Bar(x=labels, y=values, marker_color=bar_colors,
                            hovertemplate="CPI: ₩%{y:,}<extra></extra>"))
    fig2.update_layout(**plot(showlegend=False, yaxis=dict(gridcolor=COLORS["grid"], tickprefix="₩", tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=COLORS["text"], size=10)), height=280))
    st.plotly_chart(fig2, use_container_width=True)

# ── 인사이트 3·10: 타겟팅 ───────────────────────────────
st.markdown('<div class="section-label">타겟팅 전략</div>', unsafe_allow_html=True)
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("**인사이트 3 — 리타겟 vs 논타겟 효율 비교**")
    st.caption("리타겟이 CPI ₩930, CPA ₩1,737로 논타겟(CPI ₩1,207 / CPA ₩2,255) 대비 각각 23%, 23% 절감. 반복사용자도 69% 더 많이 확보.")
    metrics = ["CPI (₩)", "CPA 계좌개설 (₩)", "반복사용자 (만명)"]
    fig3 = go.Figure()
    fig3.add_bar(name="논타겟", x=metrics, y=[1207, 2255, 171.9], marker_color="rgba(107,114,128,0.6)")
    fig3.add_bar(name="리타겟", x=metrics, y=[930, 1737, 289.9], marker_color=COLORS["naver"])
    fig3.update_layout(**plot(barmode="group", yaxis=dict(gridcolor=COLORS["grid"], tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=COLORS["text"], size=10)), height=260))
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.markdown("**인사이트 10 — 채널 × 타겟 유형 CPA 히트맵**")
    st.caption("구글 리타겟이 ₩1,051로 전체 최저. 네이버는 리타겟도 ₩3,833으로 다른 채널 논타겟보다 비쌈.")
    heatmap_data = {
        "채널": ["구글", "페이스북", "네이버"],
        "논타겟 CPA": [1366, 2172, 4990],
        "리타겟 CPA": [1051, 1674, 3833],
        "절감률": ["▼ 23%", "▼ 23%", "▼ 23%"],
    }
    df_hm = pd.DataFrame(heatmap_data)
    fig_hm = go.Figure()
    fig_hm.add_bar(name="논타겟 CPA", x=df_hm["채널"], y=df_hm["논타겟 CPA"],
                   marker_color=["rgba(59,130,246,0.5)", "rgba(192,132,252,0.5)", "rgba(251,146,60,0.5)"],
                   hovertemplate="논타겟 CPA: ₩%{y:,}<extra></extra>")
    fig_hm.add_bar(name="리타겟 CPA", x=df_hm["채널"], y=df_hm["리타겟 CPA"],
                   marker_color=[COLORS["google"], "rgba(96,165,250,0.8)", COLORS["naver"]],
                   hovertemplate="리타겟 CPA: ₩%{y:,}<extra></extra>")
    fig_hm.update_layout(**plot(barmode="group", yaxis=dict(gridcolor=COLORS["grid"], tickprefix="₩", tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=COLORS["text"], size=10)), height=260))
    st.plotly_chart(fig_hm, use_container_width=True)
    st.caption("* 리타겟 우위는 채널 무관 일관됨. 단, 네이버 전체 비용 수준이 타 채널 대비 2~4배 높음.")

# ── 인사이트 5: 퍼널 ────────────────────────────────────
st.markdown('<div class="section-label">전환 퍼널 분석</div>', unsafe_allow_html=True)
st.markdown("**인사이트 5 — 전체 퍼널 전환율 · 최대 병목 구간 식별**")
st.caption("광고 노출 → 계좌개설 최종 전환율 0.31%. 계좌개설 후 첫거래(51.2%)와 반복사용 후 자동이체설정(21.9%) 두 구간이 주요 이탈 지점.")

funnel_data = [
    ("광고노출",   4551502359, 100,  "#3b82f6", False, ""),
    ("광고클릭",   47028365,   1.03, "#3b82f6", False, ""),
    ("앱설치",     26445622,   56.2, "#6366f1", False, ""),
    ("앱실행",     23799277,   90.0, "#8b5cf6", False, ""),
    ("회원가입",   18397121,   77.3, "#10b981", False, ""),
    ("계좌개설",   14155628,   76.9, "#10b981", False, ""),
    ("첫거래",     7243732,    51.2, "#f59e0b", True,  "⚠ 최대 병목"),
    ("반복사용",   4617161,    63.7, "#f97316", False, ""),
    ("자동이체설정",1012122,   21.9, "#ef4444", True,  "⚠ 이탈 구간"),
    ("추천완료",   506229,     50.0, "#8b5cf6", False, ""),
]

for i, (stage, count, pct, color, warn, warn_text) in enumerate(funnel_data):
    bar_w = 100 if i == 0 else max(pct, 2)
    pct_color = "#fbbf24" if warn else ("#34d399" if pct >= 70 else ("#60a5fa" if pct >= 50 else "#f87171"))
    pct_label = "–" if i == 0 else f"{pct}%"
    warn_html = f'<span style="font-size:11px;color:#fbbf24;margin-left:8px;">{warn_text}</span>' if warn else ""
    inner = f"이전 단계 대비 {pct}%" if i > 0 else "기준"
    st.markdown(f"""
    <div style="display:flex; align-items:center; padding:8px 0; border-bottom:1px solid #1a1e2a; gap:12px;">
      <div style="width:90px; font-size:12px; color:#8b93a8; flex-shrink:0;">{stage}</div>
      <div style="flex:1; background:#1a1e2a; border-radius:4px; height:28px; overflow:hidden;">
        <div style="width:{bar_w}%; height:100%; background:{color}20; border-left:3px solid {color}; border-radius:4px; display:flex; align-items:center; padding:0 10px; font-size:11px; font-weight:600; color:{color}; white-space:nowrap;">
          {inner}{warn_html}
        </div>
      </div>
      <div style="width:50px; text-align:right; font-size:13px; font-weight:700; color:{pct_color}; flex-shrink:0;">{pct_label}</div>
      <div style="width:120px; text-align:right; font-size:11px; color:#4b5268; flex-shrink:0;">{count:,}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 인사이트 6·7: 캠페인 목적 & 크리에이티브 ────────────
st.markdown('<div class="section-label">캠페인 목적별 퍼널 효율</div>', unsafe_allow_html=True)
col_e, col_f = st.columns(2)

with col_e:
    st.markdown("**인사이트 6 — 목적 설정이 하류 전환을 결정**")
    st.caption("계좌개설 목적 캠페인이 회원가입 목적보다 계좌→첫거래(60% vs 40%), 첫거래→반복(72% vs 48%)에서 20~24%p 높음.")
    stages = ["앱→회원가입", "회원→계좌개설", "계좌→첫거래", "첫거래→반복사용"]
    fig6 = go.Figure()
    fig6.add_bar(name="계좌개설 목적", x=stages, y=[63, 99, 60, 72], marker_color="rgba(59,130,246,0.8)")
    fig6.add_bar(name="회원가입 목적", x=stages, y=[75.6, 60, 40, 48], marker_color="rgba(236,72,153,0.8)")
    fig6.update_layout(**plot(barmode="group", yaxis=dict(gridcolor=COLORS["grid"], ticksuffix="%", range=[0,110], tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=COLORS["text"], size=10)), height=260))
    st.plotly_chart(fig6, use_container_width=True)

with col_f:
    st.markdown("**인사이트 7 — 영상이 이미지보다 CPI 9% 낮고 계좌개설 31% 많음**")
    st.caption("영상: CPI ₩784 / CPA ₩1,463. 이미지: CPI ₩860 / CPA ₩1,607. 네이버 키워드는 CPI와 CPA 모두 2~3배 이상 높아 효율 열위.")
    formats = ["영상", "이미지", "브랜드키워드", "일반키워드"]
    fig7 = go.Figure()
    fig7.add_bar(name="CPI (₩)", x=formats, y=[784, 860, 2071, 2690], marker_color="rgba(139,92,246,0.8)")
    fig7.add_bar(name="CPA 계좌개설 (₩)", x=formats, y=[1463, 1607, 3872, 5028], marker_color="rgba(6,182,212,0.6)")
    fig7.update_layout(**plot(barmode="group", yaxis=dict(gridcolor=COLORS["grid"], tickprefix="₩", tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=COLORS["text"], size=10)), height=280))
    st.plotly_chart(fig7, use_container_width=True)

# ── 인사이트 8·9: 시계열 & 예산 ────────────────────────
st.markdown('<div class="section-label">시계열 & 예산 배분</div>', unsafe_allow_html=True)
col_g, col_h = st.columns(2)

with col_g:
    st.markdown("**인사이트 9 — 월별 CPI 추이 · 4분기 비용 급등**")
    st.caption("1월 ₩870 → 12월 ₩1,265 (45% 상승). 3·9·12월 지출 급증 구간에서 CPI도 동시 상승. 1~2분기 저비용 구간 활용이 유리.")
    months = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]
    cpi = [870,945,1114,966,1011,896,872,913,1157,1060,1152,1265]
    budget = [16.94,16.95,29.21,20.25,22.77,17.25,16.81,18.67,31.02,24.44,25.4,33.45]
    fig8 = go.Figure()
    fig8.add_scatter(name="CPI (₩)", x=months, y=cpi, line=dict(color=COLORS["google"], width=2.5),
                     fill="tozeroy", fillcolor="rgba(59,130,246,0.08)", mode="lines+markers",
                     yaxis="y", hovertemplate="CPI: ₩%{y:,}<extra></extra>")
    fig8.add_scatter(name="광고비 (억원)", x=months, y=budget, line=dict(color="#6b7280", width=1.5, dash="dash"),
                     mode="lines+markers", yaxis="y2", hovertemplate="%{y}억<extra></extra>")
    fig8.update_layout(**plot(
        yaxis=dict(title="CPI (₩)", gridcolor=COLORS["grid"], tickprefix="₩", tickfont=dict(color=COLORS["google"], size=10)),
        yaxis2=dict(title="광고비 (억원)", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)", ticksuffix="억", tickfont=dict(color="#6b7280", size=10)),
        height=270
    ))
    st.plotly_chart(fig8, use_container_width=True)

with col_h:
    st.markdown("**인사이트 8 — 자동이체·추천 전환율은 채널 무관**")
    st.caption("자동이체율 구글 3.84% / 페이스북 3.82% / 네이버 3.82%. 추천율도 약 11%로 전 채널 동일. 광고 최적화 문제가 아닌 앱 내 UX 이슈임을 시사.")
    channels = ["구글", "페이스북", "네이버검색"]
    fig9 = go.Figure()
    fig9.add_bar(name="자동이체 설정률 (%)", x=channels, y=[3.84, 3.82, 3.82], marker_color="rgba(245,158,11,0.8)")
    fig9.add_bar(name="추천 완료율 (%)", x=channels, y=[10.99, 10.97, 10.86], marker_color="rgba(139,92,246,0.7)")
    fig9.update_layout(**plot(barmode="group", yaxis=dict(gridcolor=COLORS["grid"], ticksuffix="%", tickfont=dict(color=COLORS["text"], size=10)), xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=COLORS["text"], size=10)), height=270))
    st.plotly_chart(fig9, use_container_width=True)

# ── 인사이트 요약 ────────────────────────────────────────
st.markdown('<div class="section-label">10가지 인사이트 요약</div>', unsafe_allow_html=True)

insights = [
    (1, "#3b82f6", "#1a2744", "#60a5fa", "채널", "구글이 가장 효율적인 앱설치 채널",
     "구글 CPI ₩626으로 페이스북(₩995) 대비 37%, 네이버(₩2,280) 대비 72% 저렴. 그러나 구글 예산 비중은 25%로 가장 낮아 예산 배분이 성과와 역전됨."),
    (2, "#ec4899", "#2a0f1a", "#f472b6", "채널", "페이스북 예산 42% 투입 — 효율은 중간",
     "페이스북 CPI ₩995, CPA ₩1,860. 예산 비중(42%) 대비 계좌개설 비중(44%)은 균형적이나, 구글 대비 CPI 59% 높아 효율 개선 여지 있음."),
    (3, "#f59e0b", "#2a1a0f", "#fbbf24", "채널", "네이버 일반키워드 CPI·CPA 전체 최하",
     "일반키워드 CPI ₩2,690 / CPA ₩5,028로 구글 영상 대비 각각 4.5배, 4.5배 비쌈. 브랜드키워드는 방어 목적 유지 가능하나 일반키워드 예산 축소 검토 필요."),
    (4, "#10b981", "#0f2a1a", "#34d399", "타겟팅", "리타겟이 논타겟 대비 CPA 23% 절감",
     "리타겟 계좌개설 CPA ₩1,737 vs 논타겟 ₩2,255. 반복사용자도 70% 더 많이 확보. 채널 무관하게 모든 채널에서 리타겟 우위 일관됨."),
    (5, "#ef4444", "#2a0f0f", "#f87171", "퍼널", '"계좌개설 → 첫거래" 전환이 퍼널 최대 병목',
     "계좌개설 후 첫거래 전환율 51.2% — 퍼널 내 가장 큰 이탈 구간. 계좌를 만들고 거래를 안 하는 사용자에 대한 온보딩 넛지(첫거래 혜택, 투자 가이드) 강화 필요."),
    (6, "#6366f1", "#1a1a2a", "#818cf8", "전략", "캠페인 목적 설정이 하류 전환율을 좌우",
     "계좌개설 목적 캠페인은 계좌→첫거래 60% / 첫거래→반복 72%. 회원가입 목적은 각각 40% / 48%. 동일 예산에도 목적 설정만으로 실질 수익 기여가 크게 달라짐."),
    (7, "#8b5cf6", "#1e1a2a", "#c084fc", "크리에이티브", "영상 크리에이티브가 이미지보다 전방위 우세",
     "영상 CPI ₩784 / CPA ₩1,463. 이미지는 각각 ₩860 / ₩1,607. 제작 비용이 허용하는 범위 내 영상 비중 확대가 ROI에 유리."),
    (8, "#f59e0b", "#2a1a0f", "#fbbf24", "UX", "자동이체 설정률 3.8% — 광고가 아닌 제품 문제",
     "구글 3.84% / 페이스북 3.82% / 네이버 3.82%로 채널과 무관하게 동일. 광고 타겟팅·크리에이티브 문제가 아닌 앱 내 자동이체 설정 UX 개선이 핵심."),
    (9, "#06b6d4", "#0f2a2a", "#22d3ee", "예산배분", "4분기 예산 30.5% 집중 — 그러나 CPI 연중 최고",
     "4분기 광고비 비중 30.5%이지만 CPI ₩1,164로 최고. 저비용 구간인 1~2분기(CPI ₩870~945)로 예산 분산하는 평탄화 전략이 전체 효율 향상에 유리."),
    (10, "#34d399", "#0f2a1a", "#34d399", "성장", "추천 전환율 11% — 채널·포맷 무관 균등",
     "반복사용자 중 추천 완료율이 전 채널 약 11%로 동일. 리퍼럴 성장은 광고 노출보다 내재 사용자 만족도에 의존. 추천 프로그램 성과 향상을 위해 서비스 경험 개선이 선행 필요."),
]

with st.container():
    st.markdown('<div style="background:#13161f; border:1px solid #1e2130; border-radius:12px; padding:18px 22px;">', unsafe_allow_html=True)
    for n, color, tag_bg, tag_color, tag, title, desc in insights:
        st.markdown(f"""
        <div class="insight-item">
          <div class="insight-num" style="background:{color}18; color:{color};">{n}</div>
          <div>
            <div class="insight-title">
              <span class="tag" style="background:{tag_bg}; color:{tag_color};">{tag}</span>
              {title}
            </div>
            <div class="insight-desc">{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
