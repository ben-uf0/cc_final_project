
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_csv("nama_10_gdp_1_Data.csv")
df = df[["TIME", "GEO", "NA_ITEM", "Value","UNIT"]]
df = df[~df.GEO.str.contains("Euro")]

available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()
available_units = df["UNIT"].unique()

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.H2('GNAD Final Assignment',style={'textAlign': 'left', 'color': 'red'}),
    html.H4('Graph 1',style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label('Select Option'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
        id='Select_Unit',
        options=[{'label': i, 'value': i} for i in available_units],
        value='Current prices, million euro')
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Select Indicator'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic'), #this is the graph figure
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    html.Div(style={'height': 50, 'display': 'inline-block'}),
    html.Div([
    html.Div(style={'height': 80, 'display': 'inline-block'}),
    html.H3('Graph 2',style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label('Select Indicator'),
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
        id='Unit_Selection',
        options=[{'label': i, 'value': i} for i in available_units],
        value='Current prices, million euro'
    )],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label(children='Select Country'),
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Austria'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='country_graph')])
])

# the callback is the function that will update the figure. Everytime I change something the callback function changes the data and layout and creates a new graph!
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
    dash.dependencies.Input('Select_Unit', 'value')])

def update_graph1(xaxis_column_name, yaxis_column_name,
                 year_value, Select_Unit):
    dff = df[df['TIME'] == year_value]#dff is a dataframe that is fitered for a year
    dfff = dff[dff["UNIT"] == Select_Unit]
    
    return {
        'data': [go.Scatter(
            x=dfff[dfff["NA_ITEM"] == xaxis_column_name]['Value'],
            y=dfff[dfff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dfff[dfff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )]
    }

@app.callback(
    dash.dependencies.Output('country_graph', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis', 'value'),
    dash.dependencies.Input('Unit_Selection', 'value')])

def update_graph2(country, yaxis, Unit_Selection):
    dff=df[df["GEO"]==country]
    dfff=dff[dff["UNIT"]== Unit_Selection]
    return {
        'data': [go.Scatter(
            y=dfff[dfff["NA_ITEM"] == yaxis]['Value'],
            x=dfff['TIME'].unique()
        )],
        'layout': go.Layout(
            xaxis={
                'title': "years"},
            yaxis={
                'title': yaxis},
            margin={'l': 90, 'b': 15, 't': 65, 'r': 90},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

