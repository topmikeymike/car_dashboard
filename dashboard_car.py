import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data = pd.read_csv('cardatagap.csv')

# Selectbox to select model
selected_model = st.selectbox('Select Model (above chart)', data['NAMA_MODEL_YANG_SEBENAR'].unique(), key='selectbox_above_chart')

# Filter data based on selected model
filtered_data = data[data['NAMA_MODEL_YANG_SEBENAR'] == selected_model]

# Line chart
chart = alt.Chart(filtered_data).mark_line(point=True).encode(
    x=alt.X('TAHUN_DIBUAT:O', title='Year', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('COUNT_NAMA_MODEL_YANG_SEBENAR:Q', title='Count'),
    tooltip=['TAHUN_DIBUAT:O', 'COUNT_NAMA_MODEL_YANG_SEBENAR:Q']
).properties(
    width=900,
    height=600,
    title=f'Time Series for {selected_model}'
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

# Create a reference table for the values of each dot in the line chart
reference_data = pd.DataFrame(filtered_data[['TAHUN_DIBUAT', 'COUNT_NAMA_MODEL_YANG_SEBENAR']])
reference_data.columns = ['Year', 'Count']
reference_data['Year'] = reference_data['Year'].astype(str)
reference_data = reference_data.set_index('Year')

# Display the reference table
st.write("Reference Table:")
st.write(reference_data)
