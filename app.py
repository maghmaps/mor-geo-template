import chorol
import postal_office
import beaches_ma
import streamlit as st
from PIL import Image

img_morocco = Image.open('static/morocco_logo.png')

PAGES = {
    "Covid": chorol,
    "Postal Office": postal_office,
    "Beaches": beaches_ma
}
st.set_page_config(layout="wide", page_icon=img_morocco, page_title="MA map templates")
st.sidebar.title('Morocco Map templates')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()