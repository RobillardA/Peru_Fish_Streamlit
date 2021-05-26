import streamlit as st
import pandas as pd
import altair as alt

st.title('Gap Minder')

st.markdown("*Here's some text*")

DATA_URL = ('https://raw.githubusercontent.com/MikeTrizna/binder_demo/master/gapminder_data.tsv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL, sep='\t')
    return data

def bubble_chart(df, year, continent = 'All'):
    if continent == 'All':
        df_year = df[df['year'] == year].copy()
        chart_title = f'{year}: All continents'
    else:
        df_year = df[(df['year'] == year) & (df['continent'] == continent)]
        chart_title = f'{year}: {continent}'
    alt_chart = alt.Chart(df_year).mark_circle().encode(
        alt.X('gdpPercap:Q', scale=alt.Scale(type='log', domain=(100, 100000))),
        alt.Y('lifeExp:Q', scale=alt.Scale(domain=(25, 90))),
        size=alt.Size('pop:Q'),
        color='continent:N',
        tooltip=['country', 'lifeExp', 'pop', 'gdpPercap']
    ).properties(title=chart_title).interactive()
    return alt_chart

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done!")

possible_years = data['year'].unique()

continent = st.selectbox('Cotinent',
                        ['All','Asia', 'Europe', 'Africa', 'Americas', 'Oceania'])

gap_year = st.slider('Year', min_value=1952, max_value=2007, step=5)

test_chart = bubble_chart(data, gap_year, continent)
st.altair_chart(test_chart, use_container_width=True)