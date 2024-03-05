import streamlit as st
import pandas as pd
import altair as alt

# Load the first data
data1 = pd.read_csv("final_data.csv")

# Load the second data
data2 = pd.read_csv("KUMP_PENDAPATAN_W_PRICE.csv")

# Corporate colors
corporate_blue = "#4682b4"
corporate_gray = "#f4f4f4"

# Corporate header style for Data 1
st.markdown("<h3 style='text-align: center; color: corporate_blue;'>(Prototype)</h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: corporate_blue;'>Car Dashboard</h1>", unsafe_allow_html=True)

# Total count of cars manufactured over the years for Data 1
total_cars = data1['Count(DOSM_ID)'].sum()

# Corporate section style for Data 1
st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Total Count of Cars Manufactured</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 32px; font-weight: bold; color: {corporate_blue};'>{total_cars}</p>", unsafe_allow_html=True)

# Top 10 highest counts based on NAMA_MODEL_YANG_SEBENAR for Data 1
top_counts_data1 = data1.groupby('NAMA_MODEL_YANG_SEBENAR')['Count(DOSM_ID)'].sum().nlargest(10).reset_index()

# Calculate average price for each model in top 10 highest counts for Data 1
average_prices_data1 = data1.groupby('NAMA_MODEL_YANG_SEBENAR')['PRICE(RM)'].mean().reset_index()
top_counts_data1 = pd.merge(top_counts_data1, average_prices_data1, on='NAMA_MODEL_YANG_SEBENAR')

# Corporate section style for Data 1
st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Top 10 Highest Counts based on Car Model with Average Prices</h2>", unsafe_allow_html=True)

# Visualization - Bar chart for the top 10 highest counts based on Car Model with average prices for Data 1
bar_chart_data1 = alt.Chart(top_counts_data1).mark_bar().encode(
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

# Display the bar chart for Data 1
st.altair_chart(bar_chart_data1, use_container_width=True)

# Reference table for top 10 highest counts with average prices for Data 1
st.write("### Reference Table")
with st.markdown("<div style='overflow-x: auto;'>"):
    st.write(top_counts_data1.style.set_table_styles([
        {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('border', '2px solid #4682b4')]},
        {'selector': 'th', 'props': [('background-color', '#4682b4'), ('color', 'white'), ('font-size', '16px'), ('padding', '10px')]},
        {'selector': 'td', 'props': [('font-size', '14px'), ('padding', '8px'), ('border', '1px solid #4682b4')]}
    ]))

####################################################################################################################################################################

# Selection for car manufacturer and model for Data 1
selected_buatan_data1 = st.selectbox("Select Car Manufacturer (BUATAN):", data1['BUATAN'].unique())

# Filter unique car models based on selected manufacturer for Data 1
models_for_selected_buatan_data1 = data1[data1['BUATAN'] == selected_buatan_data1]['NAMA_MODEL_YANG_SEBENAR'].unique()

# Selection for car model based on selected manufacturer for Data 1
selected_model_data1 = st.selectbox("Select Car Model (NAMA_MODEL_YANG_SEBENAR):", models_for_selected_buatan_data1)

# Filter the data based on selected values for Data 1
filtered_data_data1 = data1[(data1['BUATAN'] == selected_buatan_data1) & (data1['NAMA_MODEL_YANG_SEBENAR'] == selected_model_data1)]

# Display the filtered data for Data 1
st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Filtered Data </h2>", unsafe_allow_html=True)
st.write(filtered_data_data1.reset_index(drop=True))  # Reset index without dropping it

# Visualization - Bar chart for count of cars manufactured per year for Data 1
chart_data_data1 = data1.groupby('TAHUN_DIBUAT')['Count(DOSM_ID)'].sum().reset_index()
chart_data1 = alt.Chart(chart_data_data1).mark_bar().encode(
    x='TAHUN_DIBUAT:O',
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)']
).properties(
    title='Count of Cars Manufactured per Year',
    width=600,
    height=400
)

st.markdown("<h2 style='text-align: center; color: corporate_blue;'>Count of Cars Manufactured per Year</h2>", unsafe_allow_html=True)
st.altair_chart(chart_data1, use_container_width=True)

# Visualization - Bar chart for count of cars manufactured per year based on NAMA_MODEL_YANG_SEBENAR for Data 1
model_chart_data_data1 = data1.groupby(['TAHUN_DIBUAT', 'NAMA_MODEL_YANG_SEBENAR'])['Count(DOSM_ID)'].sum().reset_index()
model_chart_data1 = alt.Chart(model_chart_data_data1[model_chart_data_data1['NAMA_MODEL_YANG_SEBENAR'] == selected_model_data1]).mark_bar().encode(
    x='TAHUN_DIBUAT:O',
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)'],
).properties(
    title=f'Count of {selected_model_data1} Cars Manufactured per Year',
    width=600,
    height=400
)

st.markdown(f"<h2 style='text-align: center; color: corporate_blue;'>Count of {selected_model_data1} Cars Manufactured per Year</h2>", unsafe_allow_html=True)
st.altair_chart(model_chart_data1, use_container_width=True)

# Filter data for selected car model for Data 1
selected_model_data_data1 = data1[data1['NAMA_MODEL_YANG_SEBENAR'] == selected_model_data1]

# Visualization - Line chart for average price of cars over the years for the selected model for Data 1
price_chart_data_data1 = selected_model_data_data1.groupby('TAHUN_DIBUAT')['PRICE(RM)'].mean().reset_index()
price_chart_data1 = alt.Chart(price_chart_data_data1).mark_line().encode(
    x='TAHUN_DIBUAT:O',
    y='PRICE(RM):Q',
    tooltip=['TAHUN_DIBUAT', alt.Tooltip('PRICE(RM)', format='.2f')]
).properties(
    title=f'Average Price of {selected_model_data1} Over the Years',
    width=600,
    height=400
)

st.markdown(f"<h2 style='text-align: center; color: corporate_blue;'>Average Price of {selected_model_data1} Over the Years</h2>", unsafe_allow_html=True)
st.altair_chart(price_chart_data1, use_container_width=True)

# Visualization - Histogram for car age distribution for the selected model for Data 1
histogram_data1 = alt.Chart(selected_model_data_data1).mark_bar().encode(
    alt.X("TAHUN_DIBUAT:O", title="Year of Manufacture"),
    y='Count(DOSM_ID):Q',
    tooltip=['TAHUN_DIBUAT', 'Count(DOSM_ID)'],
).properties(
    title=f'Distribution of Car Age for {selected_model_data1} ',
    width=600,
    height=400
)

st.markdown(f"<h2 style='text-align: center; color: corporate_blue;'>Distribution of Car Age for {selected_model_data1} </h2>", unsafe_allow_html=True)
st.altair_chart(histogram_data1, use_container_width=True)


# Visualizations Section for Data 2
st.write("## Visualizations")

# Household Income Distribution for Data 2
st.write("### Household Income Distribution")
income_chart_data2 = alt.Chart(data2).mark_bar().encode(
    x=alt.X('KUMPULAN_PENDAPATAN', title='Income Group'),
    y=alt.Y('sum(Count(NO_IR)):Q', title='Number of Households', axis=alt.Axis(grid=False)),
    color='KUMPULAN_PENDAPATAN',
    tooltip=['KUMPULAN_PENDAPATAN', 'sum(Count(NO_IR))']
).properties(
    width=600,
    height=400,
    title='Household Income Distribution'
).interactive()
st.altair_chart(income_chart_data2)

st.write("### Reference Group Income")
st.image("gg.PNG", use_column_width=True)

# Interactive selection for income group for Data 2
selected_income_group_data2 = st.selectbox('Select Income Group:', data2['KUMPULAN_PENDAPATAN'].unique())

# Filter data based on selected income group for Data 2
filtered_data_data2 = data2[data2['KUMPULAN_PENDAPATAN'] == selected_income_group_data2]

# Most Popular Car Brands for selected income group for Data 2
brand_counts_data2 = filtered_data_data2.groupby('BUATAN')['Count(NO_IR)'].sum().sort_values(ascending=False).head(15)
st.write(f"### Top 15 Most Popular Car Brands for Income Group {selected_income_group_data2} for Data 2")
brand_chart_data2 = alt.Chart(filtered_data_data2).mark_bar().encode(
    x=alt.X('BUATAN:N', title='Car Brand', sort='-y'),
    y=alt.Y('sum(Count(NO_IR)):Q', title='Number of Households'),
    tooltip=['BUATAN', 'sum(Count(NO_IR))']
).transform_filter(
    alt.FieldOneOfPredicate(field='BUATAN', oneOf=brand_counts_data2.index.tolist())
).properties(
    width=800,
    height=400,
    title=f'Top 15 Most Popular Car Brands for Income Group {selected_income_group_data2} '
).interactive()
st.altair_chart(brand_chart_data2)

# Most Popular Car Models for selected income group for Data 2
model_counts_data2 = filtered_data_data2.groupby('NAMA_MODEL_YANG_SEBENAR')['Count(NO_IR)'].sum().sort_values(ascending=False).head(15)
st.write(f"### Top 15 Most Popular Car Models for Income Group {selected_income_group_data2} ")
model_chart_data2 = alt.Chart(filtered_data_data2).mark_bar().encode(
    x=alt.X('NAMA_MODEL_YANG_SEBENAR:N', title='Car Model', sort='-y'),
    y=alt.Y('sum(Count(NO_IR)):Q', title='Number of Households'),
    tooltip=['NAMA_MODEL_YANG_SEBENAR', 'sum(Count(NO_IR))']
).transform_filter(
    alt.FieldOneOfPredicate(field='NAMA_MODEL_YANG_SEBENAR', oneOf=model_counts_data2.index.tolist())
).properties(
    width=800,
    height=400,
    title=f'Top 15 Most Popular Car Models for Income Group {selected_income_group_data2}'
).interactive()
st.altair_chart(model_chart_data2)

# Reference Table for Data 2
st.write("## Reference Table")
st.write("Below is the reference table for all data based on the selected income group:")
st.dataframe(filtered_data_data2, height=600)  # Adjust the height as per your preference


# Corporate footer style for Data 1
st.markdown("<div style='text-align: center; padding-top: 12px; color: corporate_gray;'>© 2024 Team Usecase. All rights reserved.</div>", unsafe_allow_html=True)
