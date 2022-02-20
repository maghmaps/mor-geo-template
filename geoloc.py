import streamlit as st
import pandas as pd
import pydeck as pdk

postes = pd.read_excel("geodata/agences-de-pm-avec-coordonnes-spatiales.xls")
postes.columns = postes.columns.tolist()[:-2] + ["longitude", "latitude"]

mapbox_dark = 'mapbox://styles/snat/ckzpwerds000a14ma6l76yecv'
mapbox_chill = 'mapbox://styles/snat/ckovh4n3t0bkh18t3kr3o2854'
mapbox_pink = 'mapbox://styles/snat/ckovhievq107c18moysya7axu'
mapbox_stree = "mapbox://styles/snat/ckztx7onj00tj14p8pmkbb0y8"
mapbox_satel = "mapbox://styles/snat/ckztxcmz1004a14palj45lpte"

def app():
    st.title('Postal offices in Morocco')
    h = st.color_picker('Pick A Color', '#DA8C58').lstrip('#')
    color = list(int(h[i:i+2], 16) for i in (0, 2, 4))

    styles = ('Street', 'Chill', 'Dark', 'Pink', 'Satellite')
    style = st.select_slider(
         'Map styles',
         options=styles)

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
        tooltip={"text": "nom: {RESEAU}\nadresse: {ADRESSE}"},
        initial_view_state = pdk.data_utils.viewport_helpers.compute_view(points=postes[['longitude','latitude']],
                                                                         view_proportion=1),
        layers=[
             pdk.Layer(
                 'ScatterplotLayer',
                 data=postes,
                 pickable=True,
                opacity=0.4,
                stroked=True,
                filled=True,
                 get_position=['longitude','latitude'],
                 get_fill_color=color,#[255, 140, 0],
                 get_line_color=[0, 0, 0],
                 get_radius=100,
                 radius_min_pixels=2,
                 radius_max_pixels=100,
                 radius_scale=6,
                 lineWidthMinPixels=1
             ),
         ],
     ))