import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

avl_months = ["January","February","March","April","May","June"]
avl_days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday"]

def get_city():
    """Receiving a city name as user input.

    INPUT:
    city: String value

    OUTPUT:
    city: The function checks if the city name is one of the required city (Chicago, New york, Washington)
    and returns it if the value is True. If the value is False it prompts the user as an invalid input and
    asks again for a valid input"""

    city = input("Would you like to see the data for Chicago, New york or Washington?\n").lower()
    while city != "chicago" and city != "new york" and city != "washington":
        print("You have entered an invalid input.")
        city = input("Would you like to see the data for Chicago, New york or Washington?\n").lower()
    return city

def get_month():
    """Receiving a month name as user input.

    INPUT:
    month: String value

    OUTPUT:
    month: The function checks if the month name is one of the required month from the set "avl_months"
    and returns it if the value is True. If the value is False it prompts the user as an invalid input and
    asks again for a valid input"""

    month = input("Please enter the month. January, February, March, April, May, June?\n").title()
    while month not in avl_months:
        print("You have entered an invalid input.")
        month = input("Please enter the month. January, February, March, April, May, June?\n").title()
    return month

def get_day():
    """Receiving a day name as user input.

    INPUT:
    day: String value

    OUTPUT:
    day: The function checks if the day name is one of the required day from the set "avl_days"
    and returns it if the value is True. If the value is False it prompts the user as an invalid input and
    asks again for a valid input"""

    day = input("Please enter the day. Sunday, Monday, Tuesday, Wednesday, Thursday, Friday?\n").title()
    while day not in avl_days:
        print("You have entered an invalid input.")
        day = input("Please enter the day. Sunday, Monday, Tuesday, Wednesday, Thursday, Friday?\n").title()
    return day

def display_data(df):
    """Displaying the dataframe.

    INPUT:
    df: dataframe

    OUTPUT:
    The first 5 rows of the dataframe is displayed and the code prompts the user to display more.
    If the user input is yes, next 5 rows are displayed. If no the code breaks"""

    del df["month"]
    del df["start_end"]
    del df["hour"]
    i = 0
    x = True
    while x:
        j = 0
        while j < 5:
            if i < len(df):
                print(df.iloc[i])
                print("\n")
                i+=1
                j+=1
        x = input("Would you like to see more data? yes/no\n").lower()
        if x == "yes":
            x = True
        else:
            x = False

def time_stats(df):
    """Displaying the time stats.

    INPUT:
    df: dataframe

    OUTPUT:
    The most common month, most common day of week and most common hour of day from the dataframe is displayed"""

    pop_month = df['month'].value_counts().idxmax()
    pop_day = df['day_of_week'].value_counts().idxmax()
    pop_hour = df['hour'].value_counts().idxmax()
    print("POPULAR TIMES OF TRAVEL")
    print("\tMost common month: {}".format(avl_months[pop_month-1]))
    print("\tMost common day of week: {}".format(pop_day))
    print("\tMost common hour of day: {}".format(pop_hour))

def station_stats(df):
    """Displaying the time stats.

    INPUT:
    df: dataframe

    OUTPUT:
    The Most common Start Station, Most common End Station and Most common Trip from start to end from the dataframe is displayed"""

    df['start_end'] = df['Start Station'] + " to " + df['End Station']
    pop_startst = df['Start Station'].value_counts().idxmax()
    pop_endst = df['End Station'].value_counts().idxmax()
    pop_strtend = df['start_end'].value_counts().idxmax()
    print("POPULAR STATIONS AND TRIPS")
    print("\tMost common Start Station: {}".format(pop_startst))
    print("\tMost common End Station: {}".format(pop_endst))
    print("\tMost common Trip from start to end: {}".format(pop_strtend))

def trip_duration_stats(df):
    """Displaying the time stats.

    INPUT:
    df: dataframe

    OUTPUT:
    The Total travel time and Average travel time from the dataframe is displayed"""

    sum_time = df["Trip Duration"].sum()
    avg_time = df["Trip Duration"].mean()
    print("TRIP DURATION")
    print("\tTotal travel time: {}".format(sum_time))
    print("\tAverage travel time: {}".format(avg_time))

def user_stats(df):
    """Displaying the time stats.

    INPUT:
    df: dataframe

    OUTPUT:
    The count of User type, count of Gender and the most common recent birth year from the dataframe is displayed"""

    user_type = df['User Type'].value_counts()
    print("USER INFO")
    print("\tUser type:")
    print(user_type)
    if city != "washington":
        req_birth_year = df.loc[df['Birth Year'] > 1990]
        gender = df['Gender'].value_counts()
        pop_birth_year = req_birth_year['Birth Year'].value_counts().idxmax()
        print("\tGender:")
        print(gender)
        print("\tMost common Birth year(recent): {}".format(int(pop_birth_year)))

a = True
print('Hello! Let\'s explore some US bikeshare data!')
while a:
    city = get_city()

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    time_filter = input("Would you like to filter data by month, day, both or not at all? Type \"none\" for no time filter\n").lower()
    while time_filter != "month" and time_filter != "day" and time_filter != "both" and time_filter != "none":
        print("You have entered an invalid input.")
        time_filter = input("Would you like to filter data by month, day, both or not at all? Type \"none\" for no time filter\n").lower()

    if time_filter == "month":
        month = get_month()
        df = df.loc[df['month'] == avl_months.index(month)+1]

    elif time_filter == "day":
        day = get_day()
        df = df.loc[df['day_of_week'] == day]

    elif time_filter == "both":
        month = get_month()
        day = get_day()
        df = df.loc[df['month'] == avl_months.index(month)+1]
        df = df.loc[df['day_of_week'] == day]

    if city != "washington":
        df['User Type'] = df['User Type'].fillna("Not available")
        df['Gender'] = df['Gender'].fillna("Not available")


    time_stats(df)

    print("\n")

    station_stats(df)

    print("\n")

    trip_duration_stats(df)

    print("\n")

    user_stats(df)


    disp = input("Would you like to display the data? yes/no\n").lower()
    if disp == "yes":
        display_data(df)

    a = input("Would you like to restart? yes/no\n").lower()
    if a == "yes":
        a = True
    else:
        a = False
