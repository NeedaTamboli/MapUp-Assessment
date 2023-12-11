#!/usr/bin/env python
# coding: utf-8

# Python Task 2

# In[ ]:





# In[ ]:


# Python Task 2


# ## Question 1: Distance Matrix Calculation
# 
# Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[82]:


import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# In[48]:


df = pd.read_csv("dataset-3.csv")
df


# In[49]:


df.columns


# In[50]:


def calculate_distance_matrix(data_path):
    # Load the dataset
    unique_ids = sorted(set(df['id_start'].unique()).union(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)
    distance_matrix = distance_matrix.fillna(0)

    for index, row in df.iterrows():
        start, end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance

    for i in distance_matrix.index:
        for j in distance_matrix.index:
            if i == j:
                continue
            if distance_matrix.at[i, j] == 0:
                for k in distance_matrix.index:
                    if i != k and j != k and distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix


# In[51]:


# Replace 'dataset-3.csv' with the actual path to your dataset
result_df = calculate_distance_matrix(df)

# Display the resulting DataFrame
result_df


# In[52]:


df = result_df.copy()


# ## Question 2: Unroll Distance Matrix
# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[61]:


def unroll_distance_matrix(df):
    unrolled_df = pd.DataFrame(columns= ['id_start', 'id_end', 'distance'])
    for i in df.index:
        for j in df.index:
            if i != j and df.at[i,j] != 0:
                unrolled_df = pd.concat([unrolled_df, pd.DataFrame({'id_start':[i], 'id_end':[j], 'distance': [df.at[i,j]]})], ignore_index = True)
                
    return unrolled_df


# In[62]:


result_unrolled_df = unroll_distance_matrix(df)
result_unrolled_df


# In[ ]:





# ## Question 3: Finding IDs within Percentage Threshold
# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[63]:


def find_ids_within_ten_percentage_threshold(df, reference_id):
    
    reference_avg_distance = df[df['id_start'] == reference_id]['id_start'].mean()
    
    lower_threshold = reference_avg_distance - (reference_avg_distance * 0.10)
    upper_threshold = reference_avg_distance + (reference_avg_distance * 0.10)
    
    within_threshold_values = df[(df['id_start'] >= lower_threshold) & (df['id_start'] <= upper_threshold)]['id_start']
    
    sorted_within_threshold_values = sorted(within_threshold_values.unique())
    
    return sorted_within_threshold_values


# In[65]:


reference_id = result_unrolled_df['id_start']


# In[66]:


result_list = find_ids_within_ten_percentage_threshold(result_unrolled_df, reference_id)
result_list


# ## Question 4: Calculate Toll Rate
# Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:

# In[68]:


def calculate_toll_rate(df):
    rate_coefficients = {'moto':0.8, 'car':1.2, 'rv':1.5, 'bus':2.2, 'truck':3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient
        
    return df


# In[69]:


result_with_toll_rates = calculate_toll_rate(result_unrolled_df)
result_with_toll_rates


# In[ ]:





# In[84]:


import datetime
data = pd.DataFrame({'id_start': [1, 2, 3, 4, 5, 6],'id_end': [2, 3, 4, 5, 6, 1],'distance': [10, 15, 12, 8, 9, 11]})


# ## Question 5: Calculate Time-Based Toll Rates
# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[79]:


from datetime import datetime, time


# In[80]:


def calculate_time_based_toll_rates(df):
    # Calculate toll rates based on distance for different vehicle types
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    # Generate time intervals for weekdays and weekends
    weekday_intervals = [
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0), 0.8),
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0), 1.2),
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59), 0.8)
    ]
    weekend_intervals = [
        (datetime.time(0, 0, 0), datetime.time(23, 59, 59), 0.7)
    ]

    # Create lists to store data for new columns
    start_day_list, start_time_list, end_day_list, end_time_list = [], [], [], []
    moto_list, car_list, rv_list, bus_list, truck_list = [], [], [], [], []

    # Get unique (id_start, id_end) pairs
    unique_pairs = df[['id_start', 'id_end']].drop_duplicates()

    # Iterate through unique pairs and time intervals to create rows for each interval
    for index, row in unique_pairs.iterrows():
        id_start, id_end = row['id_start'], row['id_end']
        for day in range(7):  # Iterate for all 7 days
            for interval in weekday_intervals if day < 5 else weekend_intervals:  # Choose intervals based on weekdays or weekends
                start_time, end_time, discount_factor = interval
                start_day_list.append(datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=day), '%A'))
                end_day_list.append(datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=day), '%A'))
                start_time_list.append(start_time)
                end_time_list.append(end_time)
                moto_list.append(df.loc[(df['id_start'] == id_start) & (df['id_end'] == id_end), 'moto'].iloc[0] * discount_factor)
                car_list.append(df.loc[(df['id_start'] == id_start) & (df['id_end'] == id_end), 'car'].iloc[0] * discount_factor)
                rv_list.append(df.loc[(df['id_start'] == id_start) & (df['id_end'] == id_end), 'rv'].iloc[0] * discount_factor)
                bus_list.append(df.loc[(df['id_start'] == id_start) & (df['id_end'] == id_end), 'bus'].iloc[0] * discount_factor)
                truck_list.append(df.loc[(df['id_start'] == id_start) & (df['id_end'] == id_end), 'truck'].iloc[0] * discount_factor)

    # Create a new DataFrame with calculated columns
    new_df = pd.DataFrame({
        'start_day': start_day_list,
        'start_time': start_time_list,
        'end_day': end_day_list,
        'end_time': end_time_list,
        'moto': moto_list,
        'car': car_list,
        'rv': rv_list,
        'bus': bus_list,
        'truck': truck_list
    })

    return new_df


# In[85]:


# Call the function with your DataFrame
result_with_time_based_rates = calculate_time_based_toll_rates(data)
result_with_time_based_rates


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




