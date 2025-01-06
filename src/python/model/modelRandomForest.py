
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


def get_season(data, log=False):
    '''
    gets the season for a datetime var
    '''
    month = data.month
    if month in [3, 4,5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'

def get_time_of_day(data, log=False):
    '''
    gets the time of day for a datetime var
    NOTE - make sure 20 hour clock
    '''
    hour = data.hour
    if hour < 8:
        return 'dawn'
    elif hour < 11:
        return 'morning'
    elif hour < 5:
        return 'afternoon'
    else:
        return 'evening'


def print_shape(df_input, message, log=False):
    '''
    prints the shape of the dataframe
    '''
    print("shape after {}:{}".format(message, df_input.shape))


def filter_data_for_modeling(df_input, is_member_rack=True, log=True):
    '''
    will filter the data for modeling
    '''
    # log
    if log:
        print("got df input of shape: {}".format(df_input.shape))

    # clean out nulls in all columns
    df_result = df_input.dropna()
    print_shape(df_input=df_result, message='after dropna')

    # create a date column
    # Convert the 'datetime_column' to datetime if it's not already
    df_result['TimeOut'] = pd.to_datetime(df_result['TimeOut'])
    # Extract just the date part and create a new column
    df_result['date_trip'] = df_result['TimeOut'].dt.date    

    # add season column
    df_result['season'] = df_result['date_trip'].map(get_season)
    print_shape(df_input=df_result, message='after season set')

    # recast owner id to int
    # first filter put 'Junior'
    df_result = df_result[-df_result['Rack'].isin(['Junior', 'Outside'])]
    df_result['Rack'] = df_result['Rack'].astype(int)

    # if rack, filter down to just rack member owned boats
    if is_member_rack:
        df_result = df_result[df_result['ClubBoat'] == 0]
        print_shape(df_input=df_result, message='after member filter')
        df_result = df_result[df_result['Rack'] > 0]
        print_shape(df_input=df_result, message='after rack filter')

    # filter out less than 3 miles
    df_result['Miles'] = df_result['Miles'].astype(float)
    df_result = df_result[df_result['Miles'] >= 3]
    print_shape(df_input=df_result, message='after 3 mile filter')


    # log
    if log:
        print("got df result of shape: {}".format(df_result.shape))

    # return
    return df_result


def aggregate_data(df_input, year=2024, log=False):
    '''
    aggregate data by year
    '''
    # count number trips per season over 3 miles
    # spring, fall, summer columns total
    # also percentage columns of tataol
    # total year trips column
    # avg trip length by season




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

    # add season
    # df_trips['season'] = df_trips['date_trip'].map(get_season)

    # analyse
    analyse_data(df_input=df_trips)

    # print sample
    print(df_trips.head())





