from geopy.geocoders import Nominatim
import folium
import webbrowser
import requests
import random
import colorsys

class MapPlot:
    def __init__(self):
        #Locate Starting poin at China
        self.geolocator = Nominatim(user_agent="my-app")
        self.map = folium.Map(location=[35.8617, 104.1954], zoom_start=4)

        url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
        country_shapes = f"{url}/world-countries.json"
        self.countries_geojson = requests.get(country_shapes).json()

    def get_coordinate(self,countryname):
        #Get Coordinate (Latitude,Longtitude) using geolocatoer
        location = self.geolocator.geocode(countryname)
        return [location.latitude, location.longitude]

    def generate_random_colors(self,num_colors):
        #generate random color in hexadecimal and return list of colors
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

    def getMapPlot(self, Dictcountryname:dict):
        #get Countrie Coordinate Shape
        self.map = folium.Map(location=[35.8617, 104.1954], zoom_start=4)
        #Count number of countries
        CountCountryDict = self.CountnumberofCountry(Dictcountryname)
        #Take country name data
        listcountryname = list(Dictcountryname.keys())
        #generate random color
        listcolor = self.generate_random_colors(len(CountCountryDict))
        #Loop depend on number of Listcountryname
        for i in range(len(listcountryname)):
            count = CountCountryDict[listcountryname[i]]
            try:
                #get coordinate with geolocator
                coords = self.get_coordinate(listcountryname[i])
                #set marker to coordinate
                folium.Marker([coords[0], coords[1]],icon=folium.features.DivIcon(icon_size=(150,36),icon_anchor=(0,0),
                html=f'<div style="font-size: 24pt; color: red; font-weight: bold">{count}</div>')).add_to(self.map)
                for feature in self.countries_geojson["features"]:
                    #Loop for get all of coordinates for that countries to draw a border and fill with color
                    if feature["properties"]["name"].lower() == listcountryname[i]:
                        folium.GeoJson(feature,name=listcountryname[i],style_function=lambda x, 
                        i=i: {'fillColor': listcolor[i], 'color': 'black', 'weight': 2},
                        tooltip=listcountryname[i]).add_to(self.map)
            except:
                pass
        #save map and open broswer
        self.map.save("Map.html")
    
    def CountnumberofCountry(self,Dictcountry):
        #Count the number of countries
        CountCountry = {}
        for country in Dictcountry:
           CountCountry[country] = Dictcountry[country]
        return CountCountry
    
if __name__ == "__main__":
    map_plot = MapPlot()
    map_plot.getMapPlot({"france":1, "spain":5, "germany":1, "italy":7, "united states of america":9, "china":6})








        
        
