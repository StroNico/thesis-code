# -*- coding: utf-8 -*-
"""
Pruning from local database of NEOCC .rwo observation files

"""

import urllib
import urllib.request 
import os
import time
from pathlib import Path
from MD_library import RMS_from_FO
import math
import shutil
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, kstest
from scipy.stats import rankdata



databaseFile="MPCORB_11_2024.dat"



#Definiamo un po' di variabili generali

line_start=  43
search_gap= 1419703 - 43
line_start_eff=line_start-1
line_end=line_start+search_gap
obs_code_list=list()
minimum_year_threshold=2015
reliable_obs_threshold = 0.5
RMSThreshold = 0.838
oppositions_min = 3
line_interval = 1000

min_observ_admitted=20;
weird_tracking=['s','S','r','R','v','V']

asteroid_found_master_path='ASTEROIDS FOUND\\'

''' 
initialisation of some data
'''
one_year_obs = 0
two_years_obs = 0
ast_with_old_obs = 0
low_obs_ast = 0
radar_track_with_identification = 0
radar_tracking = 0
with_identification = 0
unreliable_observatories = 0
low_oppositions = 0

RMSAst_vec = []


######    USEFUL FUNCTIONS

def Julianday_greg(D,M,Y):
    a=math.floor((14-M)/12);
    y=Y+4800-a;
    m=M+12*a-3;

    return D+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-math.floor(y/100)+math.floor(y/400)-32045;

def Save_detail_file(saved_file_path):
    AnomAst_detail = open('%s\\Details_on_asteroids_found.txt' %path_saving,'a');
    Asteroid_Detail_string=AstName+" in "+saved_file_path+"\n";
    AnomAst_detail.write(Asteroid_Detail_string)
    AnomAst_detail.close()


def progress_check(line):
    if line > line_start and (line - line_start) % line_interval == 0:
        perc_complete = (line - line_start) * 100 / search_gap
        print(f"{perc_complete:.1f}% complete...")


Add_string = ""


path_tracking=asteroid_found_master_path+'Radar tracking';
Path(path_tracking).mkdir(parents=True, exist_ok=True)

subpath_track_identif=asteroid_found_master_path+'Radar tracking\\with identification';
Path(subpath_track_identif).mkdir(parents=True, exist_ok=True)

path_identification=asteroid_found_master_path+'Identification'
Path(path_identification).mkdir(parents=True, exist_ok=True)

path_one_year_obs=asteroid_found_master_path+'Obs with 1 opposition'
Path(path_one_year_obs).mkdir(parents=True, exist_ok=True)

path_two_year_obs=asteroid_found_master_path+'Obs with 2 oppositions'
Path(path_two_year_obs).mkdir(parents=True, exist_ok=True)

path_low_n_obs=(asteroid_found_master_path+'Asteroids with less than {} obs').format(min_observ_admitted)
Path(path_low_n_obs).mkdir(parents=True, exist_ok=True)

path_unreliable_obs=(asteroid_found_master_path+'Observations from unreliable obs')
Path(path_unreliable_obs).mkdir(parents=True, exist_ok=True)

path_generic=(asteroid_found_master_path+'Without outstanding features')
Path(path_generic).mkdir(parents=True, exist_ok=True)


path_old_observations=(asteroid_found_master_path+'Files with old observations')
Path(path_old_observations).mkdir(parents=True, exist_ok=True)

subpath_unreliable_track=path_unreliable_obs+'\\Radar tracking';
Path(subpath_unreliable_track).mkdir(parents=True, exist_ok=True)

subsubpath__unreliable_track_identif=subpath_unreliable_track+'\\with identification';
Path(subsubpath__unreliable_track_identif).mkdir(parents=True, exist_ok=True)

subpath_unreliable_identif=path_unreliable_obs+'\\With identification(s)';
Path(subpath_unreliable_identif).mkdir(parents=True, exist_ok=True)

path_unclear = (asteroid_found_master_path+'unclear')
Path(path_unclear).mkdir(parents=True, exist_ok=True)



######## LIST OF RELIBLE SURVEYS

File_obs="reliable_surveys.txt"

file_surveys = open(File_obs, 'r')

try:
    for line_surveys in file_surveys:
        obs_code_list.append(line_surveys[0:3])
finally:
    file_surveys.close()
    
# print(obs_code_list)




Path("LINES_SEARCHED").mkdir(parents=True, exist_ok=True)

cartella="LINES_SEARCHED\\{}-{}"
path_saving = cartella.format(line_start,line_end)
 
try:
    os.mkdir(path_saving)
except OSError:
    print ("Creation of the directory %s failed" % path_saving)
    
    
with open(databaseFile) as Data_File:


    start=time.time()
    
    
    line_origin=0;
    for x in Data_File:
        if line_origin > line_end:
            break
        if line_origin > line_start_eff:
            
            oppositions = int(x[123:127])
            
            
            
            
            AstNum_string=((x[166:174]).strip()).replace("(","").replace(")","")
            
            
            if not AstNum_string == "":
                
                
                AstNum=int(AstNum_string)
                
                Ast_folder=math.floor(AstNum/1000)
                
                Ast_fileName=(local_database_folder+"numbered/{:04d}/{}.rwo").format(Ast_folder,AstNum)
               
                AstName = str(AstNum)
            
            else:
                
                AstName=((x[166:193]).strip()).replace(" ","")
               
                
                if "P-L" in AstName:
            
                
                    Ast_fileName=local_database_folder+"unnumbered/unusual/P-L/"+AstName+".rwo"
                    
                else:
                    
                 
                    Ast_folder=AstName[0:5]
                    
                    Ast_fileName=local_database_folder+"unnumbered/"+Ast_folder+"/"+AstName+".rwo"
            
         
            fileRWO = Ast_fileName
            
            if os.path.exists(Ast_fileName):
                '''
                Ast_fileName = Ast_fileName.replace("D:" , "/mnt/d")
                # file_queue.put(Ast_fileName)
                '''
            
                
                
             
             
                with open(fileRWO) as fileRWO_Ast:
                    
                        for i, line in enumerate(fileRWO_Ast):
                            
                             
                             if i == 2:
                                 
                                  
                                      
                                   
                                    RMS_string=line.replace('RMSast  =   ','')
                                    
                                    RMSAst=float(RMS_string)
                                   
                                 
                                 
                                 
                             elif i>2:
                                   break
                      
                      
                        if RMSAst > RMSThreshold:
                       
        
                        
                         
                            same_year_obs=1;
                            radar_obs=0;
                          
                            counter_unreliable_obs=0;
                            counter_reliable_observer=0
                            list_ast_name=list()
                            list_ast_year=list()
                            list_ast_month=list()
                            list_ast_day=list()
                          
                            for j, line in enumerate(fileRWO_Ast):
                                if j==3:
                                 
                                    decoded_line = line
                                    list_ast_name.append(decoded_line.split(None,1)[0])    
                                 
                                    list_ast_year.append(int(decoded_line[17:21]))              
                           
                                    first_month=int(decoded_line[22:24])
                                    first_day=int(decoded_line[25:27])
                                    
                               
                                    first_obs_JD=Julianday_greg(first_day,first_month,list_ast_year[0])
                                   
                                   
                                    tracker=decoded_line[13]                          
                                    if tracker  in  weird_tracking:
                                        radar_obs=1;
                                   
                                     
                                    if not decoded_line[180:183]  in obs_code_list:
                                        counter_unreliable_obs+=1    
                                    elif decoded_line[180:183]  in obs_code_list:
                                        counter_reliable_observer+=1
                                    
                                    
                               
                                
                                elif j>3:
                                    
                                   
                                    decoded_line = line
                                    
                                    if decoded_line[0]=='!':
                                        break
                                    
                                    if not decoded_line.split(None,1)[0]  in list_ast_name:  
                                        list_ast_name.append(decoded_line.split(None,1)[0])
                                  
                                     
                              
                                    list_ast_month.append(int(decoded_line[22:24]))
                                    list_ast_day.append(int(decoded_line[25:27]))
                                    if not int(decoded_line[17:21]) in list_ast_year:  
                                        list_ast_year.append(int(decoded_line[17:21]))
                                    
                                    if radar_obs==0:
                                         if  decoded_line[13] in weird_tracking:
                                             radar_obs=1;
                                    
                                    
                                    if not decoded_line[180:183]   in obs_code_list:      
                                            counter_unreliable_obs+=1             
                                    elif decoded_line[180:183]  in obs_code_list:
                                        counter_reliable_observer+=1
                                    
                                    
                                    
                                 
                            
                            observation_total_counter=counter_reliable_observer+counter_unreliable_obs
                       
                            
                          
                            last_obs_JD=Julianday_greg(list_ast_day[-1],list_ast_month[-1],list_ast_year[-1])
                            
                       
                            
                            #0
                            if oppositions < oppositions_min:
                                low_oppositions += 1
                                
                            #1    
                            elif len(list_ast_year)==1:     
                                 
                                 AstFileName=(Add_string + path_one_year_obs+'\\'+AstName+   
                                              " observed only in year {} for {} days.txt").format(list_ast_year[0],
                                                                                                  last_obs_JD-first_obs_JD+1)
                                 
                                 shutil.copy (fileRWO, AstFileName)
                                 ### SAVING DETAIL-FILE
                                 Save_detail_file(Add_string + path_one_year_obs)
                                 
                                 one_year_obs += 1
                            #2     
                            elif len(list_ast_year)==2:     
                                    
                                AstFileName=(Add_string + path_two_year_obs+'\\'+AstName+  
                                             " observed only in years {}, {}.txt").format(*list_ast_year)
                                shutil.copy (fileRWO, AstFileName)
                                ### SAVING DETAIL-FILE
                                Save_detail_file(Add_string + path_two_year_obs)
                                
                                two_years_obs += 1
                                
                                #3
                            elif list_ast_year[-1] < minimum_year_threshold:     
                                    
                                    AstFileName=(Add_string + path_old_observations+'\\'+AstName+   
                                                 " last observation in {}.txt").format(list_ast_year[-1])
                                    shutil.copy (fileRWO, AstFileName)
                                    ### SAVING DETAIL-FILE
                                    Save_detail_file(Add_string + path_old_observations)
                                    
                                    ast_with_old_obs += 1
                            #4 
                            elif observation_total_counter<min_observ_admitted:     
                                
                                AstFileName=(Add_string + path_low_n_obs+'\\'+AstName+   
                                             " just {} observations time span {} days.txt").format(observation_total_counter,
                                                                                         last_obs_JD-first_obs_JD+1)
                                shutil.copy (fileRWO, AstFileName)
                                ### SAVING DETAIL-FILE
                                Save_detail_file(Add_string + path_low_n_obs)
                                
                                low_obs_ast += 1
                            
                            #5
                            elif (counter_reliable_observer/observation_total_counter) < reliable_obs_threshold:   
                            
                                if  radar_obs==1:     
                                    
                                    if (len(list_ast_name)-1)>0:
                                        
                                        AstFileName=(Add_string + subsubpath__unreliable_track_identif+'\\'+AstName+  
                                                     " unreliable obs and radar with {} identification(s)"+".txt").format(len(list_ast_name)-1)
                                        shutil.copy (fileRWO, AstFileName)
                                        
                                        ### SAVING DETAIL-FILE
                                        Save_detail_file(Add_string + subsubpath__unreliable_track_identif)
                                        
                                        radar_track_with_identification += 1
                                      
                                    else:    
                                         
                                         AstFileName=Add_string + subpath_unreliable_track+'\\'+AstName+" unreliable obs and radar.txt"
                                         shutil.copy (fileRWO, AstFileName)
                                         ### SAVING DETAIL-FILE
                                         Save_detail_file(Add_string + subpath_unreliable_track)  
                                         
                                         radar_tracking += 1
                                         
                                         
                                elif  len(list_ast_name)-1>0:   
                                    
                                    AstFileName=(Add_string + subpath_unreliable_identif+'\\'+AstName+  
                                                 " with {} identification(s).txt").format(len(list_ast_name)-1)
                                    shutil.copy (fileRWO, AstFileName)
                                    ### SAVING DETAIL-FILE
                                    Save_detail_file(Add_string + subpath_unreliable_identif)
                                    
                                    with_identification += 1
                                
                                
                                else:  
                                    
                                    AstFileName=(Add_string + path_unreliable_obs+'\\'+AstName+  
                                                 " with {:.1f}% unreliable observations.txt").format(counter_unreliable_obs*100/observation_total_counter)
                                    shutil.copy (fileRWO, AstFileName)
                                    ### SAVING DETAIL-FILE
                                    Save_detail_file(Add_string + path_unreliable_obs)
                                    
                                    unreliable_observatories += 1
                            
                            
                           
                            #6 
                            elif radar_obs==1:     
                                
                                if (len(list_ast_name)-1)>0:
                                    
                                    AstFileName=(Add_string + subpath_track_identif+'\\'+AstName+ 
                                                 " with {} identification(s)"+".txt").format(len(list_ast_name)-1)
                                    shutil.copy (fileRWO, AstFileName)
                                    
                                    ### SAVING DETAIL-FILE
                                    Save_detail_file(Add_string + subpath_track_identif)
                                    
                                    radar_track_with_identification += 1
                                else:    
                                    
                                    AstFileName=Add_string + path_tracking+'\\'+AstName+".txt"
                                    shutil.copy (fileRWO, AstFileName)
                                    ### SAVING DETAIL-FILE
                                    Save_detail_file(Add_string + path_tracking)
                                    
                                    radar_tracking += 1
                             
                            #7        
                            elif len(list_ast_name)-1>0:   
                            
                       
                                    
                                    AstFileName=(Add_string + path_identification+'\\'+AstName+  
                                                 " with {} identification(s).txt").format(len(list_ast_name)-1)
                                    shutil.copy (fileRWO, AstFileName)
                                    ### SAVING DETAIL-FILE
                                    Save_detail_file(Add_string + path_identification)
                                    
                                    with_identification += 1
                            
                       
                            #8
                            else:
                                
                               
                                AstFileName=(path_generic+'\\'+AstName+".txt")
                                shutil.copy (fileRWO, AstFileName)
                                ### SAVING DETAIL-FILE
                             
                                Save_detail_file( path_generic)
                                
                  
                      
                                RMSAst_vec.append(RMSAst)
                            
                        elif RMSAst != 0.:
                            RMSAst_vec.append(RMSAst)
                        
              
                
                
              
            progress_check(line_origin)    
                
                
                
        line_origin=line_origin+1
        
    
    
    
     
        
end=time.time()
print(("Total duration = {}").format(end-start))
print(("Time per asteroid = {}").format(((end-start)/search_gap)))


#Now data analysis
# Save to file
with open("RMS_vec.pkl", "wb") as file:
    pickle.dump(RMSAst_vec, file)
    
average = np.mean(RMSAst_vec)
std_dev = np.std(RMSAst_vec)

# plot

# 3. Generate a Histogram for Visualization
plt.figure(figsize=(8, 6))
plt.hist(RMSAst_vec, bins=int(np.floor(np.sqrt(len(RMSAst_vec)))), color='blue', edgecolor='black', alpha=0.7)
plt.title("Histogram of Data", fontsize=16)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig(f"Images/histogram_threshold{RMSThreshold}.png", dpi=300, bbox_inches='tight')  # Save as PNG
plt.show()

# Print results
print(f"Average (Mean): {average:.2f}")
print(f"Standard Deviation: {std_dev:.2f}")
    
######################## statistical analysis (biased gaussian)

RMSAst_vec = np.array(RMSAst_vec)

# Step 1: Fit Gaussian to the data (without normalization)
mu, sigma = norm.fit(RMSAst_vec)

# Step 2: Visualize the data and fitted Gaussian
x = np.linspace(min(RMSAst_vec), max(RMSAst_vec), 2000)
pdf = norm.pdf(x, mu, sigma)

plt.plot(x, pdf, "r--", label=f"Fitted Gaussian (mean={mu:.2f}, std={sigma:.2f})")
plt.hist(RMSAst_vec, bins=int(np.floor(np.sqrt(len(RMSAst_vec)))), density=True, alpha=0.6, color="blue", label="Data Histogram")
plt.legend()
plt.title("Data and Gaussian Fit")
plt.show()

# Step 3: Identify outliers using a threshold on the right tail
# We can choose a threshold, e.g., 3 standard deviations from the mean (this is just an example)
threshold = mu + 3 * sigma

# Step 4: Exclude data points above the threshold (right tail)
pure_gaussian_data = RMSAst_vec[RMSAst_vec <= threshold]
outliers = RMSAst_vec[RMSAst_vec > threshold]

# Step 5: Visualize the pure Gaussian data and outliers
plt.figure(figsize=(10, 6))
plt.hist(pure_gaussian_data, bins=int(np.floor(np.sqrt(len(pure_gaussian_data)))), density=True, alpha=0.6, color="green", label="Pure Gaussian Data")
plt.hist(outliers, bins=int(np.floor(np.sqrt(len(outliers)))), density=True, alpha=0.6, color="red", label="Outliers")
plt.axvline(threshold, color="purple", linestyle="--", label=f"Threshold (mean + 3*std)")
plt.title(f"Data after Excluding Outliers (Threshold: {threshold:.2f})")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()
plt.show()

# Step 6: Validate if the remaining data is Gaussian
ks_stat, p_value = kstest((pure_gaussian_data - mu) / sigma, "norm")
print(f"Kolmogorov-Smirnov Test: KS Statistic = {ks_stat:.3f}, p-value = {p_value:.3f}")
if p_value > 0.05:
    print("The remaining data closely follows a Gaussian distribution.")
else:
    print("The remaining data does not follow a Gaussian distribution.")

# Step 7: Report summary
print(f"Original Data Size: {len(RMSAst_vec)}")
print(f"Pure Gaussian Data Size: {len(pure_gaussian_data)}")
print(f"Outliers Size: {len(outliers)}")
