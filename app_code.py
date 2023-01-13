import streamlit as st
import pandas as pd

sale_data = pd.read_csv('flats_for_sale.csv')
sale_data['time'] = pd.to_datetime(sale_data['time'], format='%Y-%m-%d')

# st.dataframe(sale_data)

sale_summary = sale_data.groupby('time')
sale_summary = sale_summary.agg(
                                count = ('price', 'count'),
                                mean_price_per_square = ('price_per_square_m', 'mean'),
                                median_price_per_square = ('price_per_square_m', 'median'),
                                p_sum = ('price', 'sum'),
                                mean_rooms = ('rooms', 'mean'),
                                mean_square_m = ('square_m', 'mean')
                                )

# st.line_chart(sale_summary['count'])

from bokeh.plotting import figure
chart = figure()
chart.line(sale_summary.index, sale_summary['count'])
st.bokeh_chart(chhart)
#  use_container_width=True


# st.title('web app title')
# st.text('web app text')
# st.text_input('first name')
# st.number_input('pick a number')

# import plotly.express as px

# fig = px.histogram(data, x="price_per_square_m", nbins=100)
# st.plotly_chart(fig, theme="streamlit")

# st.dataframe(data)

