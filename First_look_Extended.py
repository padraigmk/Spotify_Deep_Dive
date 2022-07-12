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

# https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
cwd = os.getcwd()
path = cwd + '\\MyData'

all_files = glob.glob(os.path.join(path, "endsong*"))

li = []

for filename in all_files:
    df = pd.read_json(filename)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
