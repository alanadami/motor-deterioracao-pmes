import pandas as pd
from config import HIST_WINDOW_MIN, HIST_WINDOW_MAX, RECENT_WINDOW


def validate_minimum_history(df: pd.DataFrame):
    if len(df) < HIST_WINDOW_MIN:
        raise ValueError(
            f"Histórico insuficiente. Necessário pelo menos {HIST_WINDOW_MIN} meses."
        )
    return True


def calculate_historical_median(series: pd.Series):
    if len(series) > HIST_WINDOW_MAX:
        series = series.tail(HIST_WINDOW_MAX)
    return series.median()


def calculate_recent_mean(series: pd.Series):
    if len(series) < RECENT_WINDOW:
        return series.mean()
    return series.tail(RECENT_WINDOW).mean()