import streamlit as st
import geopandas as gpd
import pydeck as pdk
from PIL import Image
from pathlib import Path
import base64

img_pavillon = 'static/pavillonbleu.jpg'
img_toilet = 'static/wc.png'
img_bus = 'static/public-transport.png'
img_water = 'static/drinkable-water.png'
img_shower = 'static/shower.png'
img_firstaid = 'static/first-aid-kit.png'
img_waste = 'static/recycle-bin.png'
img_lifeguard = 'static/life-saver.png'
img_security = 'static/guard.png'
img_morocco = 'static/morocco_logo.png'
img_bad_water = 'static/no-swimming.png'

mapbox_dark = 'mapbox://styles/snat/ckzpwerds000a14ma6l76yecv'
mapbox_chill = 'mapbox://styles/snat/ckovh4n3t0bkh18t3kr3o2854'
mapbox_pink = 'mapbox://styles/snat/ckovhievq107c18moysya7axu'
mapbox_stree = "mapbox://styles/snat/ckztx7onj00tj14p8pmkbb0y8"
mapbox_satel = "mapbox://styles/snat/ckztxcmz1004a14palj45lpte"

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

header_html = "<h1>Morocco Beaches <img src='data:image/png;base64,{}' class='img-fluid' style='width:40px;height:40px;'></h1>".format(
    img_to_bytes("static/morocco_logo.png")
)

def add_img_to_tooltip(Img_path):
    header_html = "<img src='data:image/png;base64,{}' style='width:20px;height:20px;'>".format(
    img_to_bytes(Img_path)
)
    return header_html

def app():
    
    df = gpd.read_file("geodata/beaches_ma.geojson")# source view-source:https://labo.environnement.gov.ma/plages-api
    st.markdown(header_html, unsafe_allow_html=True)
    
    colstyle1, colstyle2 = st.columns([1,3])
    with colstyle1:
        h = st.color_picker('Pick A Color', '#DA8C58').lstrip('#')
        color = list(int(h[i:i+2], 16) for i in (0, 2, 4))
    with colstyle2:
        styles = ('Street', 'Chill', 'Dark', 'Pink', 'Satellite')
        style = st.select_slider(
             'Map styles',
             options=styles)
    
    tooltip = {
       "html": "{nameFr} {nameAr} <br/> \
       city : {commune} <br/> \
       Length: {lngPlage} km <br/> \
       <img src={image_phone} alt='' style='width:150px;height:150px;'> <br/> \
       "
    }
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col0 = st.columns(10)
    with col1:
        toilet = st.checkbox("WC", key=st.image(Image.open(img_toilet), width=30))
        if toilet:
            df= df[df["toilets"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_toilet)
    with col2:
        bus = st.checkbox("Public Transport", key=st.image(Image.open(img_bus), width=30))
        if bus:
            df= df[df["transport"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_bus)
    with col3:
        potable_water = st.checkbox("Drinkable water", key=st.image(Image.open(img_water), width=30))
        if potable_water:
            df= df[df["reseauAEP"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_water)
    with col4:
        shower = st.checkbox("Shower", key=st.image(Image.open(img_shower), width=30))
        if shower:
            df= df[df["douches"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_shower)
    with col5:
        wastebasket = st.checkbox("Waste Bin", key=st.image(Image.open(img_waste), width=30))
        if wastebasket:
            df= df[df["poubelles"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_waste)
    with col6:
        ambulance = st.checkbox("First aid", key=st.image(Image.open(img_firstaid), width=30))
        if ambulance:
            df= df[df["centrePremiersSoins"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_firstaid)
    with col7:
        oncoming_police_car = st.checkbox("Security", key=st.image(Image.open(img_security), width=30))
        if oncoming_police_car:
            df= df[df["surete"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_security)
    with col8:
        clean = st.checkbox("Lifeguard", key=st.image(Image.open(img_lifeguard), width=30))
        if clean:
            df= df[df["baignade"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_lifeguard)
    with col9:
        pavillon_bl = st.checkbox("pavillon bleu", key=st.image(Image.open(img_pavillon), width=30))
        if pavillon_bl:
            df= df[df["pavillonBleu"]==True]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_pavillon)
    with col0:
        bad_water = st.checkbox("Bad water", key=st.image(Image.open(img_bad_water), width=30))
        if bad_water:
            df= df[df["quality"]==-1]
            tooltip["html"] = tooltip["html"] + add_img_to_tooltip(img_bad_water)
        
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
        tooltip=tooltip,
        initial_view_state = pdk.ViewState(latitude=28.256621, longitude=-10.41288, zoom=4, max_zoom=20, min_zoom=2), #morocco
        layers=[
             pdk.Layer(
                 'ScatterplotLayer',
                 data=df,
                 pickable=True,
                opacity=0.4,
                stroked=True,
                filled=True,
                 get_position=['longitude','latitude'],
                 get_fill_color=color,#[255, 140, 0],
                 get_line_color=[0, 0, 0],
                 get_radius=100,
                 radius_min_pixels=5,
                 radius_max_pixels=100,
                 radius_scale=6,
                 lineWidthMinPixels=1
             ),
         ],
     ))