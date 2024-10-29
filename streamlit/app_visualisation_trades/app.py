import streamlit as st 
import numpy as np
import random
import matplotlib.pyplot as plt

N = st.sidebar.slider("Nombre de trades", 1, 1000, 100)
win_rate = st.sidebar.slider("Win rate", 0, 100, 50)
yield_win = st.sidebar.slider("Gain par trade gagnant", 0, 10, 3)
yield_loss = st.sidebar.slider("Perte par trade perdant", -10, 0, -3)

nb_winning_trades = int(N*win_rate/100)
nb_losing_trades = N - nb_winning_trades

wins = yield_win * np.ones(nb_winning_trades)
losses = yield_loss * np.ones(nb_losing_trades)

trades = list(wins) + list(losses)
random.shuffle(trades)
sharpe = np.round(np.mean(trades) / np.std(trades), 2)

evolution = 1 + np.array(trades)/100
all_capital_evolution = [100000] + list(100000*evolution.cumprod())

fig, ax = plt.subplots()
ax.plot(all_capital_evolution)
ax.set_xlabel('Temps')
ax.set_ylabel('Prix')
ax.set_title('Evolution du capital')
st.pyplot(fig)

st.write(sharpe)
