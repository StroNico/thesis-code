# -*- coding: utf-8 -*-
"""
Generates the RMS statistics per year, per class, per observatory
"""


import urllib
import numpy as np
from pathlib import Path


obs_code_list=list()

# subpath=list()
RMS_master_path='Surveys\\'
subpath=["TNO","MBA","NEA"]


new_headline="Year     Res RA     Res DEC    Obs per year   \n"


File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for linea_surveys in file_surveys:
        obs_code_list.append(linea_surveys[0:3])
finally:
    file_surveys.close()
    
    
    
for folder in subpath:
    for obs in obs_code_list:
        
        
        
        path_observ_details_data=RMS_master_path+folder+'\\'+obs      #                     
        Path(path_observ_details_data).mkdir(parents=True, exist_ok=True)
    
    
       
        
        with open(path_observ_details_data +'\\'+ obs + "_year_statistics.txt", 'w') as f_res:
                     f_res.write(new_headline)
                     f_res.close()
    
        
    
       
    
        File_dat=RMS_master_path + folder +"\\"+ obs + ".txt"
        
        
        f = open(File_dat, 'r')
        
      
        
        vec_year=list()
        vec_res_RA=list()
        vec_res_DEC=list()
        
        
        try:
            
             line_origin=0;
             for linea in f:
                 
                 if line_origin>0:
                     vec_year.append(int(linea[0:5]))
                     vec_res_DEC.append(float(linea[35:43]))
                     vec_res_RA.append(float(linea[25:33]))
                     
                 line_origin=line_origin+1
              
        finally:
            if f is not None:
               f.close()
               
               
        print(len(vec_res_DEC))
        
        vec_res_DEC_sorted=[x for _,x in sorted(zip(vec_year,vec_res_DEC),reverse=True)]
        vec_res_RA_sorted=[x for _,x in sorted(zip(vec_year,vec_res_RA),reverse=True)]
        vec_year_sorted=sorted(vec_year,reverse=True)
        
        
       
        
        year_res=0;
        
        for i, year_array in enumerate(vec_year_sorted):
            
            if i==0:
                year_res=year_array;
                compute_res_DEC=list();
                compute_res_RA=list();
                obs_per_year=0;
                
            if year_array==year_res:
                compute_res_DEC.append(vec_res_DEC_sorted[i])
                compute_res_RA.append(vec_res_RA_sorted[i])
                obs_per_year=obs_per_year+1;
                
            elif year_array is not year_res:
                
                
                rms_DEC = np.sqrt(np.mean(np.array(compute_res_DEC)**2))
                rms_RA = np.sqrt(np.mean(np.array(compute_res_RA)**2))
            
                with open(path_observ_details_data +'\\'+ obs + "_year_statistics.txt", 'a') as f_res:
                             f_res.write(("{:d}    {: .3f}      {: .3f}       {:d}\n").format(year_res, rms_RA, rms_DEC, obs_per_year))
                             f_res.close()
            
                
                compute_res_DEC=list();
                compute_res_RA=list();
                
                obs_per_year=1;
                
                compute_res_DEC.append(vec_res_DEC_sorted[i])
                compute_res_RA.append(vec_res_RA_sorted[i])
                
                year_res=year_array
                
              
                
            if i==len(vec_year_sorted)-1:
                     rms_DEC = np.sqrt(np.mean(np.array(compute_res_DEC)**2))
                     rms_RA = np.sqrt(np.mean(np.array(compute_res_RA)**2))
                 
                     with open(path_observ_details_data +'\\'+ obs + "_year_statistics.txt", 'a') as f_res:
                                  f_res.write(("{:d}    {: .3f}      {: .3f}       {:d}\n").format(year_res, rms_RA, rms_DEC, obs_per_year))
                                  f_res.close()
            
            
            
            

                
        
        
        