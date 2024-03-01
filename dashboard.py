import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import plotly.express as px

df = pd.read_csv("data.csv")

# Parse 'Month' column
df['Year'] = df['Month'].apply(lambda x: int(x.split('-')[1]))
df['Month'] = df['Month'].apply(lambda x: x.split('-')[0])
df['Month'] = pd.to_datetime(df['Month'] + '-01-' + df['Year'].astype(str))

# Create a list of unique years
unique_years = sorted(df['Year'].unique())

selected_year = st.sidebar.selectbox("Select Year", ['All'] + [str(year) for year in unique_years])

filtered_df = df.copy()

if st.sidebar.button("Apply", on_click=None):
    if selected_year != 'All':
        filtered_df = filtered_df[df['Year'] == int(selected_year)]

if not filtered_df.empty:
    # Convert commodity price columns to numeric
    commodity_cols = ['Coarse wool Price', 'Copra Price', 'Cotton Price', 'Fine wool Price', 
                      'Hard log Price', 'Hard sawnwood Price', 'Hide Price', 'Plywood Price', 
                      'Rubber Price', 'Softlog Price', 'Soft sawnwood Price', 'Wood pulp Price']
    filtered_df[commodity_cols] = filtered_df[commodity_cols].apply(pd.to_numeric, errors='coerce')
    
    # Melt the dataframe to long format for plotting
    melted_df = pd.melt(filtered_df, id_vars=['Month'], value_vars=commodity_cols, var_name='Commodity', value_name='Price')

    # Create a column layout
    col1, col2 = st.columns(2)

    # Plot line chart for visualization in the first column
    with col1:
        fig_line = px.line(filtered_df, x='Month', y=commodity_cols, title='Commodity Prices Over Time')
        st.plotly_chart(fig_line)

    # Sidebar for selecting commodities for the bar chart
    all_option = st.sidebar.checkbox("Select All Commodities")
    if all_option:
        selected_commodities = commodity_cols
    else:
        selected_commodities = st.sidebar.multiselect("Select Commodities", ['All'] + commodity_cols, default=commodity_cols)

    # Filter melted dataframe based on selected commodities
    if 'All' in selected_commodities:
        filtered_melted_df = melted_df
    else:
        filtered_melted_df = melted_df[melted_df['Commodity'].isin(selected_commodities)]

    # Plot bar chart for price changes in the second column
    with col2:
        fig_bar = px.bar(filtered_melted_df, x='Month', y='Price', color='Commodity', barmode='group', title='Price Changes Over Time')
        fig_bar.update_layout(xaxis_title='Month', yaxis_title='Price')
        st.plotly_chart(fig_bar)
else:
    st.write("No data available for the selected year.")

st.dataframe(filtered_df)
