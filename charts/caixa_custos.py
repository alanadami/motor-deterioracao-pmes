import plotly.graph_objects as go


def plot_caixa_custos(df, recent_window, last_n=None):
    data = df.tail(last_n) if last_n else df
    custos_media = data["custos"].rolling(recent_window, min_periods=1).mean()

    fig = go.Figure()
    fig.add_scatter(
        x=data["data"],
        y=data["caixa"],
        mode="lines+markers",
        name="Caixa",
        line=dict(color="#2E86DE", width=2),
        marker=dict(size=6),
    )
    fig.add_scatter(
        x=data["data"],
        y=custos_media,
        mode="lines",
        name=f"Custos médios ({recent_window}m)",
        line=dict(color="#E67E22", width=2, dash="dash"),
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=10, r=10, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.08)")
    return fig
