
# imports
import pandas as pd 
import utils.constants as const

# constants


# methods
def load_trip_data(log=True):
    '''
    load 22-24 trips data to df
    '''
    df_result = pd.read_csv(const.FILE_TRIPS_MERGED, sep='\t')

    # log
    if log:
        print(df_result.head())

    # return
    return df_result


def filter_data_for_modeling(df_input, log=True):
    '''
    will filter the data for modeling
    '''
    # log
    if log:
        print("got df input of shape: {}".format(df_input.shape))

    # clean out nulls
    df_result = df_input.dropna()

    # create a date column
    # Convert the 'datetime_column' to datetime if it's not already
    df_result['TimeOut'] = pd.to_datetime(df_result['TimeOut'])
    # Extract just the date part and create a new column
    df_result['date_trip'] = df_result['TimeOut'].dt.date    

    # log
    if log:
        print("got df result of shape: {}".format(df_result.shape))

    # return
    return df_result


def analyse_data(df_input, log=True):
    '''
    will print analysis on the data
    '''
    print("null analysis: \n{}".format(df_input.isnull().sum()))


# main
if __name__ == "__main__":
    # load the data
    df_trips = load_trip_data()

    # analyse
    analyse_data(df_input=df_trips)

    # clean the data
    df_trips = filter_data_for_modeling(df_input=df_trips)

    # analyse
    analyse_data(df_input=df_trips)

    # print sample
    print(df_trips.head())





