import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

#This is a styling option

def title_Intro():
  with open ("IntroMarkdown.md", "r") as file:
    data = file.read()
    #.replace('\n', '')
  st.markdown(data)

def plotMap(citiesdata, projection=None):
  centerLocation = (citiesdata["lat"].mean(), citiesdata["lng"].mean())
  if projection is None:
    projection="natural earth"
  fig2 = px.line_geo(citiesdata, lat="lat", lon="lng",hover_name="Location",
                  projection=projection,
                  )

  fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},hovermode = "x unified"
  ,hoverlabel=dict(
        bgcolor= "#d3d3d3",
        font_size=10,))
  fig2.update_geos(
    resolution=50,
    #showcoastlines=True, coastlinecolor="#d3d3d3",
    showland=True, landcolor="#e0efef",
    showocean=True, oceancolor="#c0e8e8",
    bgcolor="#002b36",
  )
  st.plotly_chart(fig2)  

