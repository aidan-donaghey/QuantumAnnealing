from re import template
import pandas as pd
import os
import gmaps
import APIKey
import streamlit as st
import pydeck as pdk
import numpy as np
import googlemaps
import SessionState
import Quantum_Annealing as qa
import plotly.io as pio


from urllib.error import URLError

import plotly.graph_objects as go
import plotly.express as px


gmaps = googlemaps.Client(key=APIKey.googleMapsKey)





cities = []
infoList = []
ss = SessionState.get(cities = cities, infoList = infoList)

citiesdata = pd.DataFrame(ss.infoList, columns =["Location","lat","lng"] )



def quantumCityOrder(cities, sol=None):
  n_city = len(cities)
  cities_dict = dict(cities)
  # draw path
  if sol:
      city_order = []
      for i in range(n_city):
          for j in range(n_city):
              if sol[0][f'c[{i}][{j}]'] == 1:
                  city_order.append(j)
      # st.write("The new city order is...")
      # st.write(city_order)
      return city_order
              

form = st.form(key='my_form')
text = form.text_input(label='Enter some text')
submit_button = form.form_submit_button(label='Submit')




if submit_button:
  ss.cities.append(gmaps.geocode(text))
  ss.infoList.append([gmaps.geocode(text)[0]["formatted_address"],gmaps.geocode(text)[0]['geometry']['location']['lat'] ,gmaps.geocode(text)[0]['geometry']['location']['lng']])
  citiesdata = pd.DataFrame(ss.infoList, columns =["Location","lat","lng"] )

st.write(f"You have currently Selected {len(ss.infoList)} cities")
if len(ss.infoList)!=0:
  st.dataframe(citiesdata,width=700, height=768)




# plotbutton = st.button("Plot The unoptimised Map")

# if plotbutton:
centerLocation = (citiesdata["lat"].mean(), citiesdata["lng"].mean())
print(centerLocation)
# fig = px.line_mapbox(citiesdata, lat="lat", lon="lng",zoom=0.8, height=300,hover_name="Location", center=dict(lat=centerLocation[0], lon=centerLocation[1]))
# fig.update_layout(mapbox_style="carto-darkmatter",margin={"r":0,"t":0,"l":0,"b":0},
# hoverlabel=dict(
#       bgcolor="white",
#       font_size=16,))
# st.plotly_chart(fig)  
fig2 = px.line_geo(citiesdata, lat="lat", lon="lng",hover_name="Location",
                #projection="orthographic"
                )
fig2.update_layout(mapbox_style="carto-darkmatter",margin={"r":0,"t":0,"l":0,"b":0},
hoverlabel=dict(
      bgcolor="white",
      font_size=16,))
fig2.update_geos(
  resolution=50,
  showcoastlines=True, coastlinecolor="RebeccaPurple",
  showland=True, landcolor="LightGreen",
  showocean=True, oceancolor="LightBlue",
  #showlakes=True, lakecolor="Blue",
  #showrivers=True, rivercolor="Blue"
)
st.plotly_chart(fig2)  


#st.write(qa.setcities(citiesdata))
#st.write("Below is the getcities func")
#st.write(qa.getcities())

QAbutton = st.button("Run the QA")
if QAbutton:
  bestsample = qa.RunQA(qa.setcities(citiesdata))
  sortedOrder = quantumCityOrder(qa.setcities(citiesdata),bestsample)
  #figure = qa.plot_cityQuantum(qa.setcities(citiesdata),bestsample)
  # We need to get it to plot it on the map now from best sample
  
  #st.pyplot(figure)
  ordredcities = citiesdata.reindex(sortedOrder)
  # orderdcities = ordredcities.append(ordredcities.iloc[0])
  df2 = ordredcities.iloc[0]
  ordredcities = ordredcities.append(df2, ignore_index = True)
  # print(ordredcities)
  # st.dataframe(ordredcities)

  #Actually Plotting the data
  centerLocation = (ordredcities["lat"].mean(), ordredcities["lng"].mean())
  # print(centerLocation)
  st.title("This is the fasteset route to hit all places and return home")
  # fig = px.line_mapbox(ordredcities, lat="lat", lon="lng",zoom=0.8, height=300,hover_name="Location", center=dict(lat=centerLocation[0], lon=centerLocation[1]))
  # fig.update_layout(mapbox_style="carto-darkmatter",margin={"r":0,"t":0,"l":0,"b":0},
  # hoverlabel=dict(
  #       bgcolor="white",
  #       font_size=16,))
  fig3 = px.line_geo(ordredcities, lat="lat", lon="lng",hover_name="Location",
                  #projection="orthographic"
                  )
  fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
  hoverlabel=dict(
        bgcolor="white",
        font_size=16,))
  fig3.update_geos(
    resolution=50,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    #showlakes=True, lakecolor="Blue",
    #showrivers=True, rivercolor="Blue"
  )
  st.plotly_chart(fig3)  
    
  
  # st.plotly_chart(fig)  



