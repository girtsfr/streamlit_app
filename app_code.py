import streamlit as st
import pandas as pd

for_sale_data = pd.read_csv('flats_for_sale.csv')
for_sale_data['time'] = pd.to_datetime(for_sale_data['time'], format='%Y-%m-%d')

st.dataframe(for_sale_data)



# st.title('web app title')
# st.text('web app text')
# st.text_input('first name')
# st.number_input('pick a number')

# import plotly.express as px

# fig = px.histogram(data, x="price_per_square_m", nbins=100)
# st.plotly_chart(fig, theme="streamlit")

# st.dataframe(data)

