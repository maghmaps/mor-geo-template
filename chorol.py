import streamlit as st
import pydeck as pdk
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
import geopandas as gpd
from string import Template

def color_mapper(x=None, Min=None, Max=None, cmap=None, rcmap=None):   
    norm = mpl.colors.Normalize(vmin=Min, vmax=Max)
    if rcmap:
        cmap = cmap + "_r"
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return list(np.array(m.to_rgba(x))*255)

colormaps = {'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'}
gpdf = gpd.read_file("geodata/regions-covid-all-meth1.geojson")
mapbox_dark = 'mapbox://styles/snat/ckzpwerds000a14ma6l76yecv'
mapbox_chill = 'mapbox://styles/snat/ckovh4n3t0bkh18t3kr3o2854'
mapbox_pink = 'mapbox://styles/snat/ckovhievq107c18moysya7axu'
mapbox_stree = "mapbox://styles/snat/ckztx7onj00tj14p8pmkbb0y8"
mapbox_satel = "mapbox://styles/snat/ckztxcmz1004a14palj45lpte"
styles = ('Street', 'Chill', 'Dark', 'Pink', 'Satellite')

def app():
    st.title('Monthly Covid-19 deaths / cases in Morocco')
    colsl1, colsl2 = st.columns([1,4])
    with colsl1:
        Type = st.select_slider(
             'Cases | Deaths',
             options=('Cases', 'deaths'))

    if Type=="deaths":
        colnames = [el for el in gpdf.columns if "deaths_" in el]
    elif Type=="Cases":
        colnames = [el for el in gpdf.columns if "cases_" in el]
    with colsl2:
        colname = st.select_slider(
             'Year_month',
             options=colnames)
    
    col1, col2, col3 = st.columns([1,1,4])
    with col3:
        style = st.select_slider(
             'Map styles',
             options=styles)
    with col1:
        cmapoption = st.selectbox(
             'Colormaps',
             colormaps)
    with col2:
        opacity = st.number_input('Color opacity',min_value=0.0, max_value=1.0, step=0.1, value=0.6)
    
    rcmap = st.checkbox('Reverse colormap')
    
    if style=="Dark":
        map_style = mapbox_dark
    elif style=="Chill":
        map_style = mapbox_chill
    elif style=="Pink":
        map_style = mapbox_pink
    elif style=="Street":
        map_style = mapbox_stree
    elif style=="Satellite":
        map_style = mapbox_satel

    gpdf["fill_color"] = gpdf[colname].apply(lambda x:color_mapper(x, min(gpdf[colname]),
                                                                   max(gpdf[colname]), cmapoption, rcmap))

    geoj_layer = pdk.Layer(
        "GeoJsonLayer",
        gpdf,
        opacity=opacity,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        get_elevation=colname,
        get_fill_color="fill_color",
        get_line_color=[255, 255, 255],
    )

    t = Template("region: {region}\n$Type: {$colname}")
    final_tooltip = t.substitute(Type=Type, colname=colname)

    st.pydeck_chart(pdk.Deck(
        map_provider="mapbox",
        map_style=map_style,
        tooltip={"text": final_tooltip},
        initial_view_state = pdk.ViewState(latitude=28.256621, longitude=-10.41288, zoom=4, max_zoom=10, min_zoom=2), #morocco
        layers=[geoj_layer],
     ))