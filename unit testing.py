import pandas as pd
import numpy as np

import os

folder_path = 'exports'

files = os.listdir(folder_path)
excel_files = [f for f in files if f.endswith('.xlsx')]

dfs = []
for file in excel_files:
    df = pd.read_excel(os.path.join(folder_path, file), sheet_name='general_info')
    dfs.append(df)

concatenated_df = pd.concat(dfs, ignore_index=True)

database = pd.read_excel("database.xlsx")

joined_dfs = database.merge(concatenated_df, on='Image Name', how='inner')

joined_dfs['Error'] = np.where((joined_dfs['total_x'] == joined_dfs['total_y']) & (joined_dfs['subtotal_x'] == joined_dfs['subtotal_y']), 0, 1)
print(f"Propotion of mistakes: {round(sum(joined_dfs['Error'])/len(joined_dfs['Error']),2)*100}%")

result_df_filtered_errors = joined_dfs[joined_dfs['Error'] == 1]
result_df_filtered_errors.to_excel("exports/errors.xlsx")

