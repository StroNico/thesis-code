# -*- coding: utf-8 -*-
"""
Script to collect the observation data per observatory per class (RA_res, DEC_res, magnitude, catalog, year of obs...) 
from the online NEOCC database using their API
"""

import urllib
import urllib.request 
import os
import time
from pathlib import Path
import math

    ######    USEFUL FUNCTIONS
    
def Julianday_greg(D,M,Y):
        a=math.floor((14-M)/12);
        y=Y+4800-a;
        m=M+12*a-3;
    
        return D+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-math.floor(y/100)+math.floor(y/400)-32045;
    
    
    
def progress_check(line):
        if line>line_start:
            perc_complete=(line-line_start)*100/search_gap
            if (perc_complete/8).is_integer():
              print("{} % complete...".format(perc_complete))

RMS_master_path='Surveys\\'

databaseFile="MPCORB_01_2023.dat"
obs_code_list=list()


Path_MBA=RMS_master_path+'MBA\\';
Path(Path_MBA).mkdir(parents=True, exist_ok=True)

Path_NEA=RMS_master_path+'NEA\\';
Path(Path_NEA).mkdir(parents=True, exist_ok=True)

Path_TNO=RMS_master_path+'TNO\\';
Path(Path_TNO).mkdir(parents=True, exist_ok=True)



File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for line_surveys in file_surveys:
        obs_code_list.append(line_surveys[0:3])
finally:
    file_surveys.close()
    
# print(obs_code_list)



####Generic constants

line_start=43   #Line of Ceres
line_origin=line_start


while line_origin  <  587517:  #Size of MPCORB.dat file  
    Data_File=open(databaseFile)
    line_start=line_origin
    search_gap=587517-line_start  #One can break the process, to prevent connection errors with the servers
    line_start_eff=line_start-1
    linea_fine=line_start+search_gap
    q_NEA=1.3 #au
    q_TNO=30 #au
    q_MBA_in=1.78 #au
    q_MBA_out=5  #au
    Num_asteroids=0;
    Num_observations=0;
    

    
    
    ###### GENERATE THE FOLDERS AND FILES
    
    Headline="Year       JD      Mag    Res RA    Res DEC   Cat     Mag Band\n"
    
    
    for oss in obs_code_list:
    
    
            with open(Path_MBA+oss+".txt", 'w') as f_a:
                f_a.write(Headline)
                f_a.close()
               
            with open(Path_NEA+oss+".txt", 'w') as f_b:
                f_b.write(Headline)
                f_b.close()
    
            with open(Path_TNO+oss+".txt", 'w') as f_c:
                f_c.write(Headline)
                f_c.close()
    
    
    
    # Path("LINES_SEARCHED").mkdir(parents=True, exist_ok=True)
    
    # cartella="LINES_SEARCHED\\{}-{}"
    # path_saving = cartella.format(line_start,linea_fine)
     
    # try:
    #     os.mkdir(path_saving)
    # except OSError:
    #     print ("Creation of the directory %s failed" % path_saving)
    #     Data_File.close()
    # else:
    
    start=time.time()
        
        
    line_origin=0;
    for x in Data_File:
           
            if line_origin > linea_fine:
                break
            if line_origin > line_start_eff:
               
                #SORT DYNAMIC CLASS ON PERIHELION
                
                q= float(x[92:102]) * (1- float(x[70:79]))
                # print(x[123:127])
                saving=0;
                if float(x[123:127])>2:
                    
                    if q < q_NEA:
                        path_saving=Path_NEA
                        saving=1
                        
                    if q > q_TNO:
                        path_saving=Path_TNO
                        # saving=1;
                        
                        
                    if q > q_MBA_in and q < q_MBA_out:
                        path_saving=Path_MBA
                        saving=1;
                        
               
                
             
                   
                if saving==1:
                    
                  Num_asteroids= Num_asteroids+1; 
                   
                  #Access the NEOCC online databse thorough their API
                  
                  AstName_long=x[166:193]
                  AstName_stripped=AstName_long.strip()
                  AstName=AstName_stripped.replace("(","").replace(" ","").replace(")"," ")
                  AstName_url=AstName.replace(" ","%20").replace("-","").replace("'","%27").replace("`","").replace("|","%7C")
                    #print(AstName)
                  url="https://neo.ssa.esa.int/PSDB-portlet/download?file={}.rwo"
                  
                  RWOName=url.format(AstName_url)
                  fileRWO_Ast = urllib.request.urlopen(RWOName,timeout=400)
                   
                  for j, line in enumerate(fileRWO_Ast):
                    
                    
                    if j>6:
                        
                       
                        decoded_line = line.decode("utf-8")
                        
                        if decoded_line[0]=='!':
                            break
                        
                        if decoded_line[180:183] in obs_code_list:
                        
                            if int(decoded_line[194])==1:
                                year=(int(decoded_line[17:21]))    # saving observation year
                                month=int(decoded_line[22:24])
                                day=int(decoded_line[25:27])
                                
                                JD=Julianday_greg(day,month,year)
                                
                                
                                res_RA=float(decoded_line[95:102])
                                res_DEC=float(decoded_line[148:155])
                                
                                if  not decoded_line[156:159].strip():
                                    Mag=0.0
                                else: 
                                    Mag=float(decoded_line[156:160])
                                
                                Cat=decoded_line[178]
                                
                                Mag_band=decoded_line[161]
                                
                                Num_observations=Num_observations+1;
                                # Each observation is saved in the observatory/dynamic class reference file
                                with open(path_saving+decoded_line[180:183]+".txt",'a') as Data_saved:
                                   Data_saved.write(("{}    {}   {:04.1f}   {: .3f}    {: .3f}      {}      {}\n").format(
                                    year,JD,Mag,res_RA,res_DEC,Cat,Mag_band))
                                   Data_saved.close()
                                    
                                    
                    
        
            progress_check(line_origin)    
                
                
                
            line_origin=line_origin+1
        
    
    
    
    Data_File.close()
        
    end=time.time()
    print(("Total duration = {}").format(end-start))
    print(("Time per asteroid = {}").format(((end-start)/search_gap)))


