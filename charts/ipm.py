import plotly.graph_objects as go


def plot_ipm(df, baseline_margem, baseline_label=None, last_n=None):
    data = df.tail(last_n) if last_n else df
    colors = ["#E74C3C" if v < baseline_margem else "#2E86DE" for v in data["margem"]]
    fig = go.Figure()
    fig.add_bar(
        x=data["data"],
        y=data["margem"],
        marker_color=colors,
        name="Margem",
        marker_line_width=0,
        opacity=0.9,
    )
    fig.add_scatter(
        x=data["data"],
        y=[baseline_margem] * len(data),
        mode="lines",
        name=baseline_label or "Baseline",
        line=dict(color="#1C1E21", dash="dash", width=2),
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=10, r=10, t=40, b=20),
        bargap=0.2,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.08)")
    return fig
