# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 22:21:47 2024

@author: Masou
"""

import os
import json
import re
import pandas as pd
import time
from datetime import datetime

# Global variables
MAIN_DIR = 'data/'  # Update this to your main directory path
OUTPUT_DIR = 'output/'

PATTERN  = r'speedrunned'
PATTERN = r'.*ve\sspeedrunned'
PATTERN = r'.*ve\sspeedrun'
PATTERN = r'.*ve\sspeedran'
PATTERN = r'ragequitted'
PATTERN = r'.*ve\sragequit'


def read_json_file(file_path):
    """Read a JSON file and return its content, skipping lines with errors."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # Skip lines that cause JSON decoding errors
    return data

def format_datetime(datetime_str):
    """Format the datetime string to remove milliseconds and 'Z'."""
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")

def find_tweets_matching_pattern(tweets, pattern):
    """Find and return tweets matching the given pattern."""
    return [tweet for tweet in tweets if re.search(pattern, tweet['text'])]

def extract_tweet_metadata(tweets):
    """Extract metadata from tweets."""
    metadata = {
        'ID': [],
        'Text': [],
        'Date': [],
        'Country': [],
        'Network': [],
        'Language': []
    }
    for tweet in tweets:
        if 'geo' in tweet:
            metadata['ID'].append(tweet['id'])
            metadata['Text'].append(tweet['text'])
            metadata['Date'].append(format_datetime(tweet['created_at']))
            metadata['Country'].append(tweet['geo']['country_code'])
            metadata['Network'].append(tweet['author']['public_metrics']['following_count'])
            metadata['Language'].append(tweet['lang'])
    return metadata

def save_to_excel(data, pattern, output_dir):
    """Save the extracted data to an Excel file."""
    df = pd.DataFrame(data)
    filename = os.path.join(output_dir, f"{pattern}.xlsx")
    df.to_excel(filename, index=False, engine='openpyxl')

def main(main_dir, output_dir, pattern):
    start_time = time.time()
    
    all_tweets_metadata = {'ID': [], 'Text': [], 'Date': [], 'Country': [], 'Network': [], 'Language': []}
    
    for root, dirs, files in os.walk(main_dir):
        json_files = [os.path.join(root, file) for file in files if file.endswith('.json')]
        for json_file in json_files:
            tweets = read_json_file(json_file)
            matching_tweets = find_tweets_matching_pattern(tweets, pattern)
            if matching_tweets:
                tweet_metadata = extract_tweet_metadata(matching_tweets)
                for key in all_tweets_metadata:
                    all_tweets_metadata[key].extend(tweet_metadata[key])
    
    if all_tweets_metadata['ID']:  # Check if there are any matching tweets
        save_to_excel(all_tweets_metadata, pattern, output_dir)
    
    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"Pattern searched: {pattern}")
    print(f"Time taken: {elapsed_time_minutes:.2f} minutes")

if __name__ == "__main__":
    main(MAIN_DIR, OUTPUT_DIR, PATTERN)

