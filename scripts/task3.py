# !pip3 install numpy pandas matplotlib seaborn sklearn

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Loading the data
db = pd.read_csv("../data/telcom.csv", na_values=['?', None])
print(db.describe())

# Checking for missing values
print(db.isna().sum())

# CLEANING DATA
## dropping rows for columns with Unidue identifiers for customer data since we cannot fill missing values with existing data
db.dropna(subset = ['MSISDN/Number'], inplace=True)
db.dropna(subset = ['Bearer Id'], inplace=True)

# Filling in values with mean
db_clean = db.fillna(db.mean(), inplace = True)
# fill obj columns with mode 
db['Handset Type'] = db['Handset Type'].fillna(db['Handset Type'].mode()[0])
db['Handset Manufacturer'] = db['Handset Manufacturer'].fillna(db['Handset Manufacturer'].mode()[0])
db['Last Location Name'] = db['Last Location Name'].fillna(db['Last Location Name'].mode()[0])

print(db.isna().sum())
print(db.shape)

df = db[['MSISDN/Number','Avg RTT DL (ms)', 'Avg RTT UL (ms)','Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)','Handset Type']].groupby(['MSISDN/Number']).sum()
print(df.head)

df['Avg RTT'] = (df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)'])/2
df['Avg TP'] = (df['Avg Bearer TP DL (kbps)'] + df['Avg Bearer TP UL (kbps)'])/2 
df['Avg Tcp Retrans'] = (df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)'])/2 

print(df.head())

# Aggregation per user
df_data = df[['MSISDN/Number', 'Avg RTT', 'Avg TP', 'Avg Tcp Retrans']]
print(df_data.head())

# Top 10
print(df_data.nlargest(10, 'Avg Tcp Retrans', keep='last'))
print(df_data.nlargest(10, 'Avg RTT', keep='last'))
print(df_data.nlargest(10, 'Avg TP', keep='last'))

# Bottom 10
print(df_data.nsmallest(10, 'Avg Tcp Retrans', keep='last'))
print(df_data.nsmallest(10, 'Avg RTT', keep='last'))
print(df_data.nsmallest(10, 'Avg TP', keep='last'))

# 10 Most frequent
n = 10
print(df_data['Avg Tcp Retrans'].value_counts()[:n].index.tolist())
n = 10
print(df_data['Avg RTT'].value_counts()[:n].index.tolist())
n = 10
print(df_data['Avg TP'].value_counts()[:n].index.tolist())


