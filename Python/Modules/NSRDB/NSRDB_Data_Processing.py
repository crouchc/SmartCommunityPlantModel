#Conversion of WeatherData_Extractor from matlab to python
# Author: Chris Crouch and Ninad Gaikwad

import sys
import os
import numpy as np
import pandas as pd
import datetime
from scipy.io import savemat

sys.path.append(os.getcwd())   #Need to put path of CodesFromSwefaConverted in order to run

from CodeFrom_SWEEFA.py import *

def WeatherData_Extractor(HEMSWeatherData_Input,Simulation_Params,WeatherData_FileName):         #WDI = HEMSWeatherData_input, SP = Simulation_Params
    
    ######### Getting the Desired Variables from Input Dictionnaries ##########

    # HEMSWeatherData_Input #
    WeatherDataFile_Path=HEMSWeatherData_Input['WeatherDataFile_Path']
    StartYear=HEMSWeatherData_Input['StartYear']
    StartMonth=HEMSWeatherData_Input['StartMonth']
    StartDay=HEMSWeatherData_Input['StartDay']
    StartTime=HEMSWeatherData_Input['StartTime']
    EndYear=HEMSWeatherData_Input['EndYear']
    EndMonth=HEMSWeatherData_Input['EndMonth']
    EndDay=HEMSWeatherData_Input['EndDay']
    EndTime=HEMSWeatherData_Input['EndTime']
    
    # Simulation_Params #
    FileRes=Simulation_Params['FileRes']
    Simulation_StepSize=Simulation_Params['Simulation_StepSize']
    StepSize=Simulation_Params['StepSize']    
   
    ################### Getting DateTime and Weather Data ##################### 
   
    #  Getting Weather Data from CSV File #
    FullData = np.genfromtxt(WeatherDataFile_Path, delimiter = ",")
    
    # Get the Date-Time Matrix #
    DateTime_Matrix = FullData[:, 0:4]
    [Row, Col] = DateTime_Matrix.shape
    
    ######### Computing Correct Indices for Weather Data Extraction ###########
    
    DateTimeMatrixAggregate_ForSlicer= np.concatenate((DateTime_Matrix, np.zeros((Row,1))))
        
    DateTimeSeriesSlicer_Dict = DateTimeSeriesSlicer(DateTimeMatrixAggregate_ForSlicer,1,FileRes,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,StartTime,EndTime)
    
    StartIndex_Aggregate = DateTimeSeriesSlicer_Dict['StartIndex']
    EndIndex_Aggregate = DateTimeSeriesSlicer_Dict['EndIndex']
    
    ##################### Getting required Weather Data ####################### 
    
    # Getting Wind Speed Data #
    Ws = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][15]    #Double check all these indicies
    
    # Getting Temperature Data # 
    T_am = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][19]  
    
    # Getting Irradiance Data #
    GHI = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][6]
    DNI = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][5]    
   
    ############### Creating HEMSWeatherData_Output - Dict ####################
    
    # Initializing HEMSWeatherData_Output # 
    HEMSWeatherData_Output = {}
    
    HEMSWeatherData_Output['Ws']=Ws
    HEMSWeatherData_Output['T_am']=T_am
    HEMSWeatherData_Output['GHI']=GHI
    HEMSWeatherData_Output['DNI']=DNI
    HEMSWeatherData_Output['DateTimeVector']=DateTimeVector
    HEMSWeatherData_Output['DateTime_Matrix']=DateTime_Matrix    
    
    ################### Saving Output Dict as .mat File #######################
    
    savemat(WeatherData_FileName+".mat", HEMSWeatherData_Output)
    
    #################### Return  HEMSWeatherData_Output #######################
    
    return HEMSWeatherData_Output

def WeatherData_Extractor_MPC(HEMSWeatherData_Input,Simulation_Params,MPC_Params,WeatherData_FileName):         #WDI = HEMSWeatherData_input, SP = Simulation_Params
    
    ######### Getting the Desired Variables from Input Dictionnaries ##########

    # HEMSWeatherData_Input #
    WeatherDataFile_Path=HEMSWeatherData_Input['WeatherDataFile_Path']
    StartYear=HEMSWeatherData_Input['StartYear']
    StartMonth=HEMSWeatherData_Input['StartMonth']
    StartDay=HEMSWeatherData_Input['StartDay']
    StartTime=HEMSWeatherData_Input['StartTime']
    EndYear=HEMSWeatherData_Input['EndYear']
    EndMonth=HEMSWeatherData_Input['EndMonth']
    EndDay=HEMSWeatherData_Input['EndDay']
    EndTime=HEMSWeatherData_Input['EndTime']
    
    # Simulation_Params #
    FileRes=Simulation_Params['FileRes']
    Simulation_StepSize=Simulation_Params['Simulation_StepSize']
    StepSize=Simulation_Params['StepSize']    
    
    # MPC_Params #    
    MPC_ComputationLength_Day=MPC_Params['MPC_ComputationLength_Day']    
    MPC_StepLengthUsed=MPC_Params['MPC_StepLengthUsed']  
    
    ########################### Basic Computations ############################
    
    # Converting Decimal time to HH:MM:SS #
    TimeStamp= DeciToHM( EndTime );
    
    EndHour=TimeStamp[0]
    EndMin=TimeStamp[1]
    EndSec=TimeStamp[2]
    
    Actual_EndDay = datetime.datetime(EndYear,EndMonth,EndDay,EndHour,EndMin,EndSec);
    
    Duration_Hours=MPC_ComputationLength_Day*24;
    
    Duration = datetime.timedelta(hours=Duration_Hours);
    
    MPC_EndDay=Actual_EndDay+Duration;
    
    EndYear=MPC_EndDay.year;
    EndMonth=MPC_EndDay.month;
    EndDay=MPC_EndDay.day;
    EndHour=MPC_EndDay.hour;
    EndMin=MPC_EndDay.minute;
    EndSec=MPC_EndDay.second;
    
    # Converting HH:MM:SS to Decimal Time #
    [EndTime]=HMToDeci( EndHour,EndMin,EndSec );
    
    Duration_TimeSteps=Duration_Hours*(60/FileRes);    
   
    ################### Getting DateTime and Weather Data ##################### 
   
    #  Getting Weather Data from CSV File #
    FullData = np.genfromtxt(WeatherDataFile_Path, delimiter = ",")
    
    # Get the Date-Time Matrix #
    DateTime_Matrix = FullData[:, 0:4]
    [Row, Col] = DateTime_Matrix.shape
    
    ######### Computing Correct Indices for Weather Data Extraction ###########
    
    DateTimeMatrixAggregate_ForSlicer= np.concatenate((DateTime_Matrix, np.zeros((Row,1))))
        
    DateTimeSeriesSlicer_Dict = DateTimeSeriesSlicer(DateTimeMatrixAggregate_ForSlicer,1,FileRes,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,StartTime,EndTime)
    
    StartIndex_Aggregate = DateTimeSeriesSlicer_Dict['StartIndex']
    EndIndex_Aggregate = DateTimeSeriesSlicer_Dict['EndIndex']
    
    ##################### Getting required Weather Data ####################### 
    
    # Getting Wind Speed Data #
    Ws = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][15]    #Double check all these indicies
    
    # Getting Temperature Data # 
    T_am = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][19]  
    
    # Getting Irradiance Data #
    GHI = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][6]
    DNI = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][5]    
    
    # Computing Actual and MPC TimeSteps #
    MPC_TimeSteps=np.size(GHI,0);
    Simulation_TimeSteps=MPC_TimeSteps-Duration_TimeSteps;
   
    ############### Creating HEMSWeatherData_Output - Dict ####################
    
    # Initializing HEMSWeatherData_Output # 
    HEMSWeatherData_MPC_Output = {}
    
    HEMSWeatherData_MPC_Output['Ws']=Ws
    HEMSWeatherData_MPC_Output['T_am']=T_am
    HEMSWeatherData_MPC_Output['GHI']=GHI
    HEMSWeatherData_MPC_Output['DNI']=DNI
    HEMSWeatherData_MPC_Output['DateTime_Matrix']=DateTime_Matrix  
    HEMSWeatherData_MPC_Output['Ws_Sim']=Ws[0:Simulation_TimeSteps]
    HEMSWeatherData_MPC_Output['T_am_Sim']=T_am[0:Simulation_TimeSteps]
    HEMSWeatherData_MPC_Output['GHI_Sim']=GHI[0:Simulation_TimeSteps]
    HEMSWeatherData_MPC_Output['DNI_Sim']=DNI[0:Simulation_TimeSteps]
    HEMSWeatherData_MPC_Output['MPC_TimeSteps']=MPC_TimeSteps
    HEMSWeatherData_MPC_Output['Simulation_TimeSteps']=Simulation_TimeSteps
    HEMSWeatherData_MPC_Output['Duration_TimeSteps']=Duration_TimeSteps    
    
    ################### Saving Output Dict as .mat File #######################
    
    savemat(WeatherData_FileName+".mat", HEMSWeatherData_MPC_Output)  
    
    ################## Return  HEMSWeatherData_MPC_Output #####################
    
    return HEMSWeatherData_MPC_Output    


def NSRDB_Low2HighRes(OriginalResolution,NewResolution,ProcessingType,WeatherFileLoad_Full):
    
    ### Weather Data - Low Resolution to High Resolution - Zero Order Hold ####
    
    WeatherFileLoad_Full = np.array(WeaterFileLoad_Full)
    
    [R,C] = np.shape(WeatherFileLoad_Full)
    
    FileRes = OriginalResolution
    
    ##################### Creating New Resolution File ########################
    
    # Full File to be Processed #
    if (ProcessingType == 1):
        
        # Getting Start and End DateTime #
        StartDay=WeatherFileLoad_Full[0,0];
        StartMonth=WeatherFileLoad_Full[0,1];
        StartYear=WeatherFileLoad_Full[0,2];
        StartTime=WeatherFileLoad_Full[0,3];
        
        # Decimal Time to HMS #
        TimeStamp = DeciToHM(StartTime)
        
        StartHr=TimeStamp[0]
        StartMin=TimeStamp[1]
        StartSec=TimeStamp[2]
        
        EndDay=WeatherFileLoad_Full[R-1,0];
        EndMonth=WeatherFileLoad_Full[R-1,1];
        EndYear=WeatherFileLoad_Full[R-1,2];
        EndTime=WeatherFileLoad_Full[R-1,3];
    
        # Decimal Time to HMS #
        TimeStamp= DeciToHM( EndTime );
        
        EndHour=TimeStamp[0]
        EndMin=TimeStamp[1]
        EndSec=TimeStamp[2] 
        
    # Part of the File to be Processed we take User Input #    
    elif (ProcessingType == 2): # Part of the File to be Processed we take User Input
        
        # Getting Start and End DateTime #
        StartDay=1
        StartMonth=1
        StartYear=2017
        StartTime=0
        
        # Decimal Time to HMS #
        TimeStamp = DeciToHM(StartTime)
        
        StartHr=TimeStamp[0]
        StartMin=TimeStamp[1]
        StartSec=TimeStamp[2] 
    
        EndDay=31
        EndMonth=12
        EndYear=2017
        EndTime=23.5
        
        # Decimal Time to HMS #
        TimeStamp= DeciToHM( EndTime );
        
        EndHour=TimeStamp[0]
        EndMin=TimeStamp[1]
        EndSec=TimeStamp[2]   
        
    DateTimeSeriesSlicer_Dict = DateTimeSeriesSlicer(WeatherFileLoad_Full,1,OriginalResolution,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,0,EndTime)

    StartIndex_Aggregate = DateTimeSeriesSlicer_Dict['StartIndex']
    EndIndex_Aggregate = DateTimeSeriesSlicer_Dict['EndIndex']
    
    ####################### Changing File Resolution ##########################
    
    # Creating DateTime Object #
    Start_DateTime=datetime.datetime(StartYear,StartMonth,StartDay,StartHr,StartMin,StartSec)
    End_DateTime=datetime.datetime(EndYear,EndMonth,EndDay,EndHr,EndMin,EndSec)

    # Creating New Resolution Duration
    NewResolution_Duration=datetime.timedelta(minutes=NewResolution)

    # Initializing Important Quantities#
    NewResFile=np.zeros((1,C)) 
    
    DateTimeArray = [Start_DateTime] 
    
    Counter_NewTime=0 
    Counter_OldTime=StartIndex_Aggregate
    
    # While Loop for New Resolution File    
    while (DateTimeArray[Counter_NewTime]<=End_DateTime):
        
     
        if (Counter_OldTime==0):
            
            # Decomposing New DateTime #
            Day=DateTimeArray[Counter_NewTime].day
            Month=DateTimeArray[Counter_NewTime].month
            Year=DateTimeArray[Counter_NewTime].year
            
            Hour=DateTimeArray[Counter_NewTime].hour
            Minute=DateTimeArray[Counter_NewTime].minute
            Second=DateTimeArray[Counter_NewTime].second
            
            # Converting HMS to Decimal Time #
            Time  = HMToDeci( Hour,Minute,Second )
            
            # Updating NewRes File with OldRes File #
            NewResFile=np.append(NewResFile,[np.concatenate(np.array([Day,Month,Year,Time]),WeatherFileLoad_Full[Counter_OldTime,4:])],axis=0)            
                        
            # Incrementing Counter #
            Counter_OldTime=Counter_OldTime+1           
            
        else:
            
            # Getting Current and Previous OldRes File DateTime #
            CurrentDay=WeatherFileLoad_Full[Counter_OldTime,0]
            CurrentMonth=WeatherFileLoad_Full[Counter_OldTime,1]
            CurrentYear=WeatherFileLoad_Full[Counter_OldTime,2]
            
            CurrentTime=WeatherFileLoad_Full[Counter_OldTime,3]
            
            # Converting Decimal Time to HMS # 
            TimeStamp = DeciToHM( CurrentTime ) 
            
            CurrentHr=TimeStamp[0]
            CurrentMin=TimeStamp[1]
            CurrentSec=TimeStamp[2] 
            
            PreviousDay=WeatherFileLoad_Full[Counter_OldTime-1,1]
            PreviousMonth=WeatherFileLoad_Full[Counter_OldTime-1,2]
            PreviousYear=WeatherFileLoad_Full[Counter_OldTime-1,3]
                         
            PreviousTime=WeatherFileLoad_Full[Counter_OldTime-1,4]
            
            # Converting Decimal Time to HMS #
            TimeStamp = DeciToHM( PreviousTime )      
           
            PreviousHr=TimeStamp[0]
            PreviousMin=TimeStamp[1]
            PreviousSec=TimeStamp[2] 
            
            # Converting To DateTime Object #
            CurrentDateTime_OldResFile=datetime.datetime(CurrentYear,CurrentMonth,CurrentDay,CurrentHr,CurrentMin,CurrentSec)
            PreviousDateTime_OldResFile=datetime.datetime(PreviousYear,PreviousMonth,PreviousDay,PreviousHr,PreviousMin,PreviousSec)
            
            if ((DateTimeArray[Counter_NewTime]<=CurrentDateTime_OldResFile)and(DateTimeArray[Counter_NewTime]>PreviousDateTime_OldResFile)):
                
                # Decomposing New DateTime #
                Day=DateTimeArray[Counter_NewTime].day
                Month=DateTimeArray[Counter_NewTime].month
                Year=DateTimeArray[Counter_NewTime].year
    
                Hour=DateTimeArray[Counter_NewTime].hour
                Minute=DateTimeArray[Counter_NewTime].minute
                Second=DateTimeArray[Counter_NewTime].second
    
                # Converting HMS to Decimal Time #
                [ Time ] = HMToDeci( Hour,Minute,Second )
    
                # Updating NewRes File with OldRes File #
                NewResFile=np.append(NewResFile,[np.concatenate(np.array([Day,Month,Year,Time]),WeatherFileLoad_Full[Counter_OldTime,4:])],axis=0)            
                                
            else:
                
                # Incrementing Counter #
                Counter_OldTime=Counter_OldTime+1             
    
                # Decomposing New DateTime #
                Day=DateTimeArray[Counter_NewTime].day
                Month=DateTimeArray[Counter_NewTime].month
                Year=DateTimeArray[Counter_NewTime].year
    
                Hour=DateTimeArray[Counter_NewTime].hour
                Minute=DateTimeArray[Counter_NewTime].minute
                Second=DateTimeArray[Counter_NewTime].second
    
                # Converting HMS to Decimal Time #
                [ Time ] = HMToDeci( Hour,Minute,Second )
    
                # Updating NewRes File with OldRes File #
                NewResFile=np.append(NewResFile,[np.concatenate(np.array([Day,Month,Year,Time]),WeatherFileLoad_Full[Counter_OldTime,4:])],axis=0)            
              
              
        # Creating Next New Resolution DateTime #
        DateTimeArray[Counter_NewTime+1]=DateTimeArray(Counter_NewTime)+NewResolution_Duration
    
        # Incrementing Counter #
        Counter_NewTime=Counter_NewTime+1 
        
        
    # Removing First Row from NewResFile
    NewResFile=np.delete(NewResFile,0,0)
    
    ########################### Return  NewResFile ############################
    
    return NewResFile      
    
   
def WeatherDataProcessing_CityWise(MainFolder_Path,DestinationFolder_Path,OriginalFile_Res,NewFile_Res_List): 
    
    ############### Step 1 - Getting List of all Sub-Folders ##################
    
    Folder_List=os.listdir(MainFolder_Path)
    
    ### Step 2 - Starting the Main Folder Loop for Weather File Processing ####
    
    for i in range(0,len(Folder_List),1):
        
        # Getting Current Sub-Folder Name #
        Folder_Name=Folder_List[i]
        
        # Getting Current City-State Name #
        CityStateName=Folder_Name
        
        # Getting Sub-Folder Path #
        SubFolder_Path=os.path.join(MainFolder_Path,Folder_Name)
        
        # Getting Files list from Sub-Folder #
        Files_List=os.listdir(SubFolder_Path)        
        
        # Creating Destination Directory #
        DestinationDirectory_CityState_Name=CityStateName
        DestinationDirectory_CityState_Path=os.path.join(DestinationFolder_Path,DestinationDirectory_CityState_Name)
        os.mkdir(DestinationDirectory_CityState_Path)        
        
       ######## Step 3 - Starting the Loop for Weather File Processing ######## 
       
        for j in range(0,len(Files_List),1):
        
            # Getting Real File Name #
            File_Name=Files_List[j]
            
            # Getting Information from the File Name #
            FileName4_Contents=File_Name.split("_")
            Lat=FileName4_Contents[1]
            Long=FileName4_Contents[2]
            Year=FileName4_Contents[3]
            
            # Getting Weather File Path
            WeatherFile_Path=os.path.join(SubFolder_Path,File_Name)
            
            # Reading Weather File #
            ActualFile=np.genfromtxt(WeatherFile_Path, delimiter = ",", skipheader=3)
           
            ###### Step 4: Changing Date-Time Stamp Columns for Utility #######
           
            # Initializing New Datetime Stamp #
            DateTime_Stamp=np.zeros([1,4])
           
            # Getting Shape of Actual File #
            [R,C]=ActualFile.shape
           
            for k in range(0,R,1):
               
                 Hour=ActualFile[k,3]
                
                 Min=ActualFile[k,4]
                
                 [ TimeDeci ] = HMToDeci( Hour,Min,0 )
                
                 DateTimeStamp=np.append(DateTime_Stamp,[np.concatenate(([ActualFile[k,2]],[ActualFile[k,1]],[ActualFile[k,0]],[TimeDeci]))],axis=0)
                 
            # Removing First Row from DateTimeStamp #
            DateTimeStamp=np.delete(DateTimeStamp,0,0)
            
            # Creating New Actual File with Updated Date-Time #
            ActualFile=np.concatenate(DateTimeStamp,ActualFile[:,5:],axis=1)
            
            ####### Step 6 - Preprocessing Time Resolution of the Files #######
            
            for j in range(0,len(NewFile_Res_List),1):
                
                # Changing Resolution of Original File to New User-Defined higher resolution
                [NewResFile_ResNew] = NSRDB_Low2HighRes(OriginalFile_Res,NewFile_Res_List[j],1,ActualFile);
                                
                DestinationDirectory_Res_Name="Res_"+str(NewFile_Res_List[j])
                DestinationDirectory_Res_Path=os.path.join(DestinationDirectory_CityState_Path,DestinationDirectory_Res_Name)
                os.mkdir(DestinationDirectory_Res_Path)
                
                # Creating New Resolution File Name
                NewRes_File_Name=CityStateName+"_"+str(Year)+"__WeatherData_NSRDB_"+str(OriginalFile_Res)+"minTo"+str(NewFile_Res_List[j])+"_minRes.csv"
                
                # Creating New Resolution File Path
                NewRes_File_Path=os.path.join(DestinationDirectory_Res_Path,NewRes_File_Name)
                
                # Save New Resolution File in appropriate Folder as CSV
                np.savetxt(NewRes_File_Path, NewResFile_ResNew, delimiter=",")


           