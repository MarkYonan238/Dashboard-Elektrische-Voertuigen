#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import plotly.express as px
import streamlit as st
import geopandas as gpd
import numpy as np
import folium
from folium import plugins
from streamlit_folium import folium_static
from PIL import Image
import statsmodels.api as sm
import plotly.graph_objects as go


# In[2]:


#Sidebar info
st.set_page_config(layout="wide")
rad = st.sidebar.radio(options=('Home', 'Maps', 'Laadpaal Info', 'Elektrische Voertuigen'), 
                        label='Selecteer Categorie')
st.sidebar.markdown('#')
st.sidebar.markdown('#')

st.sidebar.subheader('Gemaakt Door:')
st.sidebar.write('• Mara van Boeckel')
st.sidebar.write('• Aniska Sinnige')
st.sidebar.write('• Maarten van der Veer')
st.sidebar.write('• Mark Yonan')


# ## Home

# In[3]:


if rad == 'Home':
    st.title('Dashboard Elektrische Voertuigen Nederland')
    img = Image.open("foto.png")
    st.image(img, width=800)
    "Het aanbod van elektrische auto's is de afgelopen jaren steeds meer gegroeid. Dat is ook te zien op de weg. Het percentage elektrische auto’s op de weg lijkt steeds groter te worden. Om dat te onderzoeken hebben we gekeken naar data van de RDW over elektrische voertuigen. Ook is er gekeken naar de plaatsing van laadpalen in Drenthe en een verdeling van de laadtijden per paal. Er wordt een regressielijn gevisualiseerd om een voorspelling te kunnen maken over de groei van auto’s van verschillende brandstoftypes. "
    "Indien de verwachte groei gevonden wordt voor het aantal elektrische auto’s wordt ook gekeken naar de hoeveelheid elektrische laadpalen per elektrische auto en hoeveel er daar nodig van zijn met de groei van elektrische auto’s"

# ## Maps

# In[4]:


if rad == 'Maps':
    st.header('Map Visualisaties')
    st.markdown('#')
    st.subheader('Aantal Laadpalen Drenthe')
    'Onderstaande afbeelding geeft een kaart weer van de laadpaal locaties in de provincie Drenthe.'
    ##############################################################################################################
    #Code laadpalen Drenthe
    gpd_provinces = gpd.read_file('provinces.geojson')
    df_map = pd.read_csv('map_data_cleaned.csv')
    df_dr = df_map[df_map['Province'] == 'Drenthe']

    map_dr = folium.Map(location=[52.9476012, 6.6230586], zoom_start=9.4, tiles='cartodbpositron')

    for row in df_dr.iterrows():
        row_values = row[1] 
        location = [row_values['LAT'], row_values['LNG']]
        popup = ('Adres: ' + str(row_values['Address Line']))
        marker = folium.Marker(location = location, popup = popup, icon=folium.Icon(icon='flash', color='green'))
        marker.add_to(map_dr)
    
    
    folium.GeoJson(gpd_provinces.iloc[0]['geometry']).add_to(map_dr)

    folium_static(map_dr)
    ##############################################################################################################
    st.markdown('#')
    st.markdown('#')
    st.subheader('Heatmap Laadpalen Drenthe')
    '...'
    
    #Code heatmap Drenthe
    map_heat = folium.Map(location=[52.9476012, 6.6230586], zoom_start=9.4, tiles='cartodbpositron')

    map_heat.add_child(plugins.HeatMap(df_dr[['LAT', 'LNG']].values, radius=19))
    folium.Marker(location=[52.993668, 6.548259],popup='<strong>'+'Assen'+'</strong>').add_to(map_heat)
    folium.Marker(location=[52.7558037, 6.9095851],popup='<strong>'+'Emmen'+'</strong>').add_to(map_heat)
    folium.Marker(location=[52.7286158, 6.4701002],popup='<strong>'+'Hoogeveen'+'</strong>').add_to(map_heat)
    folium.Marker(location=[53.1383574, 6.4123693],popup='<strong>'+'Roden'+'</strong>').add_to(map_heat)
    folium.Marker(location=[53.0841274, 6.6648434],popup='<strong>'+'Zuidlaren'+'</strong>').add_to(map_heat)

    folium.GeoJson(gpd_provinces.iloc[0]['geometry']).add_to(map_heat)

    folium_static(map_heat)
    ##############################################################################################################
    st.markdown('#')
    st.markdown('#')
    st.subheader('Tarieven Laadpalen Drenthe')
    '...'
    
    #Code tarieven laadpalen
    def bekend(prijs):
        if prijs != 0:
            color = 'green'
        elif prijs == 0:
            color = 'red'
        
        return color

    #popup voor tarief
    def prijs(totaal):
        if totaal != 0:
            popup = '€' + str(totaal) + ' per kWh'
        elif totaal == 0:
            popup = 'Onbekend Tarief'
        
        return popup


    map_tr = folium.Map(location=[52.9476012, 6.6230586], zoom_start=9.4, tiles='cartodbpositron')

    for row in df_dr.iterrows():
        row_values = row[1] 
        location = [row_values['LAT'], row_values['LNG']]
        popup = (prijs(row_values['Usage Cost']))
        marker = folium.Marker(location = location, popup = popup, icon=folium.Icon(icon='flash', 
                                                                                color=
                                                                                    bekend(row_values['Usage Cost'])))
        marker.add_to(map_tr)    
    
    folium.GeoJson(gpd_provinces.iloc[0]['geometry']).add_to(map_tr)

    folium_static(map_tr)
    ##############################################################################################################
    st.markdown('#')
    st.markdown('#')
    st.subheader('Gemaakte Laadpalen per Jaar Nederland')
    '...'
    
    #Code histogram laadpalen jaren
    df_map['Date Created'] = pd.to_datetime(df_map['Date Created'])

    fig = px.histogram(x=df_map['Date Created'].dt.year)

    fig.update_layout({'xaxis':{'title':{'text': 'Jaar'}},
                   'yaxis':{'title':{'text':'Aantal Gemaakte Laadpalen'}},
                   'title':{'text':'Gemaakte laadpalen per jaar Nederland', 'x':0.5}}, 
                  xaxis = dict(tickmode = 'linear', tick0 = 2011, dtick = 1), 
                  bargap=0.2)    

    st.plotly_chart(fig)
    ##############################################################################################################
    st.markdown('#')
    st.subheader('Aantal Laadpalen per Provincie')
    '...'
    
    #Code laadpalen per provincie
    df_lprov= pd.read_csv('Laadpaal_Prov.csv')
    df_lprov_pivot = df_lprov.pivot(columns=['name'], values='# Laadpalen')
    df_lprov_pivot.fillna(0, inplace=True)

    fig1 = px.choropleth_mapbox(df_lprov, geojson=gpd_provinces, color='# Laadpalen', locations='name', 
                            center={"lat": 52.210216, "lon":4.895168 }, 
                            mapbox_style="carto-positron", zoom=6, featureidkey="properties.name", 
                            color_continuous_scale='reds')

    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    button1 =  dict(method = "update",
                args = [{'z': [ df_lprov['# Laadpalen'] ] }],
                label = "Alle")
    button2 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Noord-Holland'] ]}],
                label = "Noord-Holland")
    button3 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Zuid-Holland'] ]}],
                label = "Zuid-Holland")
    button4 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Zeeland'] ]}],
                label = "Zeeland")
    button5 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Noord-Brabant'] ]}],
                label = "Noord-Brabant")
    button6 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Limburg'] ]}],
                label = "Limburg")
    button7 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Utrecht'] ]}],
                label = "Utrecht")
    button8 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Gelderland'] ]}],
                label = "Gelderland")
    button9 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Overijssel'] ]}],
                label = "Overijssel")
    button10 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Drenthe'] ]}],
                label = "Drenthe")
    button11 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Groningen'] ]}],
                label = "Groningen")
    button12 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Friesland (Fryslân)'] ]}],
                label = "Friesland")
    button13 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Flevoland'] ]}],
                label = "Flevoland")

    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig1.update_layout(coloraxis_colorbar_thickness=23,
                  updatemenus=[dict(buttons=[button1, button2, button3, button4, button5, button6, button7, button8,
                                            button9, button10, button11, button12, button13])]) 

    st.plotly_chart(fig1)


# ## Laadpaal Info

# In[5]:


if rad == 'Laadpaal Info':
    st.header('Laadpaal Visualisaties')
    st.markdown('#')
    st.subheader('Verdeling Laadtijden')
    '...'
    ##############################################################################################################
    #Code verdeling laadtijden
    paal = pd.read_csv('laadpaaldata2.csv')

    fig2 = px.histogram(paal, x='M2')

    x=paal['M2'].mean()
    x1=paal['M2'].median()
    fig2.add_annotation(x=x, y=400, arrowhead=1, text='<b>Gemiddelde : 232 min</b>')
    fig2.add_annotation(x=x1, y=1000, arrowhead=1, text='<b>Mediaan : 58 min</b>', xanchor='left')

    fig2.update_layout({'xaxis':{'title':{'text': 'Laadtijd (min)'}},
                   'yaxis':{'title':{'text':'Frequentie'}}, 
                   'title':{'text':'Histogram van de laadtijd', 'x':0.5}})
    fig2.update(layout_xaxis_range = [0,1024])
    fig2.update_layout(bargap=0.2, xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 50))

    st.plotly_chart(fig2)


# ## Elektrische Voertuigen

# In[6]:


if rad == 'Elektrische Voertuigen':
    st.header('Visualisaties Elektrische Voertuigen')
    st.markdown('#')
    st.subheader('Aantal Voertuigen per Brandstof Categorie')
    '...'
    ##############################################################################################################
    cm = pd.read_csv('cmm.csv')

    #Code lijndiagram per brandstof categorie
    fig3= px.ecdf(cm, x='Datum', color='Brandstof omschrijving', ecdfnorm=None, log_y=True)

    fig3.update_layout({'xaxis':{'title':{'text': 'Datum'}},
                        'yaxis':{'title':{'text':'Frequentie'}},
                        'title':{'text':'Cumulatief Lijndiagram van het # Voertuigen per Maand', 'x':0.5}})
    fig3.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")])), rangeslider=dict(visible=True), type="date"))

    st.plotly_chart(fig3)
    ##############################################################################################################
    st.markdown('#')
    st.markdown('#')
    st.subheader('Voorspelling Aantal Voertuigen per Brandstof Categorie')
    '...'
    st.markdown('#')
    st.markdown('#')
    
    dropdown = st.selectbox('Selecteer Brandstof Categorie', ('Benzine', 'Elektriciteit', 'Diesel', 'LPG', 
                                                              'Waterstof', 'CNG'))

    #Code voorspelling aantal voertuigen
    df_vr = pd.DataFrame({'Datum':cm['Datum'].sort_values().unique(), 
                    'Aantal Benzine':cm[cm['Brandstof omschrijving'] == 'Benzine']
                                          ['Datum'].value_counts().sort_index(), 
                    'Aantal Elektriciteit':cm[cm['Brandstof omschrijving'] == 'Elektriciteit']
                                          ['Datum'].value_counts().sort_index(), 
                    'Aantal Diesel':cm[cm['Brandstof omschrijving'] == 'Diesel']
                                          ['Datum'].value_counts().sort_index(), 
                    'Aantal LPG':cm[cm['Brandstof omschrijving'] == 'LPG']
                                          ['Datum'].value_counts().sort_index(), 
                    'Aantal Waterstof':cm[cm['Brandstof omschrijving'] == 'Waterstof']
                                          ['Datum'].value_counts().sort_index(), 
                    'Aantal CNG':cm[cm['Brandstof omschrijving'] == 'CNG']
                                          ['Datum'].value_counts().sort_index()})

    df_vr.fillna(0, inplace=True)
    df_vr['Datum'] = pd.to_datetime(df_vr['Datum'])
    df_vr['Datum1'] = list(np.arange(0, 632))
    df_vr = df_vr.reset_index()
    df_vr.drop(['index'], axis=1, inplace=True)
    
    if dropdown == 'Benzine':
        #Benzine
        fig4 = px.scatter(df_vr, x='Datum1', y='Aantal Benzine', trendline='ols', trendline_color_override='red')
        fig4.update_layout({'xaxis':{'title':{'text': 'Data (Dag)'}},  
                            'yaxis':{'title':{'text':"Aantal auto's"}}, 
                            'title':{'text':"Voorspelling Aantal Auto's 2020-2021 (Benzine)", 
                            'x':0.5}})
        st.plotly_chart(fig4)
        
    elif dropdown == 'Elektriciteit':
        #Elektriciteit
        fig5 = px.scatter(df_vr, x='Datum1', y='Aantal Elektriciteit', trendline='ols',trendline_color_override='red')
        fig5.update_layout({'xaxis':{'title':{'text': 'Data (Dag)'}}, 
                            'yaxis':{'title':{'text':"Aantal auto's"}}, 
                            'title':{'text':"Voorspelling Aantal Auto's 2020-2021 (Elektriciteit)", 
                            'x':0.5}})
        st.plotly_chart(fig5)
        
    elif dropdown == 'Diesel':
        #Diesel
        fig6 = px.scatter(df_vr, x='Datum1', y='Aantal Diesel', trendline='ols', trendline_color_override='red')
        fig6.update_layout({'xaxis':{'title':{'text': 'Data (Dag)'}}, 
                            'yaxis':{'title':{'text':"Aantal auto's"}}, 
                            'title':{'text':"Voorspelling Aantal Auto's 2020-2021 (Diesel)", 
                            'x':0.5}})
        st.plotly_chart(fig6)
        
    elif dropdown == 'LPG':
        #LPG
        fig7 = px.scatter(df_vr, x='Datum1', y='Aantal LPG', trendline='ols', trendline_color_override='red')
        fig7.update_layout({'xaxis':{'title':{'text': 'Data (Dag)'}}, 
                            'yaxis':{'title':{'text':"Aantal auto's"}}, 
                            'title':{'text':"Voorspelling Aantal Auto's 2020-2021 (LPG)", 
                            'x':0.5}})
        st.plotly_chart(fig7)
        
    elif dropdown == 'Waterstof':
        #Waterstof
        fig8 = px.scatter(df_vr, x='Datum1', y='Aantal Waterstof', trendline='ols', trendline_color_override='red')
        fig8.update_layout({'xaxis':{'title':{'text': 'Data (Dag)'}}, 
                            'yaxis':{'title':{'text':"Aantal auto's"}}, 
                            'title':{'text':"Voorspelling Aantal Auto's 2020-2021 (Waterstof)", 
                            'x':0.5}})
        st.plotly_chart(fig8)
        
    elif dropdown == 'CNG':
        #CNG
        fig9 = px.scatter(df_vr, x='Datum1', y='Aantal CNG', trendline='ols', trendline_color_override='red')
        fig9.update_layout({'xaxis':{'title':{'text': 'Data (Dag)'}}, 
                            'yaxis':{'title':{'text':"Aantal auto's"}}, 
                            'title':{'text':"Voorspelling Aantal Auto's 2020-2021 (CNG)", 
                            'x':0.5}})
        st.plotly_chart(fig9)

