import streamlit as st  
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the file into a DataFrame
    df_kpis = pd.read_csv(uploaded_file)

for col in df_kpis.columns:
    try:
        df_kpis[col] = df_kpis[col].astype(float)
    except:
        pass

x_col = st.selectbox("x_col", df_kpis.columns.tolist())
y_col = st.selectbox("y_col", df_kpis.columns.tolist())


df_kpis.sort_values(by = x_col, ascending = False, inplace = True)
fig, ax = plt.subplots()
ax.plot(df_kpis[x_col].values, df_kpis[y_col].values, '.')
plt.xlabel(x_col)
plt.ylabel(y_col)
plt.grid()
st.pyplot(fig)


pairplot_cols = st.multiselect("columns to compare", df_kpis.columns.tolist())
hue_col = st.selectbox("color column", df_kpis.columns.tolist())
all_cols = pairplot_cols + [hue_col]

if pairplot_cols:
    fig = plt.figure(figsize=(8, 6))  # Create a figure
    sns.pairplot(df_kpis[all_cols], hue=hue_col)  # Corrected pairplot
    st.pyplot(fig)  # Display plot in Streamlit
    
    df_corr = df_kpis[all_cols].corr()
    st.dataframe(df_corr, hide_index = True)
else:
    st.warning("Please select at least one column for the pairplot.")



