# -*- coding: utf-8 -*-
"""
Script to get the magnitude statistics per observatories per dynamic class
"""


import urllib
import numpy as np
from pathlib import Path


obs_code_list=list()
magn_bands_list=list()
correction_bands_list=list()

# subpath=list()
RMS_master_path='Surveys\\'
subpath=["TNO","MBA","NEA"]


headline="magn.     Res RA     Res DEC    Obs per magn.   \n"


File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for linea_surveys in file_surveys:
        obs_code_list.append(linea_surveys[0:3])
finally:
    file_surveys.close()
    
    
File_band="Mangitude_band_correction.txt"   #File containing the magnitude band correction to reference to V-band

file_bands=open(File_band,'r')
try:
    for i,linea_band in enumerate(file_bands):
        if i>0:
            magn_bands_list.append(linea_band.split()[0])
            correction_bands_list.append(float(linea_band.split()[1]))
finally:
        file_bands.close()





magnitude_vector=np.arange(10,24,0.4)
    

    
for folder in subpath:
    for obs in obs_code_list:
        
        
        
        path_observ_details_data=RMS_master_path+folder+'\\'+obs      #                 
        Path(path_observ_details_data).mkdir(parents=True, exist_ok=True)
    
    

        
        with open(path_observ_details_data +'\\'+ obs + "_magnitude_statistics.txt", 'w') as f_res:
                     f_res.write(headline)
                     f_res.close()
    
        
    
       
    
        File_dat=RMS_master_path + folder +"\\"+ obs + ".txt"
        
        
        f = open(File_dat, 'r')
        
       
        
        vec_magn=list()
        vec_res_RA=list()
        vec_res_DEC=list()
        
        
        try:
             
             line_origin=0;
             for linea in f:
                 
                 if line_origin>0:
                     
                     magn_val=float(linea[17:24])
                     
                     if magn_val !=0:
                         
                         #Magnitude band "debiasing"
                         magn_band=linea[54]
                         if magn_band==" ":
                             magn_band="blank"
                         
                         for indice_band, band_data in enumerate(magn_bands_list):
                             if magn_band==band_data:
                                 magn_val+=correction_bands_list[indice_band]
                                 break
                         
                         
                         
                         
                         
                     
                         vec_magn.append( min(magnitude_vector, key=lambda x:abs(x-magn_val)))
                         vec_res_DEC.append(float(linea[35:43]))
                         vec_res_RA.append(float(linea[25:33]))
                     
                 line_origin=line_origin+1
              
        finally:
            if f is not None:
               f.close()
               
               
        print(len(vec_res_DEC))
        
        vec_res_DEC_sorted=[x for _,x in sorted(zip(vec_magn,vec_res_DEC),reverse=True)]
        vec_res_RA_sorted=[x for _,x in sorted(zip(vec_magn,vec_res_RA),reverse=True)]
        vec_magn_sorted=sorted(vec_magn,reverse=True)
        
        
        
        
        magn_res=0;
        
        for i, magn_vettore in enumerate(vec_magn_sorted):
            
            if i==0:
                magn_res=magn_vettore;
                compute_res_DEC=list();
                compute_res_RA=list();
                obs_per_magn=0;
                
            if magn_vettore==magn_res:
                compute_res_DEC.append(vec_res_DEC_sorted[i])
                compute_res_RA.append(vec_res_RA_sorted[i])
                obs_per_magn=obs_per_magn+1;
                
            elif magn_vettore is not magn_res:
               
                rms_DEC = np.sqrt(np.mean(np.array(compute_res_DEC)**2))
                rms_RA = np.sqrt(np.mean(np.array(compute_res_RA)**2))
            
                with open(path_observ_details_data +'\\'+ obs + "_magnitude_statistics.txt", 'a') as f_res:
                             f_res.write(("{: .2f}        {: .4f}      {: .4f}       {:d}\n").format(magn_res, rms_RA, rms_DEC, obs_per_magn))
                             f_res.close()
            
                
                compute_res_DEC=list();
                compute_res_RA=list();
                
                obs_per_magn=1;
                
                compute_res_DEC.append(vec_res_DEC_sorted[i])
                compute_res_RA.append(vec_res_RA_sorted[i])
                
                magn_res=magn_vettore
                
                
                
            if i==len(vec_magn_sorted)-1:
                     rms_DEC = np.sqrt(np.mean(np.array(compute_res_DEC)**2))
                     rms_RA = np.sqrt(np.mean(np.array(compute_res_RA)**2))
                 
                     with open(path_observ_details_data +'\\'+ obs + "_magnitude_statistics.txt", 'a') as f_res:
                                  f_res.write(("{: .2f}        {: .4f}      {: .4f}       {:d}\n").format(magn_res, rms_RA, rms_DEC, obs_per_magn))
                                  f_res.close()
            
            
            
            

                
        
        
        