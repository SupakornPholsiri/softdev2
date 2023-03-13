import plotly.graph_objs as go

# Define the data to be plotted
freq = [10, 8, 6, 4, 2]
keywords = ["apple", "banana", "cherry", "date", "elderberry"]

# Create a bar chart using Plotly
data = [go.Bar(x=keywords, y=freq)]

# Define the layout of the chart
layout = go.Layout(title="Word Frequency", xaxis=dict(title="Keywords"), yaxis=dict(title="Frequency"))

# Create the figure
fig = go.Figure(data=data, layout=layout)

# Show the figure
fig.show()
