import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data = pd.read_csv("final_data.csv")

# Title
st.title("Car Dashboard")

# Selection for car manufacturer and model
selected_buatan = st.selectbox("Select Car Manufacturer (BUATAN):", data['BUATAN'].unique())

# Filter unique car models based on selected manufacturer
models_for_selected_buatan = data[data['BUATAN'] == selected_buatan]['NAMA_MODEL_YANG_SEBENAR'].unique()

# Selection for car model based on selected manufacturer
selected_model = st.selectbox("Select Car Model (NAMA_MODEL_YANG_SEBENAR):", models_for_selected_buatan)

# Filter the data based on selected values
filtered_data = data[(data['BUATAN'] == selected_buatan) & (data['NAMA_MODEL_YANG_SEBENAR'] == selected_model)]

# Display the filtered data
st.write("## Filtered Data")
st.write(filtered_data.reset_index(drop=True))  # Reset index without dropping it

# Visualization - Bar chart for count of cars manufactured per year
chart_data = data.groupby('TAHUN_DIBUAT')['Count(DOSM_ID)'].sum().reset_index()
chart = alt.Chart(chart_data).mark_bar().encode(
    x='TAHUN_DIBUAT:O',
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)']
).properties(
    title='Count of Cars Manufactured per Year'
).interactive()

st.write("## Count of Cars Manufactured per Year")
st.altair_chart(chart, use_container_width=True)

# Filter data for selected car model
selected_model_data = data[data['NAMA_MODEL_YANG_SEBENAR'] == selected_model]

# Visualization - Line chart for average price of cars over the years for the selected model
price_chart_data = selected_model_data.groupby('TAHUN_DIBUAT')['PRICE(RM)'].mean().reset_index()
price_chart = alt.Chart(price_chart_data).mark_line().encode(
    x='TAHUN_DIBUAT:O',
    y='PRICE(RM):Q',
    tooltip=['TAHUN_DIBUAT', alt.Tooltip('PRICE(RM)', format='.2f')]
).properties(
    title=f'Average Price of {selected_model} Over the Years'
).interactive()

st.write(f"## Average Price of {selected_model} Over the Years")
st.altair_chart(price_chart, use_container_width=True)

# Visualization - Histogram for car age distribution for the selected model
histogram = alt.Chart(selected_model_data).mark_bar().encode(
    alt.X("TAHUN_DIBUAT:O", title="Year of Manufacture"),
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)'],
).properties(
    title=f'Distribution of Car Age for {selected_model}'
).interactive()

st.write(f"## Distribution of Car Age for {selected_model}")
st.altair_chart(histogram, use_container_width=True)

# Copyright notice
st.markdown("<div style='text-align: center; padding-top: 20px;'>© 2024 Team Usecase. All rights reserved.</div>", unsafe_allow_html=True)
