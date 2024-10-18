import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
 
######################################################################
### IMPORTING DATA ###
sale_data = pd.read_pickle('sale_data.pkl')
rent_data = pd.read_pickle('rent_data.pkl')


######################################################################
### DEFINE FILTER RANGES
# max_floors = int(sale_data['floor'].max())
# max_rooms = int(sale_data['rooms'].max())
# max_size = int(sale_data['square_m'].max())
max_floors = int(33)
max_rooms = int(6)
max_size = int(640)


######################################################################
### SIDEBAR ###
### REGION SELECTION
regions = sale_data['region'].value_counts().index.values
regions = np.insert(regions, 0, 'All regions')

select_region = st.sidebar.selectbox('Select region:', regions)

if select_region != 'All regions':
    sale_data = sale_data[sale_data['region'] == select_region]
    rent_data = rent_data[rent_data['region'] == select_region]
    
    
### FLOOR SELECTION
select_floor = st.sidebar.slider('Select floor:', value=[1, max_floors], min_value = 1, max_value = max_floors)

sale_data = sale_data[sale_data['floor'] >= select_floor[0]]
sale_data = sale_data[sale_data['floor'] <= select_floor[1]]

rent_data = rent_data[rent_data['floor'] >= select_floor[0]]
rent_data = rent_data[rent_data['floor'] <= select_floor[1]]


### ROOM COUNT SELECTION
select_rooms = st.sidebar.slider('Select room count:', value=[1, max_rooms], min_value = 1, max_value = max_rooms)

sale_data = sale_data[sale_data['rooms'] >= select_rooms[0]]
sale_data = sale_data[sale_data['rooms'] <= select_rooms[1]]

rent_data = rent_data[rent_data['rooms'] >= select_rooms[0]]
rent_data = rent_data[rent_data['rooms'] <= select_rooms[1]]


### SIZE SELECTION
select_size = st.sidebar.slider('Select size (square meters):', value=[1, max_size], min_value = 1, max_value = max_size)

sale_data = sale_data[sale_data['square_m'] >= select_size[0]]
sale_data = sale_data[sale_data['square_m'] <= select_size[1]]

rent_data = rent_data[rent_data['square_m'] >= select_size[0]]
rent_data = rent_data[rent_data['square_m'] <= select_size[1]]


######################################################################
### CREATE SUMMARY TABLE
sale_summary = sale_data.groupby('time')
sale_summary = sale_summary.agg(
                                count = ('rooms', 'count'),
                                mean_price_per_square = ('price_per_square_m', 'mean')
                                )

rent_summary = rent_data.groupby('time')
rent_summary = rent_summary.agg(
                                count = ('rooms', 'count'),
                                mean_price_per_square = ('price_per_square_m', 'mean')
                                )


######################################################################
### TABS ###
# sale_tab, rent_tab = st.tabs(['FOR SALE', 'FOR RENT'])
sale_tab, rent_tab, yields_tab = st.tabs(['FOR SALE', 'FOR RENT', 'YIELDS'])

######################################################################
### FOR SALE TAB ###
sale_tab.header('Apartments for sale')
sale_tab.caption('On the sidebar at the left, you can specify the criteria by which you want to filter the data. All charts and tables in all the tabs are automatically updated right after the filter setting is changed. Once per day, at around midnight, the dataset is updated with the latest advertisement data.')
sale_tab.caption('')

### CHARTS
sale_tab.subheader('Count of listings')
sale_tab.caption('Below chart shows how many apartments were listed for sale at particular dates')
fig_sale_count = px.line(sale_summary, y='count')
sale_tab.plotly_chart(fig_sale_count, theme="streamlit")

sale_tab.subheader('Average price per square meter')
sale_tab.caption('Below chart shows what was the average price per square meter at particular dates')
fig_sale_price = px.line(sale_summary, y='mean_price_per_square', labels={'mean_price_per_square':'mean price per square meter'})
sale_tab.plotly_chart(fig_sale_price, theme="streamlit")


### FILTER PAST X MONTHS

sale_tab.subheader('Price distribution for listings posted in the last X months')
sale_tab.caption('Below histogram shows the distribution of prices per square meter for advertisments that were posted in the last X months (you can specify the lookback period)')

sale_months_back = sale_tab.number_input('Choose lookback time frame (in months):', min_value=1, max_value=12, value=6, key='sales_lookback')
sale_hist = sale_data[sale_data['time'] >= pd.to_datetime('now') - pd.DateOffset(months=sale_months_back)]

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

fig_sale_histogram = px.histogram(sale_hist, x="price_per_square_m")
fig_sale_histogram.update_xaxes(range=[0, 5000])

sale_tab.plotly_chart(fig_sale_histogram, theme="streamlit")



# ######################################################################
# ### FOR RENT TAB ###
# rent_tab.header('Apartments for rent')
# rent_tab.caption('On the sidebar at the left, you can specify the criteria by which you want to filter the data. All charts and tables in all the tabs are automatically updated right after the filter setting is changed. Once per day, at around midnight, the dataset is updated with the latest advertisement data.')
# rent_tab.caption('')

# ### CHARTS
# rent_tab.subheader('Count of listings')
# rent_tab.caption('Below chart shows how many apartments were listed for rent at particular dates')
# fig_rent_count = px.line(rent_summary, y='count')
# rent_tab.plotly_chart(fig_rent_count, theme="streamlit")

# rent_tab.subheader('Average price per square meter')
# rent_tab.caption('Below chart shows what was the average price per square meter at particular dates')
# fig_rent_price = px.line(rent_summary, y='mean_price_per_square', labels={'mean_price_per_square':'mean price per square meter'})
# rent_tab.plotly_chart(fig_rent_price, theme="streamlit")


# ### FILTER PAST X MONTHS

# rent_tab.subheader('Price distribution for listings posted in the last X months')
# rent_tab.caption('Below histogram shows the distribution of prices per square meter for advertisments that were posted in the last X months (you can specify the lookback period)')

# rent_months_back = rent_tab.number_input('Choose lookback time frame (in months):', min_value=1, max_value=12, value=6, key='rents_lookback')
# rent_hist = rent_data[rent_data['time'] >= pd.to_datetime('now') - pd.DateOffset(months=rent_months_back)]

# rent_hist['idx'] = (
#     rent_hist['rooms'].astype(str)
#     + '-'
#     + rent_hist['square_m'].astype(str)
#     + '-'
#     + rent_hist['floor'].astype(str)
#     + '-'
#     + rent_hist['price'].astype(str)
#     + '-'
#     + rent_hist['street'].astype(str)
# )

# rent_hist = rent_hist.drop_duplicates(subset='idx')

# fig_rent_histogram = px.histogram(rent_hist, x="price_per_square_m")
# fig_rent_histogram.update_xaxes(range=[0, 30])

# rent_tab.plotly_chart(fig_rent_histogram, theme="streamlit")


# ### DATAFRAME WITH CURRENT OPEN LISTINGS
# rent_open_listings = rent_data[~rent_data['link'].isna()][[
#     'street',
#     'square_m',
#     'rooms',
#     'floor',
# #     'building_total_floors',
# #     'serie',
#     'price',
#     'price_per_square_m',
#     'link']]


# rent_tab.subheader('Active listings')
# rent_tab.caption('Below table shows all apartment listings that are currently active')
# rent_tab.dataframe(rent_open_listings)


# ######################################################################
# ### YIELDS TAB ###

# yield_annual = ((rent_summary['mean_price_per_square'] * 12) / sale_summary['mean_price_per_square']) * 100

# ### CHARTS
# yields_tab.subheader('Annual yield')
# yields_tab.caption('Below chart shows the annual yield of renting out an apartment, according to average rent and sale price per square meter. The formula is:')
# yields_tab.caption('(AVG rent price per square meter * 12)  /  AVG sale price per square meter')

# fig_yield = px.line(yield_annual, y='mean_price_per_square', labels={'mean_price_per_square':'annual yield (%)'})
# yields_tab.plotly_chart(fig_yield, theme="streamlit")
