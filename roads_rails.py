import streamlit as st
# import pandas as pd
import pydeck as pdk
import geofeather

roads = geofeather.from_geofeather('geodata/gis.osm_roads_free_1.feather')
railways =  geofeather.from_geofeather("geodata/gis.osm_railways_free_1.feather")
road_types = ["motorway", "primary", "secondary", "railways", "road bridges", "road tunnels"]

mapbox_dark = 'mapbox://styles/snat/ckzpwerds000a14ma6l76yecv'
mapbox_chill = 'mapbox://styles/snat/ckovh4n3t0bkh18t3kr3o2854'
mapbox_pink = 'mapbox://styles/snat/ckovhievq107c18moysya7axu'
mapbox_stree = "mapbox://styles/snat/ckztx7onj00tj14p8pmkbb0y8"
mapbox_satel = "mapbox://styles/snat/ckztxcmz1004a14palj45lpte"

def app():
    
    tooltip = {
       "html": "{fclass} {name} <br/> \
       code : {code} <br/> \
       maxspeed: {maxspeed} <br/> \
       oneway : {oneway} <br/>\
       "
    }
    
    st.title('Road and railways :flag-ma:')
    
    
    
    
    
    styles = ('Street', 'Chill', 'Dark', 'Pink', 'Satellite')
    
    col1, col2, col3, col4 = st.columns([1,2,2,9])
    with col1:
        h = st.color_picker('Pick A Color', '#DA8C58').lstrip('#')
        color = list(int(h[i:i+2], 16) for i in (0, 2, 4))
    with col2:
        opacity = st.number_input('Color opacity',min_value=0.0, max_value=1.0, step=0.1, value=0.6)
    with col3:
        linewidth = st.number_input('Line width',min_value=0, max_value=10, step=1, value=3)
    with col4:
        style = st.select_slider(
         'Map styles',
         options=styles)
        
    option = st.selectbox(
         'Road type',
         road_types)
    
    if option=="railways":
        df = railways
        tooltip = {
           "html": "{fclass} {name} <br/> \
           code : {code} <br/> \
           "
        }
    if option=="motorway":
        df = roads[roads.fclass=="motorway"]
    if option=="primary":
        df = roads[roads.fclass=="primary"]
    if option=="secondary":
        df = roads[roads.fclass=="secondary"]
    if option=="road bridges":
        df = roads[roads.bridge=="T"]
    if option=="road tunnels":
        df = roads[roads.tunnel=="T"]
        
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
    
    
    st.pydeck_chart(pdk.Deck(
        map_provider="mapbox",
        map_style=map_style,
        tooltip = {
           "html": "{fclass} {name} <br/> \
           code : {code} <br/> \
           "
        },
        initial_view_state = pdk.ViewState(latitude=28.256621, longitude=-10.41288, zoom=4, max_zoom=20, min_zoom=2), #morocco
        layers=[
             pdk.Layer(
                 'GeoJsonLayer',
                 data=df,
                 pickable=True,
                opacity=opacity,
                stroked=True,
                filled=True,
                 get_line_color=color,
                 lineWidthMinPixels=linewidth,
                 width_min_pixels=100,
                 width_scale=20
             ),],
     ))
    st.markdown("Reference data from http://geossc.ma/", unsafe_allow_html=True)