import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import random
from datetime import date, datetime

### generate data
k = 1000
year = 2020
month = 12
min_day = 1
max_day = 14
date_str = [f'{year}-{month}-{str(d).zfill(2)}' for d in range(min_day, max_day + 1)]

first = ['100', '121', '196', '45', '172']
second = ['123', '11', '47', '96', '89']
third = ['45', '56', '97', '86', '3']
n1 = random.choices(first, k=k)
n2 = random.choices(second, k=k)
n3 = np.random.randint(0, 256, size=k)
n4 = np.random.randint(0, 256, size=k)
ips = [str(n1[i]) + '.' + str(n2[i]) + '.' + str(n3[i]) + '.' + str(n4[i]) for i in range(k)]

dates = random.choices(date_str, k=k)
df = pd.DataFrame(dates, columns=['date'])

days = random.choices(date_str, k=k)
day_group = []
for date_str in dates:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    if dt.weekday() in (5, 6):
        day_group.append('weekend')
    else:
        day_group.append('weekday')

df['ips'] = ips
df['hour'] = random.choices(['02:00:00', '06:00:00', '10:00:00', '14:00:00', '18:00:00', '22:00:00'], k=k)
df['flows'] = np.abs(np.random.normal(1, 100, k)).astype('int')
df['bytes'] = np.abs(np.random.normal(40, 60000, k)).astype('int')
df['packets'] = np.abs(np.random.normal(1, 500, k)).astype('int')
df['flow_duration'] = np.abs(np.random.normal(1, 200, k)).astype('int')
df['communications'] = np.abs(np.random.normal(1, 80, k)).astype('int')
df['country'] = np.abs(np.random.normal(1, 50, k)*100).astype(int)
df['k'] = random.choices([2, 3, 4, 5, 6, 7], k=k)
df['working_hour_group'] = random.choices(['non_working', 'primary_working', 'secondary_working'], k=k)
df['day_group'] = day_group
df['subnet'] = random.choices([str(i) for i in range(5)], k=k)
df['count'] = 1
df['labels'] = random.choices([str(i) for i in range(5)], k=k)

df.loc[df['bytes'] <= 1000, 'labels'] = '0'
df.loc[(df['bytes'] <= 5000) & (df['bytes'] > 990), 'labels'] = '1'
df.loc[(df['bytes'] <= 30000) & (df['bytes'] > 4950), 'labels'] = '2'
df.loc[(df['bytes'] <= 80000) & (df['bytes'] > 29950), 'labels'] = '3'
df.loc[df['bytes'] > 79950, 'labels'] = '4'

df['description'] = '0'
df.loc[df['labels'] == '0', 'description'] = 'very low activity and risk'
df.loc[df['labels'] == '1', 'description'] = 'low activity and risk'
df.loc[df['labels'] == '2', 'description'] = 'medium activity and risk'
df.loc[df['labels'] == '3', 'description'] = 'high activity and risk'
df.loc[df['labels'] == '4', 'description'] = 'very high activity and risk'


### dictionaries and features
date_dict = [{'label': date, 'value': date} for date in dates]
features = ['flows', 'bytes', 'packets', 'flow_duration', 'communications', 'country']
feature_dict = [{'label': x, 'value': x} for x in features]
box_plot_x_dict = [{'label': 'k', 'value': 'k'},
                    {'label': 'subnet', 'value':'subnet'},
                   {'label': 'working hour group', 'value': 'working_hour_group'},
                   {'label': 'day group', 'value':'day_group'}]
day_group_dict = [{'label': x, 'value': x} for x in df['day_group'].unique()]
working_hour_dict = [{'label': 'all', 'value': 'all'}] + [{'label': x, 'value': x} for x in df['working_hour_group'].unique()]
unique_labels = sorted(df['labels'].unique())
label_dict = [{'label': x, 'value': x} for x in unique_labels]


### create dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

### layout
app.layout = dbc.Container([
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='date_selector',
                                        min_date_allowed=date(year, month, min_day),
                                        max_date_allowed=date(year, month, max_day),
                                        initial_visible_month=date(year, month, min_day),
                                        end_date=date(year, month, max_day),
                                        clearable=True,
                                        # persistence=True,
                                        # persisted_props=['start_date', 'end_date'],
                                        # persistence_type='memory',
                                        updatemode='singledate'
                                    )

                                ], width={'size':2}, xs=12, sm=6, md=3, lg=2, xl=2,
                                    style={'text-align': 'center'},
                                    className='mb-3'),
                                dbc.Col([
                                    html.Label('Working Hour Group', className='text-center'),
                                    dcc.Dropdown(id='working_hour_group_selector', multi=True, value='all',
                                                 options=working_hour_dict)
                                ], width={'size':2}, xs=12, sm=12, md=4, lg=2, xl=2,
                                    style={'text-align': 'center'},
                                    className='mb-3'),
                                dbc.Col([
                                    html.Label('Box Plot X', className='text-center'),
                                    dcc.Dropdown(id='box_x_selector', value='k',
                                                 options=box_plot_x_dict)
                                ], width={'size':2}, xs=12, sm=12, md=4, lg=2, xl=2,
                                    style={'text-align': 'center'},
                                    className='mb-3'),
                                dbc.Col([
                                    html.Label('X', className='text-center'),
                                    dcc.Dropdown(id='x_selector', value='flows',
                                                 options=feature_dict)
                                ], width={'size':2}, xs=12, sm=12, md=4, lg=2, xl=2,
                                    style={'text-align': 'center'},
                                    className='mb-3'),
                                dbc.Col([
                                    html.Label('Y', className='text-center'),
                                    dcc.Dropdown(id='y_selector', value='packets',
                                                 options=feature_dict)
                                ], width={'size':2}, xs=12, sm=12, md=4, lg=2, xl=2,
                                    style={'text-align': 'center'},
                                    className='mb-3'),

                                dbc.Col([
                                    html.Label('Label', className='text-center'),
                                    dcc.Checklist(id='label_selector', value=unique_labels,
                                                  options=label_dict,
                                                  labelClassName='mr-3')
                                ], width={'size':2}, xs=12, sm=12, md=4, lg=2, xl=2,
                                    style={'text-align': 'center'},
                                    className='mb-3')
                            ], id='selectors'),

                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='box_plot'),
                                    dcc.Graph(id='heatmap_plot')
                                ], id='graph_col1', width={'size': 4}, xs=12, sm=12, md=6, lg=4, xl=4),

                                dbc.Col([
                                    dcc.Graph(id='sunburst_plot'),
                                    dcc.Graph(id='polar_plot')
                                ], id='graph_col2', width={'size': 4}, xs=12, sm=12, md=6, lg=4, xl=4),

                                dbc.Col([
                                    dcc.Graph(id='scatter_plot'),
                                    dcc.Graph(id='hist_plot')
                                ], id='graph_col3', width={'size': 4}, xs=12, sm=12, md=6, lg=4, xl=4)
                            ], id='graph'),
], fluid=True)


# ### callback
@app.callback(Output('box_plot', 'figure'),
              [Input('date_selector', 'start_date'),
               Input('date_selector', 'end_date'),
               Input('box_x_selector', 'value'),
               Input('y_selector', 'value'),
               Input('label_selector', 'value'),
               Input('working_hour_group_selector', 'value')])
def update_box_plot(start_date, end_date, selected_box_x, selected_y, selected_label,
                    selected_working_hour_group):

    ### filter by date
    if start_date:
        filtered_df = df[df['date'] == start_date]

    if end_date:
        filtered_df = df[df['date'] == end_date]

    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if type(selected_label) == str:
        selected_label = [selected_label]

    filtered_df = filtered_df[filtered_df['labels'].isin(selected_label)]

    if type(selected_working_hour_group) == str:
        selected_working_hour_group = [selected_working_hour_group]

    if 'all' not in selected_working_hour_group:
        filtered_df = filtered_df[filtered_df['working_hour_group'].isin(selected_working_hour_group)]

    fig = px.box(filtered_df, x=selected_box_x, y=selected_y)

    ### format output string
    x_str = ' '.join(selected_box_x.split('_'))
    y_str = ' '.join(selected_y.split('_'))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f"{x_str} vs. {y_str}",
        title_font_color='#408ec6',
        xaxis={'title': f'{x_str}', 'color':'#BBBBBB'},
        yaxis={'title': f'{y_str}', 'color':'#BBBBBB'}
    )

    return fig


@app.callback(Output('sunburst_plot', 'figure'),
              [Input('date_selector', 'start_date'),
               Input('date_selector', 'end_date'),
               Input('y_selector', 'value'),
               Input('label_selector', 'value'),
               Input('working_hour_group_selector', 'value')])
def update_sunburst_plot(start_date, end_date, selected_y, selected_label, selected_working_hour_group):
    ### filter by date
    if start_date:
        filtered_df = df[df['date'] == start_date]

    if end_date:
        filtered_df = df[df['date'] == end_date]

    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if type(selected_label) == str:
        selected_label = [selected_label]

    filtered_df = filtered_df[filtered_df['labels'].isin(selected_label)]

    if type(selected_working_hour_group) == str:
        selected_working_hour_group = [selected_working_hour_group]

    if 'all' not in selected_working_hour_group:
        filtered_df = filtered_df[filtered_df['working_hour_group'].isin(selected_working_hour_group)]

    fig = px.sunburst(filtered_df, path=['labels', 'day_group', 'working_hour_group'],
                      color=selected_y,
                      maxdepth=-1,
                      color_continuous_scale=px.colors.sequential.YlGnBu,
                      hover_name='labels',
                      hover_data={'labels': False})

    y_str = ' '.join(selected_y.split('_'))

    fig.update_traces(textinfo='label+percent parent')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f"{y_str}",
        title_font_color='#408ec6'
        )
    fig.update_coloraxes(colorbar_title=dict(text=y_str))

    return fig


@app.callback(Output('scatter_plot', 'figure'),
              [Input('date_selector', 'start_date'),
               Input('date_selector', 'end_date'),
               Input('x_selector', 'value'),
               Input('y_selector', 'value'),
               Input('label_selector', 'value'),
               Input('working_hour_group_selector', 'value')])
def update_scatter_plot(start_date, end_date, selected_x, selected_y, selected_label,
                    selected_working_hour_group):

    ### filter by date
    if start_date:
        filtered_df = df[df['date'] == start_date]

    if end_date:
        filtered_df = df[df['date'] == end_date]

    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if type(selected_label) == str:
        selected_label = [selected_label]

    filtered_df = filtered_df[filtered_df['labels'].isin(selected_label)]

    if type(selected_working_hour_group) == str:
        selected_working_hour_group = [selected_working_hour_group]

    if 'all' not in selected_working_hour_group:
        filtered_df = filtered_df[filtered_df['working_hour_group'].isin(selected_working_hour_group)]

    fig = px.scatter(filtered_df, x=selected_x, y=selected_y, size=selected_y,
                     symbol_sequence=['pentagon'],
                     category_orders={'labels': unique_labels},
                     color='labels',
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     hover_data=['ips', 'labels', selected_y, selected_x, 'description'])

    y_str = ' '.join(selected_y.split('_'))
    x_str = ' '.join(selected_x.split('_'))
    fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title=f'{x_str} vs. {y_str}',
                    title_font_color='#408ec6',
                    xaxis={'title': f'{x_str}', 'color':'#BBBBBB'},
                    yaxis={'title': f'{y_str}', 'color': '#BBBBBB'})

    return fig


@app.callback(Output('heatmap_plot', 'figure'),
              [Input('date_selector', 'start_date'),
               Input('date_selector', 'end_date'),
               Input('label_selector', 'value')])
def update_heatmap_plot(start_date, end_date, selected_label):
    ### filter by date
    if start_date:
        filtered_df = df[df['date'] == start_date]

    if end_date:
        filtered_df = df[df['date'] == end_date]

    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if type(selected_label) == str:
        selected_label = [selected_label]

    filtered_df = filtered_df[filtered_df['labels'].isin(selected_label)]
    fig = px.density_heatmap(filtered_df, x='working_hour_group', y='day_group', z='count',
                             color_continuous_scale=px.colors.sequential.YlGnBu,
                             #color_continuous_scale='haline'
                             )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f'working hour group vs. day group',
        title_font_color='#408ec6',
        xaxis={'title': 'working hour group', 'color':'#BBBBBB'},
        yaxis={'title': 'day group', 'color':'#BBBBBB'}
    )

    return fig


@app.callback(Output('polar_plot', 'figure'),
              [Input('date_selector', 'start_date'),
               Input('date_selector', 'end_date'),
               Input('y_selector', 'value'),
               Input('label_selector', 'value'),
               Input('working_hour_group_selector', 'value')])
def update_polar_plot(start_date, end_date, selected_y, selected_label, selected_working_hour_group):
    ### filter by date
    if start_date:
        filtered_df = df[df['date'] == start_date]

    if end_date:
        filtered_df = df[df['date'] == end_date]

    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if type(selected_label) == str:
        selected_label = [selected_label]

    filtered_df = filtered_df[filtered_df['labels'].isin(selected_label)]

    if type(selected_working_hour_group) == str:
        selected_working_hour_group = [selected_working_hour_group]

    if 'all' not in selected_working_hour_group:
        filtered_df = filtered_df[filtered_df['working_hour_group'].isin(selected_working_hour_group)]

    fig = px.line_polar(filtered_df, r=selected_y, theta='hour', color='labels',
                        category_orders={'labels': [label for label in unique_labels]},
                        color_discrete_sequence=px.colors.qualitative.Safe)
    y_str = ' '.join(selected_y.split())
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f'{y_str} vs. time',
        title_font_color='#408ec6')
    # change the color of the polar axes
    fig.update_polars(bgcolor='rgb(17, 17, 17)')

    return fig


@app.callback(Output('hist_plot', 'figure'),
              [Input('date_selector', 'start_date'),
               Input('date_selector', 'end_date'),
               Input('x_selector', 'value'),
               Input('label_selector', 'value'),
               Input('working_hour_group_selector', 'value')])
def update_hist_plot(start_date, end_date, selected_x, selected_label, selected_working_hour_group):
    if start_date:
        filtered_df = df[df['date'] == start_date]

    if end_date:
        filtered_df = df[df['date'] == end_date]

    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if type(selected_label) == str:
        selected_label = [selected_label]

    filtered_df = filtered_df[filtered_df['labels'].isin(selected_label)]

    if type(selected_working_hour_group) == str:
        selected_working_hour_group = [selected_working_hour_group]

    if 'all' not in selected_working_hour_group:
        filtered_df = filtered_df[filtered_df['working_hour_group'].isin(selected_working_hour_group)]

    fig = px.histogram(filtered_df, x=selected_x, y='count', color_discrete_sequence=['rgb(51,34,136)'])

    x_str = ' '.join(selected_x.split())
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f"{x_str} vs. count",
        title_font_color='#408ec6',
        xaxis={'title': f'{x_str}', 'color': '#BBBBBB'},
        yaxis={'title': 'count', 'color': '#BBBBBB'})

    return fig

if __name__ == '__main__':
    app.run_server()
