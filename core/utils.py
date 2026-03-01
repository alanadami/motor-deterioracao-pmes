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


def to_native(obj):
    """
    Converte recursivamente tipos numpy para tipos nativos do Python.
    """
    import numpy as np

    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_native(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj
    
   

def format_for_display(obj):
    """
    Formata saída para apresentação:
    - Todos os floats com 2 casas decimais
    - Campos monetários recebem prefixo 'R$ '
    """

    monetary_keys = {
        "margem_media_recente",
        "media_recente",
        "baseline_margem",
    }

    if isinstance(obj, dict):
        formatted = {}
        for k, v in obj.items():
            if isinstance(v, float):
                if k in monetary_keys:
                    formatted[k] = f"R$ {v:,.2f}"
                else:
                    formatted[k] = round(v, 2)
            else:
                formatted[k] = format_for_display(v)
        return formatted

    elif isinstance(obj, list):
        return [format_for_display(v) for v in obj]

    else:
        return obj