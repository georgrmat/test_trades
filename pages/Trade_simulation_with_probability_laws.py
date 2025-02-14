import streamlit as st
from utils.probability_simulation_functions import get_lognormal_params, get_positive_negative_extreme_normal_proportions

# Define a title and subtitle for the app
st.title("Paramètres de Simulation")
st.subheader("Configurez vos paramètres pour les simulations de trades ci-dessous")

# Group inputs into logical sections for better user experience
with st.expander("Fréquence des Trades et Détails de la Simulation", expanded=True):
    st.markdown("### Paramètres Généraux")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        N_trades_day = st.number_input("Nombre de trades moyen par jour", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    with col2:
        var_trades_day = st.number_input("Variance du nombre de trades par jour", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
    with col3:
        N_days = st.number_input("Nombre de jours simulés", min_value=0, max_value=2000, value=100, step=1)

# Section for trade outcome distribution
with st.expander("Distribution des Résultats des Trades"):
    st.markdown("### Paramètres de Distribution des Résultats")
    col1, col2 = st.columns(2)
    with col1:
        win_rate = st.number_input("Taux de réussite (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
        positive_extreme_trade_proportion = st.number_input("Proportion de trades positifs extrêmes (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        xm_pos = st.number_input("Seuil trades positifs normaux - extrêmes", min_value=0.0, max_value=100.0, value=3.0, step=0.1)
    with col2:
        negative_extreme_trade_proportion = st.number_input("Proportion de trades négatifs extrêmes (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        xm_neg = st.number_input("Seuil trades négatifs normaux - extrêmes", min_value=0.0, max_value=100.0, value=3.0, step=0.1)

# Section for positive trades
with st.expander("Paramètres des Trades Positifs"):
    st.markdown("### Paramètres des Trades Positifs Extrêmes et Normaux")
    col1, col2 = st.columns(2)
    with col1:
        mu_pos_extreme = st.number_input("Rendement moyen extrême positif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        var_pos_extreme = st.number_input("Variance moyenne extrême positif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    with col2:
        mu_pos_normal = st.number_input("Rendement moyen normal positif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        var_pos_normal = st.number_input("Variance moyenne normal positif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

# Section for negative trades
with st.expander("Paramètres des Trades Négatifs"):
    st.markdown("### Paramètres des Trades Négatifs Extrêmes et Normaux")
    col1, col2 = st.columns(2)
    with col1:
        mu_neg_extreme = st.number_input("Rendement moyen extrême négatif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        var_neg_extreme = st.number_input("Variance moyenne extrême négative", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    with col2:
        mu_neg_normal = st.number_input("Rendement moyen normal négatif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        var_neg_normal = st.number_input("Variance moyenne normal négatif", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

# Display calculated parameters at the bottom
st.markdown("### Paramètres Calculés")
alpha_pos = mu_pos_extreme / (mu_pos_extreme - xm_pos)
alpha_neg = mu_neg_extreme / (mu_neg_extreme - xm_neg)

st.write(f"Alpha positif : {alpha_pos:.2f}")
st.write(f"Alpha négatif : {alpha_neg:.2f}")


if st.button('Launch'):
    pass