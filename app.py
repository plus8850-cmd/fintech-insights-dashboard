import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="핀테크 광고 데이터 — 10가지 핵심 인사이트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  .block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1200px; }
  body { background: #0d0f14; }
  .kpi-wrap { background:#13161f; border:1px solid #1a1d2a; border-radius:10px; padding:16px 18px; position:relative; overflow:hidden; }
  .kpi-wrap label { font-size:11px; color:#5a6072; display:block; margin-bottom:6px; }
  .kpi-wrap .val { font-size:26px; font-weight:700; color:#f0f2f8; letter-spacing:-1px; margin:0; }
  .kpi-wrap .sub { font-size:11px; color:#5a6072; margin-top:4px; }
  .sec { font-size:10px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#3d4258;
         border-bottom:1px solid #1a1d2a; padding-bottom:6px; margin: 2rem 0 .8rem; }
  .ic { background:#13161f; border:1px solid #1a1d2a; border-radius:12px; overflow:hidden; margin-bottom:10px; padding:16px 18px 14px; }
  .icat { font-size:10px; font-weight:600; padding:2px 8px; border-radius:10px; display:inline-block; margin-bottom:4px; }
  .ititle { font-size:14px; font-weight:500; color:#e8eaf2; line-height:1.4; margin-bottom:4px; }
  .ibody { font-size:12px; color:#7b849a; line-height:1.7; }
  .ibody b { font-weight:500; color:#c8ccd8; }
  .note { font-size:10px; color:#4b5268; border-left:2px solid #2a2f45; padding-left:8px; margin-top:7px; line-height:1.55; }
  .db { background:#0d0f14; border:1px solid #1a1d2a; border-radius:8px; padding:11px 14px; margin-top:10px; }
  .dbt { font-size:9px; font-weight:600; color:#3d4258; letter-spacing:.07em; text-transform:uppercase; margin-bottom:9px; }
  .dr { display:flex; gap:0; flex-wrap:wrap; }
  .dm { padding:0 14px 6px 0; }
  .dmv { font-size:14px; font-weight:600; color:#e8eaf2; line-height:1; }
  .dml { font-size:10px; color:#3d4258; margin-top:3px; }
  .sim { background:#0a111f; border:1px solid #1e3054; border-radius:8px; padding:11px 14px; margin-top:10px; }
  .sim-t { font-size:10px; font-weight:600; color:#4a7fc1; margin-bottom:8px; }
  .sim-r { display:flex; flex-wrap:wrap; gap:0; }
  .sim-d { padding:0 14px 6px 0; }
  .sim-v { font-size:14px; font-weight:600; color:#60a5fa; line-height:1; }
  .sim-l { font-size:10px; color:#4a7fc1; margin-top:3px; }
  .abox { background:#0a1f12; border:1px solid #0f4a20; border-radius:10px; padding:14px 18px; margin-top:10px; font-size:12px; color:#4ade80; line-height:1.9; }
  .abox b { font-weight:600; color:#86efac; }
  .pill { background:#161923; border:1px solid #222636; border-radius:20px; padding:3px 11px; font-size:11px; color:#7b849a; display:inline-block; margin-right:5px; }
  .fr { display:flex; align-items:center; gap:6px; margin-bottom:4px; }
  .fl { width:110px; font-size:10px; color:#5a6072; text-align:right; flex-shrink:0; }
  .fbg { flex:1; background:#161923; border-radius:3px; height:22px; overflow:hidden; }
  .ff { height:100%; border-radius:3px; display:flex; align-items:center; padding:0 8px; font-size:10px; font-weight:500; white-space:nowrap; }
  .fp { width:42px; font-size:11px; font-weight:600; text-align:right; flex-shrink:0; }
  .fc { font-size:10px; color:#3d4258; width:90px; text-align:right; flex-shrink:0; }
</style>
""", unsafe_allow_html=True)

C = {
    "bg": "#13161f", "paper": "#0d0f14",
    "grid": "rgba(255,255,255,0.05)", "text": "#7b849a",
    "blue": "#3b82f6", "pink": "#ec4899", "green": "#10b981",
    "amber": "#f59e0b", "red": "#ef4444", "purple": "#8b5cf6",
}

def layout(**kw):
    base = dict(
        paper_bgcolor=C["paper"], plot_bgcolor=C["bg"],
        font=dict(color=C["text"], size=11),
        margin=dict(l=8, r=8, t=8, b=8),
        showlegend=True,
        legend=dict(font=dict(color=C["text"], size=11), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=C["grid"], tickfont=dict(color=C["text"], size=10), linecolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor=C["grid"], tickfont=dict(color=C["text"], size=10)),
    )
    base.update(kw)
    return base

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-bottom:1px solid #1a1d2a; padding-bottom:16px; margin-bottom:4px;">
  <h1 style="font-size:18px; font-weight:600; color:#f0f2f8; margin:0; letter-spacing:-.3px;">핀테크 광고 데이터 — 10가지 핵심 인사이트</h1>
  <p style="font-size:12px; color:#5a6072; margin:3px 0 10px;">2025년 1월~12월 · 109,500행 · 3개 채널 · 총 광고비 ₩273억</p>
  <span class="pill">구글</span><span class="pill">페이스북</span><span class="pill">네이버검색</span>
</div>
""", unsafe_allow_html=True)

# ── KPI Grid ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
for col, color, label, val, sub in [
    (k1, "#2563eb", "총 광고비",   "₩273억",  "구글 25% · 페이스북 42% · 네이버 33%"),
    (k2, "#0f766e", "총 앱설치",   "2,644만", "클릭→설치 전환율 56.2%"),
    (k3, "#b45309", "평균 CPI",    "₩1,033",  "채널 간 최대 3.6× 격차"),
    (k4, "#be185d", "총 계좌개설", "1,416만", "평균 CPA ₩1,930"),
]:
    col.markdown(f"""
    <div class="kpi-wrap" style="border-top:2px solid {color};">
      <label>{label}</label>
      <div class="val">{val}</div>
      <div class="sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 채널 효율 인사이트 1 · 2
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">채널 효율</div>', unsafe_allow_html=True)

# ── 인사이트 1 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ic">
  <span class="icat" style="background:#1a2744;color:#60a5fa;">채널</span>
  <div class="ititle">구글 CPI 최저 — 예산 비중(25%)보다 성과 비중(41%)이 높음</div>
  <div class="ibody">
    구글 CPI <b>₩626</b>으로 페이스북(₩995) 대비 37%, 네이버(₩2,280) 대비 72% 저렴.
    계좌→첫거래·첫거래→반복 전환율은 3채널 모두 동일(51.2%, 63.7%)하므로 CPI 차이가 효율 차이로 직결.
    광고비 1억당 반복사용자 구글 <b>27,961명</b> vs 네이버 7,645명으로 3.7배 차이.
  </div>
  <div class="db">
    <div class="dbt">근거 데이터</div>
    <div class="dr">
      <div class="dm"><div class="dmv" style="color:#4ade80">₩626</div><div class="dml">구글 CPI</div></div>
      <div class="dm"><div class="dmv">₩995</div><div class="dml">페이스북 CPI</div></div>
      <div class="dm"><div class="dmv" style="color:#f87171">₩2,280</div><div class="dml">네이버 CPI</div></div>
      <div class="dm"><div class="dmv" style="color:#60a5fa">24.9%</div><div class="dml">구글 광고비 비중</div></div>
      <div class="dm"><div class="dmv" style="color:#60a5fa">41.2%</div><div class="dml">구글 계좌개설 비중</div></div>
      <div class="dm"><div class="dmv" style="color:#4ade80">27,961명</div><div class="dml">구글 1억당 반복사용자</div></div>
      <div class="dm"><div class="dmv" style="color:#f87171">7,645명</div><div class="dml">네이버 1억당 반복사용자</div></div>
    </div>
  </div>
  <div class="sim">
    <div class="sim-t">예산 재배분 시뮬레이션 — 네이버 50% 삭감 → 구글 이전 시</div>
    <div class="sim-r">
      <div class="sim-d"><div class="sim-v">₩44.6억</div><div class="sim-l">절감 예산</div></div>
      <div class="sim-d"><div class="sim-v" style="color:#f87171">-104만건</div><div class="sim-l">네이버 잃는 계좌개설</div></div>
      <div class="sim-d"><div class="sim-v" style="color:#4ade80">+381만건</div><div class="sim-l">구글 획득 계좌개설</div></div>
      <div class="sim-d"><div class="sim-v" style="color:#4ade80">+265%</div><div class="sim-l">순 효율 향상</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# 인사이트 1 차트: 채널별 광고비 vs 계좌개설 비중
fig1 = go.Figure()
channels = ["구글", "페이스북", "네이버검색"]
fig1.add_bar(name="광고비 비중", x=channels, y=[24.9, 42.4, 32.7],
             marker_color=["rgba(59,130,246,.35)","rgba(236,72,153,.35)","rgba(16,185,129,.35)"],
             marker_line_color=[C["blue"], C["pink"], C["green"]], marker_line_width=2,
             hovertemplate="%{x} 광고비: %{y}%<extra></extra>")
fig1.add_bar(name="계좌개설 비중", x=channels, y=[41.2, 44.0, 14.8],
             marker_color=[C["blue"], C["pink"], C["green"]],
             hovertemplate="%{x} 계좌개설: %{y}%<extra></extra>")
fig1.update_layout(**layout(
    barmode="group", height=230,
    yaxis=dict(gridcolor=C["grid"], ticksuffix="%", tickfont=dict(color=C["text"], size=10)),
    title=dict(text="채널별 광고비 비중 vs 계좌개설 비중 (%)", font=dict(color="#5a6072", size=11), x=0),
))
st.plotly_chart(fig1, use_container_width=True)

# ── 인사이트 2 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ic">
  <span class="icat" style="background:#2a1020;color:#f472b6;">채널</span>
  <div class="ititle">네이버는 CTR 11%로 최고이나 클릭→설치 전환율 최저 — 클릭 품질 이중 문제</div>
  <div class="ibody">
    네이버 CTR <b>11.08%</b>로 3채널 중 압도적이나 클릭→앱설치 전환율(CTI)은 <b>48.1%</b>로 최저.
    높은 CTR이 오히려 저품질 클릭 신호. CPI ₩2,280·CPA ₩4,262까지 최고 수준으로 이중 비효율.
    일반키워드 CPA ₩5,028은 구글 영상(₩1,119) 대비 <b>4.5배</b>.
  </div>
  <div class="db">
    <div class="dbt">근거 데이터</div>
    <div class="dr">
      <div class="dm"><div class="dmv" style="color:#f87171">11.08%</div><div class="dml">네이버 CTR</div></div>
      <div class="dm"><div class="dmv">0.63%</div><div class="dml">구글 CTR</div></div>
      <div class="dm"><div class="dmv">1.27%</div><div class="dml">페이스북 CTR</div></div>
      <div class="dm"><div class="dmv" style="color:#f87171">48.1%</div><div class="dml">네이버 CTI</div></div>
      <div class="dm"><div class="dmv" style="color:#4ade80">61.3%</div><div class="dml">구글 CTI</div></div>
      <div class="dm"><div class="dmv">55.1%</div><div class="dml">페이스북 CTI</div></div>
      <div class="dm"><div class="dmv" style="color:#f87171">₩5,028</div><div class="dml">네이버 일반KW CPA</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

fig2 = go.Figure()
fig2.add_bar(
    name="CTI (클릭→앱설치 전환율)",
    x=["구글", "페이스북", "네이버검색"],
    y=[61.3, 55.1, 48.1],
    marker_color=[C["blue"], C["pink"], C["green"]],
    hovertemplate="%{x} CTI: %{y}%<extra></extra>",
)
fig2.update_layout(**layout(
    showlegend=False, height=200,
    yaxis=dict(gridcolor=C["grid"], ticksuffix="%", range=[40, 70], tickfont=dict(color=C["text"], size=10)),
    title=dict(text="채널별 클릭→앱설치 전환율 CTI (%)", font=dict(color="#5a6072", size=11), x=0),
))
st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 퍼널 병목 인사이트 3 · 4
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">퍼널 병목</div>', unsafe_allow_html=True)

# ── 인사이트 3 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ic">
  <span class="icat" style="background:#2a0f0f;color:#f87171;">퍼널 · 볼륨 최대 이탈</span>
  <div class="ititle">클릭→앱설치 44% 이탈 — 최대 ₩119억 낭비 추산</div>
  <div class="ibody">
    클릭 후 미설치 인원 <b>2,058만명(43.8%)</b>. 클릭당 평균 비용 ₩581 기준 <b>최대 ₩119억 낭비 추산</b>.
    절대 이탈 볼륨 기준 전체 퍼널 중 최대. 앱스토어 페이지 최적화로 CTI 5%p 개선 시
    추가 광고비 없이 계좌개설 <b>+125만건</b> 가능.
  </div>
  <div class="note">₩119억은 전체 광고비가 CPC 방식이라고 가정한 상한 추산치. 실제 CPM 비중에 따라 달라질 수 있으나 CTI 개선 필요라는 방향성은 동일.</div>
  <div class="db">
    <div class="dbt">근거 데이터</div>
    <div class="dr">
      <div class="dm"><div class="dmv" style="color:#f87171">2,058만명</div><div class="dml">미설치 이탈</div></div>
      <div class="dm"><div class="dmv" style="color:#f87171">최대 ₩119억</div><div class="dml">낭비 추산 (CPC 기준 상한)</div></div>
      <div class="dm"><div class="dmv">₩581</div><div class="dml">평균 클릭당 비용</div></div>
      <div class="dm"><div class="dmv">4,703만건</div><div class="dml">총 광고클릭</div></div>
      <div class="dm"><div class="dmv" style="color:#4ade80">+125만건</div><div class="dml">CTI 5%p 개선 시 추가 계좌개설</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 인사이트 4: 퍼널 전 구간 ─────────────────────────────────────────────────
st.markdown("""
<div class="ic">
  <span class="icat" style="background:#261a0a;color:#fbbf24;">퍼널 · 전환율 병목</span>
  <div class="ititle">계좌개설→첫거래 51.2% — 전환율 기준 최저, 이탈 691만명</div>
  <div class="ibody">
    전환율 기준 계좌→첫거래(51.2%)가 퍼널 최저 단계. 이탈 <b>691만명</b>으로 절대 볼륨 두 번째.
    첫거래 전환율 51→60% 목표 시 <b>첫거래 +125만건</b> 추가 확보.
    볼륨 병목(인사이트 3)과 구분해 각각 앱스토어 최적화 vs 온보딩 넛지로 대응해야 함.
  </div>
  <div class="db">
    <div class="dbt">퍼널 전 구간 이탈 현황</div>""", unsafe_allow_html=True)

funnel_stages = [
    ("클릭→앱설치",    56,  "#2a0f0f", "#f87171",  "43.8%↓", "이탈 2,058만명"),
    ("앱실행→회원가입", 77,  "#0a1f12", "#4ade80",  "22.7%↓", "이탈 540만명"),
    ("회원→계좌개설",   77,  "#0a1f12", "#4ade80",  "23.1%↓", "이탈 424만명"),
    ("계좌→첫거래 ★",  51,  "#261a0a", "#fbbf24",  "48.8%↓", "이탈 691만명"),
    ("반복→자동이체",   22,  "#2a0f0f", "#f87171",  "78.1%↓", "이탈 360만명"),
]
for label, pct, bg, color, down, note in funnel_stages:
    st.markdown(f"""
    <div class="fr">
      <span class="fl">{label}</span>
      <div class="fbg">
        <div class="ff" style="width:{pct}%;background:{bg};color:{color};">{pct}% 전환</div>
      </div>
      <span class="fp" style="color:{color};">{down}</span>
      <span class="fc">{note}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 퍼널 시각화 (Plotly funnel)
funnel_data = {
    "stage":  ["광고클릭", "앱설치", "앱실행", "회원가입", "계좌개설", "첫거래", "반복사용", "자동이체설정"],
    "count":  [4703, 2644, 2380, 1840, 1416, 724, 461, 101],
}
df_f = pd.DataFrame(funnel_data)
fig_fn = go.Figure(go.Funnel(
    y=df_f["stage"], x=df_f["count"],
    textinfo="value+percent previous",
    marker=dict(color=[C["blue"], "#6366f1", "#8b5cf6", C["green"], C["green"], C["amber"], "#f97316", C["red"]]),
    connector=dict(line=dict(color="#1a1d2a", width=1)),
    hovertemplate="%{y}: %{x}만명 (%{percentPrevious:.1%})<extra></extra>",
))
fig_fn.update_layout(**layout(
    showlegend=False, height=320,
    title=dict(text="전체 퍼널 전환 현황 (단위: 만명)", font=dict(color="#5a6072", size=11), x=0),
    yaxis=dict(tickfont=dict(color=C["text"], size=11), gridcolor="rgba(0,0,0,0)"),
))
st.plotly_chart(fig_fn, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 타겟팅 & 크리에이티브 인사이트 5 · 6
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">타겟팅 & 크리에이티브</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="ic" style="height:100%;">
      <span class="icat" style="background:#0a1f12;color:#4ade80;">타겟팅</span>
      <div class="ititle">리타겟이 논타겟 대비 CPA 23% 절감 — CPM 더 비싸지만 CTI 높아 역전</div>
      <div class="ibody">
        리타겟 CPM ₩6,781로 논타겟(₩5,223)보다 <b>30% 비싸지만</b>,
        클릭→설치 전환율(CTI) <b>62.5% vs 48.1%</b>로 높아 CPI ₩930 vs ₩1,207로 역전.
        CPA도 <b>₩1,737 vs ₩2,255</b>로 23% 절감. 채널 무관 일관된 우위.
      </div>
      <div class="db">
        <div class="dbt">근거 데이터</div>
        <div class="dr">
          <div class="dm"><div class="dmv" style="color:#f87171">₩6,781</div><div class="dml">리타겟 CPM</div></div>
          <div class="dm"><div class="dmv">₩5,223</div><div class="dml">논타겟 CPM</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">62.5%</div><div class="dml">리타겟 CTI</div></div>
          <div class="dm"><div class="dmv">48.1%</div><div class="dml">논타겟 CTI</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">₩930</div><div class="dml">리타겟 CPI</div></div>
          <div class="dm"><div class="dmv">₩1,207</div><div class="dml">논타겟 CPI</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">₩1,737</div><div class="dml">리타겟 CPA</div></div>
          <div class="dm"><div class="dmv">₩2,255</div><div class="dml">논타겟 CPA</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    fig5 = go.Figure()
    fig5.add_bar(name="논타겟", x=["CPM(₩)", "CPI(₩)", "CPA(₩)"],
                 y=[5223, 1207, 2255], marker_color="rgba(107,114,128,.7)")
    fig5.add_bar(name="리타겟", x=["CPM(₩)", "CPI(₩)", "CPA(₩)"],
                 y=[6781, 930, 1737], marker_color=C["green"])
    fig5.update_layout(**layout(barmode="group", height=220, showlegend=True,
        yaxis=dict(gridcolor=C["grid"], tickprefix="₩", tickfont=dict(color=C["text"], size=10))))
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown("""
    <div class="ic" style="height:100%;">
      <span class="icat" style="background:#1e1a30;color:#c084fc;">크리에이티브</span>
      <div class="ititle">영상이 이미지보다 CPI 9% 낮고 계좌개설 31% 더 많음</div>
      <div class="ibody">
        영상 CPI <b>₩784</b> / CPA <b>₩1,463</b>. 이미지 CPI ₩860 / CPA ₩1,607.
        계좌개설 영상 <b>684만 vs 이미지 522만으로 31% 차이</b>.
        네이버 키워드는 영상 대비 CPI 2.6~3.4배. 영상 제작비가 허용되는 범위에서 영상 비중 확대가 ROI에 직결.
      </div>
      <div class="db">
        <div class="dbt">근거 데이터</div>
        <div class="dr">
          <div class="dm"><div class="dmv" style="color:#4ade80">₩784</div><div class="dml">영상 CPI</div></div>
          <div class="dm"><div class="dmv">₩860</div><div class="dml">이미지 CPI</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">₩1,463</div><div class="dml">영상 CPA</div></div>
          <div class="dm"><div class="dmv">₩1,607</div><div class="dml">이미지 CPA</div></div>
          <div class="dm"><div class="dmv">684만</div><div class="dml">영상 계좌개설</div></div>
          <div class="dm"><div class="dmv">522만</div><div class="dml">이미지 계좌개설</div></div>
          <div class="dm"><div class="dmv" style="color:#f87171">₩5,028</div><div class="dml">일반KW CPA</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    fig6 = go.Figure(go.Bar(
        x=["영상", "이미지", "브랜드키워드", "일반키워드"],
        y=[784, 860, 2071, 2690],
        marker_color=[C["green"], C["blue"], C["amber"], C["red"]],
        hovertemplate="CPI: ₩%{y:,}<extra></extra>",
    ))
    fig6.update_layout(**layout(showlegend=False, height=220,
        yaxis=dict(gridcolor=C["grid"], tickprefix="₩", tickfont=dict(color=C["text"], size=10)),
        title=dict(text="포맷별 CPI 비교", font=dict(color="#5a6072", size=11), x=0),
    ))
    st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 캠페인 설계 & 예산 배분 인사이트 7 · 8
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">캠페인 설계 & 예산 배분</div>', unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    st.markdown("""
    <div class="ic">
      <span class="icat" style="background:#1a2744;color:#60a5fa;">전략</span>
      <div class="ititle">계좌개설 목적 캠페인이 하류 전환율 더 높음 — 의도 높은 사용자 유입 효과</div>
      <div class="ibody">
        계좌개설 목적: 계좌→첫거래 <b>60%</b>, 첫거래→반복 <b>72%</b>.
        회원가입 목적: 각각 40%, 48%로 <b>20~24%p 낮음</b>.
        CPA도 계좌개설 목적 ₩1,740 vs 회원가입 목적 ₩2,171로 20% 절감.
      </div>
      <div class="db">
        <div class="dbt">근거 데이터</div>
        <div class="dr">
          <div class="dm"><div class="dmv" style="color:#60a5fa">60%</div><div class="dml">계좌개설 목적 · 계좌→첫거래</div></div>
          <div class="dm"><div class="dmv" style="color:#f87171">40%</div><div class="dml">회원가입 목적 · 계좌→첫거래</div></div>
          <div class="dm"><div class="dmv" style="color:#60a5fa">72%</div><div class="dml">계좌개설 목적 · 첫거래→반복</div></div>
          <div class="dm"><div class="dmv" style="color:#f87171">48%</div><div class="dml">회원가입 목적 · 첫거래→반복</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">₩1,740</div><div class="dml">계좌개설 목적 CPA</div></div>
          <div class="dm"><div class="dmv">₩2,171</div><div class="dml">회원가입 목적 CPA</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    fig7 = go.Figure()
    stages7 = ["계좌→첫거래", "첫거래→반복사용"]
    fig7.add_bar(name="계좌개설 목적", x=stages7, y=[60, 72], marker_color="rgba(59,130,246,.8)")
    fig7.add_bar(name="회원가입 목적", x=stages7, y=[40, 48], marker_color="rgba(236,72,153,.8)")
    fig7.update_layout(**layout(barmode="group", height=220,
        yaxis=dict(gridcolor=C["grid"], ticksuffix="%", range=[0, 90], tickfont=dict(color=C["text"], size=10))))
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.markdown("""
    <div class="ic">
      <span class="icat" style="background:#261a0a;color:#fbbf24;">예산 배분</span>
      <div class="ititle">예산 증가 → CPI 상승 (r=0.963) — 급격한 스케일업이 단가를 올림</div>
      <div class="ibody">
        CPI와 월 광고비 상관계수 <b>r=0.963, r²=0.93</b>. 광고비 변동이 CPI 변동의 <b>93%를 설명</b>.
        저예산 월(20억 미만) 평균 CPI ₩899 vs 고예산 월 ₩1,104로 <b>22.7% 차이</b>.
        예산 배분 자체보다 <b>점진적 스케일업</b>으로 단가 상승을 완화해야 함.
      </div>
      <div class="db">
        <div class="dbt">근거 데이터</div>
        <div class="dr">
          <div class="dm"><div class="dmv">r=0.963</div><div class="dml">광고비↔CPI 상관계수</div></div>
          <div class="dm"><div class="dmv">r²=0.93</div><div class="dml">CPI 변동 설명력</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">₩899</div><div class="dml">저예산 월 평균 CPI</div></div>
          <div class="dm"><div class="dmv" style="color:#f87171">₩1,104</div><div class="dml">고예산 월 평균 CPI</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">₩870</div><div class="dml">1월 CPI 최저</div></div>
          <div class="dm"><div class="dmv" style="color:#f87171">₩1,265</div><div class="dml">12월 CPI 최고</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    months = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]
    cpi_m  = [870,945,1114,966,1011,896,872,913,1157,1060,1152,1265]
    budget_m = [16.9,17.0,29.2,20.2,22.8,17.3,16.8,18.7,31.0,24.4,25.4,33.5]
    fig8 = go.Figure()
    fig8.add_scatter(name="CPI (₩)", x=months, y=cpi_m,
                     line=dict(color=C["blue"], width=2.5), fill="tozeroy",
                     fillcolor="rgba(59,130,246,.08)", mode="lines+markers",
                     yaxis="y", hovertemplate="CPI: ₩%{y:,}<extra></extra>")
    fig8.add_scatter(name="광고비 (억원)", x=months, y=budget_m,
                     line=dict(color="#374151", width=1.5, dash="dash"),
                     mode="lines+markers", yaxis="y2",
                     hovertemplate="%{y}억<extra></extra>")
    fig8.update_layout(**layout(height=240,
        yaxis=dict(gridcolor=C["grid"], tickprefix="₩", tickfont=dict(color=C["blue"], size=10)),
        yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(0,0,0,0)",
                    ticksuffix="억", tickfont=dict(color="#6b7280", size=10)),
    ))
    st.plotly_chart(fig8, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 제품 & 성장 인사이트 9 · 10
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">제품 & 성장</div>', unsafe_allow_html=True)

col9, col10 = st.columns(2)

with col9:
    st.markdown("""
    <div class="ic">
      <span class="icat" style="background:#2a0f0f;color:#f87171;">제품 UX</span>
      <div class="ititle">자동이체 설정률 3.8% — 전 채널 동일, 360만명 이탈은 제품 UX 문제</div>
      <div class="ibody">
        반복사용자 461만명 중 자동이체 설정 완료 21.9%뿐. <b>360만명(78.1%)</b>이 이탈.
        구글 3.84% / 페이스북 3.82% / 네이버 3.82%로 채널·포맷과 <b>완전히 무관</b>.
        광고 최적화로는 해결 불가. 설정률 3.8→6% 목표 시 자동이체 <b>+10만건</b> 추가 가능.
      </div>
      <div class="db">
        <div class="dbt">근거 데이터</div>
        <div class="dr">
          <div class="dm"><div class="dmv" style="color:#f87171">78.1%</div><div class="dml">반복사용자 중 미설정</div></div>
          <div class="dm"><div class="dmv" style="color:#f87171">360만명</div><div class="dml">이탈 절대 규모</div></div>
          <div class="dm"><div class="dmv">3.84%</div><div class="dml">구글 자동이체율</div></div>
          <div class="dm"><div class="dmv">3.82%</div><div class="dml">페이스북 자동이체율</div></div>
          <div class="dm"><div class="dmv">3.82%</div><div class="dml">네이버 자동이체율</div></div>
          <div class="dm"><div class="dmv">461만명</div><div class="dml">반복사용자 모수</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    fig9a = go.Figure()
    ch = ["구글", "페이스북", "네이버검색"]
    fig9a.add_bar(name="자동이체 설정률", x=ch, y=[3.84, 3.82, 3.82], marker_color=C["amber"])
    fig9a.add_bar(name="추천 완료율", x=ch, y=[10.99, 10.97, 10.86], marker_color=C["purple"])
    fig9a.update_layout(**layout(barmode="group", height=200,
        yaxis=dict(gridcolor=C["grid"], ticksuffix="%", tickfont=dict(color=C["text"], size=10)),
        title=dict(text="채널별 자동이체 설정률 & 추천 완료율 (%)", font=dict(color="#5a6072", size=11), x=0),
    ))
    st.plotly_chart(fig9a, use_container_width=True)

with col10:
    st.markdown("""
    <div class="ic">
      <span class="icat" style="background:#0a1f12;color:#4ade80;">성장</span>
      <div class="ititle">추천 전환율 11% — 채널 무관, 서비스 만족도에 의존</div>
      <div class="ibody">
        반복사용자 중 추천 완료율 구글 10.99% / 페이스북 10.97% / 네이버 10.86%로 <b>전 채널 거의 동일</b>.
        자동이체→추천 전환도 구글 50.1% / 네이버 49.6%로 동일. 광고 타겟팅·크리에이티브와 무관.
        리퍼럴 확대를 원한다면 <b>서비스 경험(혜택 설계·추천 플로우 UX) 개선</b>이 선행 필요.
      </div>
      <div class="db">
        <div class="dbt">근거 데이터</div>
        <div class="dr">
          <div class="dm"><div class="dmv">10.99%</div><div class="dml">구글 추천율</div></div>
          <div class="dm"><div class="dmv">10.97%</div><div class="dml">페이스북 추천율</div></div>
          <div class="dm"><div class="dmv">10.86%</div><div class="dml">네이버 추천율</div></div>
          <div class="dm"><div class="dmv" style="color:#4ade80">506만명</div><div class="dml">연간 추천 완료</div></div>
          <div class="dm"><div class="dmv">461만명</div><div class="dml">반복사용자 모수</div></div>
          <div class="dm"><div class="dmv">50.1%</div><div class="dml">자동이체→추천 전환</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    growth_labels = ["반복사용자", "자동이체설정", "추천완료"]
    growth_vals   = [461, 101, 51]
    fig10 = go.Figure(go.Bar(
        x=growth_labels, y=growth_vals,
        marker_color=[C["green"], C["amber"], C["purple"]],
        text=[f"{v}만명" for v in growth_vals],
        textposition="outside",
        textfont=dict(color=C["text"], size=10),
        hovertemplate="%{x}: %{y}만명<extra></extra>",
    ))
    fig10.update_layout(**layout(showlegend=False, height=200,
        yaxis=dict(gridcolor=C["grid"], ticksuffix="만", tickfont=dict(color=C["text"], size=10)),
        title=dict(text="성장 퍼널 후단 (만명)", font=dict(color="#5a6072", size=11), x=0),
    ))
    st.plotly_chart(fig10, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 액션플랜
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec">액션플랜</div>', unsafe_allow_html=True)
st.markdown("""
<div class="abox">
  <b>임팩트 순 우선순위 3가지</b><br>
  1. 앱스토어 최적화 — 추가 광고비 없이 CTI 5%p 개선 시 계좌개설 +125만건 (인사이트 3)<br>
  2. 계좌 후 첫거래 온보딩 강화 — 7일 이내 넛지·혜택 설계, 전환율 51→60% 목표, +125만건 (인사이트 4)<br>
  3. 네이버→구글 예산 50% 이전 — 동일 예산으로 계좌개설 순 +277만건, 효율 +265% (인사이트 1·2)
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
