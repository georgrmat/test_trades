import streamlit as st  
import matplotlib.pyplot as plt
import pandas as pd

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the file into a DataFrame
    df_kpis = pd.read_csv(uploaded_file)

x_col = st.selectbox("x_col", df_kpis.columns.tolist())
y_col = st.selectbox("y_col", df_kpis.columns.tolist())


df_kpis.sort_values(by = x_col, ascending = False, inplace = True)
fig, ax = plt.subplots()
ax.plot(df_kpis[x_col].values, df_kpis[y_col].values, '.')
ax.xlabel(x_col)
ax.ylabel(y_col)
ax.grid()
st.pyplot(fig)



