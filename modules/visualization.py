import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

SEGMENT_COLORS = {
    "Strategic Target": "#C8753D",
    "Academic Leader": "#24577A",
    "Emerging Adopter": "#5F8D6A",
    "Low Priority": "#9AA4AD",
}


def ranking_chart(table: pd.DataFrame, top_n: int = 15) -> go.Figure:
    data = table.nsmallest(top_n, "commercial_rank").sort_values("commercial_priority_score")
    fig = px.bar(data, x="commercial_priority_score", y="name", orientation="h", color="segment", color_discrete_map=SEGMENT_COLORS)
    fig.update_layout(height=520, xaxis_title="Commercial Priority Score", yaxis_title=None, legend_title=None, margin=dict(l=10, r=10, t=20, b=10))
    return fig


def priority_matrix(segment: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        segment, x="expert_score", y="statistical_score", color="segment", hover_name="name",
        hover_data={"institution": True, "expert_score": ":.1f", "statistical_score": ":.1f"},
        color_discrete_map=SEGMENT_COLORS,
    )
    fig.add_vline(x=segment["expert_score"].median(), line_dash="dot", line_color="#94A3B8")
    fig.add_hline(y=segment["statistical_score"].median(), line_dash="dot", line_color="#94A3B8")
    fig.update_layout(height=540, xaxis_title="Expert Adoption Score", yaxis_title="Statistical Research Intelligence Score", legend_title=None, margin=dict(l=10, r=10, t=20, b=10))
    return fig


def score_distribution(table: pd.DataFrame) -> go.Figure:
    fig = px.histogram(table, x="commercial_priority_score", nbins=18, color_discrete_sequence=["#0F8B8D"])
    fig.update_layout(height=360, xaxis_title="Commercial Priority Score", yaxis_title="연구자 수", bargap=0.06, margin=dict(l=10, r=10, t=20, b=10))
    return fig
