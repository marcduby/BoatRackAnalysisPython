

# imports
import pandas as pd
import utils.constants as const

# constants

# Load the first CSV file
df_boats = pd.read_csv(const.FILE_BOATS)
df_trips_22 = pd.read_csv(const.FILE_TRIPS_22)
df_trips_23 = pd.read_csv(const.FILE_TRIPS_23)
df_trips_24 = pd.read_csv(const.FILE_TRIPS_24)

# Merge the two DataFrames on the 'BoatId' column
# Optionally, you can specify how you want to join: 'inner', 'outer', 'left', or 'right'
# result_df = pd.merge(df1, df2, on='BoatId', how='inner')
df_result_24 = pd.merge(df_boats, df_trips_24, on='BoatId')

# get the headers
# Convert column headers to a list
column_headers_list = df_result_24.columns.tolist()

# Print the list of column headers
print("inital columns: {}".format(column_headers_list))

# filter to only columns needed
df_filtered = df_result_24[const.LIST_COLUMNS_PERSONAL_BOATS]
column_headers_list = df_filtered.columns.tolist()
print("\nremaining columns for rack analysis: {}".format(column_headers_list))
print("dataframe shape: {}".format(df_filtered.shape))
print("null analysis: {}".format(df_filtered.isnull().sum()))

# print(result_df)
