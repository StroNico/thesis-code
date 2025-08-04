# -*- coding: utf-8 -*-
"""
To count the number of observations listed per each catalog per asteroid class
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


new_headline="Cat    n obs    \n"



File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for line_surveys in file_surveys:
        obs_code_list.append(line_surveys[0:3])
finally:
    file_surveys.close()


for folder in subpath:
    
 
    with open(RMS_master_path + folder +"\\"+folder+"_n_obs_cat.txt", 'w') as f_res:
                  # f_res.write(new_headline)
                  f_res.close()
    
    
    vec_catalog=list()
    for obs in obs_code_list:
        File_dat=RMS_master_path + folder +"\\"+ obs + ".txt"
        
        
        f = open(File_dat, 'r')
        
        # vec_res_RA=list()
        # vec_res_DEC=list()
        try:
             
             line_origin=0;
             for linea in f:
                 
                 if line_origin>0:
                     vec_catalog.append((linea[47]))
                 
            
                     
                 line_origin=line_origin+1
              
        finally:
            if f is not None:
               f.close()
        
        print(line_origin-1)
        
    vec_catalog_sorted=sorted(vec_catalog,reverse=True)
       
    catalog_res='0';
        
    for i, catalog_array in enumerate(vec_catalog_sorted):
            if i==0:
                catalog_res=catalog_array;
        
                obs_per_cat=0;
            
            if catalog_array==catalog_res:
            
                obs_per_cat=obs_per_cat+1;
            
            elif catalog_array is not catalog_res:
            
                with open(RMS_master_path + folder +"\\"+folder+"_n_obs_cat.txt", 'a') as f_res:
                             f_res.write((catalog_res+"     {:d}\n").format( obs_per_cat))
                             f_res.close()
            
            
                obs_per_cat=1;
                
                catalog_res=catalog_array
                
                
    if i==len(vec_catalog_sorted)-1:     
                with open(RMS_master_path + folder +"\\"+folder+"_n_obs_cat.txt", 'a') as f_res:
        
                    f_res.write((catalog_res+"     {:d}\n").format( obs_per_cat))
                    f_res.close()
    
        
    
    cat_list=list()
    cat_num_list=list()
    
    file_cat = open(RMS_master_path + folder +"\\"+folder+"_n_obs_cat.txt", 'r')
    try:
          for linea_cat in file_cat:
              cat_list.append(linea_cat[0])
              cat_num_list.append(int(linea_cat[4:-1]))
             
            
    finally:
          file_surveys.close()   
         
         
    cat_num_list_sorted=sorted(cat_num_list,reverse=True)     
    cat_list_sorted=[x for _,x in sorted(zip(cat_num_list,cat_list),reverse=True)]
         
    with open(RMS_master_path + folder +"\\"+folder+"_n_obs_cat_sorted.txt", 'w') as f_res:
                  f_res.write(new_headline)
                  f_res.close()
                 
    for i,cat_sortato in enumerate(cat_list_sorted):
        
        with open(RMS_master_path + folder +"\\"+folder+"_n_obs_cat_sorted.txt", 'a') as f_res:

            f_res.write((cat_sortato+"     {:d}\n").format( cat_num_list_sorted[i]))
            f_res.close()
    
    
    
    
    
    
        # with open(RMS_master_path + folder +"\\"+folder+"_n_obs.txt", 'a') as f_res:
        #              f_res.write((obs+"    {:d} \n").format(line_origin-1))
        #              f_res.close()
        
        
        
        
        
        
        
        
        
        