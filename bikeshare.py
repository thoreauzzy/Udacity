import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

LINE_LEN = 90
# print long string with repeating char, used to separate sections of output
print_line = lambda char: print(char[0] * LINE_LEN)


def print_processing_time(start_time):
    time_str = "[... %s seconds]" % round((time.time() - start_time), 3)
    print(time_str.rjust(LINE_LEN))
    print_line('-')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_list = []
    num_cities = 0

    for a_city in CITY_DATA:
        cities_list.append(a_city)
        num_cities += 1
        print('        {0:20}. {1}'.format(num_cities, a_city.title()))

    # ask user to input a number for a city from the list; easier for user than string input
    while True:
        try:
            city_num = int(input("\n    Enter a number for the city (1 - {}):  ".format(len(cities_list))))
        except:
            continue

        if city_num in range(1, len(cities_list) + 1):
            break

    # get the city's name in string format from the list
    city = cities_list[city_num - 1]

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("    Enter the month with January=1, June=6 or 'a' for all:  ")
        except:
            print("        ---->>  Valid input:  1 - 6, a")
            continue

        if month == 'a':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            # reassign the string name for the month
            month = MONTHS[int(month) - 1]
            break
        else:
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("    Enter the day with Monday=1, Sunday=7 or 'a' for all:  ")
        except:
            print("        ---->>  Valid input:  1 - 7, a")
            continue

        if day == 'a':
            day = 'all'
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            # reassign the string name for the day
            day = WEEKDAYS[int(day) - 1]  # here we MUST -1 to get correct index
            break
        else:
            continue

    print('-' * 40)
    return city, month, day


def filter_summary(city, month, day, init_total_rides, df):
    """
    Displays selected city, filters chosen, and simple stats on dataset.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int) init_total_rides - total number of rides in selected city before filter
        (dataframe) df - filtered dataset
    """
    start_time = time.time()

    filtered_rides = len(df)
    num_stations_start = len(df['Start Station'].unique())
    num_stations_end = len(df['End Station'].unique())

    print('  Gathering statistics for:      ', city)
    print('    Filters (month, day):        ', month, ', ', day)
    print('    Total rides in dataset:      ', init_total_rides)
    print('    Rides in filtered set:       ', filtered_rides)
    print('    Number of start stations:    ', num_stations_start)
    print('    Number of end stations:      ', num_stations_end)

    print_processing_time(start_time)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month  # range (1-12)
    df['day_of_week'] = df['Start Time'].dt.dayofweek  # range (0-6)
    df['hour'] = df['Start Time'].dt.hour  # range (0-23)

    init_total_rides = len(df)
    filtered_rides = init_total_rides  # initially

    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month_i = MONTHS.index(month) + 1  # index() returns 0-based, so +1

        # filter by month to create the new dataframe
        df = df[df.month == month_i]
        month = month.title()

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the WEEKDAYS list to get the corresponding int
        day_i = WEEKDAYS.index(day)  # index() returns 0-based, matches df

        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day_i]
        day = day.title()

    print_processing_time(start_time)

    filter_summary(city.title(), month, day, init_total_rides, df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print(common_month)
    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(common_day_of_week)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(common_start)
    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(common_end)
    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print(common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print(total_travel)

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("There is no gender information in this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(
            f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\ntype (Yes or yes) or type (No or no)")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
