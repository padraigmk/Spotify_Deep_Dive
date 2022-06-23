# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 18:19:42 2022

@author: padra
"""
import plotly.express as px
import numpy as np
import datetime as dt
import pandas as pd
from plotly.offline import plot


df0 = pd.read_json(r'MyData\StreamingHistory0.json')
df1 = pd.read_json(r'MyData\StreamingHistory1.json')

df = pd.concat([df0, df1])

# full name to distinguish between soings with the same name and different artists
df['fullName'] = df['artistName'] + '-' + df['trackName']
# Acts as a lookup for songName and artistName

top_songs = df.groupby(['fullName']).count().sort_values(
    by=['msPlayed'], ascending=False).head(20).reset_index()

top_songs['songPlayCount'] = top_songs['endTime']  # rename column
top_songs.drop(top_songs.columns.difference(
    ['fullName', 'songPlayCount']), 1, inplace=True)  # drop unecessary columns
top_songs = pd.merge(top_songs, df.drop_duplicates(['fullName']), how='inner', on=[
                     'fullName'])  # add trackName and artistName


top_artists = df.groupby(['artistName']).count().sort_values(
    by=['msPlayed'], ascending=False).head(20)

top_artists['artistPlayCount'] = top_artists['endTime']  # rename column
top_artists.drop(top_artists.columns.difference(
    ['artistPlayCount']), 1, inplace=True)  # drop unecessary columns
top_artists = pd.merge(top_artists, df.drop_duplicates(['artistName']), how='inner', on=[
                       'artistName'])  # add trackName and artistName


song_play_time = df.groupby(['fullName']).sum().sort_values(
    by=['msPlayed'], ascending=False)/1000  # in seconds

artist_play_time = df.groupby(['artistName']).sum().sort_values(
    by=['msPlayed'], ascending=False)/1000  # in seconds

n_songs = df.groupby(['fullName']).count()
n_songs = len(n_songs.index)

n_artists = df.groupby(['artistName']).count()
n_artists = len(n_artists.index)

# Figures

fig_top_songs = px.bar(top_songs, y='songPlayCount',
                       x='trackName', title="Most Played Songs (Last 12 Months)", color='artistName')
# fig_top_songs.update_traces(marker_color='rgb(200,100,225)', marker_line_color='rgb(8,48,107)',
# marker_line_width=1.5, opacity=0.8)
plot(fig_top_songs)


fig_top_artists = px.bar(top_artists, y='artistPlayCount',
                         x='artistName', title="Most Played Artists")
fig_top_artists.update_traces(marker_color='rgb(100,255,100)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.8)
plot(fig_top_artists)
