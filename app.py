from pathlib import Path

import streamlit as st

from modules.data_loader import build_researcher_table, load_data
from modules.network import create_network_figure
from modules.profile import get_profile, korean_consideration, korean_driver, split_explanations
from modules.ranking import display_ranking, filter_ranking
from modules.visualization import priority_matrix, ranking_chart, score_distribution

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo.png"

st.set_page_config(page_title="StrataMap Research Intelligence Platform", page_icon=str(LOGO), layout="wide")
st.markdown(
    """
    <style>
      .stApp { background: #F7F9FA; color: #17324D; }
      .block-container { max-width: 1320px; padding-top: 2rem; }
      [data-testid="stMetric"] { background: white; border: 1px solid #E3E8EC; border-radius: 16px; padding: 18px; box-shadow: 0 4px 16px rgba(23,50,77,.05); }
      .hero { background: linear-gradient(135deg,#17324D,#24577A); color:white; padding:30px 34px; border-radius:22px; margin-bottom:18px; }
      .hero h1 { margin:0 0 8px 0; font-size:2.1rem; }
      .hero p { margin:0; color:#DCE8EF; font-size:1.05rem; line-height:1.6; }
      .profile-card { background:white; border:1px solid #E3E8EC; border-radius:18px; padding:22px; }
      .credit { text-align:center; color:#64748B; margin-top:42px; padding:22px 0; border-top:1px solid #DDE4E8; line-height:1.7; }
      .small-note { color:#64748B; font-size:.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    data = load_data()
    researchers = build_researcher_table()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"데이터를 불러올 수 없습니다. 관리자에게 문의해 주세요.\n\n{exc}")
    st.stop()

header_logo, header_text = st.columns([1, 7], vertical_alignment="center")
with header_logo:
    st.image(str(LOGO), width=112)
with header_text:
    st.markdown(
        """<div class="hero"><h1>StrataMap Research Intelligence Platform</h1>
        <p>공개 연구 데이터를 기반으로 한<br>Spatial Transcriptomics 연구자 분석 플랫폼</p></div>""",
        unsafe_allow_html=True,
    )

institution_count = researchers["institution"].nunique()
c1, c2, c3 = st.columns(3)
c1.metric("분석 연구자 수", f"{len(researchers)}명")
c2.metric("기관 수", f"{institution_count}개")
c3.metric("Data Version", "2026")

home_tab, ranking_tab, profile_tab, network_tab = st.tabs(["홈", "연구자 Ranking", "연구자 Profile", "Network Map"])

with home_tab:
    st.subheader("플랫폼 소개")
    st.write("한국 Spatial Transcriptomics 및 Single-cell 연구 생태계를 공개 연구 데이터로 구조화하고, 연구 영향력·기술 활동·협업 관계를 함께 탐색하는 Research Intelligence MVP입니다.")
    st.info("본 플랫폼은 구매 확률 또는 전환 예측 시스템이 아닙니다. 공개 연구 evidence를 기반으로 과학적·상업적 검토 순서를 지원합니다.")
    st.subheader("데이터와 방법론")
    cols = st.columns(4)
    phases = [
        ("Phase 1", "Master Dataset", "158명 연구자의 identity, publication, institution, technology evidence를 통합했습니다."),
        ("Phase 2", "Research Intelligence Features", "Research Impact, Technology Adoption, Momentum, Network, Institution 차원을 구성했습니다."),
        ("Phase 3", "Dual Scoring Model", "Expert 가중 모델과 PCA 기반 Statistical 모델을 독립적으로 비교했습니다."),
        ("Phase 4", "Commercial Prioritization", "두 관점을 결합하고 segment, tier, 설명 프로필을 생성했습니다."),
    ]
    for col, (phase, title, text) in zip(cols, phases):
        with col:
            st.markdown(f"<div class='profile-card'><b>{phase}</b><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)
    st.subheader("우선순위 개요")
    left, right = st.columns([1.1, 1])
    with left: st.plotly_chart(ranking_chart(researchers), width="stretch", config={"displayModeBar": False})
    with right: st.plotly_chart(score_distribution(researchers), width="stretch", config={"displayModeBar": False})

with ranking_tab:
    st.subheader("연구자 우선순위")
    f1, f2, f3, f4 = st.columns([1.2, 1, .8, 1])
    search = f1.text_input("검색", placeholder="연구자명 또는 기관")
    institutions = f2.multiselect("기관", sorted(researchers["institution"].dropna().unique()))
    tiers = f3.multiselect("Tier", ["Tier S", "Tier A", "Tier B", "Tier C"])
    segments = f4.multiselect("Segment", ["Strategic Target", "Academic Leader", "Emerging Adopter", "Low Priority"])
    filtered = filter_ranking(researchers, search, institutions, tiers, segments)
    st.caption(f"검색 결과 {len(filtered)}명 · Score 내림차순")
    st.dataframe(
        display_ranking(filtered), hide_index=True, width="stretch", height=560,
        column_config={
            "Commercial Priority Score": st.column_config.ProgressColumn("Commercial Priority Score", min_value=0, max_value=100, format="%.1f"),
            "순위": st.column_config.NumberColumn("순위", format="%d"),
        },
    )
    st.plotly_chart(ranking_chart(filtered, min(20, len(filtered))) if len(filtered) else ranking_chart(researchers.head(0)), width="stretch", config={"displayModeBar": False})

with profile_tab:
    st.subheader("연구자 상세 프로필")
    options = researchers.assign(label=researchers["name"] + " · " + researchers["institution"])
    selected_label = st.selectbox("연구자 선택", options["label"], index=0)
    selected_id = options.loc[options["label"] == selected_label, "researcher_id"].iloc[0]
    profile = get_profile(selected_id, data["profile"], data["master"])
    st.markdown(f"<div class='profile-card'><h2>{profile['name']}</h2><p>{profile['institution']}</p></div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Commercial Priority Score", f"{profile['commercial_priority_score']:.1f}")
    m2.metric("Tier", profile["tier"])
    m3.metric("Segment", profile["segment"])
    m4, m5 = st.columns(2)
    m4.metric("Research Intelligence Score", f"{profile['research_intelligence_score']:.1f}")
    m5.metric("Technology Adoption Score", f"{profile['technology_adoption_score']:.1f}")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("#### 추천 이유")
        for item in split_explanations(profile.get("key_drivers")): st.success("✓ " + korean_driver(item))
    with d2:
        st.markdown("#### Potential considerations")
        for item in split_explanations(profile.get("considerations")): st.warning("△ " + korean_consideration(item))
    st.markdown("#### 연구 evidence")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Publications", int(profile.get("publication_count", 0)))
    e2.metric("H-index", int(profile.get("h_index", 0)))
    e3.metric("Spatial evidence", int(profile.get("spatial_transcriptomics_count", 0)))
    e4.metric("Single-cell evidence", int(profile.get("single_cell_count", 0)))

with network_tab:
    st.subheader("연구자 관계 Network Map")
    network_label = st.selectbox("중심 연구자 선택", options["label"], index=0, key="network_researcher")
    network_id = options.loc[options["label"] == network_label, "researcher_id"].iloc[0]
    max_neighbors = st.slider("표시할 최대 연결 연구자 수", 5, 40, 24)
    fig, related_edges = create_network_figure(network_id, data["network"], researchers, max_neighbors)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption(f"후보 연구자군 내부 연결 {len(related_edges)}개를 표시합니다. 선은 공저 관계이며 tooltip에서 공저 논문 수와 최근 협업 여부를 확인할 수 있습니다.")
    st.plotly_chart(priority_matrix(data["segment"]), width="stretch", config={"displayModeBar": False})

st.markdown("<div class='credit'>Developed by Woongsun Choi<br>Illumina Korea<br>2026</div>", unsafe_allow_html=True)
