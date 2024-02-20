import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data = pd.read_csv('cardatagap.csv')

# Set the title
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #2876eb; font-size: 36px; font-family: "Arial Black", Gadget, sans-serif;'>CAR MODEL IN MALAYSIA TIME SERIES</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Multiselect to select car models
all_models = data['NAMA_MODEL_YANG_SEBENAR'].unique()
default_selected_models = ["SAGA"]  # Set default models here
selected_models = st.multiselect('Select Car Models:', ['All'] + list(all_models), default=default_selected_models, key='multiselect_models')

# Filter data based on selected models
if "All" in selected_models:
    filtered_data = data
else:
    filtered_data = data[data['NAMA_MODEL_YANG_SEBENAR'].isin(selected_models)]

# Check if any model is selected
if not selected_models:
    st.error("Please select at least one car model.")
else:
    # Line chart
    chart = alt.Chart(filtered_data).mark_line(point=True).encode(
        x=alt.X('TAHUN_DIBUAT:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('COUNT_NAMA_MODEL_YANG_SEBENAR:Q', title='Count'),
        color='NAMA_MODEL_YANG_SEBENAR:N',
        tooltip=['TAHUN_DIBUAT:O', 'COUNT_NAMA_MODEL_YANG_SEBENAR:Q']
    ).properties(
        width=900,
        height=600,
        title='Time Series for Selected Car Models'
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)

    # Create a reference table for the values of each dot in the line chart
    reference_data = pd.DataFrame(filtered_data[['TAHUN_DIBUAT', 'COUNT_NAMA_MODEL_YANG_SEBENAR', 'NAMA_MODEL_YANG_SEBENAR']])
    reference_data.columns = ['Year', 'Count', 'Car Model']
    reference_data['Year'] = reference_data['Year'].astype(str)
    reference_data = reference_data.pivot(index='Car Model', columns='Year', values='Count')

    # Fill NaN values with 0
    reference_data.fillna(0, inplace=True)

    # Apply styles to the reference table
    def apply_styles(df):
        return df.style.applymap(lambda x: 'background-color: #f2f2f2', subset=pd.IndexSlice[:, df.columns[0]]).applymap(lambda x: 'background-color: #f2f2f2', subset=pd.IndexSlice[df.index[0], :])

    # Display the reference table with Streamlit default theme
    st.markdown("<h2>Reference Table</h2>", unsafe_allow_html=True)
    st.write(apply_styles(reference_data))
