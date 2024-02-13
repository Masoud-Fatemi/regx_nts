# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 17:11:36 2024

@author: Masou

related to "Kimmo-Ilari Juntunen", a studet who asked for data (check uef email for more info)

"""
import os

input_dir = 'data/'

#to get all the json files in a directory
json_files = [file for file in os.listdir(input_dir) if file.endswith('.json')]
