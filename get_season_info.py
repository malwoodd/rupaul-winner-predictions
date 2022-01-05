# -*- coding: utf-8 -*-
"""get_season_info.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e_KMzhh5flzAvXnuPIMaxWa9UmJ7IYXZ
"""

import requests
from urllib.request import urlopen as uReq
from collections import namedtuple
import pandas as pd
from google.colab import drive
drive.mount('drive')

season_properties = ['id', 'name', 'reg_season', 'reg_place', 'as_season', 'as_place']
Season = namedtuple("Season", season_properties)

queens_url = "http://www.nokeynoshade.party/api/queens/all"

response = requests.get(url=queens_url)

queens_json = response.json()

print(queens_json)

#get list of ids

list_of_ids = []

for queen in queens_json:
  list_of_ids.append(queen['id'])

print(list_of_ids)

#get name, seasonNumber, place, from ID

def create_season_tuple(queen):
  reg_season = []
  reg_place = []
  as_season = []
  as_place = []
  #print(queen)
  seasons_url = 'http://www.nokeynoshade.party/api/queens/' + str(queen)
  #print(seasons_url)
  response = requests.get(url=seasons_url)
  seasons_json = response.json()

  id = seasons_json['id']
  name = seasons_json['name']
  #print(len(seasons_json['seasons']))
  num_season = (len(seasons_json['seasons']))
  
  if num_season >= 1:
    for season in seasons_json['seasons']:
      if "A" not in season['seasonNumber']:
        #print("reg", season['seasonNumber'])
        reg_season.append(season['seasonNumber'])
        reg_place.append(season['place'])
      else:
        #print("as", season['seasonNumber'])
        as_season.append(season['seasonNumber'])
        as_place.append(season['place'])

  season_tuple = Season(id, name, reg_season, reg_place, as_season, as_place)

  return season_tuple

#run list of ids through tuple function to create seasons list
seasons_list = []

for queen in list_of_ids:
  season_info = create_season_tuple(queen)
  seasons_list.append(season_info)

print(seasons_list)

seasons_dataframe = pd.DataFrame.from_records(seasons_list, columns=season_data)

seasons_dataframe.to_csv("/content/drive/MyDrive/Developer/Seasons.csv", index=False)

seasons_dataframe.head()