
# imports
import pandas as pd 
import utils.constants as const
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split



# constants
# gets ris of setting by copy warnings
pd.options.mode.chained_assignment = None 

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
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'


def get_time_of_day(hour, log=False):
    '''
    gets the time of day for a datetime var
    NOTE - make sure 20 hour clock
    '''
    hour = hour
    if hour < 8:
        return 'Dawn'
    elif hour < 11:
        return 'Morning'
    elif hour < 17:
        return 'Afternoon'
    else:
        return 'Evening'


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
    # avoid pd warning
    df_result['TimeOut'] = pd.to_datetime(df_result['TimeOut'])
    # df_result.loc[:, 'TimeOut'] = pd.to_datetime(df_result['TimeOut'])
    # Extract just the date part and create a new column
    df_result['TripDate'] = df_result['TimeOut'].dt.date    

    # add season column
    df_result['Season'] = df_result['TripDate'].map(get_season)
    print_shape(df_input=df_result, message='after season set')

    # add time of day
    df_result['TripHour'] = df_result['TimeOut'].dt.hour
    df_result['PartOfDay'] = df_result['TripHour'].apply(get_time_of_day)    
    print_shape(df_input=df_result, message='after time of day set')

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


def aggregate_season_data(df_input, year=2024, log=True):
    '''
    will aggregate the boat trip data by season
    '''
    # initialize

    # filter by year
    df_year = df_input[df_input['Year'] == year]

    # pivot
    # pivot_df = df_input.pivot_table(index='BoatId', columns='Season', aggfunc=len, fill_value=0)
    # if log:
    #     print("pivot df: \n{}".format(pivot_df.head()))

    # Group by 'Boat' and 'TimeOfDay', count, and unstack
    grouped_df = df_year.groupby(['BoatId', 'Season']).size().unstack(fill_value=0)
    if log:
        print("grouped df: \n{}".format(grouped_df.head()))

    # NOTE - by year as well
    # # Group by 'Boat', 'Year', and 'TimeOfDay', count, and unstack
    # grouped_df = df.groupby(['Boat', 'Year', 'TimeOfDay']).size().unstack(fill_value=0)
    # print(grouped_df)

    # return
    return grouped_df


def aggregate_time_of_day_data(df_input, year=2024, log=True):
    '''
    will aggregate the boat trip data by time of day
    '''
    # initialize

    # filter by year
    df_year = df_input[df_input['Year'] == year]

    # pivot
    # pivot_df = df_input.pivot_table(index='BoatId', columns='Season', aggfunc=len, fill_value=0)
    # if log:
    #     print("pivot df: \n{}".format(pivot_df.head()))

    # Group by 'Boat' and 'TimeOfDay', count, and unstack
    grouped_df = df_year.groupby(['BoatId', 'PartOfDay']).size().unstack(fill_value=0)
    if log:
        print("grouped df: \n{}".format(grouped_df.head()))

    # return
    return grouped_df


def aggregate_data(df_input, year=2024, log=False):
    '''
    aggregate data by year
    '''
    # count number trips per season over 3 miles
    # spring, fall, summer columns total
    # also percentage columns of tataol
    # total year trips column
    # avg trip length by season


def fit_random_forest_and_analize(df_input, column_target, list_column_todrop, log=True):
    '''
    fit to a random forest and analyze the features
    '''
    # # Encoding categorical data
    # label_encoder = LabelEncoder()
    # df['Feature2'] = label_encoder.fit_transform(df['Feature2'])

    # log input
    if log:
        print("\nfor cat feature importance, got data: \n{}".format(df_input.head()))

    # drop columns

    # Splitting the data into features and target
    X_train = df_input.drop(column_target, axis=1)
    y_train = df_input[column_target]

    # Splitting the dataset into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Initialize the model
    rf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    rf.fit(X_train, y_train)

    # Getting feature importance
    feature_importance = rf.feature_importances_
    map_feature_importance = dict(zip(X_train.columns, feature_importance))
    df_feature_importance = pd.DataFrame({'Feature': X_train.columns, 'ImportanceLowHigh': feature_importance})
    if log:
        print("feature importance: \n{}".format(df_feature_importance))

    # return
    return df_feature_importance


def analyse_data(df_input, log=True):
    '''
    will print analysis on the data
    '''
    print("null analysis: \n{}".format(df_input.isnull().sum()))


def fit_random_forest_regressor(df_input, column_target, list_column_todrop, yearInput=0, log=True):
    '''
    using random forest regressor
    '''
    # log input
    if log:
        print("\nfor continuous feature importance, got data: \n{}".format(df_input.head()))

    # Assume df is your DataFrame and 'target' is your continuous target variable
    X_train = df_input.drop(column_target, axis=1)
    y_train = df_input[column_target]

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    feature_importances = model.feature_importances_

    # Print feature importances
    df_importances = pd.DataFrame({'Feature': X_train.columns, 'ImportanceContinuous': feature_importances})
    print("for year: {} - random forest regresor feature importance: \n{}\n".format(yearInput, df_importances.sort_values(by='ImportanceContinuous', ascending=False)))

    # return
    return df_importances


# main
if __name__ == "__main__":
    # initialize
    debug = False

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

    # aggregate
    df_season = aggregate_season_data(df_input=df_trips)
    df_time_of_day = aggregate_time_of_day_data(df_input=df_trips)

    # TODO - loop here
    yearToStudy = 2024

    # sum by year
    df_grouped_sum = df_trips[df_trips['Year'] == yearToStudy].groupby('BoatId').size().reset_index(name='YearTrips')
    if debug:
        print("grouped sum: \n{}\n".format(df_grouped_sum.head()))

    # combine data by year/boat
    df_merged = pd.merge(df_grouped_sum, df_season, on='BoatId', how='inner')
    df_merged = pd.merge(df_merged, df_time_of_day, on='BoatId', how='inner')
    if debug:
        print("merged: \n{}\n".format(df_merged.head()))

    # calc percentages
    for col in ['Fall', 'Spring', 'Summer', 'Dawn', 'Morning', 'Afternoon', 'Evening']:
        df_merged[col + 'Perc'] = df_merged[col]/df_merged['YearTrips']
    if debug:
        print("merged: \n{}\n".format(df_merged.head()))

    # filter out less than 33 rows
    df_low_rows = df_merged[df_merged['YearTrips'] < 33]
    print("year: {}, got low row dataset of shape: {} from original dataset of shape: {}\n".format(yearToStudy, df_low_rows.shape, df_merged.shape))

    # regressor
    columns_to_model = ['YearTrips', 'FallPerc', 'SpringPerc', 'SummerPerc']
    df_cont_feature_importance = fit_random_forest_regressor(df_input=df_low_rows[columns_to_model], column_target='YearTrips', list_column_todrop=[], yearInput=yearToStudy)

    # simple correlations
    columns_to_model = ['YearTrips', 'FallPerc', 'SpringPerc', 'SummerPerc']
    df_input_correlation = df_merged[columns_to_model]
    # log input
    if debug:
        print("year: {} - for correlation, got data: \n{}".format(yearToStudy, df_input_correlation.head()))
    df_correlations = df_input_correlation.corr()['YearTrips'].drop('YearTrips', axis=0).to_frame()
    df_correlations.columns = ['CorrelationWithYearTrips']
    df_correlations.index.name = 'Feature'
    print("year: {} - correlations: \n{}\n".format(yearToStudy,df_correlations))

    # merge aggregate data
    # df_agg_merged = pd.merge(df_cat_feature_importance, df_cont_feature_importance, on='Feature', how='inner')
    df_agg_merged = pd.merge(df_cont_feature_importance, df_correlations, on='Feature', how='inner')
    print("year: {} - merged aggregation: \n{}".format(yearToStudy, df_agg_merged))























#     # categorize total trips per year
#     # df_merged['YearTripCat'] = pd.cut(df_merged['YearTrips'], bins=[0, 25, 50, 75, 1000], labels=['Low', 'Medium', 'High', 'Very High'], include_lowest=True)
#     df_merged['YearTripCat'] = pd.cut(df_merged['YearTrips'], bins=[0, 40, 1000], labels=['Low', 'High'], include_lowest=True)
#     print("merged: \n{}\n".format(df_merged.head()))

#     # fit random forest
#     # get feature analysis
#     columns_to_model = ['YearTripCat', 'FallPerc', 'SpringPerc', 'SummerPerc', 'DawnPerc', 'MorningPerc', 'AfternoonPerc', 'EveningPerc']
#     df_cat_feature_importance = fit_random_forest_and_analize(df_input=df_merged[columns_to_model], column_target='YearTripCat', list_column_todrop=[])

#     # regressor
#     columns_to_model = ['YearTrips', 'FallPerc', 'SpringPerc', 'SummerPerc', 'DawnPerc', 'MorningPerc', 'AfternoonPerc', 'EveningPerc']
#     df_cont_feature_importance = fit_random_forest_regressor(df_input=df_merged[columns_to_model], column_target='YearTrips', list_column_todrop=[])

#     # simple correlations
#     columns_to_model = ['YearTrips', 'FallPerc', 'SpringPerc', 'SummerPerc', 'DawnPerc', 'MorningPerc', 'AfternoonPerc', 'EveningPerc']
#     df_input_correlation = df_merged[columns_to_model]
#     # log input
#     print("\nfor correlation, got data: \n{}".format(df_input_correlation.head()))
#     df_correlations = df_input_correlation.corr()['YearTrips'].drop('YearTrips', axis=0).to_frame()
#     df_correlations.columns = ['CorrelationWithYearTrips']
#     df_correlations.index.name = 'Feature'
#     # df_tran_corr = pd.DataFrame(df_correlations).T
#     print("\ncorrelations: \n{}".format(df_correlations))
#     # df_new_corr = pd.DataFrame([df_correlations.values], columns=df_correlations.index)
#     # df_new_corr.index = ['Correlation']
#     # print("\ncorrleations: \n{}".format(df_new_corr))

#     # merge aggregate data
#     df_agg_merged = pd.merge(df_cat_feature_importance, df_cont_feature_importance, on='Feature', how='inner')
#     df_agg_merged = pd.merge(df_agg_merged, df_correlations, on='Feature', how='inner')
#     print("\nmerged aggregation: \n{}".format(df_agg_merged))

# # TODO
# # - sum by year for all boats
# # - categorize sum by year?

