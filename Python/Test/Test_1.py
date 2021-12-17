# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 02:57:29 2021

@author: ninad
"""

    ####################### Creating DateTime Vector ##########################
    
    # Initializing DateTimeVector #      
    DateTimeVector = []    
    
    # Creating Datetime Objects for DateTimeVector #
    for i in range(StartIndex_Agggregate, EndIndex_Aggregate+1, 1):
        
        # Creating Datetime Object #
        Day = DateTimeMatrix[i][0]
        Month = DateTimeMatrix[i][1]
        Year = DateTimeMatrix[i][2]
        Time = DateTimeMatrix[i][3]
        
        [hr, minn, sec] = DeciToHm(Time)
        
        #Does this need to be formatted someway or is it just for dispaly?
        DateTimeVector.append(datetime.datetime(Year, Month, Day, hr, minn, sec))
    
    # Getting Sliced DateTime Matrix #
    DateTime_Matrix=FullData[StartIndex_Aggregate:EndIndex_Aggregate+1,1:4+1]