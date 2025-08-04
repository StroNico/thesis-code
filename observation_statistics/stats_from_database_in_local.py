# -*- coding: utf-8 -*-
"""
Script to collect the observation data per observatory per class (RA_res, DEC_res, magnitude, catalog, year of obs...) 
from an observations database saved in local hard drive
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
        if line>linea_inizio:
            perc_complete=(line-linea_inizio)*100/search_gap
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

######## PRIMA DI TUTTO GENERIAMO LA LISTA DI OSSERVATORI AFFIDABILI

File_obs="considered_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for linea_surveys in file_surveys:
        obs_code_list.append(linea_surveys[0:3])
finally:
    file_surveys.close()
    



# DATABASE FOLDER

local_database_folder="Your_Database_folder"







Data_File=open(databaseFile)

# Generic constants

linea_inizio= 43
search_gap=1264449-43
linea_inizio_eff=linea_inizio-1
linea_fine=linea_inizio+search_gap

q_NEA=1.3 #au
q_TNO=30 #au
q_MBA_in=1.78 #au
q_MBA_out=5  #au
Num_asteroids=0;
Num_observations=0;


##### CREATE FOLDERS AND FILES

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
# path_saving = cartella.format(linea_inizio,linea_fine)
 
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
        if line_origin > linea_inizio_eff:
            
           #SORT THE CLASS BASED ON PERIHELION
            
            q= float(x[92:102]) * (1- float(x[70:79]))
            # print(x[123:127])
            saving_flag=0;
            if float(x[123:127])>2:
                
                if q < q_NEA:
                    path_saving=Path_NEA
                    saving_flag=1
                    
                if q > q_TNO:
                    path_saving=Path_TNO
                    saving_flag=1;
                    
                    
                if q > q_MBA_in and q < q_MBA_out:
                    path_saving=Path_MBA
                    saving_flag=1;
                    
           
    
               
            if saving_flag==1:
                
             # Finding the file in the format it is saved in the local database, provided by NEOCC upon request
                
              Num_asteroids= Num_asteroids+1; 
              
              AstNum_string=((x[166:174]).strip()).replace("(","").replace(")","")
              
              if not AstNum_string == "":
                  
                  #The asteroid is numbered, we get the number, from it the name of the folder, of the file, and the rwo itself
                  
                  AstNum=int(AstNum_string)
                  
                  Ast_folder=math.floor(AstNum/1000)
                  
                  Ast_fileName=(local_database_folder+"numbered\\{:04d}\\{}.rwo").format(Ast_folder,AstNum)
              
              else:
                  
                  AstName=((x[166:193]).strip()).replace(" ","")
                  
                  if "P-L" in AstName:
                      #So ther directory is unnumbered//unusual
                  
                      Ast_fileName=local_database_folder+"unnumbered\\unusual\\P-L\\"+AstName+".rwo"
                      
                  else:
                      
                      #We must take the firs 5 digits of AstName
                      Ast_folder=AstName[0:5]
                      
                      Ast_fileName=local_database_folder+"unnumbered\\"+Ast_folder+"\\"+AstName+".rwo"
              
              
              
             
                
              # Now we have to gain access to the rwo files in the database
                

              try:
                  rwo_file=open( Ast_fileName, 'r')

                  for j, line in enumerate(rwo_file):
                    
                    
                    if j>6:
                        
                       
                        decoded_line = line        
                        
                        if decoded_line[0]=='!':
                            break
                        
                        if decoded_line[180:183] in obs_code_list:
                        
                            if int(decoded_line[194])==1:
                                year=(int(decoded_line[17:21]))    # saving year of observation
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
                               
                                with open(path_saving+decoded_line[180:183]+".txt",'a') as Data_saved:
                                   Data_saved.write(("{}    {}   {:04.1f}   {: .3f}    {: .3f}      {}      {}\n").format(
                                    year,JD,Mag,res_RA,res_DEC,Cat,Mag_band))
                                   Data_saved.close()
                                    
                  
                  rwo_file.close()              
                                
              except:
                  print(Ast_fileName+" not found")
                                
                            
    
        progress_check(line_origin)    
            
            
            
        line_origin=line_origin+1
    



Data_File.close()
    
end=time.time()
print(("Total duration = {}").format(end-start))
print(("Time per asteroid = {}").format(((end-start)/search_gap)))


