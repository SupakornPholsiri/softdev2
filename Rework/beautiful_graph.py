import plotly.graph_objs as go
from pymongo import MongoClient
import plotly.graph_objs as go
import plotly.offline as pyo
import random

def generate_hex_colors(num_colors):
    hex_chars = "0123456789ABCDEF"
    colors = []
    for _ in range(num_colors):
        color = ""
        for i in range(6):
            color += random.choice(hex_chars)
        colors.append("#" + color)
    return colors


# Connect to the MongoDB instance
mongo = MongoClient("localhost:27017")
SearchEngine = mongo['SearchEngine']
webdb = SearchEngine['WebDB']

# Fetch data from the MongoDB instance
target = "iot"
data = webdb.find({"key": target}, {'_id': 0})
listdata = {}
keyword = ""
for i in data:
    keyword = i['key']
    listdata = i['value']
sorted_d = dict(sorted(listdata.items(), key=lambda item: item[1], reverse=True))


# Extract the keyword frequencies and the corresponding keywords
freq = list(sorted_d.values())[0:9]
keywords = list(sorted_d.keys())[0:9]

# Define a color for each keyword
colors = generate_hex_colors(len(keywords))

# Create a bar chart using Plotly
data = [go.Bar(x=keywords, y=freq, marker=dict(color=colors))]

layout = go.Layout(title=keyword,
                   xaxis=dict(title="Keywords"),
                   yaxis=dict(title="Frequency"),
                   plot_bgcolor='#0e1111',  # Set the background color of the plot to black
                   paper_bgcolor='#F0F0F0',  # Set the background color of the paper
                   font=dict(size=14, color='#000000'))  # Set the font color
fig = go.Figure(data=data, layout=layout)
# Show the figure

pyo.plot(fig, filename='myplot.html')