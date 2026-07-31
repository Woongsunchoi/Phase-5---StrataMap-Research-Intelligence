import pandas as pd


def filter_ranking(
    table: pd.DataFrame,
    search: str = "",
    institutions: list[str] | None = None,
    tiers: list[str] | None = None,
    segments: list[str] | None = None,
) -> pd.DataFrame:
    result = table.copy()
    if search.strip():
        term = search.strip().casefold()
        mask = result["name"].fillna("").str.casefold().str.contains(term, regex=False)
        mask |= result["institution"].fillna("").str.casefold().str.contains(term, regex=False)
        result = result[mask]
    if institutions:
        result = result[result["institution"].isin(institutions)]
    if tiers:
        result = result[result["tier"].isin(tiers)]
    if segments:
        result = result[result["segment"].isin(segments)]
    return result.sort_values(["commercial_priority_score", "name"], ascending=[False, True])


def display_ranking(table: pd.DataFrame) -> pd.DataFrame:
    return table[
        ["commercial_rank", "name", "institution", "commercial_priority_score", "tier", "segment"]
    ].rename(
        columns={
            "commercial_rank": "순위",
            "name": "연구자명",
            "institution": "기관",
            "commercial_priority_score": "Commercial Priority Score",
            "tier": "Tier",
            "segment": "Segment",
        }
    )
