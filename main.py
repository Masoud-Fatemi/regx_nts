# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 17:11:36 2024

@author: Masou

 - related to "Kimmo-Ilari Juntunen", a studet who asked for data (check uef email for more info)
 - results for each of patterns in a separate csv file with the tweet text, date, country, 
     network size and language as the metadata

"""
import os
import json
import re
import pandas as pd
import time
start = time.time()

def read_json_list(path):
    data = []
    with open(path, 'r') as file:
        for line in file.readlines():
            data.append(json.loads(line))
    return data

def clean_time(datetime):
    # Split the string to remove the milliseconds and 'Z'
    datetime = datetime.split('.')[0]  # Removes the milliseconds
    # Replace 'T' with a space to separate date and time
    datetime = datetime.replace('T', ' ')
    return datetime

save = True
input_dir = 'data/'
output_dir = 'output/'

pattern  = r'speedrunned'
# pattern = r'.*ve\sspeedrunned'
# pattern = r'.*ve\sspeedrun'
# pattern = r'.*ve\sspeedran'
# pattern = r'ragequitted'
# pattern = r'.*ve\sragequit'

tweet_ids = list()
tweet_text, date = list(), list()
country, network = list(), list()
language = list()


#to get all the json files in a directory
json_files = [file for file in os.listdir(input_dir) if file.endswith('.json')]

for json_file in json_files:
    
    tweets = read_json_list(input_dir+json_file)

    for tweet in tweets:
        
        text = tweet['text']
        
        # Find all matches of the pattern in the text
        matches = re.findall(pattern, text)
        # Count the number of matches
        count = len(matches)
        
        if count > 0:
            for i in range(count):
                tweet_ids.append(tweet['id'])
                tweet_text.append(text)
                date.append(clean_time(tweet['created_at']))
                country.append(tweet['geo']['country_code'])
                network.append(tweet['author']['public_metrics']['following_count'])
                language.append(tweet['lang'])
                
results = {
    'ID':tweet_ids,
    'Text': tweet_text,
    'Date': date,
    'Country': country,
    'Network': network,
    'language': language
    }
df = pd.DataFrame(results)

if save:
    df.to_excel(output_dir + pattern + '.xlsx', index=False, engine='openpyxl')
    
print(round((time.time()-start)/60, 0))