

# directory constants
# NOTE: change this setting for portability
DIR_DATA = "/Users/mduby/Data/Personal/CbcRack/"
DIR_DATA = "/home/javaprog/Data/Personal/CbcRack/"

# rest
DIR_DATA_PANDAS_22 = DIR_DATA + "Csv22/"
DIR_DATA_PANDAS_23 = DIR_DATA + "Csv23/"
DIR_DATA_PANDAS_24 = DIR_DATA + "Csv24/"
DIR_DATA_PANDAS_MERGED = DIR_DATA + "Merged/"


# file constants
FILE_BOATS = DIR_DATA_PANDAS_24 + "Boats.csv"
FILE_TRIPS_22 = DIR_DATA_PANDAS_22 + "Trips.csv"
FILE_TRIPS_23 = DIR_DATA_PANDAS_23 + "Trips.csv"
FILE_TRIPS_24 = DIR_DATA_PANDAS_24 + "Trips.csv"
FILE_TRIPS_MERGED = DIR_DATA_PANDAS_MERGED + "TripsMerged.tsv"

# FILE_2024 = DIR_DATA + "CBC_DATA_2024ReviewDB.MDB"

# data constants
# ['BoatId', 'BoatName', 'BoatMaker', 'BoatTypeId', 'Rack', 'WeightClass', 'ClubBoat', 'OwnerId', 'BoatYear', 'Category', 'BoatFullName', 'Comments', 'Hidden', 'TripID', 'SignedBy', 'TimeOut', 'TimeIn', 'Miles', 'BoatOK', 'NeedsWork', 'WorkComment', 'OtherComments', 'WorkCompleted', 'FirstChoice']
LIST_COLUMNS_PERSONAL_BOATS = ['Year', 'BoatId', 'BoatName', 'BoatTypeId', 'Rack', 'ClubBoat', 'OwnerId', 'TripID', 'SignedBy', 'TimeOut', 'TimeIn', 'Miles']
