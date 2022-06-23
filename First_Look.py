# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 18:19:42 2022

@author: padra
"""

import pandas as pd
import datetime as dt
import numpy as np

df0 = pd.read_json(r'MyData\StreamingHistory0.json')
df1 = pd.read_json(r'MyData\StreamingHistory1.json')

df = pd.concat([df0, df1])

# full name to distinguish between soings with the same name and different artists
df['fullName'] = df['artistName'] + '-' + df['trackName']

top_songs = df.groupby(['fullName']).count().sort_values(
    by=['msPlayed'], ascending=False).head(20)

top_songs['songPlayCount'] = top_songs['endTime']  # rename column
top_songs.drop(top_songs.columns.difference(
    ['songPlayCount']), 1, inplace=True)  # drop unecessary columns


top_artists = df.groupby(['artistName']).count().sort_values(
    by=['msPlayed'], ascending=False).head(20)

top_artists['artistPlayCount'] = top_artists['endTime']  # rename column
top_artists.drop(top_artists.columns.difference(
    ['artistPlayCount']), 1, inplace=True)  # drop unecessary columns

song_play_time = df.groupby(['fullName']).sum().sort_values(
    by=['msPlayed'], ascending=False)/1000  # in seconds

artist_play_time = df.groupby(['artistName']).sum().sort_values(
    by=['msPlayed'], ascending=False)/1000  # in seconds

n_songs = df.groupby(['fullName']).count()
n_songs = len(n_songs.index)

n_artists = df.groupby(['artistName']).count()
n_artists = len(n_artists.index)

# play_time = play_time.merge(df, on='fullName', how='left') try to get track and artist name back into the df
