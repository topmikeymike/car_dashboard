import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data = pd.read_csv("final_data.csv")

# Corporate colors
corporate_blue = "#4682b4"
corporate_gray = "#f4f4f4"


# Corporate header style
st.markdown("<h3 style='text-align: center; color: corporate_blue;'>(Prototype)</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: corporate_blue;'>Car Dashboard</h1>", unsafe_allow_html=True)

# Total count of cars manufactured over the years
total_cars = data['Count(DOSM_ID)'].sum()

# Corporate section style
st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Total Count of Cars Manufactured</h2>", unsafe_allow_html=True)

# Corporate section style
st.markdown(f"<p style='text-align: center; font-size: 32px; font-weight: bold; color: {corporate_blue};'>{total_cars}</p>", unsafe_allow_html=True)

# Top 10 highest counts based on NAMA_MODEL_YANG_SEBENAR
top_counts = data.groupby('NAMA_MODEL_YANG_SEBENAR')['Count(DOSM_ID)'].sum().nlargest(10).reset_index()

# Calculate average price for each model in top 10 highest counts
average_prices = data.groupby('NAMA_MODEL_YANG_SEBENAR')['PRICE(RM)'].mean().reset_index()
top_counts = pd.merge(top_counts, average_prices, on='NAMA_MODEL_YANG_SEBENAR')

# Corporate section style
st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Top 10 Highest Counts based on Car Model with Average Prices</h2>", unsafe_allow_html=True)

# Visualization - Bar chart for the top 10 highest counts based on Car Model with average prices
bar_chart = alt.Chart(top_counts).mark_bar().encode(
    x=alt.X('NAMA_MODEL_YANG_SEBENAR:N', title='Car Model'),
    y=alt.Y('Count(DOSM_ID):Q', title='Count'),
    color=alt.Color('NAMA_MODEL_YANG_SEBENAR:N', legend=None),
    tooltip=['NAMA_MODEL_YANG_SEBENAR', 'Count(DOSM_ID)', 'PRICE(RM)'],
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=14,
    titleFontSize=16
)

# Display the bar chart
st.altair_chart(bar_chart, use_container_width=True)


# Reference table for top 10 highest counts with average prices
st.write("### Reference Table")
with st.markdown("<div style='overflow-x: auto;'>"):
    st.write(top_counts.style.set_table_styles([
        {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('border', '2px solid #4682b4')]},
        {'selector': 'th', 'props': [('background-color', '#4682b4'), ('color', 'white'), ('font-size', '16px'), ('padding', '10px')]},
        {'selector': 'td', 'props': [('font-size', '14px'), ('padding', '8px'), ('border', '1px solid #4682b4')]}
    ]))

####################################################################################################################################################################

# Selection for car manufacturer and model
selected_buatan = st.selectbox("Select Car Manufacturer (BUATAN):", data['BUATAN'].unique())

# Filter unique car models based on selected manufacturer
models_for_selected_buatan = data[data['BUATAN'] == selected_buatan]['NAMA_MODEL_YANG_SEBENAR'].unique()

# Selection for car model based on selected manufacturer
selected_model = st.selectbox("Select Car Model (NAMA_MODEL_YANG_SEBENAR):", models_for_selected_buatan)

# Filter the data based on selected values
filtered_data = data[(data['BUATAN'] == selected_buatan) & (data['NAMA_MODEL_YANG_SEBENAR'] == selected_model)]

# Display the filtered data
st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Filtered Data</h2>", unsafe_allow_html=True)
st.write(filtered_data.reset_index(drop=True))  # Reset index without dropping it

# Visualization - Bar chart for count of cars manufactured per year
chart_data = data.groupby('TAHUN_DIBUAT')['Count(DOSM_ID)'].sum().reset_index()
chart = alt.Chart(chart_data).mark_bar().encode(
    x='TAHUN_DIBUAT:O',
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)']
).properties(
    title='Count of Cars Manufactured per Year',
    width=600,
    height=400
)

st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Count of Cars Manufactured per Year</h2>", unsafe_allow_html=True)
st.altair_chart(chart, use_container_width=True)

# Visualization - Bar chart for count of cars manufactured per year based on NAMA_MODEL_YANG_SEBENAR
model_chart_data = data.groupby(['TAHUN_DIBUAT', 'NAMA_MODEL_YANG_SEBENAR'])['Count(DOSM_ID)'].sum().reset_index()
model_chart = alt.Chart(model_chart_data[model_chart_data['NAMA_MODEL_YANG_SEBENAR'] == selected_model]).mark_bar().encode(
    x='TAHUN_DIBUAT:O',
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)'],
).properties(
    title=f'Count of {selected_model} Cars Manufactured per Year',
    width=600,
    height=400
)

st.markdown(f"<h2 style='text-align: center; color: corporate_blue;'>Count of {selected_model} Cars Manufactured per Year</h2>", unsafe_allow_html=True)
st.altair_chart(model_chart, use_container_width=True)

# Filter data for selected car model
selected_model_data = data[data['NAMA_MODEL_YANG_SEBENAR'] == selected_model]

# Visualization - Line chart for average price of cars over the years for the selected model
price_chart_data = selected_model_data.groupby('TAHUN_DIBUAT')['PRICE(RM)'].mean().reset_index()
price_chart = alt.Chart(price_chart_data).mark_line().encode(
    x='TAHUN_DIBUAT:O',
    y='PRICE(RM):Q',
    tooltip=['TAHUN_DIBUAT', alt.Tooltip('PRICE(RM)', format='.2f')]
).properties(
    title=f'Average Price of {selected_model} Over the Years',
    width=600,
    height=400
)

st.markdown(f"<h2 style='text-align: center; color: corporate_blue;'>Average Price of {selected_model} Over the Years</h2>", unsafe_allow_html=True)
st.altair_chart(price_chart, use_container_width=True)

# Visualization - Histogram for car age distribution for the selected model
histogram = alt.Chart(selected_model_data).mark_bar().encode(
    alt.X("TAHUN_DIBUAT:O", title="Year of Manufacture"),
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)'],
).properties(
    title=f'Distribution of Car Age for {selected_model}',
    width=600,
    height=400
)

st.markdown(f"<h2 style='text-align: center; color: corporate_blue;'>Distribution of Car Age for {selected_model}</h2>", unsafe_allow_html=True)
st.altair_chart(histogram, use_container_width=True)

# Corporate footer style
st.markdown("<div style='text-align: center; padding-top: 20px; color: corporate_gray;'>© 2024 Team Usecase. All rights reserved.</div>", unsafe_allow_html=True)
