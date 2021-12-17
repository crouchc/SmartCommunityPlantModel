#Conversion of WeatherData_Extractor from matlab to python
#Author: Chris Crouch

import numpy as np
import pandas as pd

from CodesFromSwefa.py import *

def WeatherData_Extractor(WDI,SP,WeatherData_FileName):         #WDI = HEMSWeatherData_input, SP = Simulation_Params
    FullData = np.genfromtxt(WDI.WeatherDataFile_Path, delimiter = ",")
    
    #Get the date time matrix fir 4 rows and all colums
    DateTime_Matrix = FullData[:, 0:4]
    [rows, cols] = DateTime_Matrix.shape
    
    EndTime=24-(SP.FileRes/60)
    
    DateTimeMatrixAggregate_ForSlicer= np.concatenate((DateTime_Matrix, np.zeros((rows,1))))
        
    dictvals = DateTimeSeriesSlicer(DateTimeMatrixAggregate_ForSlicer, 1, WDI.FileRes, WDI.StartYear, WDI.EndYear, WDI.StartMonth, WDI.EndMonth, WDI.StartDay, WDI.EndDay,WDI.StartTime, WDI.EndTime)
    StartIndex_Aggregate = dictvals['StartIndex']
    EndIndex_Aggregate = dictvals['EndIndex']
    
    
    Ws = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][15]    #Double check all these indicies
    T_am = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][20]  
    GHI = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][6]
    DNI = FullData[StartIndex_Aggregate:EndIndex_Aggregate+1][5]
    
    counter = 0
    
    DateTimeVector = []
    for i in range(StartIndex_Agggregate, EndIndex_Aggregate+1, 1):
        counter += 1
        Day = DateTimeMatrix[i][0]
        Month = DateTimeMatrix[i][1]
        Year = DateTimeMatrix[i][2]
        Time = DateTimeMatrix[i][3]
        
        [hr, minn, sec] = DeciToHm(Time)
        
        #Does this need to be formatted someway or is it just for dispaly?
        DateTimeVector.append(DateTime(Year, Month, Day, hr, minn, sec))
    
    HEMSWeatherData_Output = {'Ws': Ws, 'T_am':T_am, 'GHI':GHI, 'DNI':DNI, 'DateTimeVector':DateTimeVector, 'DateTime_Matrix':DateTime_Matrix}
    
    df = pd.DataFrame(data = HEMSWeatherData_Output)
    df.to_excel('HEMSWeatherData_Output.xlsx', index = False, header = False)
    
    Day_Data = FullData[StartIndex_Aggregate:EndIndex_Aggregate,:]
    
    #Not sure what this is doing
    for i in range(360):
        if i == 1:
            SingleDay_WeatherFile_1 = Day_Data
        SingleDay_WeatherFile_1 = np.vstack(SingleDay_WeatherFile_1, DayData)
    
    return HEMSWeatherData_Output

def NSRDB_Low2HighRes(OriginalResolution,NewResolution,ProcessingType,WeatherFileLoad_Full):
    WeatherFileLoad_Full = np.array(WeaterFileLoad_Full)
    [R,C] = np.shape(WeatherFileLoad_Full)
    
    FileRes = OriginalResolution
    
    #Creating new resolution File
    if (ProcessingType == 1):
        # Getting Start and End DateTime
        StartDay=WeatherFileLoad_Full(0,0);
        StartMonth=WeatherFileLoad_Full(0,1);
        StartYear=WeatherFileLoad_Full(0,2);
        StartTime=WeatherFileLoad_Full(0,3);
        
        [StartHr,StartMin,StartSec] = DeciToHM(StartTime) # Decimal Time to HMS
        
        EndDay=WeatherFileLoad_Full(R-1,0);
        EndMonth=WeatherFileLoad_Full(R-1,1);
        EndYear=WeatherFileLoad_Full(R-1,2);
        EndTime=WeatherFileLoad_Full(R-1,3);
    
        [EndHr,EndMin,EndSec] = DeciToHM(EndTime) # Decimal Time to HMS  
        
    elif (ProcessingType == 2): # Part of the File to be Processed we take User Input
        # Getting Start and End DateTime
        StartDay=1
        StartMonth=1
        StartYear=2017
        StartTime=0
    
        [StartHr,StartMin,StartSec] = DeciToHM(StartTime) #Decimal Time to HMS
    
        EndDay=31
        EndMonth=12
        EndYear=2017
        EndTime=23.5
    
        [EndHr,EndMin,EndSec] = DeciToHM(EndTime) # Decimal Time to HMS  
        
    [OriginalData,StartIndex,EndIndex] = DateTimeSeriesSlicer(WeatherFileLoad_Full,1,OriginalResolution,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,0,EndTime)
    
    # Creating DateTime Object
    Start_DateTime=datetime(StartYear,StartMonth,StartDay,StartHr,StartMin,StartSec)
    End_DateTime=datetime(EndYear,EndMonth,EndDay,EndHr,EndMin,EndSec)

    # Creating New Resolution Duration
#need to convert duration or find library
    #NewResolution_Duration=duration(0,NewResolution,0)
    
    # While Loop for New Resolution File
    NewResFile=np.zeros((1,C)) # Initializing
    
    DateTimeArray = Start_DateTime # Initializing
    
    Counter_NewTime=1 # Initilizing
    Counter_OldTime=StartIndex # Initializing
    
    

def duration(hrs = 0, mins=0, secs=0):
    val = []
    if (hrs != 0):
        for i in range(len(hrs)):
            val.append()
    