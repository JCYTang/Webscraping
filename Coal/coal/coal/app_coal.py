import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Group
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from waitress import serve
from paste.translogger import TransLogger

# declare global variables
file = 'W:\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\Coal\\coal.csv'


def serve_layout():
    # layout function so that the data refreshes on page load

    df = pd.read_csv(file, parse_dates=['date'])
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df['month'] = df['date'].dt.strftime('%b')
    df['month'] = pd.Categorical(df['month'], categories=months, ordered=True)
    df = df[df['date'] > '2016-12-31']

    # get list of unique portfolio codes
    ports = df['port'].unique().tolist()
    ports.sort()
    ports.append('Total')
    port_options = [dict(label=str(port), value=str(port)) for port in ports]
    columns = [{'name': i,
                'id': i,
                'type': 'numeric',
                'format': Format(group=Group.yes)}
               for i in months]
    columns.append({'name': 'CY Total', 'id': 'CY Total', 'type': 'numeric', 'format': Format(group=Group.yes)})
    columns.insert(0, {'name': '', 'id': 'date'})
    states = ['NSW', 'QLD']
    state_options = [dict(label=str(state), value=str(state)) for state in states]

    layout = html.Div([

        # store component to store the main df with all the data
        dcc.Store(id='df', data=df.to_dict('records')),

        # store component to store the filtered dataframe
        dcc.Store(id='filtered_df', modified_timestamp=0),

        # App Heading
        html.Div([
            html.H1(
                children='Coal Throughput Data',
                style={'textAlign': 'center'}
            )
        ]),

        # Port drop down box
        html.Div([
            html.Label('Select Port:'),
            dcc.Dropdown(
                id='port-dropdown',
                options=port_options,
                value='Total'
            )
        ],
            style={'display': 'table-cell', 'width': '15%'}
        ),

        # Issuer drop down box
        html.Div([
            html.Label('Select State:'),
            dcc.Dropdown(
                id='state-dropdown',
                options=state_options,
                value='QLD'
            )
        ], style={'display': 'table-cell', 'width': '15%'}),

        html.Div([

            # dash table
            html.Div([
                dash_table.DataTable(
                    id='coal_table',
                    columns=columns,
                    # data=[dict(**{field: '' for field in fields})],
                    style_cell={'textAlign': 'left'},
                    data_timestamp=0,
                    style_as_list_view=True,
                )
            ]),

            # option payoff chart
            html.Div([
                dcc.Graph(
                    id='chart',
                    style={
                        'height': 600
                    },
                )
            ])
        ]),

    ])

    return layout


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = serve_layout


# callback function to return a dataframe that contains data for the port
@app.callback(
    [dash.dependencies.Output('filtered_df', 'data'),
     dash.dependencies.Output('coal_table', 'data')],
    [dash.dependencies.Input('port-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value')],
    [dash.dependencies.State('df', 'data')]
)
def show_data(port, state, data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['state'] == state]
    if port != 'Total':
        df = df[df['port'] == port]
        df_filter = df
    else:
        df_filter = df.groupby([df['date']]).sum()

    df_filter['%m/m'] = df_filter['coal'].pct_change()
    df_filter['%y/y'] = df_filter['coal'].pct_change(12)
    df_filter = df_filter.reset_index()

    df = df.groupby([df['date'].dt.year, df['month']]).sum()
    df = df['coal'].unstack()
    df.columns = pd.Index(list(df.columns))
    df = df.reset_index()
    df['CY Total'] = list(df.sum(axis=1))
    return df_filter.to_dict('records'), df.to_dict('records')

# callback function to update chart
@app.callback(
    dash.dependencies.Output('chart', 'figure'),
    [dash.dependencies.Input('filtered_df', 'data')],
    [dash.dependencies.State('df', 'data'),
     dash.dependencies.State('port-dropdown', 'value'),
     dash.dependencies.State('state-dropdown', 'value')]
)
def update_chart(filtered_data, data, port, state):

    if filtered_data is None:
        raise dash.exceptions.PreventUpdate

    if port != 'Total':
        df_vol = pd.DataFrame(filtered_data)
        df_change = df_vol
    else:
        df_vol = pd.DataFrame(data)
        df_vol = df_vol[df_vol['state'] == state]
        df_change = pd.DataFrame(filtered_data)

    df_vol['date'] = pd.to_datetime(df_vol['date'])
    df_change['date'] = pd.to_datetime(df_change['date'])

    bars = [go.Bar(
        x=df_vol[df_vol['port'] == i]['date'],
        y=df_vol[df_vol['port'] == i]['coal'],
        name=i
        )
        for i in df_vol['port'].unique()
    ]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_traces(data=bars)
    fig.add_trace(go.Scatter(x=df_change['date'], y=round(df_change['%m/m']*100, 2), name='%m/m', mode='lines+markers',
                             line_color='rgb(0,0,0)'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_change['date'], y=round(df_change['%y/y']*100, 2), name='%y/y', mode='lines+markers',
                             line_color='rgb(105,105,105)'), secondary_y=True)
    fig.update_layout(barmode='stack')
    fig.update_xaxes(tickangle=-45)
    fig.update_yaxes(title='Coal Volumes (t)', secondary_y=False)
    fig.update_yaxes(title='% change', secondary_y=True)

    return fig


if __name__ == '__main__':
    # app.run_server(debug=True, port=8082, host='AUD0100CK4')
    serve(TransLogger(app.server, logging_level=30), host='AUD0100CK4', port=8082)