# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

url = "http://web.sfc.keio.ac.jp/~takefuji/list.html"

with urllib.request.urlopen(url) as f:
    html = f.read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    pre = soup.pre

ls = pre.get_text().split()
data = pd.DataFrame(columns=['access_control', 'some_number', 'author', 'file_size_in_Bytes', 'month', 'day', 'time', 'file_name'])

for idx in range(0, len(ls), data.shape[1]):
    data = data.append(pd.DataFrame({
                                        data.columns[0] : ls[idx],
                                        data.columns[1] : ls[idx+1],
                                        data.columns[2] : ls[idx+2],
                                        data.columns[3] : ls[idx+3],
                                        data.columns[4] : ls[idx+4],
                                        data.columns[5] : ls[idx+5],
                                        data.columns[6] : ls[idx+6],
                                        data.columns[7] : ls[idx+7]
                                    }, index=[i for i in range(8)]), ignore_index=True
                      )

extension = set()
split = r'(\.[a-z|0-9]*\*)'
for index, row in data.iterrows():
    fileName = re.split(split, row['file_name'])
    if len(fileName) == 3: extension.add(fileName[1])
    else: print(fileName)

extDict = {}
for ext in extension:
    extDict[ext] = 0

col = ['yr']
for idx, (k, v) in enumerate(sorted(extDict.items(), key=lambda x: -x[1])):
    if idx < 19: col.append(k[:-1])
col.append('other')

import datetime
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
dt_now = datetime.datetime.now()
thisYear = int(dt_now.strftime('%Y'))
years = np.arange(thisYear, 1997, -1)
data2 = pd.DataFrame(np.zeros((years.shape[0],len(col)), dtype=int), index=years, columns=col)
data2['yr'] = years
year = thisYear
monthLastRow = int(dt_now.strftime('%m'))
split = r'(\.[a-z|0-9]*\*)'

for index, row in data.iterrows():
    if ':' in row['time']: # for new data, it's time, but for old data, it's year. We want year for new data.
        monthThisRow = months.index(row['month']) + 1
        if monthThisRow - monthLastRow > 0: year -= 1
        monthLastRow = monthThisRow
    else: year = int(row['time'])
    
    fileName = re.split(split, row['file_name'])
    if len(fileName) == 3:
        fileExtension = fileName[1][:-1]
        if fileExtension in col: data2.loc[year][fileExtension] += 1
        else: data2.loc[year]['other'] += 1

data2 = data2.sort_values('yr')
data2.to_csv('takeFileLog.tsv', index=False, sep='\t')