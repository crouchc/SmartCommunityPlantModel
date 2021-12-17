#Conversion of PecanStreetDataExtractor from matlab 
# Author: Chris Crouch and Ninad Gaikwad

import sys
import pandas as pd
import numpy as np
import os
import datetime
from scipy.io import savemat

sys.path.append(os.getcwd())   #Need to put path of CodesFromSwefaConverted in order to run

from CodeFrom_SWEEFA import *

       
def PecanStreet_Low2HighRes(OriginalResolution,NewResolution,ProcessingType,WeatherFileLoad_Full):
    
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


def PecanStreetData_Preprocessing(MainFile_Path,DestinationFolder_Path,NewFile_Name,OriginalFile_Res,NewFile_Res_List,AveragingPoints): 
    
    ######################## Step 1: Reading CSV File #########################
    
    #  Getting Weather Data from CSV File # [Might need Pandas as datetime column is string]
    ActualFile = np.genfromtxt(MainFile_Path, delimiter = ",",skipheader=1)
    
    # Getting relevant columns of data in Array format #
    ID_Array=ActualFile[:,0]
    
    DateTime_String_Array=ActualFile[:,1]
    
    Data_Array=table2arrayActualFile[:,2:]
    
    # Getting size of Data_Array #
    [DataFrame_Row,DataFrame_Column]=Data_Array.shape()
    
    # Getting number of Data Columns #
    DataCols=DataFrame_Column-2
    
    ######### Step 2: Changing Date-Time Stamp Columns for Utility ############

    # Initialization of Date Time Holder #   
    DateTimeStamp=np.zeros([1,4]) 
    
    for i in range(0,DataFrame_Row,1):
        
        DateTime_String= DateTime_String_Array[i]
         
        DateTime_String1 = DateTime_String.split(" ")
        
        DateTime_String_Date = DateTime_String1[0].split("/")
        
        DateTime_String_Time = DateTime_String1[1].split(":")
        
        Year = float(DateTime_String_Date[2])
        Month = float(DateTime_String_Date[0])
        Day = float(DateTime_String_Date[1])
        
        Hour = float(DateTime_String_Time[0])
        Min = float(DateTime_String_Time[1])
        
        [ TimeDeci ] = HMToDeci( Hour,Min,0 )
        
        # Updating NewRes File with OldRes File #
        DateTimeStamp=np.append(DateTimeStamp,[np.array([Day,Month,Year,TimeDeci])],axis=0)            
         
        # Debugger #
        print(i)
       
    # Removing First Row from DateTimeStamp
    DateTimeStamp=np.delete(DateTimeStamp,0,0)
    
    ######### Step 3: Grouping Data according to different houses #############

# Getting Unique House Indices #
Unique_Houses=unique(ID_Array)

# Getting number of Unique Houses #
Unique_Houses_Number=Unique_Houses.size

for i in range(0,Unique_Houses_Number,1)
        
    # Finding Indices for the current House #
    CurrentHouse_Indices=find(ID_Array==Unique_Houses(i));
    
    # Creating current House Dataframe #
    CurrentHouse_Dataframe=[DateTimeStamp(CurrentHouse_Indices,:),Data_Array(CurrentHouse_Indices,:)]

    # Converting NaNs to Zeros #
    CurrentHouse_Dataframe(isnan(CurrentHouse_Dataframe))=0
    
    # Clean Data for any irregularities of date-time ordering and missing data (Negatives are not converted to 0s) #
    [ ProcessedDataFrame ] = SolarPVWeatherDataCleaner_ModifiedForPecanStreet( OriginalResolution,DataCols,AveragingPoints,CurrentHouse_Dataframe )
 
    # Changing to required Resolution #
    [CurrentHouse_Dataframe_NewResFile] = PecanStreet_Low2HighRes(OriginalResolution,NewResolution,ProcessingType,ProcessedDataFrame)
    
    # Current House Name #
    CurrentHouse_Name=strcat('House_',num2str(i),'_',num2str(OriginalResolution),...
        'minTo_',num2str(NewResolution),'min','.csv')
    
    # Saving House Data in a CSV File #
    csvwrite(strcat(DataFolderPath,CurrentHouse_Name),CurrentHouse_Dataframe_NewResFile)
    
    # To be Continued.........................................................
    
     
def PecanStreet_Data_Extractor(HEMSWeatherData_Input,PecanStreet_Data_FolderPath,N_House_Vector,Type,Data_MatFile_Name):   
    
    
    # To be Continued.........................................................
    
    
def SolarPVWeatherDataCleaner_ModifiedForPecanStreet( Res,DataCols,N,DataFile ):   
    
    
    # To be Continued.........................................................
