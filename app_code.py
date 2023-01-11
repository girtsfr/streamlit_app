import streamlit as st
import pandas as pd

data = pd.read_csv('flats_for_rent_2023-01-05.csv')
data = data[['rooms', 'square_m', 'floor', 'price', 'area', 'region', 'price_per_square_m']]
data = data[data['price_per_square_m'] < 50]
data = data[data['area'] == 'riga']

st.title('web app title')
st.text('web app text')
st.text_input('first name')
st.number_input('pick a number')

import plotly.express as px

df = px.data.tips()
fig = px.histogram(data, x="price_per_square_m", nbins=100)
st.plotly_chart(fig, theme="streamlit")

st.dataframe(data)
