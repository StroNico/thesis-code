# -*- coding: utf-8 -*-
"""
This code provides the global RMS of residual per each observatory (listed in file considered_surveys.txt) per asteroid class.
"""

import urllib
import urllib.request 
import os
import time
from pathlib import Path
import math
import numpy as np



obs_code_list=list()

# subpath=list()
RMS_master_path='Surveys\\'
subpath=["TNO","MBA","NEA"]


Headline="Oss     Res RA     Res DEC    \n"



File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for line_surveys in file_surveys:
        obs_code_list.append(line_surveys[0:3])
finally:
    file_surveys.close()


for folder in subpath:
    
    # QUA CREIAMO IL FILE RESULTS_MBA/NEA/TNO
    with open(RMS_master_path + folder +"\\"+folder+"_results.txt", 'w') as f_res:
                 f_res.write(Headline)
                 f_res.close()
    
    
    
    for oss in obs_code_list:
        File_dat=RMS_master_path + folder +"\\"+ oss + ".txt"
        
        
        f = open(File_dat, 'r')
        vec_res_RA=list()
        vec_res_DEC=list()
        try:
             # do stuff with f
             line_origin=0;
             for linea in f:
                 
                 if line_origin>0:
                     vec_res_DEC.append(float(linea[35:43]))
                     vec_res_RA.append(float(linea[25:33]))
                     
                 line_origin=line_origin+1
              
        finally:
            if f is not None:
               f.close()
        
        print(len(vec_res_DEC))
        if len(vec_res_DEC)>0:
          rms_DEC = np.sqrt(np.mean(np.array(vec_res_DEC)**2))
          rms_RA = np.sqrt(np.mean(np.array(vec_res_RA)**2))
        else:
          rms_DEC=0
          rms_RA=0
        
        with open(RMS_master_path + folder +"\\"+folder+"_results.txt", 'a') as f_res:
                     f_res.write((oss+"    {: .3f}      {: .3f}  \n").format(rms_RA, rms_DEC))
                     f_res.close()
        
        
        
        
        
        
        
        
        
        