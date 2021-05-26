#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geoedfframework.utils.GeoEDFError import GeoEDFError
from geoedfframework.GeoEDFPlugin import GeoEDFPlugin

import requests
import os

""" Module for implementing the WQP input connector plugin. WQP (Water Quality Portal)
    is a public web service (REST API) operated by the US EPA and USGS.
    This module will implement the get() method required for all input plugins.
"""

class WQPInput(GeoEDFPlugin):

    base_url = "https://www.waterqualitydata.us/data"
    target_path = "data"
 
    ##TODO: 
    #       Make site_id conditionally required -- one and only one of the following:  site_id, bBox, state, county, huc
    #       Use LocationFilter to generate bBox given proper combination of lat, lon, radius, width, length, min/max_lat, min/max_lon, polygon, shapefile 
    #       Some params may be lists
    __required_params = ['site_id']
    __optional_params = ['start_date','end_date','bBox','state','county','organization','huc']

    # we use just kwargs since we need to be able to process the list of attributes
    # and their values to create the dependency graph in the GeoEDFInput super class
    def __init__(self, **kwargs):

        # list to hold all the parameter names; will be accessed in super to
        # construct dependency graph
        self.provided_params = self.__required_params + self.__optional_params

        # check that all required params have been provided
        for param in self.__required_params:
            if param not in kwargs:
                raise GeoEDFError('Required parameter %s for WQPInput not provided' % param)

	# specific check for conditioal required params

        # set all required parameters
        for key in self.__required_params:
            setattr(self,key,kwargs.get(key))

        # set optional parameters
        for key in self.__optional_params:
            # if key not provided in optional arguments, defaults value to None
            setattr(self,key,kwargs.get(key,None))

        # set defaults if none provided
        if (self.start_date is None):
            self.start_date = ''
        if (self.end_date is None):
            self.end_date = '05-01-2020'

        # class super class init
        super().__init__()

    # each Input plugin needs to implement this method
    # if error, raise exception; if not, return True

    def get(self):

        # build URL for REST API call
        wqp_url = self.base_url+"/Result/search?siteid="+self.site_id+"&StartDateLo="+self.start_date+"&StartDateHi="+self.end_date+"&mimeType=csv"

        try:
            # do REST API GET call
            results = requests.get(url=wqp_url, stream=True)
            # target_path is (re)set by the connector input instantiation
            out_path = '%s/%s.csv' % (self.target_path,self.site_id)
            with open(out_path,'wb') as out_file:
                for chunk in results.iter_content(chunk_size=1024*1024):
                    out_file.write(chunk)
        except GeoEDFError:
            raise
        except:
            raise