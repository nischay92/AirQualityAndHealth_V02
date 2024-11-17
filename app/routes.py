from flask import Blueprint, render_template, request, jsonify, send_file
from . import db
from .enums import Pollutants, IndianaCounty
from .models import AirQualityData
import pandas as pd
import folium
import plotly.express as px

import json,os
# Create a Blueprint for routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', title='Air Quality Dashboard')
#Base test for the code
@main.route('/statistics')
def statistics():
    return render_template('statistics.html',pollutants = Pollutants, countys = IndianaCounty)


@main.route('/geography')
def geography():
    return render_template('geography.html',pollutants = Pollutants, countys = IndianaCounty)

@main.route('/search', methods=['GET'])
def search():
    # Extract query parameters from the form
    data = pd.read_csv("/Users/nischay92/Documents/IUBCourse/LuddyHacks16Nov/AirQualityAndHealth_V01/AirData.csv")

    pollutant = request.args.get('pollutant')
    county = request.args.get('county')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Filter the data
    filtered_data = data[
        (data['pollutants'] == pollutant) &
        (data['county'] == county) &
        (data['date_local'] >= start_date) &
        (data['date_local'] <= end_date)
    ]

    # Convert filtered data to list of dictionaries
    results = filtered_data.to_dict(orient='records')

    # If it's an AJAX request, return JSON data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(results)

    # Otherwise, render the results page
    return render_template('/PartialPages/results.html', results=results)

@main.route('/search_geo', methods=['GET'])
def search_geo():
    # Get form data
    pollutant = request.args.get('pollutant')
    county = request.args.get('county')
    start_date = request.args.get('startdate')
    end_date = request.args.get('enddate')

    # Convert dates to datetime
    

    
    # Load the data
    data = pd.read_csv("/Users/nischay92/Documents/IUBCourse/LuddyHacks16Nov/AirQualityAndHealth_V01/AirData.csv")
    data['date_local'] = pd.to_datetime(data['date_local'], errors='coerce')

    # Filter the data based on user inputs
    filtered_data = data[(data['county'] == county) &
                         (data['pollutants'] == pollutant) &
                         (data['date_local'] >= start_date) &
                         (data['date_local'] <= end_date)]
    
        
    avg_arithmetic_mean = filtered_data['arithmetic_mean'].mean()

    
    # Prepare the map
    map_ = folium.Map(location=[40.2672, -86.1349], zoom_start=8)

    #Load the GeoJSON file for state boundaries
    geojson_file_path = "/Users/nischay92/Documents/IUBCourse/LuddyHacks16Nov/AirQualityAndHealth_V01/pollutantDataMap.geojson"  # Replace with your GeoJSON file path
    folium.GeoJson(
        geojson_file_path,
        name="State Boundaries",
        style_function=lambda feature: {
            'fillColor': 'blue',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.1,
        }
    ).add_to(map_)

    # Filter for the county
    latitude = 0
    longitude = 0
    popup_text = ""
    county_data = data[data['county'] == county] 

    if not county_data.empty:
        latitude = county_data.iloc[0]['latitude']
        longitude = county_data.iloc[0]['longitude']
    
        popup_text = (f"<b>County:</b> {county}<br>"
                        f"<b>Pollutant:</b> {pollutant}<br>"
                        f"<b>Average Value:</b> {avg_arithmetic_mean:.2f}" if avg_arithmetic_mean is not None else "No data available")
    folium.Marker(
                location=[latitude, longitude],
                popup=popup_text,
                icon=folium.Icon(color='blue', icon="info-sign")
            ).add_to(map_)
    map_path = "static/Genmap1.html"
    map_.save(map_path)
    map_html = map_._repr_html_()

    return render_template('map.html', map_html=map_html)
ss