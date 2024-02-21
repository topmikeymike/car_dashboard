import streamlit as st
import pandas as pd
import altair as alt

# Load the count data
count_data = pd.read_csv('cardatagap.csv')

# Load the price data
price_data = pd.read_csv('carlist_price.csv')

# Set the title for the count chart
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #2876eb; font-size: 36px; font-family: "Arial Black", Gadget, sans-serif;'>CAR MODEL IN MALAYSIA TIME SERIES</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Multiselect to select car models for count visualization
all_models = count_data['NAMA_MODEL_YANG_SEBENAR'].unique()
default_selected_models = ["SAGA"]  # Set default models here
selected_models = st.multiselect('Select Car Models:', ['All'] + list(all_models), default=default_selected_models, key='multiselect_models')

# Filter count data based on selected car models
if "All" in selected_models:
    filtered_count_data = count_data
else:
    filtered_count_data = count_data[count_data['NAMA_MODEL_YANG_SEBENAR'].isin(selected_models)]

# Check if any model is selected for count data
if not selected_models:
    st.error("Please select at least one car model for count visualization.")
else:
    # Set tooltip dynamically based on the number of selected car models for count data
    tooltip_fields_count = ['TAHUN_DIBUAT:O', 'COUNT_NAMA_MODEL_YANG_SEBENAR:Q']
    if len(selected_models) <= 10:
        tooltip_fields_count.append('NAMA_MODEL_YANG_SEBENAR:N')

    # Line chart for count visualization
    count_chart = alt.Chart(filtered_count_data).mark_line(point=True).encode(
        x=alt.X('TAHUN_DIBUAT:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('COUNT_NAMA_MODEL_YANG_SEBENAR:Q', title='Count'),
        color=alt.Color('NAMA_MODEL_YANG_SEBENAR:N', scale=alt.Scale(scheme='category20')),
        tooltip=tooltip_fields_count
    ).properties(
        width=900,
        height=600,
        title='Time Series for Selected Car Models (Count)'
    ).configure_legend(
        orient='bottom'
    )

    # Display the count chart
    st.altair_chart(count_chart, use_container_width=True)

    # Create a reference table for the count data
    count_reference_table = pd.DataFrame(filtered_count_data[['TAHUN_DIBUAT', 'COUNT_NAMA_MODEL_YANG_SEBENAR', 'NAMA_MODEL_YANG_SEBENAR']])
    count_reference_table.columns = ['Year', 'Count', 'Car Model']
    count_reference_table['Year'] = count_reference_table['Year'].astype(str)
    count_reference_table = count_reference_table.pivot_table(index='Car Model', columns='Year', values='Count', aggfunc='sum')  # Pivot and aggregate

    # Fill NaN values with 0 for count data
    count_reference_table.fillna(0, inplace=True)

    # Apply styles to the count reference table
    def apply_count_styles(df):
        return df.style.format("{:.0f}").applymap(lambda x: 'background-color: #f2f2f2', subset=pd.IndexSlice[:, df.columns[0]]).applymap(lambda x: 'background-color: #f2f2f2', subset=pd.IndexSlice[df.index[0], :])

    # Display the count reference table with Streamlit default theme
    st.markdown("<h2>Count Reference Table</h2>", unsafe_allow_html=True)
    st.write(apply_count_styles(count_reference_table))

# Set the title for the price chart
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #2876eb; font-size: 36px; font-family: "Arial Black", Gadget, sans-serif;'>PRICE CAR IN MALAYSIA</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Multiselect to select car models for price visualization
all_price_models = price_data['NAMA_MODEL'].unique()
default_selected_price_models = list(set(default_selected_models) & set(all_price_models))  # Ensure default models are in the options list
selected_price_models = st.multiselect('Select Car Models for Price:', ['All'] + list(all_price_models), default=default_selected_price_models, key='multiselect_price_models')

# Filter price data based on selected car models
if "All" in selected_price_models:
    filtered_price_data = price_data
else:
    filtered_price_data = price_data[price_data['NAMA_MODEL'].isin(selected_price_models)]

# Check if any model is selected for price data
if not selected_price_models:
    st.error("Please select at least one car model for price visualization.")
else:
    # Calculate average price for each car model and year
    avg_price_data = filtered_price_data.groupby(['NAMA_MODEL', 'TAHUN_DIBUAT'])['PRICE'].mean().reset_index()

    # Set tooltip dynamically based on the number of selected car models for price data
    tooltip_fields_price = ['TAHUN_DIBUAT:O', 'PRICE:Q', 'NAMA_MODEL:N']
    if len(selected_price_models) <= 10:
        tooltip_fields_price.append('NAMA_MODEL:N')

    # Line chart for price visualization
    price_chart = alt.Chart(avg_price_data).mark_line(point=True).encode(
        x=alt.X('TAHUN_DIBUAT:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('PRICE:Q', title='Average Price (MYR)'),
        color=alt.Color('NAMA_MODEL:N', scale=alt.Scale(scheme='category20')),
        tooltip=tooltip_fields_price
    ).properties(
        width=900,
        height=600,
        title='Average Price Trends for Selected Car Models'
    ).configure_legend(
        orient='bottom'
    )

    # Display the price chart
    st.altair_chart(price_chart, use_container_width=True)

    # Create a reference table for the price data
    price_reference_table = avg_price_data.pivot_table(index='NAMA_MODEL', columns='TAHUN_DIBUAT', values='PRICE', aggfunc='first')  # Pivot and aggregate

    # Fill NaN values with 0 for price data
    price_reference_table.fillna(0, inplace=True)

    # Apply styles to the price reference table
    def apply_price_styles(df):
        return df.style.format("{:.2f}")

    # Display the price reference table with Streamlit default theme
    st.markdown("<h2>Price Reference Table</h2>", unsafe_allow_html=True)
    st.write(apply_price_styles(price_reference_table))

# Copyright notice
st.markdown("<div style='text-align: center; padding-top: 10px; font-size: 12px; color: #808080;'>© 2024 Team Usecase. All rights reserved.</div>", unsafe_allow_html=True)
