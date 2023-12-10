


# Tool package for POLYMER


import netCDF4 as nc4
import ast
import numpy as np
import datetime as dt



# Get datetime object 
def get_datetime(sat_file):
    with nc4.Dataset(sat_file,"r") as nc:
        
        datetime_sat_string = nc.getncattr('sensing_time')
        datetime_sat_obj = dt.datetime.strptime(datetime_sat_string, '%Y-%m-%d %H:%M:%S')
    
    return datetime_sat_obj
    
    



def read_file(sat_file):
    
    with nc4.Dataset(sat_file,"r") as nc:
        sensor = nc.getncattr('sensor')
        
        # wavelengths 
        bands = nc.getncattr('bands_rw')
        bands = ast.literal_eval(bands)
        
        # band names 
        band_names = ['Rw' + str(item) for item in bands]

        # dimension
        width = len(nc.dimensions['width']) # equivalent to 'pixels' before 
        height = len(nc.dimensions['height']) # equivalent to 'lines' before 


        lat = nc.variables['latitude'][:,:]
        lon = nc.variables['longitude'][:,:]


        # to store data
        rhow_data = np.ma.empty([len(bands),int(height),int(width)])


        for k in range(len(bands)):
            varname = band_names[k]
            
            rhow_data[k] = nc.variables[varname][:,:]
            
    return {'bands': band_names,
            'width': width,
            'height': height,
            'lat': lat,
            'lon': lon,
            'rhow_data': rhow_data}


    ### What we need: width, height, lat, lon, rhow_data





















