import numpy as np

def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(value, max_value))


def proportion_below(series, baseline):
    """
    Proporção de valores abaixo do baseline.
    """
    if len(series) == 0:
        return 0.0
    count = np.sum(series < baseline)
    return count / len(series)


def max_consecutive_below(series, baseline):
    """
    Maior sequência consecutiva abaixo do baseline.
    """
    max_seq = 0
    current_seq = 0

    for value in series:
        if value < baseline:
            current_seq += 1
            max_seq = max(max_seq, current_seq)
        else:
            current_seq = 0

    return max_seq


def normalize_sequence(seq, window):
    """
    Normaliza sequência em relação à janela.
    """
    return clamp(seq / window)