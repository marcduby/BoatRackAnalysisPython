
# imports
import pandas_access as mdb

# Path to the MDB file
dir_data = "/Users/mduby/Data/Personal/CbcRack/"
mdb_file = dir_data + "CBC_DATA_2024ReviewDB.MDB"

# List tables in the database
print("loading file: {}".format(mdb_file))
tables = mdb.list_tables(mdb_file)
print("Tables:", tables)

# Example: Inspect schema of a specific table by reading its DataFrame
table_name = tables[0]  # Pick a table
df = mdb.read_table(mdb_file, table_name)
print(f"Schema of table {table_name}:")
print(df.info())  # Displays column names, types, and non-null counts


