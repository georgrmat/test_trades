import streamlit as st 
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from utils.kpi_functions import get_sharpe, get_sqn, get_max_drawdown


nb_trades_per_day = st.sidebar.slider("Nombre de trades par jour", 1, 50, 10)
nb_days = st.sidebar.slider("Nombre de jours de simulation", 1, 1500, 100)
win_rate = st.sidebar.slider("Win rate", 0, 100, 50)
yield_win = st.sidebar.slider("Gain par trade gagnant", 0.0, 3.0, 1.0)
yield_loss = st.sidebar.slider("Perte par trade perdant", -3.0, 0.0, -1.0)

N = nb_trades_per_day * nb_days
nb_winning_trades = int(N*win_rate/100)
nb_losing_trades = N - nb_winning_trades

wins = yield_win * np.ones(nb_winning_trades)
losses = yield_loss * np.ones(nb_losing_trades)

trades = list(wins) + list(losses)
random.shuffle(trades)

init_capital = 100000
evolution = 1 + np.array(trades)/100
all_capital_evolution_list = [init_capital] + list(init_capital*evolution.cumprod())
all_capital_evolution_series = pd.Series(all_capital_evolution_list)
final_capital = all_capital_evolution_list[-1]

fig, ax = plt.subplots()
ax.plot(all_capital_evolution_list)
ax.set_xlabel('Temps')
ax.set_ylabel('Prix')
ax.set_title('Evolution du capital')
st.pyplot(fig)

sharpe = np.round(get_sharpe(trades), 2)
sqn = np.round(get_sqn(sharpe, N), 2)
max_drawdown = get_max_drawdown(all_capital_evolution_series)


kpis = {'capital_initial': init_capital,
        'capital_final': final_capital,
        'rendement': 100 * (final_capital - init_capital)/init_capital,
        'rr': yield_win / abs(yield_loss) if yield_loss != 0 else 0,
        'win_rate': win_rate,
        'sharpe': sharpe,
        'sqn': sqn, 
        'max_drawdown': max_drawdown}

df_kpis = pd.DataFrame.from_dict(kpis, orient = 'index').T
st.dataframe(df_kpis, hide_index = True, use_container_width=True)
