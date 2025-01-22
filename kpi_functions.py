import numpy as np
import pandas as pd

def get_sharpe(trades: list):
    return np.mean(trades) / np.std(trades)



def get_sqn(sharpe: float, N: int):
    return sharpe * np.sqrt(N)


def get_max_drawdown(all_capital_evolution_series: pd.Series):
    peak_capital = all_capital_evolution_series.cummax()  # Track the peak capital at each point
    drawdown = all_capital_evolution_series - peak_capital  # Difference from the peak
    drawdown_pct = 100*drawdown / peak_capital  # Drawdown as a percentage
    max_drawdown = abs(min(drawdown_pct))
    return max_drawdown