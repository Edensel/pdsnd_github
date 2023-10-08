import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (case-insensitive)
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington? ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city name. Please choose from Chicago, New York, or Washington.')

    # Get user input for filter type (month, day, both, none) (case-insensitive)
    while True:
        filter = input('Would you like to filter the data by month, day, both, or none? ').lower()
        if filter in ['month', 'day', 'both', 'none']:
            break
        else:
            print('Invalid filter type. Please choose from month, day, both, or none.')

    # Get user input for month (case-insensitive)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if filter in ['month', 'both']:
        while True:
            month = input('Which month - January, February, March, April, May, or June? ').lower()
            if month in months:
                break
            else:
                print('Invalid month name. Please choose from January to June.')

    else:
        month = 'all'

    # Get user input for day of the week (case-insensitive)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if filter in ['day', 'both']:
        while True:
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').title()
            if day in days:
                break
            else:
                print('Invalid day name. Please choose from Monday to Sunday.')
    else:
        day = 'all'

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = df['month'].mode()[0]
    print(f'The most common month is: {months[common_month - 1]}')

    # Display the most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print(f'The most common day of the week is: {common_day}')

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f'The most common start hour is: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {popular_start_station}')

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'The most popular end station is: {popular_end_station}')

    # Display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'The most popular trip is from {popular_trip[0]} to {popular_trip[1]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    total_travel_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    print(f'Total travel time: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds')

    # Calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    minutes, seconds = divmod(mean_travel_time, 60)
    print(f'Average travel time: {int(minutes)} minutes, {int(seconds)} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print(f'Counts of each user type:\n{user_counts}')

    if 'Gender' in df.columns:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print(f'\nCounts of each gender:\n{gender_counts}')

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common birth year
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest birth year: {earliest_birth_year}')
        print(f'Most recent birth year: {most_recent_birth_year}')
        print(f'Most common birth year: {most_common_birth_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Ask the user if they want to display the raw data and print 5 rows at a time."""
    raw_data = input('\nWould you like to display raw data? Enter "yes" or "no": ').lower()
    count = 0
    while raw_data == 'yes':
        print(df.iloc[count:count+5])
        count += 5
        raw_data = input('Would you like to display the next 5 rows of raw data? Enter "yes" or "no": ').lower()
        if raw_data != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter "yes" or "no": ').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()

