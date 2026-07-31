from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

FILES = {
    "master": "master_dataset.csv",
    "priority": "hybrid_priority_score.csv",
    "segment": "commercial_segment.csv",
    "tier": "commercial_tier.csv",
    "profile": "researcher_explanation_profile.csv",
    "network": "network_edge.csv",
}

REQUIRED_COLUMNS = {
    "priority": {"researcher_id", "name", "institution", "commercial_priority_score", "commercial_rank"},
    "segment": {"researcher_id", "segment"},
    "tier": {"researcher_id", "tier"},
    "profile": {"researcher_id", "research_intelligence_score", "technology_adoption_score", "key_drivers", "considerations"},
    "network": {"researcher_id_a", "researcher_id_b", "joint_publication_count", "latest_joint_year"},
}


@st.cache_data(show_spinner=False)
def load_data() -> dict[str, pd.DataFrame]:
    missing = [name for name in FILES.values() if not (DATA_DIR / name).exists()]
    if missing:
        raise FileNotFoundError("필수 데이터 파일이 없습니다: " + ", ".join(missing))

    data = {key: pd.read_csv(DATA_DIR / filename) for key, filename in FILES.items()}
    for key, required in REQUIRED_COLUMNS.items():
        absent = required - set(data[key].columns)
        if absent:
            raise ValueError(f"{FILES[key]}에 필수 컬럼이 없습니다: {', '.join(sorted(absent))}")
    return data


@st.cache_data(show_spinner=False)
def build_researcher_table() -> pd.DataFrame:
    data = load_data()
    table = (
        data["priority"]
        .merge(data["tier"][["researcher_id", "tier"]], on="researcher_id", validate="one_to_one")
        .merge(data["segment"][["researcher_id", "segment"]], on="researcher_id", validate="one_to_one")
        .sort_values("commercial_rank")
    )
    if len(table) != 158 or table["researcher_id"].nunique() != 158:
        raise ValueError("연구자 데이터가 158명과 일치하지 않습니다.")
    return table
