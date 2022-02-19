import chorol
import geoloc
import streamlit as st
PAGES = {
    "Chorolpleth": chorol,
    "Geoloc": geoloc
}
st.sidebar.title('Morocco Map templates')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()