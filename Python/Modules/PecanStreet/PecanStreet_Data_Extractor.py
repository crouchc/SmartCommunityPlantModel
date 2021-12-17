#Conversion of PecanStreetDataExtractor from matlab 
#Author: Chris Crouch

import sys
import pandas as pd
import numpy as np
import os

sys.path.append(os.getcwd())   #Need to put path of CodesFromSwefaConverted in order to run

from CodesFromSwefa import *

class Home:
    def __init__(self, startind, endind, pv = 0, bat = 0, ev = 0):
        self.startind = startind
        self.endind = endind
        self.pv = pv
        self.ev = ev
        self.bat = bat
        
    def __repr__(self):
        return "File Used contains PV: " + str(self.pv) + " EV: " + str(self.ev) + " Bat: " + str(self.bat)
    
    def equals(self, rhs):
        if self.pv != rhs.pv:
            return False
        elif self.ev != rhs.ev:
            return False
        elif self.bat != rhs.bat:
            return False
        else:
            return True  
        
def saveOutput(prio, houses):
    if prio['1'] != 0:
        PecanStreetOutput = houses[prio['ind1']]
        print(houses[prio['ind1']])
    elif prio['2'] != 0:
        PecanStreetOutput = houses[prio['ind2']]
        print(houses[prio['ind2']])
    elif prio['3'] != 0:
        PecanStreetOutput = houses[prio['ind3']]
        print(houses[prio['ind3']])
    elif prio['4'] != 0:
        PecanStreetOutput = houses[prio['ind4']]
        print(houses[prio['ind4']])
    elif prio['5'] != 0:
        PecanStreetOutput = houses[prio['ind5']]
        print(houses[prio['ind5']])
    elif prio['6'] != 0:
        PecanStreetOutput = houses[prio['ind6']]
        print(houses[prio['ind6']])
    elif prio['7'] != 0:
        PecanStreetOutput = houses[prio['ind7']]
        print(houses[prio['ind7']])
    elif prio['8'] != 0:
        PecanStreetOutput = houses[prio['ind8']]
        print(houses[prio['ind8']])
        
        
    return PecanStreetOutput
        
def PecanStreet_Data_Extractor(HEMSWeatherData_Input,Simulation_Params,PecanStreet_Data_FolderPath,N_House_Vector,Type,Data_MatFile_Name):
    #Storing variables form object input
    StartMonth=HEMSWeatherData_Input.StartMonth
    StartDay=HEMSWeatherData_Input.StartDay
    StartTime=HEMSWeatherData_Input.StartTime
    EndMonth=HEMSWeatherData_Input.EndMonth
    EndDay=HEMSWeatherData_Input.EndDay
    EndTime=HEMSWeatherData_Input.EndTime
    
    FileRes=Simulation_Params.FileRes
    # DataFolderName=PecanStreet_Data_FolderPath
    
    #Getting correct filepath for data files
    # path = os.getcwd()
    # path = path + PecanStreet_Data_FolderPath            #Need to give relative path to files in parameter 
    # listd = os.listdir(path)
    listd = os.listdir(PecanStreet_Data_FolderPath)
    
    #Creating variable for storing data
    allDatanp = []
    
    #Iterating through all filenames
    for i in range(len(listd)):
        filename = listd[i]
        check = True
        #Characters to check if file is temporary/ we dont use it
        charlist = ['d', "\\", "<", "[", "^", 'a', '-', 'z', 'A', '-', 'Z', '_', '0', '-9', ']', "\\", 'w', '*']
        
        #Checks if the filename contains any of those characters at the beginning of the filename
        for j in range(len(charlist)):
            if (filename.find(charlist[j]) != -1):
                if (filename.index(charlist[j]) == 0):
                    check = False
                    break
        #If file is one we want save the filename and load the data into list
        if check:
            fullpathname = PecanStreet_Data_FolderPath + "\\" + filename
            allDatanp.append(np.genfromtxt(fullpathname, delimiter = ","))
            check = False
            
    #Convert python list into numpy array for better handling
    noerror = 0
    
    #Iterator through all data in numpy array
    for i in range(len(allDatanp)):
        currentVal = allDatanp[i]
        #Getting wanted values out of data
        StartYear = currentVal[0,2]
        EndYear = StartYear        #Assuming all ranges are in the same year
        #zeros = np.zeros((len(currentVal[:,0]), 1))
        
        #Getting required start and end indicies
        #DateTimeMatrixAggregate_ForSlicer = np.concatenate((currentVal[0:4], zeros), axis = 1)
        vals = DateTimeSeriesSlicer_PecanStreetData.DateTimeSeriesSlicer_PecanStreetData(currentVal[:,0:4],1,FileRes,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,StartTime,EndTime)
        OriginalSeries = vals['OriginalData']
        StartIndex_Aggregate = vals['StartIndex']
        EndIndex_Aggregate = vals['EndIndex']
        
        #Saving data from correct time range
        if (isinstance(OriginalSeries, str) != True and EndIndex_Aggregate != -1):
            Data = currentVal[StartIndex_Aggregate:EndIndex_Aggregate, :]
            noerror += 1
            
            #Adding a filenumber to the end of the data
            row, col = np.shape(Data)
            filenum = np.array([[noerror]]*row)
            Data = np.concatenate((Data, filenum), axis = 1)
            
            #Saving data withing the correct time range 
            if noerror == 1:
                dataInTimeRange = np.array(Data)
            else:
                dataInTimeRange = np.concatenate((dataInTimeRange, Data)) 
                
        else:
            print("file was not included")
            print(i)
            
    #Arranging Data Columns in Descending order of SolarPV, Battery, EV, Priority for Loads 
    dataInTimeRangeSorted = dataInTimeRange[:,0:4]
    
    #Sorted the data based on priority
    dataInTimeRangeSorted = np.concatenate((dataInTimeRangeSorted, \
                                           #Date Time
                                           dataInTimeRange[:, 65+4:67+4], \
                                           dataInTimeRange[:, 12+4:15+4], \
                                               #Solar PV, Battery, EV
                                           dataInTimeRange[:, 60+4:62+4], \
                                           dataInTimeRange[:, 25+4:26+4], \
                                           dataInTimeRange[:, 38+4:39+4], \
                                           dataInTimeRange[:, 36+4:37+4], \
                                           dataInTimeRange[:, 39+4:40+4], \
                                           dataInTimeRange[:, 37+4:38+4], \
                                           dataInTimeRange[:, 59+4:60+4], \
                                           dataInTimeRange[:, 70+4:71+4], \
                                           dataInTimeRange[:, 48+4:49+4], \
                                           dataInTimeRange[:, 52+4:53+4], \
                                               #Level 1 priority: Fridge, freezer, kitchen
                                           dataInTimeRange[:, 7+4:12+4], \
                                               #Level 2 priority: Bedroom
                                           dataInTimeRange[:, 46+4:48+4], \
                                           dataInTimeRange[:, 49+4:50+4], \
                                               #Level 3 Priority - Living Rooms, Office Room
                                           dataInTimeRange[:, 16+4:17+4], \
                                           dataInTimeRange[:, 22+4:23+4], \
                                           dataInTimeRange[:, 63+4:64+4], \
                                           dataInTimeRange[:, 21+4:22+4], \
                                           dataInTimeRange[:, 58+4:59+4], \
                                           dataInTimeRange[:, 68+4:69+4], \
                                           dataInTimeRange[:, 73+4:74+4], \
                                               #Level 4 Priority Clothes, Garbage Disposal, Pumps
                                           dataInTimeRange[:, 62+4:63+4], \
                                           dataInTimeRange[:, 5+4:7+4], \
                                           dataInTimeRange[:, 18+4:21+4], \
                                               #Level 5 Priority - Security, Bathrooms, Dinning Room, Dishwasher
                                           dataInTimeRange[:, 27+4:29+4], \
                                           dataInTimeRange[:, 69+4:70+4], \
                                           dataInTimeRange[:, 64+4:65+4], \
                                           dataInTimeRange[:, 50+4:53+4], \
                                               #Level 6 Priority - Remaining Rooms, Outside Lights
                                           dataInTimeRange[:, 4+4:5+4], \
                                           dataInTimeRange[:, 67+4:68+4], \
                                           dataInTimeRange[:, 74+4:75+4], \
                                               #Level 7 Priority - Aquarium, Lawn Sprinklers, Wine Cooler
                                           dataInTimeRange[:, 34+4:35+4], \
                                           dataInTimeRange[:, 57+4:58+4], \
                                           dataInTimeRange[:, 56+4:57+4], \
                                           dataInTimeRange[:, 35+4:36+4], \
                                           dataInTimeRange[:, 71+4:73+4],\
                                               #Level 8 Priority - Pool, Jacuzzi, Water Heater
                                           dataInTimeRange[:, 79:80] \
                                               #Filenum
                                           ), axis = 1)
    row, column = dataInTimeRangeSorted.shape
    
    #Need to find indicies of houses for each combination of PV, Bat, and EV
    #List to store houses
    houses = []
    
    #Variables to create home object
    startind = 0
    endind = 0
    j = 0;
    
    #storing all home object in list with their start and end indicies
    for i in range(noerror):
        filenum = dataInTimeRangeSorted[startind, 57]
        while (j < row and filenum == dataInTimeRangeSorted[j, 57]):
            endind += 1
            j += 1
        houses.append(Home(startind,endind-1))
        startind = endind
    
    #seeing whether or not a house object has pv, ev or bat assuming value in file would be 0 if not
    for i in range(len(houses)):
        pv = np.sum(dataInTimeRangeSorted[houses[i].startind:houses[i].endind, 4], 0) + np.sum(dataInTimeRangeSorted[houses[i].startind:houses[i].endind, 5], 0)
        ev = np.sum(dataInTimeRangeSorted[:, 7], 0) + np.sum(dataInTimeRangeSorted[:, 8], 0)
        bat = np.sum(dataInTimeRangeSorted[:, 6], 0)
        
        if pv != 0:
            houses[i].pv = 1
        if bat != 0:
            houses[i].bat = 1
        if ev != 0:
            houses[i].ev = 1
            
    # Single Large House [N_PV_Bat_EV, N_PV_Bat, N_PV_EV, N_Bat_EV, N_PV, N_Bat, N_EV, N_None]
    #Creating object for desired output
    output_house = Home(0 ,0)
    if Type == 1:
        output_house.pv = 1
        output_house.ev = 1
        output_house.bat = 1
    elif Type == 2:
        output_house.pv = 1
        output_house.ev = 0
        output_house.bat = 1
    elif Type == 3:
        output_house.pv = 1
        output_house.ev = 1
        output_house.bat = 0
    elif Type == 4:
        output_house.pv = 0
        output_house.ev = 1
        output_house.bat = 1
    elif Type == 5:
        output_house.pv = 1
        output_house.ev = 0
        output_house.bat = 0
    elif Type == 6:
        output_house.pv = 0
        output_house.ev = 0
        output_house.bat = 1
    elif Type == 7:
        output_house.pv = 0
        output_house.ev = 1
        output_house.bat = 0
    elif Type == 8:
        output_house.pv = 0
        output_house.ev = 0
        output_house.bat = 0

#Creating default values to check against the desired output
    default1 = Home(0,0,1,1,1)  #PV, Bat, EV
    default2 = Home(0,0,1,1,0)  #PV, Bat
    default3 = Home(0,0,1,0,1)  #PV, EV
    default4 = Home(0,0,0,1,1)  #Bat, EV
    default5 = Home(0,0,1,0,0)  #PV
    default6 = Home(0,0,0,1,0)  #Bat
    default7 = Home(0,0,0,0,1)  #EV
    default8 = Home(0,0,0,0,0)  #None
        
    prio = {'1': 0, 'ind1':0, '2': 0, 'ind2':0,'3': 0, 'ind3':0,'4': 0, 'ind4':0,'5': 0, 'ind5':0,'6': 0, 'ind6':0,'7': 0, 'ind7':0,'8': 0, 'ind8':0,}
    
    if (len(N_House_Vector) == 1):   #Single house with type specified in parameter
        if Type == 1: 
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default4):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default3):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default7):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default2):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default6):
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default5):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    prio['Prio'] = 9
                    prio['Ind'] = -1
        elif Type == 2:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default4):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default7):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default6):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default5): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default7):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        elif Type == 3:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default4):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default7):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default5):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default2): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default6):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        elif Type == 4:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default7):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default3):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default2):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default6): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default5):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        elif Type == 5:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default2):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default3):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default4):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default6): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default7):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        elif Type == 6:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default2):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default4):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default3):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default5): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default7):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        elif Type == 7:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default3):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default4):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default2):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default5): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default6):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default8):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        elif Type == 8:
            for i in range(len(N_House_Vector)):
                if output_house.equals(houses[i]):
                    prio['1'] = 1
                    prio['ind1'] = i
                elif houses[i].equals(default1):
                    prio['2'] = 2
                    prio['ind2'] = i
                elif houses[i].equals(default2):
                    prio['3'] = 3
                    prio['ind3'] = i
                elif houses[i].equals(default3):
                    prio['4'] = 4
                    prio['ind4'] = i
                elif houses[i].equals(default4):
                    prio['5'] = 5
                    prio['ind5'] = i
                elif houses[i].equals(default5): 
                    prio['6'] = 6
                    prio['ind6'] = i
                elif houses[i].equals(default6):
                    prio['7'] = 7
                    prio['ind7'] = i
                elif houses[i].equals(default7):
                    prio['8'] = 8
                    prio['ind8'] = i
                else:
                    print("File not found")
        
        PecanStreetOutput = saveOutput(prio, houses)    #Output is a house object that matches the highest priority possible
    
    #Smart Community - [N_PV_Bat, N_Bat, N_PV, N_None] format of N_House_Vector
    elif len(N_House_Vector) == 4:
        PecanStreetCommunityOutput = []
        housecount = sum(N_House_Vector)
        outputcount = 0
        n1 = N_House_Vector[0]
        n2 = n1 + N_House_Vector[1]
        n3 = n2 + N_House_Vector[2]
        n4 = n3 + N_House_Vector[3]
        
        while outputcount < housecount:     #add duplicate houses on multiple iterations if needed
            if housecount == outputcount:
                break
            for i in range(len(houses)):     
                if outputcount < n1:
                    if houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                elif outputcount < n2:
                    if houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                        
                elif outputcount < n3:
                    if houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                
                elif outputcount < n4:
                    if houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                        
                PecanStreetCommunityOutput.append(PecanStreetOutput)    #Output is a list of house objects that match the highest priority with a house number attached to it
                if outputcount == housecount:
                    break
                
                
    #Smart Community - [N_PV_Bat_EV, N_PV_Bat, N_PV_EV, N_Bat_EV, N_PV, N_Bat, N_EV, N_None]
    elif len(N_House_Vector) == 8:
        PecanStreetCommunityOutput = []
        housecount = sum(N_House_Vector)
        outputcount = 0
        
        n1 = N_House_Vector[0]
        n2 = n1 + N_House_Vector[1]
        n3 = n2 + N_House_Vector[2]
        n4 = n3 + N_House_Vector[3]
        n5 = n4 + N_House_Vector[4]
        n6 = n5 + N_House_Vector[5]
        n7 = n6 + N_House_Vector[6]
        n8 = n7 + N_House_Vector[7]
        
        while outputcount <= housecount:
            if outputcount == housecount:
                    break
            for i in range(len(houses)):
                if outputcount < n1:    #PV ,Bat, and EV
                    if houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                    
                elif outputcount < n2:    #PV, Bat
                    if houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                    
                elif outputcount < n3:    #PV, EV
                    if houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                    
                elif outputcount < n4:    #Bat, EV
                    if houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                
                elif outputcount < n5:     #PV
                    if houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                    
                elif outputcount < n6:    #Bat
                    if houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                    
                elif outputcount < n7:    #EV
                    if houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                    
                
                elif outputcount < n8:    #None
                    if houses[i].equals(default8):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default1):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default2):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default3):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default4):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default5):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default6):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    elif houses[i].equals(default7):
                        PecanStreetOutput = [houses[i]]
                        outputcount += 1
                        print(houses[i])
                    else:
                        print("No file found")
                
                PecanStreetCommunityOutput.append(PecanStreetOutput)
                if outputcount == housecount:
                        break
    
    #Converting list to a 3D array
    arraylist = []
    for i in range(len(PecanStreetCommunityOutput)):
        arraylist.append(dataInTimeRangeSorted[PecanStreetCommunityOutput[i][0].startind:PecanStreetCommunityOutput[i][0].endind+1, :])
    PecanStreetCommunityOutputArray = np.stack((arraylist))
    return PecanStreetCommunityOutputArray
       

    #Test Code
# class HEMS():
#     def __init__(self, sm, sd, st, em, ed, et):
#         self.StartMonth = sm
#         self.StartDay = sd
#         self.StartTime = st
#         self.EndMonth = em
#         self.EndDay = ed
#         self.EndTime = et
        
# class Simulation():
#     def __init__(self, fileres):
#         self.FileRes = fileres
        
        
# HEMSobj = HEMS(1,1,0,1,3,0)     #Need to input decimal times that are exactly equal to file
# SimParam = Simulation(10)
# Folderpath = os.path.abspath('PecanStreet_TestData(1)')     #Need to give the name of the folder which contains pecan street data
# housevec = [0,1,0,0,1,0,1,1]
# Type = 1
# outfile = "Fileoutput.xlsx"

# PecanStreetData = PecanStreet_Data_Extractor(HEMSobj, SimParam, Folderpath, housevec, Type, outfile)
        
    
    