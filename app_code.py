import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# from bokeh.plotting import figure
# from bokeh.io import curdoc
# curdoc().theme = 'dark_minimal'


### IMPORTING DATA
sale_data = pd.read_csv('flats_for_sale.csv')
sale_data['time'] = pd.to_datetime(sale_data['time'], format='%Y-%m-%d')

max_floors = int(sale_data['floor'].max())


### REGION SELECTION
regions = sale_data['region'].value_counts().index.values
regions = np.insert(regions, 0, 'All regions')

select_region = st.sidebar.selectbox('Select region:', regions)

if select_region != 'All regions':
    sale_data = sale_data[sale_data['region'] == select_region]
    
    
### FLOOR SELECTION
select_floor = st.sidebar.slider('Select floor:', value=[1, max_floors], min_value = 1, max_value = max_floors)

sale_data = sale_data[sale_data['floor'] >= select_floor[0]]
sale_data = sale_data[sale_data['floor'] <= select_floor[1]]



### CREATE SUMMARY TABLE
sale_summary = sale_data.groupby('time')
sale_summary = sale_summary.agg(
                                count = ('price', 'count'),
                                mean_price_per_square = ('price_per_square_m', 'mean'),
                                median_price_per_square = ('price_per_square_m', 'median'),
                                p_sum = ('price', 'sum'),
                                mean_rooms = ('rooms', 'mean'),
                                mean_square_m = ('square_m', 'mean')
                                )


### MAP
# st.map(sale_data[['latitude', 'longitude']].dropna())

### CHARTS
fig_count = px.line(sale_summary, y='count', title='Count of listings')
st.plotly_chart(fig_count, theme="streamlit")

fig_price = px.line(sale_summary, y='mean_price_per_square', title='Mean price per square meter', labels={'mean_price_per_square':'mean price per square meter'})
st.plotly_chart(fig_price, theme="streamlit")













# st.dataframe(sale_data)

# st.line_chart(sale_summary['count'])

### BOKEH ###
# summary_chart = figure(x_axis_type="datetime", plot_height=500)
# summary_chart.line(sale_summary.index, sale_summary['count'])
# curdoc().add_root(summary_chart)
# st.bokeh_chart(summary_chart, use_container_width=True)

# st.title('web app title')
# st.text('web app text')
# st.text_input('first name')
# st.number_input('pick a number')
