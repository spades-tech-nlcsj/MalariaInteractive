import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# Load world shapefile or GeoJSON data
@st.cache_data
def load_geo_data():
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    return world


@st.cache_data
def load_malaria_data():
    data = {
        'country': ['Brazil', 'India', 'Nigeria', 'Thailand', 'Congo (Kinshasa)'],
        '2023': [50000, 250000, 350000, 15000, 400000],
        '2025': [55000, 300000, 400000, 20000, 450000],
        '2030': [70000, 400000, 500000, 30000, 600000],
    }
    return pd.DataFrame(data)


st.title("Malaria Predictions by Country")
st.sidebar.header("Settings")


geo_data = load_geo_data()
malaria_data = load_malaria_data()


geo_data = geo_data.rename(columns={'name': 'country'})
merged_data = geo_data.merge(malaria_data, on='country', how='left')


year = st.sidebar.slider("Select Year", min_value=2023, max_value=2030, step=1)
year_column = str(year)


merged_data['cases'] = merged_data[year_column]


fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color="cases",
    hover_name="country",
    projection="natural earth",
    color_continuous_scale="YlOrRd",
    labels={'cases': 'Malaria Cases'},
    title=f"Malaria Predictions for {year}"
)

fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)

st.sidebar.write("Note: Predictions are based on hypothetical data.")
