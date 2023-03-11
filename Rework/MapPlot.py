# from geopy.geocoders import Nominatim
# import folium
# import webbrowser

# class MapPlot:
#     def __init__(self):
#         self.geolocator = Nominatim(user_agent="my-app")
#         self.map = folium.Map(location=[35.8617, 104.1954], zoom_start=4)
        
#     def get_coordinate(self,countryname):
#         coordinate = []
#         location = self.geolocator.geocode(countryname)
#         latitude = int(location.latitude)
#         longitude = int(location.longitude)
#         coordinate.append(latitude)
#         coordinate.append(longitude)
#         return coordinate
#     def getMapPlot(self,listcountryname):
#         for i in listcountryname:
#             coordinate = self.get_coordinate(i)
#             popuptext = str(i)
#             marker = folium.Marker(location=coordinate, popup=popuptext)
#             marker.add_to(self.map)
#         self.map.save("Map.html")
#         webbrowser.open("Map.html")
# a = MapPlot()
# a.getMapPlot(["Thailand","China","Thailand"])
from geopy.geocoders import Nominatim
import folium
import webbrowser
import requests
import random
import colorsys

class MapPlot:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my-app")
        self.map = folium.Map(location=[35.8617, 104.1954], zoom_start=4)

    def get_coordinate(self,countryname):
        location = self.geolocator.geocode(countryname)
        return [location.latitude, location.longitude]

    def generate_random_colors(self,num_colors):
        colors = []
        for i in range(num_colors):
            hue = i/num_colors
            saturation = random.uniform(0.4, 1.0)
            value = random.uniform(0.4, 1.0)
            color = colorsys.hsv_to_rgb(hue, saturation, value)
            r = int(color[0]*255)
            g = int(color[1]*255)
            b = int(color[2]*255)
            hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
            colors.append(hex_color)
        return colors

    def getMapPlot(self, listcountryname):
        url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
        country_shapes = f"{url}/world-countries.json"
        countries_geojson = requests.get(country_shapes).json()
        CountCountryDict = self.CountnumberofCountry(listcountryname)
        listcolor = self.generate_random_colors(len(CountCountryDict))
        print(len(CountCountryDict))
        print(listcolor)
        for i in range(len(listcountryname)):
            count = CountCountryDict[listcountryname[i]]
            try:
                coords = self.get_coordinate(listcountryname[i])
                folium.Marker([coords[0], coords[1]],icon=folium.features.DivIcon(icon_size=(150,36),icon_anchor=(0,0),html=f'<div style="font-size: 24pt; color: red; font-weight: bold">{count}</div>')).add_to(self.map)
                for feature in countries_geojson["features"]:
                    print(listcolor[i])
                    if feature["properties"]["name"] == listcountryname[i]:
                        folium.GeoJson(feature,name=listcountryname[i],style_function=lambda x: {'fillColor': listcolor[i], 'color': 'black', 'weight': 2},tooltip=listcountryname[i]).add_to(self.map)
            except:
                print(f"No coordinates found for {listcountryname[i]}")
        self.map.save("Map.html")
        webbrowser.open("Map.html")
    
    def CountnumberofCountry(self,listcountry):
        CountCountry = {}
        for i in listcountry:
            if i in CountCountry:
                CountCountry[i] = int(CountCountry[i].value) + 1
            else:
                CountCountry[i] = 1
        return CountCountry
    
map_plot = MapPlot()
map_plot.getMapPlot(["France", "Spain", "Germany", "Italy", "United States of America"])








        
        