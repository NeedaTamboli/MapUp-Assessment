#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import pandas as pd

import warnings
# Suppress warnings
warnings.filterwarnings("ignore")


# In[13]:


df = pd.read_csv("dataset-1.csv")
df.head()


# In[33]:


df["route"].unique()


# # Question 1: Car Matrix Generation
# Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# values from id_2 as columns
# values from id_1 as index
# dataframe should have values from car column
# diagonal values should be 0.
# Sample result dataframe:
# Task 1 Question 1

# In[24]:


def generate_car_matrix(dataset):
    # Create the new dataframe
    new_df = df.pivot(index='id_1', columns='id_2', values='car')
    
    # Set diagonal values to 0
    new_df.values[[range(len(new_df))]*2] = 0
    
    return new_df


# In[21]:


ans = generate_car_matrix(df)
ans


# ## Question 2: Car Type Count Calculation
# Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# low for values less than or equal to 15,
# medium for values greater than 15 and less than or equal to 25,
# high for values greater than 25.
# Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.

# In[26]:


def get_type_count(data_frame):
    # Add a new categorical column 'car_type' based on conditions
    data_frame['car_type'] = pd.cut(data_frame['car'], bins=[-float('inf'), 15, 25, float('inf')],
                                    labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_count = data_frame['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_count = dict(sorted(type_count.items()))

    return type_count


# In[25]:


# Call the function and print the result
result = get_type_count(df)
result


# ## Question 3: Bus Count Index Retrieval
# Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[27]:


def get_bus_indexes(data_frame):
    # Calculate the mean value of the 'bus' column
    mean_bus = data_frame['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = data_frame[data_frame['bus'] > 2 * mean_bus].index

    # Return the indices as a list (sorted in ascending order)
    return sorted(bus_indexes)


# In[28]:


# Call the function and print the result
result = get_bus_indexes(df)
result


# ## Question 4: Route Filtering
# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[37]:


df.groupby("route")["truck"].mean()


# In[30]:


def filter_routes(data_frame):

    # Group by 'route' and filter based on the average of 'truck' values
    selected_routes = data_frame.groupby('route').filter(lambda group: group['truck'].mean() > 7)['route'].unique()

    # Return the sorted list of selected routes
    return sorted(selected_routes)


# In[34]:


def filter_routes(data_frame):
    # Group by 'route' and calculate the average of 'truck' values
    route_avg_truck = data_frame.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index

    # Return the sorted list of selected routes
    return sorted(selected_routes)


# In[35]:


result = filter_routes(df)
result


# ## Question 5: Matrix Value Modification
# Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# If a value is 20 or less, multiply those values by 1.25.
# The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[38]:


def multiply_matrix(input_df):
    # Create a deep copy of the input DataFrame to avoid modifying the original
    modified_df = input_df.copy(deep=True)

    # Apply the specified logic to modify values
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df


# In[39]:


result = multiply_matrix(ans)
result


# ## Question 6: Time Check
# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[118]:


df1 = pd.read_csv("dataset-2.csv")
df1.head()


# In[119]:


#df1.columns


# In[120]:


#df1.info()


# In[121]:


#df1["startDay"].unique()


# In[122]:


df1["endDay"].unique()


# In[123]:


df1["startTime"].unique()


# In[124]:


df1["endTime"].unique()


# In[125]:


df1.info()


# In[160]:


def time_check(df):
# Write your logic here
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')
    full_day_coverage = (df['end_datetime'] - df['start_datetime']).dt.total_seconds() == 24 * 60 * 60
    days_of_week_coverage = df.groupby(['id', 'id_2'])['start_datetime'].transform(lambda x: x.dt.dayofweek.nunique() == 7)
    is_complete = full_day_coverage & days_of_week_coverage

    return is_complete


# In[161]:


result = time_check(df1)
result


# In[ ]:





# In[ ]:




