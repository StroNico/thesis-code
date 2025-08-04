# -*- coding: utf-8 -*-
"""
It provides the RMS statitics per catalog per asteroid class per observatory
"""
#Qui prendiamo tutti gli osservatori, prendiamo i file dentro le sottocartelle, creiamo la folder dell'osservatorio 

import urllib
import numpy as np
from pathlib import Path


obs_code_list=list()

# subpath=list()
RMS_master_path='Surveys\\'
subpath=["TNO","MBA","NEA"]


New_headline="Cat.     Res RA     Res DEC    Obs per cat.   \n"


File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for linea_surveys in file_surveys:
        obs_code_list.append(linea_surveys[0:3])
finally:
    file_surveys.close()
    
    
    
for folder in subpath:
    for oss in obs_code_list:
        

        
        path_observ_details_data=RMS_master_path+folder+'\\'+oss      #                      
        Path(path_observ_details_data).mkdir(parents=True, exist_ok=True)
    
    
     
        
        with open(path_observ_details_data +'\\'+ oss + "_catalog_statistics.txt", 'w') as f_res:
                     f_res.write(New_headline)
                     f_res.close()
    
        
    
      
    
        File_dat=RMS_master_path + folder +"\\"+ oss + ".txt"
        
        
        f = open(File_dat, 'r')
        
     
        
        vec_catalog=list()
        vec_res_RA=list()
        vec_res_DEC=list()
        
        
        try:
             
             line_origin=0;
             for linea in f:
                 
                 if line_origin>0:
                     vec_catalog.append((linea[47]))
                     vec_res_DEC.append(float(linea[35:43]))
                     vec_res_RA.append(float(linea[25:33]))
                     
                 line_origin=line_origin+1
              
        finally:
            if f is not None:
               f.close()
               
               
        print(len(vec_res_DEC))
        
        vec_res_DEC_sorted=[x for _,x in sorted(zip(vec_catalog,vec_res_DEC),reverse=True)]
        vec_res_RA_sorted=[x for _,x in sorted(zip(vec_catalog,vec_res_RA),reverse=True)]
        vec_catalog_sorted=sorted(vec_catalog,reverse=True)
        
        
       
        
        catalogo_res='0';
        
        for i, catalogo_vettore in enumerate(vec_catalog_sorted):
            
            if i==0:
                catalogo_res=catalogo_vettore;
                calcolo_res_DEC=list();
                calcolo_res_RA=list();
                obs_per_cat=0;
                
            if catalogo_vettore==catalogo_res:
                calcolo_res_DEC.append(vec_res_DEC_sorted[i])
                calcolo_res_RA.append(vec_res_RA_sorted[i])
                obs_per_cat=obs_per_cat+1;
                
            elif catalogo_vettore is not catalogo_res:
               
                
                rms_DEC = np.sqrt(np.mean(np.array(calcolo_res_DEC)**2))
                rms_RA = np.sqrt(np.mean(np.array(calcolo_res_RA)**2))
            
                with open(path_observ_details_data +'\\'+ oss + "_catalog_statistics.txt", 'a') as f_res:
                             f_res.write((catalogo_res+"        {: .3f}      {: .3f}       {:d}\n").format( rms_RA, rms_DEC, obs_per_cat))
                             f_res.close()
            
                
                calcolo_res_DEC=list();
                calcolo_res_RA=list();
                
                obs_per_cat=1;
                
                calcolo_res_DEC.append(vec_res_DEC_sorted[i])
                calcolo_res_RA.append(vec_res_RA_sorted[i])
                
                catalogo_res=catalogo_vettore
                
              
                
            if i==len(vec_catalog_sorted)-1:
                     rms_DEC = np.sqrt(np.mean(np.array(calcolo_res_DEC)**2))
                     rms_RA = np.sqrt(np.mean(np.array(calcolo_res_RA)**2))
                 
                     with open(path_observ_details_data +'\\'+ oss + "_catalog_statistics.txt", 'a') as f_res:
                                  f_res.write((catalogo_res+"        {: .3f}      {: .3f}       {:d}\n").format( rms_RA, rms_DEC, obs_per_cat))
                                  f_res.close()
            
            
            
            

                
        
        
        