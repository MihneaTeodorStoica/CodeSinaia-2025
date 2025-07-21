# import ast
import pandas as pd
import os

# os.system("powershell pwd")
# exit()

df = pd.read_csv('IntroToPy/mountains_db.tsv', sep='\t', header=None, names = ['Name', 'Elevation', 'Country', 'Code'])
num_rows = len(df['Code'].unique())
print(num_rows)
non_null_count = df['Elevation'].isnull().sum()
minh=999999
print(non_null_count)
print(df['Elevation'].max())
print(df['Elevation'].dropna().min())