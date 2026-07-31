from datetime import datetime

import networkx as nx
import pandas as pd
import plotly.graph_objects as go


def create_network_figure(
    selected_id: str,
    edges: pd.DataFrame,
    researcher_table: pd.DataFrame,
    max_neighbors: int = 24,
) -> tuple[go.Figure, pd.DataFrame]:
    relevant = edges[(edges["researcher_id_a"] == selected_id) | (edges["researcher_id_b"] == selected_id)].copy()
    relevant = relevant.sort_values("joint_publication_count", ascending=False).head(max_neighbors)
    if relevant.empty:
        return _empty_figure("선택한 연구자의 후보군 내 협업 연결이 없습니다."), relevant

    graph = nx.Graph()
    for row in relevant.itertuples(index=False):
        graph.add_edge(
            str(row.researcher_id_a),
            str(row.researcher_id_b),
            weight=float(row.joint_publication_count),
            latest_year=row.latest_joint_year,
        )
    positions = nx.spring_layout(graph, seed=42, weight="weight", k=1.2)
    names = researcher_table.set_index("researcher_id")["name"].to_dict()

    edge_x, edge_y = [], []
    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1.2, color="#B8C4CE"), hoverinfo="skip")

    node_x, node_y, labels, hover, colors, sizes = [], [], [], [], [], []
    recent_cutoff = datetime.now().year - 3
    for node in graph.nodes():
        x, y = positions[node]
        node_x.append(x); node_y.append(y)
        labels.append(names.get(node, node))
        colors.append("#C8753D" if node == selected_id else "#0F8B8D")
        sizes.append(30 if node == selected_id else 17)
        if node == selected_id:
            hover.append(f"<b>{names.get(node, node)}</b><br>선택 연구자")
        else:
            edge = graph.edges[selected_id, node]
            latest = edge.get("latest_year")
            recent = "예" if pd.notna(latest) and float(latest) >= recent_cutoff else "아니오"
            hover.append(
                f"<b>{names.get(node, node)}</b><br>공저 논문 수: {int(edge['weight'])}"
                f"<br>최근 협업: {recent}<br>최근 협업 연도: {int(latest) if pd.notna(latest) else '정보 없음'}"
            )
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=labels, textposition="top center",
        hovertext=hover, hoverinfo="text", marker=dict(size=sizes, color=colors, line=dict(width=1.5, color="white")),
        textfont=dict(size=10, color="#17324D"),
    )
    fig = go.Figure([edge_trace, node_trace])
    fig.update_layout(
        height=650, margin=dict(l=10, r=10, t=35, b=10), showlegend=False,
        plot_bgcolor="white", paper_bgcolor="white", hovermode="closest",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        title="후보 연구자군 내 공저 관계",
    )
    return fig, relevant


def _empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="#64748B"))
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False); fig.update_layout(height=500)
    return fig
