# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 20:22:47 2022

@author: padra
"""
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
import glob
from datetime import date
import datetime
from dash.dependencies import Input, Output


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#ffffff',
    'text': '#353635',
    'gridline': '#9d9e9d'
}


# %% Data Transformation


# https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
cwd = os.getcwd()
path = cwd + '\\MyData'

all_files = glob.glob(os.path.join(path, "endsong*"))

li = []

for filename in all_files:
    temp_df = pd.read_json(filename)
    li.append(temp_df)

df = pd.concat(li, axis=0, ignore_index=True)
df.dtypes

df['dt_stamp'] = pd.to_datetime(df['ts'])
df_start_date = df.sort_values(
    by=['dt_stamp']).reset_index().dt_stamp[0].date()
df_end_date = df.sort_values(
    by=['dt_stamp']).reset_index().dt_stamp[len(df.index)-1].date()

# Create profile report of dataset
# profile = ProfileReport(df, title="Pandas Profiling Report")
# profile.to_file(output_file="report.html")


top_songs = df.groupby(['spotify_track_uri']).count().sort_values(
    by=['ms_played'], ascending=False).head(15).reset_index()
top_songs['songPlayCount'] = top_songs['ts']  # rename column
top_songs = top_songs.sort_values(
    by=['ms_played'], ascending=True)
top_songs.drop(top_songs.columns.difference(
    ['spotify_track_uri', 'songPlayCount']),
    1, inplace=True)  # drop unecessary columns
top_songs = pd.merge(top_songs, df.drop_duplicates(['spotify_track_uri']),
                     how='inner',
                     on=['spotify_track_uri'])  # add trackName and artistName
top_songs.drop(top_songs.columns.difference(
    ['spotify_track_uri', 'songPlayCount',
     'master_metadata_track_name', 'master_metadata_album_artist_name',
     'master_metadata_album_album_name'
     ]), 1, inplace=True)  # drop unecessary columns
top_songs['master_metadata_track_name'] = [x[:100]
                                           for x in top_songs['master_metadata_track_name']]


top_artists = df.groupby(['master_metadata_album_artist_name']).count().sort_values(
    by=['ms_played'], ascending=False).reset_index()  # head(20)
top_artists['artistPlayCount'] = top_artists['ts']  # rename column
top_artists.drop(top_artists.columns.difference(
    ['master_metadata_album_artist_name', 'artistPlayCount']),
    1, inplace=True)  # drop unecessary columns

n_songs = df.groupby(['spotify_track_uri']).count()
n_songs = len(n_songs.index)

n_songs_artist = df.drop_duplicates(subset=["spotify_track_uri"]).groupby(
    ['master_metadata_album_artist_name']).count().sort_values(
    by=['ms_played'], ascending=False).reset_index()  # head(20)
n_songs_artist['n_songs'] = n_songs_artist['ts']  # rename column
n_songs_artist.drop(n_songs_artist.columns.difference(
    ['master_metadata_album_artist_name', 'n_songs']),
    1, inplace=True)  # drop unecessary columns

artist_df = n_songs_artist.merge(
    top_artists, how='inner',
    on='master_metadata_album_artist_name').sort_values(
    by=['artistPlayCount'], ascending=False).head(100)


hour_bins = pd.Series(range(0, 25))
df['Hour Bin'] = pd.cut(df.dt_stamp.dt.hour, hour_bins, right=False)
df_hour_bin = df.groupby('Hour Bin', as_index=False)['ts'].count()

day_bins = pd.Series(range(0, 8))
df['Day Bin'] = pd.cut(df.dt_stamp.dt.weekday, day_bins, right=False)
df_day_bin = df.groupby('Day Bin', as_index=False)['ts'].count()
df_day_bin['day'] = pd.Series(range(0, 7))

# %% Figures

# fig = px.bar(df_day_bin, x="day", y="ts")
fig = px.bar(top_songs, x="songPlayCount", y="master_metadata_track_name",  # ,
             # color="master_metadata_album_artist_name",
             labels=dict(master_metadata_track_name="Track Name",
                         songPlayCount="Play Count"),
             hover_data=['master_metadata_track_name',
                         'master_metadata_album_artist_name',
                         'master_metadata_album_album_name'],
             orientation='h',
             text="master_metadata_track_name")
fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
# fig.update_traces(textfont_size=12, textangle=0,
#                   textposition="inside", cliponaxis=False)


fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.99,
        font=dict(
                size=12,
                color="black"
        ),
    ),
    legend_title_text='Track Name'
)
fig.update_xaxes(showline=True, linewidth=0.5,
                 linecolor='black', gridcolor=colors['gridline'])


fig2 = px.scatter(artist_df, x="n_songs", y="artistPlayCount",
                  color="master_metadata_album_artist_name", hover_name="master_metadata_album_artist_name",
                  log_y=True, log_x=True, size='artistPlayCount',
                  labels=dict(n_songs="Unique Songs Listened to", artistPlayCount="Total Artist Play Count"))

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    legend_title_text='Artist Name'
)
fig2.update_xaxes(showline=True, linewidth=0.5,
                  linecolor='black', gridcolor=colors['gridline'])
fig2.update_yaxes(showline=True, linewidth=0.5,
                  linecolor='black', gridcolor=colors['gridline'])

# %% Old Layout

# app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
#     html.H1(
#         children='Hello Dash',
#         style={
#             'textAlign': 'center',
#             'color': colors['text']
#         }
#     ),

#     html.Div(children='Dash: A web application framework for your data.',
#              style={
#                  'textAlign': 'center',
#                  'color': colors['text']
#              }),

#     html.Div(children=[
#         html.Div(
#             dcc.Graph(id="example-graph",
#                       figure=fig)),
#         html.Div(
#             dcc.Graph(id="example-graph-2",
#                       figure=fig2))
#     ]),

#     # html.Div(children=[dcc.Graph(
#     #     id='example-graph',
#     #     style={'display': 'inline-block'},
#     #     figure=fig
#     # ),
#     #     dcc.Graph(
#     #     id='example-graph-2',
#     #     style={'display': 'inline-block'},
#     #     figure=fig2
#     # )])
# ])


# %% New Layout

app.layout = dbc.Container(
    [
        html.H1("Spotify Deep Dive"),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=df_start_date,
            max_date_allowed=df_end_date,
            start_date=df_start_date,
            end_date=df_end_date
        ),
        html.Div(id='output-container-date-picker-range'),
        html.Hr(),
        dbc.Row([
                dbc.Col(dcc.Graph(id='example-graph', figure=fig), md=6),
                dbc.Col(dcc.Graph(id='example-graph-2', figure=fig2), md=6),
                ],
                align="center",
                ),
    ],
    fluid=True,
)


# %% Callbacks

@ app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'Date Range: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('Date Range: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


if __name__ == '__main__':
    app.run_server(debug=True)
    app.run_server(debug=True)
