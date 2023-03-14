import plotly.graph_objs as go
from pymongo import MongoClient
# Define the data to be plotted
mongo = MongoClient("localhost:27017")
SearchEngine = mongo['SearchEngine']
webdb = SearchEngine['WebDB']

data = webdb.find({"key":"iot"},{'_id':0})
listdata = {}
keyword = ""
count = 0
for i in data:
    keyword = i['key']
    listdata = i['value']
    
print(keyword)





freq = list(listdata.values())
keywords =list(listdata.keys())
# Create a bar chart using Plotly
data = [go.Bar(x=keywords, y=freq)]

# Define the layout of the chart
layout = go.Layout(title= keyword, xaxis=dict(title="Keywords"), yaxis=dict(title="Frequency"))

# Create the figure
fig = go.Figure(data=data, layout=layout)

# Show the figure
fig.show()

