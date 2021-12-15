
# George Dimitriadis
# Made on 10/12/2021
# This is the script used to preprosess the data in the owid-covid-data.csv file to create npy arrays that the
# Blender code can read

import csv
import pandas as pd
import numpy as np

blender_meshes = ['Albania', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Czechia', 'Croatia',
                  'Cyprus',  'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
                  'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                  'North Macedonia', 'Moldova', 'Montenegro', 'Netherlands', 'Norway', 'Poland',
                  'Portugal', 'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
                  'Turkey', 'United Kingdom', 'Ukraine', 'Malta']

blender_hooks = ['Albania', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Czechia', 'Croatia',
                  'Cyprus',  'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
                  'Hungary', 'Iceland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                  'North Macedonia', 'Moldova', 'Montenegro', 'Netherlands', 'Norway', 'Poland',
                  'Portugal', 'Romania', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
                  'Turkey', 'Ukraine', 'Russia', 'Ireland', 'Malta', 'United Kingdom']

# Data file from https://covid.ourworldindata.org/data/owid-covid-data.csv
full_data_file_name = r"E:/Projects Small/2022_01_Europe_vaccinated_infographic/covid-full-data.csv"
full_data = pd.read_csv(full_data_file_name)
full_data.date = pd.to_datetime(full_data.date, dayfirst=True).dt.date
df_deaths = pd.pivot_table(full_data, values='new_deaths_smoothed_per_million', index=['date'], columns=['location'])
df_vaccines = pd.pivot_table(full_data, values='people_fully_vaccinated_per_hundred', index=['date'], columns=['location'])

df_deaths = df_deaths.fillna(method='pad')
df_deaths = df_deaths.fillna(value=-1)
df_vaccines = df_vaccines.fillna(method='pad')
df_vaccines = df_vaccines.fillna(value=-1)

df_deaths_europe = df_deaths[blender_hooks]
df_vaccines_europe = df_vaccines[blender_meshes]

np_deaths = df_deaths_europe.to_numpy()
np_vaccines = df_vaccines_europe.to_numpy()
np_dates = df_deaths.index.astype(dtype=str).to_numpy()

np.save(r'E:/Projects Small/2022_01_Europe_vaccinated_infographic/deaths.npy', np_deaths)
np.save(r'E:/Projects Small/2022_01_Europe_vaccinated_infographic/vaccinated.npy', np_vaccines)
np.save(r'E:/Projects Small/2022_01_Europe_vaccinated_infographic/dates.npy', np_dates, allow_pickle=True)

start_of_vaccination_index = df_deaths_europe.index.get_loc(df_vaccines_europe.index[0])

assert start_of_vaccination_index + df_vaccines_europe.shape[0] == df_deaths_europe.shape[0]