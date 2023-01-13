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
sale_data = sale_data.dropna(subset=['rooms'])

numeric_cols = ['rooms', 'square_m', 'floor', 'price', 'building_total_floors', 'price_per_square_m']
sale_data[numeric_cols] = sale_data[numeric_cols].astype(np.int64)

max_floors = int(sale_data['floor'].max())
max_rooms = int(sale_data['rooms'].max())
max_size = int(sale_data['square_m'].max())


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


### ROOM COUNT SELECTION
select_rooms = st.sidebar.slider('Select room count:', value=[1, max_rooms], min_value = 1, max_value = max_rooms)

sale_data = sale_data[sale_data['rooms'] >= select_rooms[0]]
sale_data = sale_data[sale_data['rooms'] <= select_rooms[1]]


### SIZE SELECTION
select_size = st.sidebar.slider('Select size (square meters):', value=[1, max_size], min_value = 1, max_value = max_size)

sale_data = sale_data[sale_data['square_m'] >= select_size[0]]
sale_data = sale_data[sale_data['square_m'] <= select_size[1]]



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
st.subheader('Count of listings')
st.caption('Below chart shows how many apartments were listed for sale at particular dates')
fig_count = px.line(sale_summary, y='count')
st.plotly_chart(fig_count, theme="streamlit")

st.header('Mean price per square meter')
fig_price = px.line(sale_summary, y='mean_price_per_square', labels={'mean_price_per_square':'mean price per square meter'})
st.plotly_chart(fig_price, theme="streamlit")



### FILTER PAST X MONTHS
months_back = st.number_input('Choose lookback period (in months):', min_value=1, max_value=12, value=6)
sale_hist = sale_data[sale_data['time'] >= pd.to_datetime('now') - pd.DateOffset(months=months_back)]

sale_hist['idx'] = (
    sale_hist['rooms'].astype(str)
    + '-'
    + sale_hist['square_m'].astype(str)
    + '-'
    + sale_hist['floor'].astype(str)
    + '-'
    + sale_hist['price'].astype(str)
    + '-'
    + sale_hist['street'].astype(str)
)

sale_hist = sale_hist.drop_duplicates(subset='idx')

fig_histogram = px.histogram(sale_hist, x="price_per_square_m")
fig_histogram.update_xaxes(range=[0, 5000])

st.plotly_chart(fig_histogram, theme="streamlit")


### DATAFRAME WITH CURRENT OPEN LISTINGS
open_listings = sale_data[~sale_data['link'].isna()][[
    'street',
    'square_m',
    'rooms',
    'floor',
#     'building_total_floors',
#     'serie',
    'price',
    'price_per_square_m',
    'link']]

st.dataframe(open_listings)





# st.line_chart(sale_summary['count'])

### BOKEH ###
# summary_chart = figure(x_axis_type="datetime", plot_height=500)
# summary_chart.line(sale_summary.index, sale_summary['count'])
# curdoc().add_root(summary_chart)
# st.bokeh_chart(summary_chart, use_container_width=True)

# st.title('web app title')
# st.text('web app text')
# st.text_input('first name')

