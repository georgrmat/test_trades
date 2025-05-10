import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Simulation Function ---
def simulate_trades(n_coins, daily_trades_per_coin, avg_gain, avg_loss, std_gain, std_loss, win_rate, n_days, capital):
    capital_per_coin = capital / n_coins
    total_trades = n_coins * daily_trades_per_coin * n_days

    all_returns = []
    equity_curves = []

    for _ in range(n_coins):
        n_trades = daily_trades_per_coin * n_days
        wins = np.random.rand(n_trades) < win_rate
        returns = np.where(
            wins,
            np.random.normal(loc=avg_gain, scale=std_gain, size=n_trades),
            np.random.normal(loc=-abs(avg_loss), scale=std_loss, size=n_trades)
        )
        all_returns.append(returns)

        # Reshape returns into daily buckets
        returns_daywise = returns.reshape((n_days, daily_trades_per_coin))
        daily_returns = np.prod(1 + returns_daywise / 100, axis=1) - 1
        equity = np.array([capital/n_coins] + list(capital_per_coin * np.cumprod(1 + daily_returns)))
        
        equity_curves.append(equity)

    all_returns = np.concatenate(all_returns)
    total_equity_curve = np.sum(equity_curves, axis=0)

    return all_returns, equity_curves, total_equity_curve, total_trades

# --- KPI Calculation ---
def compute_kpis(returns, equity_curve, initial_capital, total_trades, n_days):
    win_trades = returns[returns > 0]
    loss_trades = returns[returns <= 0]

    win_rate = len(win_trades) / total_trades
    avg_win = np.mean(win_trades) if len(win_trades) > 0 else 0
    avg_loss = np.mean(loss_trades) if len(loss_trades) > 0 else 0
    rrr = avg_win / abs(avg_loss) if avg_loss != 0 else 0
    profit_factor = np.sum(win_trades) / abs(np.sum(loss_trades)) if np.sum(loss_trades) != 0 else 0

    final_value = equity_curve[-1]
    total_return = (final_value - initial_capital) / initial_capital
    quarterly_return = total_return * 100
    annual_return = quarterly_return * 4

    # Max Drawdown
    cumulative_max = np.maximum.accumulate(equity_curve)
    drawdowns = (equity_curve - cumulative_max) / cumulative_max
    max_drawdown = np.min(drawdowns) * 100

    # Daily metrics
    daily_returns = np.diff(equity_curve) / equity_curve[:-1]
    sharpe = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(365) if np.std(daily_returns) > 0 else 0
    downside_std = np.std(daily_returns[daily_returns < 0])
    sortino = np.mean(daily_returns) / downside_std * np.sqrt(365) if downside_std > 0 else 0
    sqn = (np.sqrt(min(100, len(daily_returns))) * np.mean(daily_returns)) / np.std(daily_returns) if np.std(daily_returns) > 0 else 0

    return {
        "Win Rate (%)": round(win_rate * 100, 2),
        "Gain moyen (%)": round(avg_win, 2),
        "Perte moyenne (%)": round(avg_loss, 2),
        "RRR": round(rrr, 2),
        "Profit Factor": round(profit_factor, 2),
        "Rendement 3 mois (%)": round(quarterly_return, 2),
        "Projection annuelle (%)": round(annual_return, 2),
        "Max Drawdown (%)": round(max_drawdown, 2),
        "Sharpe Old": np.mean(returns) / np.std(returns),
        "Sharpe Ratio": round(sharpe, 2),
        "Sortino Ratio": round(sortino, 2),
        "SQN": round(sqn, 2)
    }

# --- Streamlit UI ---
st.set_page_config(page_title="Simulateur de trades")
st.title("Simulateur de trades")

with st.sidebar:
    st.header("Paramètres")
    n_coins = st.slider("Nombre de coins", 1, 200, 50)
    daily_trades = st.slider("Nombre journalier de trades par coin", 1, 10, 1)
    avg_gain = st.number_input("Gain moyen (%)", value=1.3)
    avg_loss = st.number_input("Perte moyenne (%)", value=1.0)
    std_gain = st.number_input("Ecart-type gains (%)", value=0.5)
    std_loss = st.number_input("Ecart-type pertes (%)", value=0.5)
    win_rate = st.slider("Win Rate", 0.0, 1.0, 0.56)
    n_days = st.number_input("Nombre de jours simulés", value=90)
    capital = st.number_input("Capital initial", value=100000)

# --- Run Simulation ---
returns, equity_curves, total_curve, total_trades = simulate_trades(
    n_coins, daily_trades, avg_gain, avg_loss, std_gain, std_loss, win_rate, n_days, capital
)

# --- Compute KPIs ---
kpis = compute_kpis(returns, total_curve, capital, total_trades, n_days)
st.subheader("KPIs")
st.dataframe(pd.DataFrame([kpis]).T.rename(columns={0: "Valeur"}))


# --- PnL Curve ---
st.subheader("Courbe PnL")
fig, ax = plt.subplots()
ax.plot(range(0, n_days + 1), total_curve - capital, color="black", linewidth=2)
ax.set_xlabel("Jour")
ax.set_ylabel("PnL")
ax.set_title("Evolution du PnL par jour")
ax.grid(True)
st.pyplot(fig)

# --- Histogram of Trade Returns ---
st.subheader("Distribution des rendements des trades")
fig2, ax2 = plt.subplots()
wins = returns[returns >= 0]
losses = returns[returns < 0]
ax2.hist(wins, bins=30, color="blue", alpha=0.7, edgecolor="black", label="Gains")
ax2.hist(losses, bins=30, color="red", alpha=0.7, edgecolor="black", label="Pertes")
ax2.set_title("Histogramme des rendements")
ax2.legend()
st.pyplot(fig2)
