# -*- coding: utf-8 -*-
"""
This is the code to generate the histograms related to observatory 691

"""

import urllib
import urllib.request 
import os
import time
from pathlib import Path
import math
import numpy
import matplotlib.pyplot as plt


obs_code_list=list()


RMS_master_path='Surveys\\'
subpath=["TNO","MBA","NEA"]
indice_bins=0;
num_bins=[10,280,120]
year_limit="2004"
year_limit_value=2004
year_limit="2015"
year_limit_value=2015


Linea_da_scrivere="Class      Mean RA     Sigma RA    Mean DEC    Sigma DEC   \n"




with open("Images\\691\\"+year_limit+"\\691_results.txt", 'w') as f_res:
             f_res.write(Linea_da_scrivere)
             f_res.close()
             
             
for folder in subpath:
    

    
    
    
   
    File_dat=RMS_master_path + folder +"\\691.txt"
    
    
    f = open(File_dat, 'r')
    vec_res_RA=list()
    vec_res_DEC=list()
    try:
         # do stuff with f
         line_origin=0;
         for linea in f:
             
             if line_origin>0 and int(linea[0:5])>year_limit_value-1:
                 vec_res_DEC.append(float(linea[35:43]))
                 vec_res_RA.append(float(linea[25:33]))
                 
             line_origin=line_origin+1
          
    finally:
        if f is not None:
           f.close()
    
    print(len(vec_res_DEC))
    if len(vec_res_DEC)>0:
      # rms_DEC = np.sqrt(np.mean(np.array(vec_res_DEC)**2))
      # rms_RA = np.sqrt(np.mean(np.array(vec_res_RA)**2))
      mean_RA=numpy.mean(vec_res_RA)
      mean_DEC=numpy.mean(vec_res_DEC)
      std_RA=numpy.std(vec_res_RA)
      std_DEC=numpy.std(vec_res_DEC)
      
      vec_res_RA=sorted(vec_res_RA,reverse=True)
      
     
      hist, edges = numpy.histogram(
      vec_res_RA,
      bins=num_bins[indice_bins],
      range=(min(vec_res_RA),max(vec_res_RA)),
      density=True)   
      

      
      with open("Images\\691\\"+year_limit+"\\"+folder+"histo.txt", 'w') as f_res:
        f_res.close()
      
      with open("Images\\691\\"+year_limit+"\\"+folder+"histo.txt", 'a') as f_res:
          
                   f_res.write("RA\n\n")
                   for line in hist:
                       f_res.write(("{: .5f}     ").format(line))
                   f_res.write("\n\n")
                   
                   for line in edges:
                       f_res.write(("{: .5f}     ").format(line))
                   f_res.write("\n\n")
                   
                  
                   f_res.close()
      
      
      
      vec_res_DEC=sorted(vec_res_DEC,reverse=True)
      
      hist, edges = numpy.histogram(
      vec_res_DEC,
      bins=num_bins[indice_bins],
      range=(min(vec_res_DEC),max(vec_res_DEC)),
      density=True)   
      
      with open("Images\\691\\"+year_limit+"\\"+folder+"histo.txt", 'a') as f_res:
                   f_res.write("DEC\n\n")
                   for line in hist:
                       f_res.write(("{: .5f}     ").format(line))
                   f_res.write("\n\n")
                   
                   for line in edges:
                       f_res.write(("{: .5f}     ").format(line))
                   f_res.write("\n\n")
                   
                  
                   f_res.close()
      
      

      rms_DEC=0
      rms_RA=0
    
    with open("Images\\691\\"+year_limit+"\\691_results.txt", 'a') as f_res:
                 f_res.write((folder+"       {: .4f}      {: .4f}     {: .4f}      {: .4f}  \n").format(mean_RA, std_RA,mean_DEC, std_DEC))
                 f_res.close()
            
            
            
    indice_bins=indice_bins+1       
            
            
            
            
            
            