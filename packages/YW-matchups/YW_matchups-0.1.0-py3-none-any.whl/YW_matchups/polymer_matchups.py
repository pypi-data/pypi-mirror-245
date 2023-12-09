#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 19:02:47 2023

@author: yw
"""



'''set up environment 

conda create --name YW_matchup python=3.9

conda activate YW_matchup

conda install -c conda-forge numpy pandas matplotlib netCDF4 pyproj


'''





import netCDF4 as nc4
import numpy as np
#import scipy
#import geopy.distance as gp
import sys
import glob, os
import pyproj
import datetime as dt
import pandas as pd
import ast



'''

# If there are any matching records, import satellite data.
with nc4.Dataset(sat_file,"r") as nc:
    sensor = nc.getncattr('sensor')
    
    # wavelengths 
    bands = nc.getncattr('bands_rw')
    bands = ast.literal_eval(bands)

    # dimension
    width = len(nc.dimensions['width']) # equivalent to 'pixels' before 
    height = len(nc.dimensions['height']) # equivalent to 'lines' before 


    lat = nc.variables['latitude'][:,:]
    lon = nc.variables['longitude'][:,:]


    # to store data
    rhow_data = np.empty([len(bands),int(height),int(width)])


    for k in list(range(len(bands))):
        varname = 'Rw' + str(bands[k])
        
        rhow_data[k] = nc.variables[varname][:,:]



'''


























