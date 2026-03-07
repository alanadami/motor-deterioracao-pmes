import pandas as pd
import plotly.graph_objects as go


def plot_ifc(df, coverage_override, recent_window, baseline_label=None, last_n=None):
    data = df.tail(last_n) if last_n else df
    custos_roll = data["custos"].rolling(recent_window, min_periods=1).mean()
    cobertura = data["caixa"] / custos_roll.replace(0, pd.NA)
    fig = go.Figure()
    fig.add_scatter(
        x=data["data"],
        y=cobertura,
        mode="lines+markers",
        name="Cobertura (meses)",
        line=dict(color="#6C5CE7", width=2),
        marker=dict(size=6),
    )
    fig.add_scatter(
        x=data["data"],
        y=[coverage_override] * len(data),
        mode="lines",
        name=baseline_label or "Mínimo estrutural",
        line=dict(color="#E74C3C", dash="dash", width=2),
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
