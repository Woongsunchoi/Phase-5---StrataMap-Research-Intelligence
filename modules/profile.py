import pandas as pd


def get_profile(researcher_id: str, profile: pd.DataFrame, master: pd.DataFrame) -> dict:
    row = profile.loc[profile["researcher_id"] == researcher_id]
    if row.empty:
        raise KeyError("선택한 연구자의 설명 프로필을 찾을 수 없습니다.")
    record = row.iloc[0].to_dict()
    master_row = master.loc[master["researcher_id"] == researcher_id]
    if not master_row.empty:
        record.update(master_row.iloc[0].to_dict())
    return record


def split_explanations(value: object) -> list[str]:
    if pd.isna(value) or not str(value).strip():
        return []
    return [item.strip() for item in str(value).split("|") if item.strip()]


def korean_driver(text: str) -> str:
    mapping = {
        "High technology adoption index": "높은 Technology Adoption Index",
        "High spatial-transcriptomics evidence": "풍부한 Spatial Transcriptomics 연구 evidence",
        "Strong single-cell activity": "활발한 Single-cell 연구 활동",
        "High recent research momentum": "높은 최근 연구 활동성",
        "Strong collaboration network": "강한 연구 협업 네트워크",
        "Strong institutional environment": "강한 기관 연구 환경",
        "Balanced profile without a dominant top-quartile driver": "여러 연구 지표가 균형적인 프로필",
    }
    return mapping.get(text, text)


def korean_consideration(text: str) -> str:
    mapping = {
        "Low technology evidence": "제한적인 기술 evidence",
        "Limited spatial-transcriptomics evidence": "제한적인 Spatial Transcriptomics evidence",
        "Limited single-cell activity": "제한적인 Single-cell 활동",
        "Low recent research momentum": "낮은 최근 연구 활동성",
        "Limited observed collaboration-network signal": "관찰된 협업 네트워크 signal이 제한적",
        "Limited institutional signal": "기관 signal이 제한적",
        "No bottom-quartile consideration among reviewed signals": "검토된 지표에서 뚜렷한 하위 사분위 고려사항 없음",
    }
    return mapping.get(text, text)
