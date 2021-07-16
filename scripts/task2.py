# !pip3 install numpy pandas matplotlib seaborn sklearn

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Loading the data
db = pd.read_csv("../data/telcom.csv", na_values=['?', None])

# Cleaning data
# dropping columns with more than 30% missing values
df_clean = db.drop(['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 'HTTP DL (Bytes)', 'HTTP UL (Bytes)', 'Nb of sec with 125000B < Vol DL', 'Nb of sec with 1250B < Vol UL < 6250B', 'Nb of sec with 31250B < Vol DL < 125000B', 'Nb of sec with 37500B < Vol UL', 'Nb of sec with 6250B < Vol DL < 31250B', 'Nb of sec with 6250B < Vol UL < 37500B',], axis=1)

# dropping rows for columns with Unidue identifiers for customer data since we cannot fill missing values with existing data
df_clean.dropna(subset = ['MSISDN/Number'], inplace=True)
df_clean.dropna(subset = ['Bearer Id'], inplace=True)

# filling missing values
df_clean['Nb of sec with Vol DL < 6250B'] = fix_missing_ffill(df_clean, 'Nb of sec with Vol DL < 6250B')
df_clean['Nb of sec with Vol UL < 1250B'] = fix_missing_ffill(df_clean, 'Nb of sec with Vol UL < 1250B')
df_clean['Avg RTT DL (ms)'] = fix_missing_ffill(df_clean, 'Avg RTT DL (ms)')
df_clean['Avg RTT UL (ms)'] = fix_missing_ffill(df_clean, 'Avg RTT UL (ms)')
df_clean['DL TP < 50 Kbps (%)'] = fix_missing_ffill(df_clean, 'DL TP < 50 Kbps (%)')
df_clean['50 Kbps < DL TP < 250 Kbps (%)'] = fix_missing_ffill(df_clean, '50 Kbps < DL TP < 250 Kbps (%)')
df_clean['250 Kbps < DL TP < 1 Mbps (%)'] = fix_missing_ffill(df_clean, '250 Kbps < DL TP < 1 Mbps (%)')
df_clean['DL TP > 1 Mbps (%)'] = fix_missing_ffill(df_clean, 'DL TP > 1 Mbps (%)')
df_clean['UL TP < 10 Kbps (%)'] = fix_missing_ffill(df_clean, 'UL TP < 10 Kbps (%)')
df_clean['10 Kbps < UL TP < 50 Kbps (%)'] = fix_missing_ffill(df_clean, '10 Kbps < UL TP < 50 Kbps (%)')
df_clean['50 Kbps < UL TP < 300 Kbps (%)'] = fix_missing_ffill(df_clean, '50 Kbps < UL TP < 300 Kbps (%)')
df_clean['UL TP > 300 Kbps (%)'] = fix_missing_ffill(df_clean, 'UL TP > 300 Kbps (%)')

# fill obj variables column with mode 
df_clean['Handset Manufacturer'] = df_clean['Handset Manufacturer'].fillna(df_clean['Handset Manufacturer'].mode()[0])
df_clean['Handset Type'] = df_clean['Handset Type'].fillna(df_clean['Handset Type'].mode()[0])
df_clean['Last Location Name'] = df_clean['Last Location Name'].fillna(df_clean['Last Location Name'].mode()[0])
print(df_clean.describe())

# selecting features of interest
df= df_clean[['MSISDN/Number', 'Dur. (ms)', 'Bearer Id', 'Total UL (Bytes)', 'Total DL (Bytes)']].groupby(['MSISDN/Number']).sum()
df.head()

df['Sessions Frequency'] = df['Bearer Id'].count()
df['Duration of Session'] = df['Dur. (ms)'].sum()
df['Sessions Total Traffic'] = df['Total DL (Bytes)'] + df['Total UL (Bytes)']
df.head()

# Aggregating
df_agg = df[['MSISDN/Number', 'Sessions Frequency', 'Duration of Session', 'Sessions Total Traffic']].groupby(['MSISDN/Number']).sum()
df_agg.head()

# Top 10 per column
n = 10
print(df['Sessions Frequency'].value_counts()[:n].index.tolist())

n = 10
print(df['Duration of Session'].value_counts()[:n].index.tolist())

n = 10
print(df['Sessions Total Traffic'].value_counts()[:n].index.tolist())

# Standardizing and running k-means
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() 
df_scaled = scaler.fit_transform(df)
# Checking mean and sd
print(df_scaled.mean(axis=0))
print(df_scaled.std(axis=0))

# K-means = 3
# DEPENDENCIES
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

kmeans = KMeans(n_clusters=3) # You want cluster the passenger records into 2: Survived or Not survived
kmeans.fit(df_scaled)

# Non-normalised metrics per cluster
kmeans = KMeans(n_clusters=3) 
kmeans.fit(df)

# Aggregating traffic per user
df_data_app = df_clean[['MSISDN/Number', 'Dur. (ms)', 'Social Media DL (Bytes)','Social Media UL (Bytes)', 'Google DL (Bytes)', 'Google UL (Bytes)', 'Email DL (Bytes)', 'Email UL (Bytes)', 'Youtube DL (Bytes)', 'Youtube UL (Bytes)', 'Netflix DL (Bytes)', 'Netflix UL (Bytes)', 'Gaming DL (Bytes)', 'Gaming UL (Bytes)', 'Other DL (Bytes)', 'Other UL (Bytes)', 'Total UL (Bytes)', 'Total DL (Bytes)']].groupby(['MSISDN/Number']).sum()
df_data_app['Social Media'] = df_data_app['Social Media DL (Bytes)'] + df_data_app['Social Media UL (Bytes)']
df_data_app['Google'] = df_data_app['Google DL (Bytes)'] + df_data_app['Google UL (Bytes)']
df_data_app['Email'] = df_data_app['Email DL (Bytes)'] + df_data_app['Email UL (Bytes)']
df_data_app['Youtube'] = df_data_app['Youtube DL (Bytes)'] + df_data_app['Youtube UL (Bytes)']
df_data_app['Netflix'] = df_data_app['Netflix DL (Bytes)'] + df_data_app['Netflix UL (Bytes)']
df_data_app['Gaming'] = df_data_app['Gaming DL (Bytes)'] + df_data_app['Gaming UL (Bytes)']
df_data_app['Other'] = df_data_app['Other DL (Bytes)'] + df_data_app['Other UL (Bytes)']
df_data_app['Total'] = df_data_app['Total DL (Bytes)'] + df_data_app['Total UL (Bytes)']

df_data = df_data_app[['Social Media', 'Google', 'Email', 'Youtube', 'Netflix', 'Gaming', 'Other', 'Total']]

# Top 10 per app
print(df_data.nlargest(10, 'Social Media', keep='last'))
print(df_data.nlargest(10, 'Google', keep='last'))
print(df_data.nlargest(10, 'Email', keep='last'))
print(df_data.nlargest(10, 'Youtube', keep='last'))
print(df_data.nlargest(10, 'Netflix', keep='last'))
print(df_data.nlargest(10, 'Gaming', keep='last'))
print(df_data.nlargest(10, 'Other', keep='last'))

# Top 3 most used Apps - Get logic
#n = 3
#manufacturer.value_counts()[:n].index.tolist()

# Grouping users in k engagement clusters based on the engagement metrics


