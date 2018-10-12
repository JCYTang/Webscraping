import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import pyodbc
from datetime import datetime as dt

app = dash.Dash()

server = 'imlvs03\sql2005'
database = 'DW_Development'
user = 'DWUser'
password='gI7T@JD0rEdsF'
conn = pyodbc.connect(uid=user, pwd=password, driver='{SQL Server Native Client 11.0}',server='imlvs03\sql2005',database='DW_Development')
sql = """SELECT brand, name, state, fueltype, date, price
from fuelstations join fuelprices
on fuelstations.id = fuelprices.id
order by date asc, brand asc"""
df = pd.read_sql(sql, conn)


brands = df['brand'].unique()
fueltypes = df['fueltype'].unique()
states = df['state'].unique()

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='state',
            options=[{'label': i, 'value': i} for i in states],
            placeholder='Select State'
        ),
        dcc.Dropdown(
            id='fueltype',
            options=[{'label': i, 'value': i} for i in fueltypes],
            placeholder='Select fueltype'
        ),
        dcc.Dropdown(
            id='brand',
            options=[{'label': i, 'value': i} for i in brands],
            placeholder='Select brands',
            multi=True
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=dt(2018, 9, 28),
            end_date_placeholder_text='Select a date!',
            display_format='DD MMM YYYY'
        )
    ],
    style={'width': '20%', 'display': 'inline-block'}),

    dcc.Graph(id='price_chart')

])

# @app.callback(
#     dash.dependencies.Output('price_chart', 'figure'),
#     [dash.dependencies.Input('state', 'value'),
#      dash.dependencies.Input('fueltype', 'value'),
#      dash.dependencies.Input('brand', 'value'),
#      dash.dependencies.Input('date-picker-range', 'value')])
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]
#
#     return {
#         'data': [go.Scatter(
#             x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#             y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#             text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             mode='markers',
#             marker={
#                 'size': 15,
#                 'opacity': 0.5,
#                 'line': {'width': 0.5, 'color': 'white'}
#             }
#         )],
#         'layout': go.Layout(
#             xaxis={
#                 'title': xaxis_column_name,
#                 'type': 'linear' if xaxis_type == 'Linear' else 'log'
#             },
#             yaxis={
#                 'title': yaxis_column_name,
#                 'type': 'linear' if yaxis_type == 'Linear' else 'log'
#             },
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
#             hovermode='closest'
#         )
#     }


if __name__ == '__main__':
    app.run_server()