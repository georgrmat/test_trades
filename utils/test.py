import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from utils.probability_simulation_functions import get_lognormal_params, get_positive_negative_extreme_normal_proportions, simuler_freq


# Trade settings
nb_trades_day = st.number_input("Number of trades per day", value=10)
var_trades_day = st.number_input("Variance of trades per day", value=1)
N_days = st.number_input("Number of days", value=100)

# Performance parameters
win_rate = st.number_input("Win rate", value=0.6)
positive_extreme_trade_proportion = st.number_input("Positive extreme trade proportion", value=0.1)
negative_extreme_trade_proportion = st.number_input("Negative extreme trade proportion", value=0.1)

# Trade return parameters
mu_pos_extreme = st.number_input("Mean of positive extreme trades", value=3.0)
var_pos_extreme = st.number_input("Variance of positive extreme trades", value=5.0)
mu_pos_normal = st.number_input("Mean of positive normal trades", value=0.5)
var_pos_normal = st.number_input("Variance of positive normal trades", value=2.0)

mu_neg_extreme = st.number_input("Mean of negative extreme trades", value=2.0)
var_neg_extreme = st.number_input("Variance of negative extreme trades", value=4.0)
mu_neg_normal = st.number_input("Mean of negative normal trades", value=0.4)
var_neg_normal = st.number_input("Variance of negative normal trades", value=2.0)

# Other parameters
xm_pos = st.number_input("XM Positive", value=1.3)
xm_neg = st.number_input("XM Negative", value=0.7)
fees = st.number_input("Fees", value=0.03)
proba_bad_slippage = st.number_input("Probability of bad slippage", value=0.8)
slippage = st.number_input("Slippage", value=0.1)


alpha_pos = mu_pos_extreme / (mu_pos_extreme - xm_pos)
alpha_neg = mu_neg_extreme / (mu_neg_extreme - xm_neg)

nb_trades_per_day = simuler_freq(mu = nb_trades_day, var = var_trades_day, N = N_days, law = None)
nb_trades = nb_trades_per_day.sum()
open_date = np.repeat(np.arange(1, len(nb_trades_per_day) + 1), nb_trades_per_day)
close_date = open_date + 1 + stats.poisson.rvs(mu = 0.1, size = len(open_date))

n_pos_ext, n_pos_norm, n_neg_ext, n_neg_norm =  get_positive_negative_extreme_normal_proportions(nb_trades,
                                                                                                 win_rate,
                                                                                                 positive_extreme_trade_proportion,
                                                                                                 negative_extreme_trade_proportion)

# positifs normaux
x_bar_pos = mu_pos_normal # moyenne de X
sigma_var_pos = var_pos_normal # variance empirique de X
sigma_lognormal_pos = np.log(1 + (sigma_var_pos)/(x_bar_pos**2)) # variance empirique de log(X)
mu_lognormal_pos = np.log(x_bar_pos) - 1/2*sigma_lognormal_pos # moyenne empirique

# negatifs normaux
x_bar_neg = mu_neg_normal # moyenne de X
sigma_var_neg = var_neg_normal # variance empirique de X
sigma_lognormal_neg = np.log(1 + (sigma_var_neg)/(x_bar_neg**2)) # variance empirique de log(X)
mu_lognormal_neg = np.log(x_bar_neg) - 1/2*sigma_lognormal_neg # moyenne empirique

rendements_pos_ext = stats.pareto.rvs(b = alpha_pos, scale = xm_pos, size = n_pos_ext)
rendements_pos_norm = stats.lognorm.rvs(s = np.sqrt(sigma_lognormal_pos), scale = np.exp(mu_lognormal_pos), size = n_pos_norm)
rendements_neg_ext = stats.pareto.rvs(b = alpha_neg, scale = xm_neg, size = n_neg_ext)
rendements_neg_norm = stats.lognorm.rvs(s = np.sqrt(sigma_lognormal_neg), scale = np.exp(mu_lognormal_neg), size = n_neg_norm)

yields = np.concatenate((rendements_pos_ext, rendements_pos_norm, -rendements_neg_ext, -rendements_neg_norm))
np.random.shuffle(yields)

trades = {'open_date': open_date,
          'close_date': close_date,
          'yield_pct': yields}

df_trades = pd.DataFrame.from_dict(trades, orient = 'index').T

st.dataframe(df_trades, hide_index = True)