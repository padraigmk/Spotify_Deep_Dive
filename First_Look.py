# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 18:19:42 2022

@author: padra
"""

import pandas as pd


df0 = pd.read_json(r'MyData\StreamingHistory0.json')
df1 = pd.read_json(r'MyData\StreamingHistory1.json')

df = pd.concat([df0, df1])

# full name to distinguish between soings with the same name and different artists
df['fullName'] = df['artistName'] + '-' + df['trackName']

gb_song = df.groupby(['fullName']).count().sort_values(
    by=['msPlayed'], ascending=False)
