



# find matchups 



# Strategy: throw everything here, put them into modules if too long or when necessary 


import numpy as np
import sys
import glob, os
import pyproj
import datetime as dt
import pandas as pd
import time
from . import AC_polymer







# Find all required NC files under sat_folder

def run(sat_folder=None, is_file=None, AC=None, out_file=None):
    
    
    ### Settings to be included later 
    time_window_minutes = 360
    
    # make it adaptive to sensor resolution 
    window_size = 3
    
    max_dist = 100
    
    
    
    ### Print all metadata/settings and save them in a txt file
    
    
    # Start logging in txt file
    orig_stdout = sys.stdout
    
    
    log_file = out_file.replace(".csv", ".txt")
    
    # log_file = 'tmart_log_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.txt'


    class Logger:
        def __init__(self, filename):
            self.console = sys.stdout
            self.file = open(filename, 'w')
            self.file.flush()
        def write(self, message):
            self.console.write(message)
            self.file.write(message)
        def flush(self):
            self.console.flush()
            self.file.flush()

    sys.stdout = Logger(log_file)
    
    
    
    
    
    # Metadata
    print('sat_folder: ' + str(sat_folder))
    
    print('System time: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print('sat_folder: ' + str(sat_folder))
    print('In-situ file: ' + str(is_file))
    print('AC: ' + str(AC))
    print('out_file: ' + str(out_file))
    print('log_file: ' + str(log_file))
 
    

    
    

    
    # Read in-situ data 
    df_is = pd.read_csv(is_file)
    dt_is_string = list(df_is.loc[:,"GLORIA_time"])
    dt_is_obj = [dt.datetime.strptime(dt_is_string[d],"%Y-%m-%dT%H:%M")for d in list(range(len(dt_is_string)))]
    
    
    
    
    ### find all NC files 
    
    # Keywords for .nc files 
    if AC=='POLYMER': 
        AC_file = '*.nc'
    elif AC=='ACOLITE':
        AC_file = '*L2W.nc'
    else: 
        sys.exit('Unknown AC algorithm')
    
    # Find them in the directory and subdirectory 
    # https://stackoverflow.com/questions/18394147/how-to-do-a-recursive-sub-folder-search-and-return-files-in-a-list
    sat_files = [y for x in os.walk(sat_folder) for y in glob.glob(os.path.join(x[0], AC_file))]
    
    
    
    ### Loop through each of the sat_files
    
        
    for sat_file in sat_files: 
        
        print('\nProcessing: {}'.format(sat_file))
        
        
        # for different AC!!! 
        dt_sat_obj = AC_polymer.get_datetime(sat_file)
        
        
        # The indices of in-situ data that match the sat datetime  
        is_matches = [ind for ind, s in enumerate(dt_is_obj) if abs((dt_sat_obj - s).total_seconds()/60) <= time_window_minutes]
        
        
        # If there are no matching records, skip to next satellite file.
        if len(is_matches)==0:
            print("No matches for this file within the time limit. Next...\n\n")
            continue
        elif len(is_matches) > 1:
            print('Number of matchups: ' + str(len(is_matches)))
        
        
        
        
        # If there are no matching records, skip to next satellite file.
        
        # for different AC!!! 
        sat_data = AC_polymer.read_file(sat_file)
        
        
        
        ### Loop through each of in-situ matchups, indices and row number 
        for ind, row in enumerate(is_matches):
            print('Processing in-situ match {}, row {} in spreadsheet'.format(ind, row))
            
            
            ### Identify distance 
            
            in_situ_lat = df_is.loc[row,"lat"]
            in_situ_lon = df_is.loc[row,"lon"]
            
            # Project X and Y in meters, centred at the in-situ measurement 
            proj = pyproj.Proj(proj="gnom", ellps="WGS84", lat_0=in_situ_lat,
                               lon_0=in_situ_lon, datum="WGS84", units="m")
            x, y = proj(sat_data['lon'], sat_data['lat'])
            in_situ_x, in_situ_y = proj(in_situ_lon, in_situ_lat)
            

            # Calculate distance and indices of the closest 
            dist = np.sqrt((x - in_situ_x)**2 + (y - in_situ_y)**2)
            
            
            # Pixels within the max distance, True/False
            within_max_dist = dist < max_dist
            
            # Are there any valid pixels left?
            if np.sum(within_max_dist)==0:
                print("No pixels within acceptable distance (",max_dist,"m ). Next...\n")
                continue
            
            
            indices_closest = np.argwhere(dist == np.min(dist))
            
            line = indices_closest[0][0]
            pixel = indices_closest[0][1]
            
            
            # Get pixel coordinates of window around the matching point.
            # (v = vertical/line, h = horizontal/pixel)
            v1 = np.int32(line - ((window_size-1)/2))
            v2 = np.int32(line + ((window_size+1)/2))
            h1 = np.int32(pixel - ((window_size-1)/2))
            h2 = np.int32(pixel + ((window_size+1)/2))
            
            # Trim edges of window if they're on the edge of the grid.
            line_start,line_end = max(0, v1), min(sat_data['height'], v2)
            # Window pixel start, pixel end.
            pixel_start,pixel_end = max(0, h1), min(sat_data['width'], h2)
            
            # Extract all values in this window
            rhow_data_window = sat_data['rhow_data'][:,line_start:line_end,pixel_start:pixel_end]
            
            
            # Mean values per band 
            rhow_data_mean = np.nanmean(rhow_data_window, axis=(1,2))
            
            if rhow_data_mean.mask.all(): 
                print('No water pixels found.')
                continue
            
            df_is.loc[row, sat_data['bands']] = rhow_data_mean
            


    
    # Stop logging 
    sys.stdout = orig_stdout


    return df_is
    
    
    
    
    
    
    
    
    
    
    
    
    










