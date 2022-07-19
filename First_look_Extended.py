# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 19:49:34 2022

@author: padra
"""

import plotly.express as px
import numpy as np
import datetime as dt
import pandas as pd
from plotly.offline import plot
import calendar
import os
import glob
# import dask.dataframe as dd
from pandas_profiling import ProfileReport

# https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
cwd = os.getcwd()
path = cwd + '\\MyData'

all_files = glob.glob(os.path.join(path, "endsong*"))

li = []

for filename in all_files:
    temp_df = pd.read_json(filename)
    li.append(temp_df)

df = pd.concat(li, axis=0, ignore_index=True)

# Create profile report of dataset
# profile = ProfileReport(df, title="Pandas Profiling Report")
# profile.to_file(output_file="report.html")


top_songs = df.groupby(['spotify_track_uri']).count().sort_values(
    by=['ms_played'], ascending=False).head(20).reset_index()
top_songs['songPlayCount'] = top_songs['ts']  # rename column
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

top_artists = df.groupby(['master_metadata_album_artist_name']).count().sort_values(
    by=['ms_played'], ascending=False).head(20).reset_index()
top_artists['artistPlayCount'] = top_artists['ts']  # rename column
top_artists.drop(top_artists.columns.difference(
    ['master_metadata_album_artist_name', 'artistPlayCount']),
    1, inplace=True)  # drop unecessary columns

n_songs = df.groupby(['spotify_track_uri']).count()
n_songs = len(n_songs.index)

df.dtypes

df['dt_stamp'] = pd.to_datetime(df['ts'])

hour_bins = pd.Series(range(0, 25))
df['Hour Bin'] = pd.cut(df.dt_stamp.dt.hour, hour_bins, right=False)
df_hour_bin = df.groupby('Hour Bin', as_index=False)['ts'].count()

day_bins = pd.Series(range(0, 8))
df['Day Bin'] = pd.cut(df.dt_stamp.dt.weekday, day_bins, right=False)
df_day_bin = df.groupby('Day Bin', as_index=False)['ts'].count()

df_hour_bin.plot()
df_day_bin.plot.bar()
