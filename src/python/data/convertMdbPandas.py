

import pandas as pd
import pyodbc
# import utils.constants as const

# constants
DIR_DATA = "/home/javaprog/Data/Personal/CbcRack/"
DIR_DATA_PANDAS = "/home/javaprog/Data/Personal/CbcRack/Csv"

FILE_2024 = DIR_DATA + "CBC_DATA_2024ReviewDB.MDB"

FILE = FILE_2024
DIR_OUT = DIR_DATA_PANDAS

# methods
def mdb_to_csv(mdb_path, output_folder):
    # Set up the connection string
    # conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    #             f'DBQ={mdb_path};')
    conn_str = (r'DRIVER={MDBToolsODBC};'
                f'DBQ={mdb_path};')
        
    # Establish connection to the MDB file
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Get list of all tables in the MDB file
    cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND flags=0")

    # NOTE: fix for bad encoding
    # tables = [row.name for row in cursor.fetchall()]
    for row in cursor.fetchall():
        try:
            tables.append(row.name.encode('utf-16le').decode('utf-16le'))
        except UnicodeDecodeError:
            tables.append(row.name.encode('latin1').decode('utf-8'))

    # Process each table
    for table in tables:
        print(f"Processing table: {table}")
        # Read the table into a DataFrame
        query = f"SELECT * FROM [{table}]"
        df = pd.read_sql(query, conn)
        
        # Save the DataFrame to a CSV file
        output_path = f"{output_folder}/{table}.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved {table} to {output_path}")

    # Close the database connection
    cursor.close()
    conn.close()

# main
if __name__ == "__main__":
    # initialize
    dir_out = DIR_OUT
    file_in = FILE

    # log
    print("reading file: {}".format(file_in))
    print("outputing data to: {}".format(dir_out))

    # execute
    mdb_to_csv(file_in, dir_out)




