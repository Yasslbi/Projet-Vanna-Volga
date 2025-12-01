#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 15:14:51 2025

@author: yassinelaabi
"""

#PANDAS

# Pandas is a data science package which is used for performing data analysis and data manipulation

# Pandas has 2 main structures : 
    
# 1) Series (1D Labeled Array)
# 2) DataFrame (2D Labeled Array)

import pandas as pd

# 1) Series (1D Labeled Array)

# Create A Series : List

data = [1,2,3]

df = pd.Series(data)
print(df)


# Create A Series : Dictionary

data = {"a":1, "b":2, "c":3}
df = pd.Series(data)
print(df)


data = {"Georges":100, "Max":82, "Stéphanie":95}
df = pd.Series(data)
print(df)

# Lesson : If I want to have default label (colonne à gauche), I can use List
# If I want to create manual labels, I will have to use dictionary, or i can provide index to my series

import numpy as np

data = np.array(['a','b','c','d']) #Unlabeled array
df = pd.Series(data) # labeled array
print(df)


data = np.array(['a','b','c','d']) #Unlabeled array
df = pd.Series(data, index = [1,2,3,4]) # labeled array
print(df)



# Indexing & slicing in series

data = np.array(['a','b','c','d']) #Unlabeled array
df = pd.Series(data) # labeled array
print(df)

Index_0 = df[0]
print(Index_0)

Index_1 = df[1]
print(Index_1)


# Start = 0
# Stop = 2-1 =1

print(df[0:2])


# Grab c and d

print(df[2:4])


# Basic operations on series

# np.nan = there is no value in here = this is not 0 = 

df = pd.Series([1,2,np.nan,4,5])
print(df)

# sum
print(df.sum())

# Mean or Average
print(df.mean())


# Median --> iT ARRANGE THE VALUE IN ASCENDING ORDER
# It will see the mid part

print(df.median())

# Standard deviation
print(df.std())

# Missing values (Null values)

print(df.isnull())

print(df.isnull().sum()) #nb of missing values

print(df.notnull())

print(df.notnull().sum()) #nb of correct values



# Series vs numpy

# 1D Numpy has no indexing associate with it

# 2) DataFrame (2D Labeled Array)

# How to create a dataframe 

data = {'Name':['Alice','Bob','Charlie'],
       'Salary':[10000,20000,30000],
       'Age':[45,30,35]}

df = pd.DataFrame(data)
print(df)

# Series --> We had only index name
# DataFrame  ---> We have both index name and column name
# Dataframe has both rows and column
# DataFrame -> 2D Array, tabular data



data = {'City':['New York','London','Paris'],
       'Cost':[1000,1200,1500],
       'Rating':[5,4,4.5]}

df = pd.DataFrame(data)
print(df)

# Create a dataframe using a List

data = [['New York','London','Paris'],[1000,1200,1500], [5,4,4.5]]
df = pd.DataFrame(data, columns= ['City', 'Cost', 'Rating'])
print(df)








































