from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_margem_receita(df, last_n=None):
    data = df.tail(last_n) if last_n else df
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_bar(
        x=data["data"],
        y=data["receita"],
        name="Receita",
        marker_color="#2E86DE",
        opacity=0.85,
        secondary_y=False,
    )

    fig.add_scatter(
        x=data["data"],
        y=data["margem"],
        name="Margem",
        mode="lines+markers",
        line=dict(color="#E74C3C", width=2),
        marker=dict(size=6),
        secondary_y=True,
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=10, r=10, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.2,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Receita", gridcolor="rgba(0,0,0,0.08)", secondary_y=False)
    fig.update_yaxes(title_text="Margem", gridcolor="rgba(0,0,0,0.08)", secondary_y=True)
    return fig
