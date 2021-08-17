from re import template
import pandas as pd
import os
import streamlit as st
import pydeck as pdk
import numpy as np
import googlemaps
import SessionState
import Quantum_Annealing as qa
import plotly.io as pio
import os

from urllib.error import URLError

import plotly.graph_objects as go
import plotly.express as px

import components

gmaps = googlemaps.Client(key = os.getenv('GMAPS_API'))
cities = []
infoList = []
ordredcities = []
# ss = SessionState.get(cities = cities, infoList = infoList, ordredcities = ordredcities)
# Initialization
if 'cities' not in st.session_state:
    st.session_state['cities'] = cities
if 'infoList' not in st.session_state:
    st.session_state['infoList'] = infoList
if 'ordredcities' not in st.session_state:
    st.session_state['ordredcities'] = ordredcities

citiesdata = pd.DataFrame(st.session_state['infoList'], columns =["Location","lat","lng"] )

components.title_Intro()

def quantumCityOrder(cities, sol=None):
  n_city = len(cities)
  cities_dict = dict(cities)
  if sol:
      city_order = []
      for i in range(n_city):
          for j in range(n_city):
              if sol[0][f'c[{i}][{j}]'] == 1:
                  city_order.append(j)
      return city_order
              

form = st.form(key='my_form')
text = form.text_input(label='Enter some text')
submit_button = form.form_submit_button(label='Submit')




if submit_button:
  st.session_state.cities.append(gmaps.geocode(text))
  st.session_state.infoList.append([gmaps.geocode(text)[0]["formatted_address"],gmaps.geocode(text)[0]['geometry']['location']['lat'] ,gmaps.geocode(text)[0]['geometry']['location']['lng']])
  citiesdata = pd.DataFrame(st.session_state.infoList, columns =["Location","lat","lng"] )
  




#st.write(f"You have currently Selected {len(ss.infoList)} cities")
if len(st.session_state.infoList)!=0:
  st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
  st.table(citiesdata)
  st.markdown("### Unoptimised Map")
  projection = st.radio('Choose a Map Projection', ["equirectangular","orthographic","natural earth",])
  components.plotMap(citiesdata, projection)


st.markdown("### Quantum Annealing")
st.markdown("Press the 'Run' button to run the optimisation on DWAVE's quantum annealing hardware and plot a map that will give you the shortest loop to travel to all of the locations and return home in the shortest distance possible. It may take a some time to ping their server and submit the job.")
QAbutton = st.button("Run the QA")
if QAbutton:
  dimensionality = 24000
  bestsample = qa.RunQA(qa.setcities(citiesdata),dimensionality)
  sortedOrder = quantumCityOrder(qa.setcities(citiesdata),bestsample)
  st.session_state.ordredcities = citiesdata.reindex(sortedOrder)
  df2 = st.session_state.ordredcities.iloc[0]
  st.session_state.ordredcities = st.session_state.ordredcities.append(df2, ignore_index = True)
  centerLocation = (st.session_state.ordredcities["lat"].mean(), st.session_state.ordredcities["lng"].mean())

if len(st.session_state.ordredcities)!=0:
  st.title("This is the fasteset route to hit all places and return home")
  projection2 = st.radio('Choose a Map Projection', ["equirectangular","orthographic","natural earth",], key="qaradio")
  components.plotMap(st.session_state.ordredcities, projection2)




