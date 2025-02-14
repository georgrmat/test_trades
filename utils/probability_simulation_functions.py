import pandas as pd
import numpy as np
from scipy import stats


def get_positive_negative_extreme_normal_proportions_with_dataframes(N,
                                                     df_trades, 
                                                     df_positive_trades, 
                                                     df_negative_trades, 
                                                     df_trades_extreme_positive,
                                                     df_trades_extreme_negative):
    
    nb_positive_trades = int(N * len(df_positive_trades) / len(df_trades))
    nb_negative_trades = N - nb_positive_trades

    nb_positive_extreme_trades_proportion = int(nb_positive_trades * len(df_trades_extreme_positive) / len(df_positive_trades))
    nb_positive_normal_trades_proportion = nb_positive_trades - nb_positive_extreme_trades_proportion
    
    nb_negative_extreme_trades_proportion = int(nb_negative_trades * len(df_trades_extreme_negative) / len(df_negative_trades))
    nb_negative_normal_trades_proportion = nb_negative_trades - nb_negative_extreme_trades_proportion

    return nb_positive_extreme_trades_proportion, nb_positive_normal_trades_proportion, nb_negative_extreme_trades_proportion, nb_negative_normal_trades_proportion



def get_positive_negative_extreme_normal_proportions(N: int,
                                                     win_rate: float,
                                                     positive_extreme_trades_proportion: float,
                                                     negative_extreme_trades_proportion: float) -> (float, float, float, float):
    
    nb_positive_trades = int(N * win_rate)
    nb_negative_trades = N - nb_positive_trades

    nb_positive_extreme_trades_proportion = int(nb_positive_trades * positive_extreme_trades_proportion)
    nb_positive_normal_trades_proportion = nb_positive_trades - nb_positive_extreme_trades_proportion
    
    nb_negative_extreme_trades_proportion = int(nb_negative_trades * negative_extreme_trades_proportion)
    nb_negative_normal_trades_proportion = nb_negative_trades - nb_negative_extreme_trades_proportion

    return nb_positive_extreme_trades_proportion, nb_positive_normal_trades_proportion, nb_negative_extreme_trades_proportion, nb_negative_normal_trades_proportion



def get_frequency_params(df_trades: pd.DataFrame, date_col: str) -> (float, float):
    
    nb_trades = len(df_trades)
    total_days = (df_trades[date_col].max() - df_trades[date_col].min()).days + 1
    average_trades_per_day = nb_trades / total_days

    nb_trades_per_traded_days = df_trades.groupby(date_col).size().tolist()
    nb_trades_per_day = nb_trades_per_traded_days + [0 for _ in range(total_days - len(nb_trades_per_traded_days))]

    mu = np.mean(nb_trades_per_day)
    var = np.var(nb_trades_per_day)
    
    return mu, var



def simuler_freq(mu: float, var: float, N: int, law = None):
    """
    Parameters
    ----------
    mu : float
        moyenne des donnees observees
    var : float
        variance des donnees observees
    N : TYPE, optional
        nombre de tirages (jours, mois annees simules)
    law : TYPE, optional
        loi de probabilite a simuler. Si rien, alors l'algorithme determinera la loi a utiliser

    Returns
    -------
    np.array
        renvoie l'array contenant le nombre d'evenements simules par tirage
    """
    
    if law == "poisson":
        try:
            return stats.poisson.rvs(mu = mu, size = N)
        except Exception as e:
            print("Erreur dans la fonction simuler_freq: la loi de poisson n'a pas pu etre simulee")
            print(e)
    
    elif law == "nbinom":
        try:
            p_hat = mu/var
            n_hat = p_hat*mu/(1 - p_hat)
            return stats.nbinom.rvs(n = n_hat, p = p_hat, size = N)
        except Exception as e:
            print("Erreur dans la fonction simuler_freq: la loi binomiale negative n'a pas pu etre simulee")
            print(e)
    
    else:
        try:
            if var/mu >= 5:
                p_hat = mu/var
                n_hat = p_hat*mu/(1 - p_hat)
                return stats.nbinom.rvs(n = n_hat, p = p_hat, size = N)
            else:
                return stats.poisson.rvs(mu = mu, size = N)
        except Exception as e:
            print("Erreur dans la fonction simuler_freq: la loi de frequence n'a pas pu etre simulee")
            print(e)
            
            
            
def get_lognormal_params(mu: float, var: float) -> (float, float):
    sigma_attr_pos = np.log(1 + (var)/(mu**2))
    mu_pos_normal = np.log(mu) - 1/2*sigma_attr_pos
    return mu_pos_normal, sigma_attr_pos