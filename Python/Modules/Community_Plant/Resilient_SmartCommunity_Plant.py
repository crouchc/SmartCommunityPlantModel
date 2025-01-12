#Conversion of HEMS_Plant code to more OOP style
# Author: Chris Crouch and Ninad Gaikwad

#import libraries
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#import functions

#class creation
class SmartCommunity_Plant:
    #inputs X_k_Plant,W_k_Plant,U_k,HEMSPlant_Params,HEMSHouse_Params,Community_Params,Simulation_Params
    
    #-------------------------- Location Information -------------------------%

    Location_Name='Gainesville_Fl_USA'
    hem=-1        # 1 - Eastern Hemisphere ; -1 - Western Hemisphere
    Lat=18.17     # Decimal Deg
    Long= 66.74   # Decimal Deg
    TimeZone=4    # Hours
    Ltm=60        # Deg Decimal - Time Meridian (Atlantic Standard Time)
    
    def __init__(self, X_k_Plant, Community_Params, Simulation_Params, HEMSPlant_Params = {'Location_Name':Location_Name, }):
        
        #From HEMS_CommunityHouse_Parameter_Generator
        
        #----------------------- House Thermal Specifications --------------------%

        # Thermal Resistances (K/W)
        R_w=0.0134             # External Wall
        R_attic=0.0235         # Attic
        R_roof=0.00156         # Roof
        R_im=0.00171           # Internal Mass
        R_win=0.021            # Windows
        
        # Thermal Capacitances (J/K)
        C_w=10383364           # External Wall
        C_attic=704168         # Attic
        C_im=23396403         # Internal Mass
        C_in=8665588           # Intdoor Air
        C1=0.691
        C2=0.784
        C3=0.1
        
        # Internal Heat Load [W]
        Human_Num=4
        Human_Heat=100         # 2000 kCal/Day = 2000*10^3*4.18 J/Day = 96.91 W
        Appliance_Heat=60+65+100
        
        Q_ihl=Human_Num*Human_Heat+Appliance_Heat # [W] Includes Humans and all internal appliances which contribute to the Heat gain/loss of the house
        
        Q_ac=0                 # [W] AC Load
        
        # Ventilation and Infiltration Heat Load
        Cp=1                   # @ 300K, 1atm [kJ/kg K] Specific Heat of Air
        V=0                    # Mass Flow Rate (m^3/s)
        Den_Air=1.18           # @ 300K, 1atm [kg/m^3] Air Density
        C_oew=0.01             # Coefficient used to scale the wind speed to the infiltration rate
        
        # Q_solar
        SHGC=0.8              # From ASHRAE - Fundamentals
        
        # Windows Roofs and Walls Orientation
        Alpha_w=0.9            # Radiation absorption Coefficient
        Alpha_r=0.9            # Radiation absorption Coefficient
        # Wall
        Area_w=[33,33,33,33]   # m^(2)
        Tilt_w=[90,90,90,90]   # Deg (Angle Between wall Surface and Ground Surface measured from Ground Surface)
        Azi_w=[0,90,-90,180]   # Deg (Angle of the wall Surface in the E-W plane wrt N-S axis [S-E-N -- 0-90-180 ; S-W-N -- 0-(-90)-(-180) ] )
        # Roof
        Area_r=[100]           # m^(2)
        Tilt_r=[0]             # Deg (Angle Between roof Surface and Ground Surface)
        Azi_r=[0]              # Deg (Angle of the roof Surface in the E-W plane wrt N-S axis [S-E-N -- 0-90-180 ; S-W-N -- 0-(-90)-(-180) ] )
        # Window
        Area_win=[10,10,10,10] # m^(2)
        Tilt_win=[90,90,90,90] # Deg (Angle Between window Surface and Ground Surface)
        Azi_win=[0,90,-90,180] # Deg (Angle of the window Surface in the E-W plane wrt N-S axis [S-E-N -- 0-90-180 ; S-W-N -- 0-(-90)-(-180) ] )
    
        
        #-------------------------- AC Specifications --------------------------#
        
        # Controller Load
        ACLoad_Num=1
        ACLoad_Power=3000 # Tesla Site Value
        
        AC_VolatageDip=0.3 # 30# Volage Dip at Startup causes 30# Current Dip
        AC_StartUp_LRA_Factor=6 # LRA - Locked Rotor Current usually 3-8 times rated current
        ACLoad_StartUp_Power=(1-AC_VolatageDip)^(2)*AC_StartUp_LRA_Factor*ACLoad_Power/1000 # In kW
        
        AC_COP=3.33
        T_AC_Base=24
        T_AC_DeadBand = 1
        
        T_AC_max=T_AC_Base+T_AC_DeadBand
        T_AC_min=T_AC_Base-T_AC_DeadBand
        
        T_AC= T_AC_Base
        
        AC_Indicator=1
        AC_Indicator1=1
        
        E_AC= ACLoad_Num*ACLoad_Power*Simulation_StepSize*(1/1000)
        
        #-------------------------- PV Specifications --------------------------#
        
        # Tesla Module SC325
        
        PV_TotlaModules_Num=31  # User Input - 10kW system -- 31 Modules
        PV_RatedPower=325      # User Input Watts
        PV_TempCoeff=-0.31     # User Input #/DegC
        GHI_Std = 1000         # kW/m^2
        Temp_Std = 25          # Deg C
        Eff_Inv=0.9            # Inverter Efficiency
           
        # Faiman Model for Module Temperature Computation
        Uo=25                  # Values of U_{0} varied from 23.5 to 26.5 with a combined fit = 25 W/m^{2}K
        U1=6.84                # Values of U_{1} varied from 6.25 to 7.68 with a combined fit = 6.84 W/m^{2}K
        
        PV_Total_Power = PV_TotlaModules_Num * PV_RatedPower
        
        #-------------------------- Battery Specifications --------------------------#
        
                   # User Input Volts
        DOD=0                        # Depth of Discharge (For logetivity)
        Eff_Charging_Battery=0.9       # Battery Charging Efficiency
        Eff_Discharging_Battery=0.9    # Battery Discharging Efficiency
        N1=1                           # User Input - Battery Max Changing Factor
        
        MaxRate_Charging=7.6
        
        P_AC=(ACLoad_Num*ACLoad_Power)*(1/1000)
        
        # MaxRate_Discharging=Bat_TotalStrings_Num*(Bat_Capacity2/C_Hours2)*(System_Voltage)*(1/1000) # kWatts
        MaxRate_Discharging=5
        MaxRate_Discharging_StartUp=7
        
        Battery_Energy_Max = 13.5*N1
        Battery_Energy_Min=Battery_Energy_Max*DOD
        
        #-------------------------- EV Battery Specifications --------------------------#
        
        DOD_EV=0                        # Depth of Discharge (For logetivity)
        Eff_Charging_Battery_EV=0.9       # Battery Charging Efficiency
        Eff_Discharging_Battery_EV=0.9    # Battery Discharging Efficiency
        N1_EV=1                           # User Input - Battery Max Changing Factor
        
        MaxRate_Charging_EV=7.6
        
        P_AC_EV=(ACLoad_Num*ACLoad_Power)*(1/1000)
        
        # MaxRate_Discharging=Bat_TotalStrings_Num*(Bat_Capacity2/C_Hours2)*(System_Voltage)*(1/1000) # kWatts
        MaxRate_Discharging_EV=5
        MaxRate_Discharging_StartUp_EV=7
        
        Battery_Energy_Max_EV = 13.5*N1_EV
        Battery_Energy_Min_EV=Battery_Energy_Max_EV*DOD_EV
        CarPresent = 0; #Is the car pressent 0 = no, 1 = yes
        
        HEMSPlant_Params = {} # Empty Dict

        HEMSPlant_Params['Location_Name'] = Location_Name
        HEMSPlant_Params['hem'] = hem
        HEMSPlant_Params['Lat'] = Lat
        HEMSPlant_Params['Long'] = Long
        HEMSPlant_Params['TimeZone'] = TimeZone
        HEMSPlant_Params['Ltm'] = Ltm
        
        HEMSPlant_Params['ACLoad_Num'] = ACLoad_Num
        HEMSPlant_Params['ACLoad_Power'] = ACLoad_Power
        HEMSPlant_Params['AC_COP'] = AC_COP
        HEMSPlant_Params['T_AC_Base'] = T_AC_Base
        HEMSPlant_Params['T_AC_DeadBand'] = T_AC_DeadBand
        HEMSPlant_Params['AC_Indicator'] = AC_Indicator
        HEMSPlant_Params['AC_Indicator1'] = AC_Indicator1
        HEMSPlant_Params['E_AC'] = E_AC
        HEMSPlant_Params['T_AC_max'] = T_AC_max
        HEMSPlant_Params['T_AC_min'] = T_AC_min
        HEMSPlant_Params['ACLoad_StartUp_Power'] = ACLoad_StartUp_Power
        
        HEMSPlant_Params['PV_TotlaModules_Num'] = PV_TotlaModules_Num
        HEMSPlant_Params['PV_RatedPower'] = PV_RatedPower
        HEMSPlant_Params['PV_TempCoeff'] = PV_TempCoeff
        HEMSPlant_Params['GHI_Std'] = GHI_Std
        HEMSPlant_Params['Temp_Std'] = Temp_Std
        HEMSPlant_Params['Eff_Inv'] = Eff_Inv
        HEMSPlant_Params['Uo'] = Uo
        HEMSPlant_Params['U1'] = U1
        
        HEMSPlant_Params['DOD'] = DOD
        HEMSPlant_Params['Eff_Charging_Battery'] = Eff_Charging_Battery
        HEMSPlant_Params['Eff_Discharging_Battery'] = Eff_Discharging_Battery
        HEMSPlant_Params['N1'] = N1
        HEMSPlant_Params['MaxRate_Charging'] = MaxRate_Charging
        HEMSPlant_Params['MaxRate_Discharging'] = MaxRate_Discharging
        HEMSPlant_Params['Battery_Energy_Max'] = Battery_Energy_Max
        HEMSPlant_Params['Battery_Energy_Min'] = Battery_Energy_Min
        HEMSPlant_Params['MaxRate_Discharging_StartUp'] = MaxRate_Discharging_StartUp
        
        HEMSPlant_Params['DOD_EV'] = DOD_EV
        HEMSPlant_Params['Eff_Charging_Battery_EV'] = Eff_Charging_Battery_EV
        HEMSPlant_Params['Eff_Discharging_Battery_EV'] = Eff_Discharging_Battery_EV
        HEMSPlant_Params['N1_EV'] = N1_EV
        HEMSPlant_Params['MaxRate_Charging_EV'] = MaxRate_Charging_EV
        HEMSPlant_Params['MaxRate_Discharging_EV'] = MaxRate_Discharging_EV
        HEMSPlant_Params['Battery_Energy_Max_EV'] = Battery_Energy_Max_EV
        HEMSPlant_Params['Battery_Energy_Min_EV'] = Battery_Energy_Min_EV
        HEMSPlant_Params['MaxRate_Discharging_StartUp_EV'] = MaxRate_Discharging_StartUp_EV
        HEMSPlant_Params['CarPresent'] = CarPresent
        
        #-------------------------- House Specifications -------------------------#
        
        HEMSHouse_Params = [] # Empty Struct
        
        HEMSHouse_Params['R_w'] = R_w
        HEMSHouse_Params['R_attic'] = R_attic
        HEMSHouse_Params['R_roof'] = R_roof
        HEMSHouse_Params['R_im'] = R_im
        HEMSHouse_Params['R_win'] = R_win
        HEMSHouse_Params['C_w'] = C_w
        HEMSHouse_Params['C_attic'] = C_attic
        HEMSHouse_Params['C_im'] = C_im
        HEMSHouse_Params['C_in'] = C_in
        HEMSHouse_Params['C1'] = C1
        HEMSHouse_Params['C2'] = C2
        HEMSHouse_Params['C3'] = C3
        HEMSHouse_Params['Human_Num'] = Human_Num
        HEMSHouse_Params['Human_Heat'] = Human_Heat
        HEMSHouse_Params['Appliance_Heat'] = Appliance_Heat
        HEMSHouse_Params['Q_ac'] = AC_COP*ACLoad_Power
        HEMSHouse_Params['Cp'] = Cp
        HEMSHouse_Params['V'] = V
        HEMSHouse_Params['Den_Air'] = Den_Air
        HEMSHouse_Params['C_oew'] = C_oew
        HEMSHouse_Params['SHGC'] = SHGC
        HEMSHouse_Params['Alpha_w'] = Alpha_w
        HEMSHouse_Params['Alpha_r'] = Alpha_r
        HEMSHouse_Params['Area_w'] = Area_w
        HEMSHouse_Params['Tilt_w'] = Tilt_w
        HEMSHouse_Params['Azi_w'] = Azi_w
        HEMSHouse_Params['Area_r'] = Area_r
        HEMSHouse_Params['Tilt_r'] = Tilt_r
        HEMSHouse_Params['Azi_r'] = Azi_r
        HEMSHouse_Params['Area_win'] = Area_win
        HEMSHouse_Params['Tilt_win'] = Tilt_win
        HEMSHouse_Params['Azi_win'] = Azi_win
        
        HEMSHouse_Params['ACLoad_Num'] = ACLoad_Num
        HEMSHouse_Params['ACLoad_Power'] = ACLoad_Power
        HEMSHouse_Params['AC_COP'] = AC_COP
        HEMSHouse_Params['T_AC_Base'] = T_AC_Base
        HEMSHouse_Params['T_AC_DeadBand'] = T_AC_DeadBand
        HEMSHouse_Params['AC_Indicator'] = AC_Indicator
        HEMSHouse_Params['AC_Indicator1'] = AC_Indicator1
        
        X_k_Plant = X_k_Plant
        # From W_k_Plant
        Weather_k_Plant=W_k_Plant['Weather_k_Plant']
        LoadData_k_Plant=W_k_Plant['LoadData_k_Plant']
        
        # Variable declaration 
        GHI=Weather_k_Plant['GHI']
        DNI=Weather_k_Plant['DNI']
        T_am=Weather_k_Plant['T_am']
        Ws=Weather_k_Plant['Ws']
        DateTime_Matrix = Weather_k_Plant['DateTime_Matrix']
        
        E_Load_Desired=LoadData_k_Plant['E_Load_Desired']
        E_LoadData=LoadData_k_Plant['E_LoadData']
        
        # From HEMSPlant_Params
        T_AC_Base=HEMSPlant_Params['T_AC_Base']
        T_AC_DeadBand=HEMSPlant_Params['T_AC_DeadBand']
        ACLoad_StartUp_Power=HEMSPlant_Params['ACLoad_StartUp_Power']
        
        PV_TotlaModules_Num=HEMSPlant_Params['PV_TotlaModules_Num']
        PV_RatedPower=HEMSPlant_Params['PV_RatedPower']
        PV_TempCoeff=HEMSPlant_Params['PV_TempCoeff']
        GHI_Std=HEMSPlant_Params['GHI_Std']
        Temp_Std=HEMSPlant_Params['Temp_Std']
        Eff_Inv=HEMSPlant_Params['Eff_Inv']
        Uo=HEMSPlant_Params['Uo']
        U1=HEMSPlant_Params['U1']
        
        Eff_Charging_Battery=HEMSPlant_Params['Eff_Charging_Battery']
        Eff_Discharging_Battery=HEMSPlant_Params['Eff_Discharging_Battery']
        
        MaxRate_Charging=HEMSPlant_Params['MaxRate_Charging']
        MaxRate_Discharging=HEMSPlant_Params['MaxRate_Discharging']
        Battery_Energy_Max=HEMSPlant_Params['Battery_Energy_Max']
        Battery_Energy_Min=HEMSPlant_Params['Battery_Energy_Min']
        MaxRate_Discharging_StartUp=HEMSPlant_Params['MaxRate_Discharging_StartUp']
        
        E_AC=HEMSPlant_Params['E_AC']
        
        # From Community_Params
        N_House=Community_Params['N_House']
        N_PV_Bat=Community_Params['N_PV_Bat']
        N_Bat=Community_Params['N_Bat']
        N_PV=Community_Params['N_PV']
        N_None=Community_Params['N_None']   
        
        # From Simulation_Params
        Simulation_StepSize=Simulation_Params['Simulation_StepSize']
                
        #------------------------- Load Energy at DC Side ------------------------
        E_Load_Desired_DC=E_Load_Desired/Eff_Inv
    #is this dividing the second array by Eff_inv or both arrays, and horizontal concatenation?
        E_LoadData_DC=np.hstack((E_LoadData[:,1,1:9], (E_LoadData[:,1,9+1:E_LoadData.shape[2]]/Eff_Inv)))
        
        #------------------- Getting Total PV Energy Available -------------------

        # Creating Input for PV Energy Available Generator
        PVEnergy_Generator_Input = {}
        PVEnergy_Generator_Input['PV_TotlaModules_Num']=PV_TotlaModules_Num
        PVEnergy_Generator_Input['PV_RatedPower']=PV_RatedPower
        PVEnergy_Generator_Input['PV_TempCoeff']=PV_TempCoeff
        
        PVEnergy_Generator_Input['T_am']=T_am
        PVEnergy_Generator_Input['GHI']=GHI
        PVEnergy_Generator_Input['Ws']=Ws
        
        PVEnergy_Generator_Input['Uo']=Uo
        PVEnergy_Generator_Input['U1']=U1
        
        PVEnergy_Generator_Input['Temp_Std']=Temp_Std
        PVEnergy_Generator_Input['GHI_Std']=GHI_Std
        
        PVEnergy_Generator_Input['Simulation_StepSize']=Simulation_StepSize
        
        # Computing Total Available PV Energy
        [PVEnergy_Available] = __HEMS_PVEnergy_Available_Generator(PVEnergy_Generator_Input)
        
        Total_PVEnergy_Available = (N_PV_Bat+N_PV)*PVEnergy_Available
        
        #---------------------- Computing Energy Mismatch ------------------------%

        # Battery Energy Available for Discharging dispatch
        E_Bat_Discharging_Dispatch=np.zeros((N_House,1,1))
        
        for i in range(N_PV_Bat + N_Bat): # For Battery installed Houses
            minval = min(MaxRate_Discharging*Simulation_StepSize,(X_k_Plant[i,1,4]-Battery_Energy_Min)*Eff_Discharging_Battery)
            E_Bat_Discharging_Dispatch[i,1,1] = U_k[i,1,2]*minval
            
        # Battery Energy Available for Charging dispatch
        E_Bat_Charging_Dispatch = np.zeros(N_House,1,1)
        
        for i in range(N_PV_Bat+N_Bat): # For Battery installed Houses
            minval = min(MaxRate_Charging*Simulation_StepSize,(Battery_Energy_Max-(X_k_Plant[i,1,4]))/Eff_Charging_Battery)
            E_Bat_Charging_Dispatch[i,1,1]=(U_k[i,1,1])*minval
        
        # Battery Discharging Indices
    # finding values that equal 1?
        BatteryDischarging_Indices = np.where(U_k[:,1,2] == 1)
        Battery_AboveMin_Indices = np.where(X_k_Plant[:,1,4] > Battery_Energy_Min)
    #fix intersection
        Battery_ActualDischarging_Indices = BatteryDischarging_Indices.intersection(Battery_AboveMin_Indices)
        
        # % Battery Charging Indices
        BatteryCharging_Indices = np.where(U_k[:,1,1] == 1)
        Battery_BelowMax_Indices = np.where(X_k_Plant[:,1,4] < Battery_Energy_Max)
    #fix intersction
        Battery_ActualCharging_Indices = BatteryCharging_Indices.intersection(Battery_BelowMax_Indices)
        
        # Computing Total energy desired by other loads (Not ACs)
        OtherLoad_Energy_Desired = np.zeros((N_House,1,1))
        for i in range(N_House): # For each house
    #check if E_LoadData_DC.shape works
            OtherLoad_Energy_Desired[i,1,1]=U_k[i,1,4:11]*E_LoadData_DC[i,1,9+1:E_LoadData_DC.shape[2]]
        
    #what is being summed here?
        Total_OtherLoad_Energy_Desired = np.sum(OtherLoad_Energy_Desired[:,:,3])
        
        # Total energy Desired
    #check if the sum function is working correctly for next two lines
        TotalEnergy_Desired = ((E_AC/Eff_Inv)*(sum(U_k[:,1,3])))+Total_OtherLoad_Energy_Desired+sum(E_Bat_Charging_Dispatch[Battery_ActualCharging_Indices,1,1])
        
        # Energy Mismatch
        AvailableEnergy = Total_PVEnergy_Available+sum(E_Bat_Discharging_Dispatch[Battery_ActualDischarging_Indices,1,1])
        E_Mis = AvailableEnergy-TotalEnergy_Desired
        
        #------------ Computing Total Startup Power Required for ACs -------------

        # Computing Turning On ACs
        TurningOn_AC_Vector=U_k[:,1,3]-X_k_Plant[:,1,30]
    #Replace find function
        TurningOn_AC_Indices = np.where(TurningOn_AC_Vector == 1)
        Num_TurningOn_AC=len(TurningOn_AC_Indices)

        # Computing Quantities for Energy and Power Constraints
    #does python have intersect and find functions
        val = np.where(X_k_Plant[:,1,4] > Battery_Energy_Min)
        Battery_CapableofDischarge_Indices = (np.where(U_k[:,1,2])).intersection(val)
        TotalPower_Available_Bat = len(Battery_CapableofDischarge_Indices)*(MaxRate_Discharging_StartUp)
        TotalPower_Available_PV = (Total_PVEnergy_Available)/(Simulation_StepSize)
        Total_StartUpPower_Available = TotalPower_Available_Bat+TotalPower_Available_PV
        Total_StartUpPower_AC = Num_TurningOn_AC*ACLoad_StartUp_Power

        # Computing PV Energy Available for each House with PV

        for i in range(N_House):
            # Computing PV Energy Available
            if (i <= N_PV_Bat) or ((i > (N_PV_Bat + N_Bat)) and (i <= (N_PV_Bat + N_Bat + N_PV))): # For PV installed Houses
                X_k_Plant[i,1,1] = PVEnergy_Available
                
        # Setting up Weather Dtata Struct for House Thermal Dynamics Simulation

        # Setting up HEMSWeatherData_Output1
        HEMSWeatherData_Output1 = {}
        HEMSWeatherData_Output1['Ws']=Ws
        HEMSWeatherData_Output1['T_am']=T_am
        HEMSWeatherData_Output1['GHI']=GHI
        HEMSWeatherData_Output1['DNI']=DNI
        HEMSWeatherData_Output1['DateTime_Matrix']=DateTime_Matrix
        
        # To be Continued.........................................................
        
        
        
    def __HEMS_PVEnergy_Available_Generator(self, PVEnergy_Generator_Input):
        # HEMS_PVEnergyAvailable_Generator - PV Energy Model

        # Getting desired Data from Input - Structs
        
        PV_TotlaModules_Num = PVEnergy_Generator_Input['PV_TotlaModules_Num']
        PV_RatedPower=PVEnergy_Generator_Input['PV_RatedPower']
        PV_TempCoeff=PVEnergy_Generator_Input['PV_TempCoeff']
        
        T_am=PVEnergy_Generator_Input['T_am']
        GHI=PVEnergy_Generator_Input['GHI']
        Ws=PVEnergy_Generator_Input['Ws']
        
        Uo=PVEnergy_Generator_Input['Uo']
        U1=PVEnergy_Generator_Input['U1']
        
        Temp_Std=PVEnergy_Generator_Input['Temp_Std']
        GHI_Std=PVEnergy_Generator_Input['GHI_Std']
        
        Simulation_StepSize=PVEnergy_Generator_Input['Simulation_StepSize']
        
        # Computing Total Available PV Energy

        PV_Total_Power = PV_TotlaModules_Num * PV_RatedPower
        
        PVEnergy_Available = np.empty((len(GHI)))
        
        for i in range(len(GHI)):
            # Faiman's Module Temperature Model
            Tm = T_am[i] + ((GHI[i])/(Uo+(U1*Ws[i])))
            
            # Power generated in one Module   
            PVEnergy_Available[i] = PV_Total_Power * (1 + ((PV_TempCoeff/100)* Tm - Temp_Std)) * (GHI[i]/GHI_Std) * Simulation_StepSize/1000 

    

    def HEMS_Plant(self, X_k_Plant):
        #initialize W_k_Plant
        
        
        # To be Continued.........................................................
        
        
    def __HEMS_HouseRCModel(self,HEMSHouse_Input,HEMSWeatherData_Output):
        
        
        
        # To be Continued.........................................................        
        
        
    def HEMS_Plant_FigurePlotter(self, HEMS_Plant_FigurePlotter_Input):
        EToP_Converter= (60/10) # kWh --> W
        
        ## HEMS_Plant_FigurePlotter - Plotting Figures for Controller and Plant

        ## Getting the desired data from the HEMS_Plant_Baseline_FigurePlotter_Input - Struct

        #----------------HEMS_Plant_Baseline_FigurePlotter_Input------------------#
        X_k_Plant_History = HEMS_Plant_FigurePlotter_Input['X_k_Plant_History']
        U_k_History = HEMS_Plant_FigurePlotter_Input['U_k_History']
        E_LoadData = HEMS_Plant_FigurePlotter_Input['E_LoadData']
        E_Load_Desired = HEMS_Plant_FigurePlotter_Input['E_Load_Desired']
        HEMSWeatherData_Output = HEMS_Plant_FigurePlotter_Input['HEMSWeatherData_Output']
        HEMSPlant_Params = HEMS_Plant_FigurePlotter_Input['HEMSPlant_Params']
        Community_Params = HEMS_Plant_FigurePlotter_Input['Community_Params']
        Baseline_Output_Images_Path = HEMS_Plant_FigurePlotter_Input['Baseline_Output_Images_Path']
        Single_House_Plotting_Index = HEMS_Plant_FigurePlotter_Input['Single_House_Plotting_Index']
        Simulation_Params = HEMS_Plant_FigurePlotter_Input['Simulation_Params']
        
        #-----------------------HEMSWeatherData_Output----------------------------#
        Ws=HEMSWeatherData_Output['Ws']
        T_am=HEMSWeatherData_Output['T_am']
        GHI=HEMSWeatherData_Output['GHI']
        DNI=HEMSWeatherData_Output['DNI']
        DateTimeVector=HEMSWeatherData_Output['DateTimeVector']
        DateTime_Matrix=HEMSWeatherData_Output['DateTime_Matrix']

        #---------------------------HEMSPlant_Params------------------------------#

        E_AC=HEMSPlant_Params['E_AC']
        T_AC_max=HEMSPlant_Params['T_AC_max']
        T_AC_min=HEMSPlant_Params['T_AC_min']
        ACLoad_StartUp_Power=HEMSPlant_Params['ACLoad_StartUp_Power']
        Eff_Inv=HEMSPlant_Params['Eff_Inv']

        Battery_Energy_Max=HEMSPlant_Params['Battery_Energy_Max']
        Battery_Energy_Min=HEMSPlant_Params['Battery_Energy_Min']
        MaxRate_Charging=HEMSPlant_Params['MaxRate_Charging']
        MaxRate_Discharging=HEMSPlant_Params['MaxRate_Discharging']
        Eff_Charging_Battery=HEMSPlant_Params['Eff_Charging_Battery']
        Eff_Discharging_Battery=HEMSPlant_Params['Eff_Discharging_Battery']
        MaxRate_Discharging_StartUp=HEMSPlant_Params['MaxRate_Discharging_StartUp']

        #---------------------------Community_Params['-----------------------------#
        N_House=Community_Params['N_House']
        N_PV_Bat=Community_Params['N_PV_Bat']
        N_Bat=Community_Params['N_Bat']
        N_PV=Community_Params['N_PV']
        N_None=Community_Params['N_None'] 

        #---------------------------Simulation_Params-----------------------------#

        Simulation_StepSize=Simulation_Params['Simulation_StepSize']
        
        # Basic Computation and Generating plotable quantities

        # House Numbers
        N1=N_PV_Bat
        N2=N_Bat
        N3=N_PV
        N4=N_None

        # Truncating Plant History
        X_k_Plant_History=X_k_Plant_History[:,1:X_k_Plant_History.shape[0],:]
        
        # PV Quantities - Individual Houses
        House_PV_E_Available=X_k_Plant_History[:,:,1]
        House_PV_E_Used=X_k_Plant_History[:,:,2]
        House_PV_E_UnUsed=X_k_Plant_History[:,:,3]
        
        # Battery Quantities - Individual Houses
        House_Bat_E_State=X_k_Plant_History[:,:,4]
        House_Bat_E_Charging=X_k_Plant_History[:,:,5]
        House_Bat_E_Discharging=X_k_Plant_History[:,:,6]
        
        # House Temperature Quantities - Individual Houses
        House_Temprature=X_k_Plant_History[:,:,7]
        
        # House Energy Quantities - Individual Houses
        House_Bat_E_OtherLoad_Desired=E_Load_Desired[:,:,1]
        House_Bat_E_ACLoad_Desired=U_k_History[:,:,3] * [E_AC/Eff_Inv]  #***
        House_Bat_E_TotalLoad_Desired=House_Bat_E_OtherLoad_Desired + House_Bat_E_ACLoad_Desired
        
        House_Bat_E_OtherLoad_Actual=X_k_Plant_History[:,:,12]
        House_Bat_E_ACLoad_Actual=X_k_Plant_History[:,:,11]
        House_Bat_E_TotalLoad_Actual=House_Bat_E_OtherLoad_Actual+House_Bat_E_ACLoad_Actual

        # House Controller Quantities - Individual Houses
        House_Bat_Controller_Charging_Desired=U_k_History[:,:,1]
        House_Bat_Controller_Discharging_Desired=U_k_History[:,:,2]

        House_AC_Controller_TurnOn_Desired=U_k_History[:,:,3]
        House_AC_Controller_TurnOn_Actual=X_k_Plant_History[:,:,21]

        # PV Quantities - All Houses [Addup]
        Community_PV_E_Available=sum(X_k_Plant_History[:,:,1],0)
        Community_PV_E_Used=sum(X_k_Plant_History[:,:,2],0)
        Community_PV_E_UnUsed=sum(X_k_Plant_History[:,:,3],0)

        # Battery Quantities - Individual Houses - All Houses [Addup]
        Community_Bat_E_State=sum(X_k_Plant_History[:,:,4],0)
        Community_Bat_E_Charging=sum(X_k_Plant_History[:,:,5],0)
        Community_Bat_E_Discharging=sum(X_k_Plant_History[:,:,6],0)

        # House Temperature Quantities - Individual Houses - All Houses [Average]
        Community_Temprature=mean[X_k_Plant_History[:,:,7],0]

        # House Energy Quantities - Individual Houses - All Houses [Addup]
        Community_Bat_E_OtherLoad_Desired=sum(E_Load_Desired[:,:,1],0)
        Community_Bat_E_ACLoad_Desired=sum(House_Bat_E_ACLoad_Desired[:,:,1],0)
        Community_Bat_E_TotalLoad_Desired=Community_Bat_E_ACLoad_Desired+Community_Bat_E_OtherLoad_Desired

        Community_Bat_E_OtherLoad_Actual=sum(X_k_Plant_History[:,:,12],0)
        Community_Bat_E_ACLoad_Actual=sum(X_k_Plant_History[:,:,11],0)
        Community_Bat_E_TotalLoad_Actual=Community_Bat_E_OtherLoad_Actual+Community_Bat_E_ACLoad_Actual

        # House Controller Quantities - Individual Houses - All Houses [Addup]
        Community_Bat_Controller_Charging_Desired=sum(U_k_History[:,:,1],0)
        Community_Bat_Controller_Discharging_Desired=sum(U_k_History[:,:,2],0)

        Community_AC_Controller_TurnOn_Desired=sum(U_k_History[:,:,3],0)
        Community_AC_Controller_TurnOn_Actual=sum(X_k_Plant_History[:,:,21],0)
        
        # Computing House and Community Battery SoC
        House_Bat_SoC=(((House_Bat_E_State)-Battery_Energy_Min)/(Battery_Energy_Max-Battery_Energy_Min))*100
        Community_Bat_SoC=(((Community_Bat_E_State)-((N1+N2)*Battery_Energy_Min))/(((N1+N2)*Battery_Energy_Max)-((N1+N2)*Battery_Energy_Min)))*100
        
        # Computing House and Community Generation and Demand
        House_E_Generation=House_PV_E_Used+House_Bat_E_Discharging
        House_E_Demand=House_Bat_E_Charging+House_Bat_E_TotalLoad_Actual
        
        Community_E_Generation=Community_PV_E_Used+Community_Bat_E_Discharging
        Community_E_Demand=Community_Bat_E_Charging+Community_Bat_E_TotalLoad_Actual
        
        #House/Community Level Battery Charging_Dispatchable/Discharging_Dispatchable
        House_Bat_E_Charging_Dispatchable=np.zeros((N_House,len(GHI),1)) # Initialization
        House_Bat_E_Discharging_Dispatchable=np.zeros((N_House,length(GHI),1)) # Initialization
        
        for i in range(len(GHI)-1):
            if (Community_PV_E_Available(1,i,1) >= Community_Bat_E_TotalLoad_Desired(1,ii,1)):
                for j in  range(N_PV_Bat+N_Bat-1):
                    House_Bat_E_Charging_Dispatchable(j,i,1)=min(MaxRate_Charging*Simulation_StepSize, (Battery_Energy_Max-(X_k_Plant_History(j,i,4))) / Eff_Charging_Battery)
                    House_Bat_E_Discharging_Dispatchable(j,i,1)=0;
            else:
                for j in range(N_PV_Bat+N_Bat-1):
                    House_Bat_E_Charging_Dispatchable(j,i,1)=0
                    House_Bat_E_Discharging_Dispatchable(j,i,1)=min(MaxRate_Discharging*Simulation_StepSize,(X_k_Plant_History(j,i,4)-Battery_Energy_Min)*Eff_Discharging_Battery)
        
        Community_Bat_E_Charging_Dispatchable=sum(House_Bat_E_Charging_Dispatchable[:,:,1],0)#***
        Community_Bat_E_Discharging_Dispatchable=sum(House_Bat_E_Discharging_Dispatchable[:,:,1],0)#***

        # House AC Startup Power Quantities
        Community_AC_P_StartUp_Available=(Community_PV_E_Available/Simulation_StepSize)+(Community_Bat_Controller_Charging_Desired*MaxRate_Discharging_StartUp)

        House_AC_StartUp_Desired=House_AC_Controller_TurnOn_Desired[:,:,1]-X_k_Plant_History[:,:,30]
        House_AC_StartUp_Desired = (abs(House_AC_StartUp_Desired)+House_AC_StartUp_Desired)/2
        Community_AC_StartUp_Desired = sum(House_AC_StartUp_Desired[:,:,1],0)
        Community_AC_P_StartUp_Required=Community_AC_StartUp_Desired*ACLoad_StartUp_Power

        House_AC_StartUp_Actual=X_k_Plant_History[:,:,21]-X_k_Plant_History[:,:,30]
        House_AC_StartUp_Actual = (abs(House_AC_StartUp_Actual)+House_AC_StartUp_Actual)/2
        Community_AC_StartUp_Actual = sum(House_AC_StartUp_Actual[:,:,1],0)
        Community_AC_P_StartUp_Used=Community_AC_StartUp_Actual*ACLoad_StartUp_Power

        # Creating Grouping Indices
        N_All_Indices = range(1,N_House+1)
        N_PV_Bat_Only_Indices = range(1,N1+1)
        N_Bat_Only_Indices = range(N1+1,N2+1)
        N_PV_Only_Indices = range(N2+1,N3+1)
        N_None_Only_Indices = range(N3+1,N4+1)
        
        ## DateTime Vector to Hours

        D=DateTimeVector[1]-DateTimeVector[0]

#might need function for this but isnt time already in minutes?
        #M=minutes(D)

        H=M/60

        L=len(DateTimeVector)

        HoursVector=np.zeros((L,1))
        HoursVector=np.zeros((L,1))
        
        for i in range(2,L+1)
            HoursVector[i,1] = HoursVector[i-1,1] + H

        Len_Hours_Vector=len(HoursVector)        
                
        #---------------------------------------House PV Power Plots - Availabe/Used/Unused------------------------------------

        fig, ax = plt.subplots()
        #Find size that is good for graphs (no auto?)
        fig.set_size_inches(10,5)

        ax.set_title("House Level - PV Power")
        ax.set_xlabel("Time (hours)")  #use latex for hours and kW
        ax.set_ylabel("Power (kW)")
         
        #Set x and y limits for graph with data and uncomment
        plt.xlim([min(x), max(x)])

        #add ax.plot for more sets
        for i in range(N_PV_BAT_Only_Indicies.union(N_PV_Only_Indicies)):
            ax.plot(HoursVector, EToP_Converter*House_PV_E_Available[i,0:Len_Hours_Vector,0], color = "black", linewidth=3, label="PV Power Available")
            ax.plot(HoursVector, EToP_Converter*House_PV_E_Used[i,0:Len_Hours_Vector,0], color = "blue", linewidth=4, label="PV Power Used")
            ax.plot(HoursVector, EToP_Converter*House_PV_E_UnUsed[i,0:Len_Hours_Vector,0], color = "red", linewidth=2, label="PV Power Unused")

        ax.legend()

        #Can convert to jpeg with python image library if needed
        plt.savefig('House_PV_Power_A_U_UnU.png', dpi = 100)
        
        #--------------------------------------Community PV Power Plots - Availabe/Used/Unused--------------------------------
        
        fig, ax = plt.subplots()
        #Find size that is good for graphs (no auto?)
        fig.set_size_inches(10,5)

        ax.set_title("Community Level - PV Power")
        ax.set_xlabel("Time (hours)")  #use latex for hours and kW
        ax.set_ylabel("Power (kW)")
         
        #Set x and y limits for graph with data and uncomment
        plt.xlim([min(x), max(x)])

        #add ax.plot for more sets
        ax.plot(HoursVector, EToP_Converter*Community_PV_E_Available[0,0:Len_Hours_Vector,0], color = "black", linewidth=3, label="PV Power Available")
        ax.plot(HoursVector, EToP_Converter*Community_PV_E_Used[0,0:Len_Hours_Vector,0], color = "blue", linewidth=4, label="PV Power Used")
        ax.plot(HoursVector, EToP_Converter*Community_PV_E_UnUsed[0,0:Len_Hours_Vector,0], color = "red", linewidth=2, label="PV Power Unused")

        ax.legend()

        #Can convert to jpeg with python image library if needed
        plt.savefig('Community_PV_Power_A_U_UnU.png', dpi = 100)
        
        #----------------------------------------House Battery SoC/Bat_Charging/Bat_Discharging Plots-------------------------- 
        
        fig, ax = plt.subplots()
        #Find size that is good for graphs (no auto?)
        fig.set_size_inches(10,5)

        ax.set_title("House Level - Battery SoC/Charging/Discharging")
        ax.set_xlabel("Time (hours)")  #use latex for hours and kW
        ax.set_ylabel("%")
         
        #Set x and y limits for graph with data and uncomment
        plt.xlim([min(x), max(x)])

        #add ax.plot for more sets
        for i in range(N_PV_Bat_Only_Indices.union(N_Bat_Only_Indices)):
            ax.plot(HoursVector,House_Bat_SoC[i,1:Len_Hours_Vector,1], color = "blue", linewidth=3, label="SoC")

        ax.plot(HoursVector, 100*np.ones((Len_Hours_Vector,1)), "--", color = "black", linewidth=4, label="")
        ax.plot(HoursVector, 0*np.ones((Len_Hours_Vector,1)), "--", color = "black", linewidth=2, label="")
        
        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        for i in range(N_PV_Bat_Only_Indices.union(N_Bat_Only_Indices)):
            ax.plot(HoursVector, EToP_Converter*House_Bat_E_Charging[i,1:Len_Hours_Vector,1], color = "green", linewidth=3, label="Battery Charging Power")
            ax.plot(HoursVector, EToP_Converter*House_Bat_E_Charging[i,1:Len_Hours_Vector,1], color = "red", linewidth=3, label="Battery Discharging Power")
        
        ax2.set_ylabel("Power (kW)")
        
        ax.legend()

        #Can convert to jpeg with python image library if needed
        plt.savefig('House_Bat_SoC_C_DisC.png', dpi = 100)
        
        #-----------------------------------------Community Battery SoC/Bat_Charging/Bat_Discharging Plots---------------------
        
        fig, ax = plt.subplots()
        #Find size that is good for graphs (no auto?)
        fig.set_size_inches(10,5)

        ax.set_title("Community Level - Battery SoC/Charging/Discharging")
        ax.set_xlabel("Time (hours)")  #use latex for hours and kW
        ax.set_ylabel("%")
         
        #Set x and y limits for graph with data and uncomment
        plt.xlim([min(x), max(x)])

        #add ax.plot for more sets
        ax.plot(HoursVector, Community_Bat_SoC[1,1:Len_Hours_Vector,1], color = "blue", linewidth=1.5, label="SoC")
        ax.plot(HoursVector, 100*np.ones((Len_Hours_Vector,1)), "--", color = "black", linewidth=1, label="")
        ax.plot(HoursVector, 0*np.ones((Len_Hours_Vector,1)), "--", color = "black", linewidth=1, label="")
        
        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        ax.plot(HoursVector, EToP_Converter*Community_Bat_E_Charging[i,1:Len_Hours_Vector,1], color = "green", linewidth=1, label="Battery Charging Power")
        ax.plot(HoursVector, EToP_Converter*Community_Bat_E_Charging[i,1:Len_Hours_Vector,1], color = "red", linewidth=1, label="Battery Discharging Power")

        ax2.set_ylabel("Power (kW)")
        
        ax.legend()

        #Can convert to jpeg with python image library if needed
        plt.savefig('Community_Bat_SoC_C_DisC.png', dpi = 100)
        
        #------------------------------------------------------House Level - Temperature---------------------------------------
        
        fig, ax = plt.subplots()
        #Find size that is good for graphs (no auto?)
        fig.set_size_inches(10,5)

        ax.set_title("House Level - Temperature")
        ax.set_xlabel("Time (hours)")  #use latex for hours and kW
        ax.set_ylabel("Temperature (C)")
         
        #Set x and y limits for graph with data and uncomment
        plt.xlim([min(x), max(x)])

        #add ax.plot for more sets
        for i in range(len(N_House)):
            ax.plot(HoursVector, House_Temprature[i,1:Len_Hours_Vector,1], color = "blue", linewidth=2, label="")
            
        ax.plot(HoursVector, T_AC_max*np.ones((Len_Hours_Vector,1)), "--", color = "black", linewidth=3, label="")
        ax.plot(HoursVector, T_AC_min*np.ones((Len_Hours_Vector,1)), "--", color = "black", linewidth=3, label="")

        ax.legend()

        #Can convert to jpeg with python image library if needed
        plt.savefig('House_Temperature.png', dpi = 100)
        
        # To be Continued.........................................................     
    
        
    def HEMS_Plant_Performance_Computer(self, HEMS_PerformanceComputation_Input):
        
        # HEMS_Plant_Performance_Computer - Computing Performance Measure of the Simulation

        # Getting the desired data from the HEMS_Plant_Baseline_FigurePlotter_Input - Struct

        #---------------------HEMS_PerformanceComputation-------------------------%
        X_k_Plant_History = HEMS_PerformanceComputation["X_k_Plant_History"]
        U_k_History = HEMS_PerformanceComputation["U_k_History"]
        E_LoadData = HEMS_PerformanceComputation["E_LoadData"]
        E_Load_Desired = HEMS_PerformanceComputation["E_Load_Desired"]
        HEMSWeatherData_Output = HEMS_PerformanceComputation["HEMSWeatherData_Output"]
        HEMSPlant_Params = HEMS_PerformanceComputation["HEMSPlant_Params"]
        Community_Params = HEMS_PerformanceComputation["Community_Params"]
        
        #-----------------------HEMSWeatherData_Output----------------------------#
        Ws = HEMSWeatherData_Output["Ws"]
        T_am = HEMSWeatherData_Output["T_am"]
        GHI = HEMSWeatherData_Output["GHI"]
        DNI = HEMSWeatherData_Output["DNI"]
        DateTimeVector = HEMSWeatherData_Output["DateTimeVector"]
        DateTime_Matrix = HEMSWeatherData_Output["DateTime_Matrix"]

        #---------------------------HEMSPlant_Params------------------------------#

        E_AC = HEMSPlant_Params["E_AC"]
        T_AC_max = HEMSPlant_Params["T_AC_max"]
        T_AC_min = HEMSPlant_Params["T_AC_min"]
        ACLoad_StartUp_Power = HEMSPlant_Params["ACLoad_StartUp_Power"]
        Eff_Inv = HEMSPlant_Params["Eff_Inv"]

        Battery_Energy_Max = HEMSPlant_Params["Battery_Energy_Max"]
        Battery_Energy_Min = HEMSPlant_Params["Battery_Energy_Min"]
        MaxRate_Charging = HEMSPlant_Params["MaxRate_Charging"]
        MaxRate_Discharging = HEMSPlant_Params["MaxRate_Discharging"]
        Eff_Charging_Battery = HEMSPlant_Params["Eff_Charging_Battery"]
        Eff_Discharging_Battery = HEMSPlant_Params["Eff_Discharging_Battery"]
        MaxRate_Discharging_StartUp = HEMSPlant_Params["MaxRate_Discharging_StartUp"]

        #---------------------------Community_Params-----------------------------#

        N_House = Community_Params["N_House"]
        N_PV_Bat = Community_Params["N_PV_Bat"]
        N_Bat = Community_Params["N_Bat"]
        N_PV = Community_Params["N_PV"]
        N_None = Community_Params["N_None"] 
        
        ## Basic Computation

        # House Numbers
        N1 = N_PV_Bat
        N2 = N_Bat
        N3 = N_PV
        N4 = N_None

        # Truncating Plant History
        X_k_Plant_History = X_k_Plant_History[:,0:X_k_Plant_History.shape[1],:]

        # Computing Number of Days of Simulation
        Start_DateTime = DateTimeVector[0]
        End_DateTime = DateTimeVector[DateTimeVector.size]

        TotalNum_Days_Simulation = daysact[Start_DateTime,End_DateTime]
        
        ## Performance Metric Computation

        # For All Houses AC
        
        for j in range(len(N_House)):
            #For one house AC
            AC_Death_TimeTotal=0
            for i in range(len(X_k_Plant_History[j,:,6])):
                if (X_k_Plant_History[j,i,6] > (T_AC_max+2)):
                    AC_Death_TimeTotal = AC_Death_TimeTotal + (10/60) # Hours
                    
            AC_Death_AvgPerDay[j] = AC_Death_TimeTotal / (TotalNum_Days_Simulation)
            
        # For All Houses All Other Loads
        
        All_Served=X_k_Plant_History[:,:,11]
        All_Desired=E_Load_Desired[:,:,0]
        
        for j in range(len(N_House)):
            
            # For One House All Other Loads
            All_Desired_Points=0
            All_Served_Points=0
            for i in range(len(All_Served)):
                if(All_Desired[j,i,1] > 0):
                    All_Desired_Points = All_Desired_Points+1
                    
                if((All_Served[j,i,1] < All_Desired[j,i,1]) and (not(All_Served[j,i,1] < 0))):
                    # NC Load Not Served
                    x = 0
                elif ((All_Served[j,i,1] == All_Desired[j,i,1]) and (not(All_Served[j,i,1] <= 0))):
                    All_Served_Points=All_Served_Points+1;

            Percentage_All_Served[j] = ((All_Served_Points)/(All_Desired_Points)*(100))
            
        #For All Houses Critical Loads
        C_Served=X_k_Plant_History[:,:,12]
        C_Desired=E_LoadData[:,:,0]
        
        for j in range(len(N_House)):

            # For One House Critical Loads
            C_Desired_Points=0
            C_Served_Points=0
            for i in range(len(C_Served)):
                if (C_Desired[j,i,0] > 0):
                    C_Desired_Points=C_Desired_Points+1
                if ((C_Served[j,i,0] < C_Desired[j,i,1]) and (not(C_Served[j,i,0] < 0))):
                    # NC Load Not Served
                    x=0
                elif ((C_Served[j,i,0] == C_Desired[j,i,0]) and (not(C_Served[j,i,0] <= 0))):
                    C_Served_Points=C_Served_Points+1

            Percentage_C_Served[j] = ((C_Served_Points)/(C_Desired_Points)*(100))
            
        # For All Houses
        for j in range(len(N_House)):
            
            # For One House PRM and SRM    
            PRM[j] = 1-(AC_Death_AvgPerDay[j]/24)

            SRM_C[j] = Percentage_C_Served[j]/100

            SRM_All[j]=Percentage_All_Served[j]/100
        
        #RP =  (h*PRM) + ((1-h)*SRM_C.mean(axis = 0)

        # Computing Performance Measure for entire Community
        AC_Death_AvgPerDay_Community  =  AC_Death_AvgPerDay.mean(axis = 0)
        Percentage_All_Served_Community = Percentage_All_Served.mean(axis = 0)
        Percentage_C_Served_Community = Percentage_C_Served.mean(axis = 0)
        PRM_Community = PRM.mean(axis = 0)
        SRM_C_Community = SRM_C.mean(axis = 0)
        SRM_All_Community =SRM_All.mean(axis = 0)
        
        ## Priniting Results

        # Priniting Quantitative Results for each House
        for i in range(len(N_House)):
            
            print('Average Fridge Death for House:{:d} (PLP) = {:.4f} Hours/Day'.format(i,AC_Death_AvgPerDay[i]))
            
            print('Percentage of Non-Critical Loads served for House:{:d} (SLP) = {:.4f} %/Day'.format(i,Percentage_C_Served[i]))
            
            print('Percentage of All Loads served for House:{:d} (SLP) = {:.4f} %/Day'.format(i,Percentage_All_Served[i]))
            
            print('House:{:d} (PRM) = {:.4f} Hours/Day'.format(i,PRM[i]))
            
            print('House:{:d} (SRM_C) = {:.4f} %/Day'.format(i,SRM_C[i]))
            
            print('House:{:d} (SRM_All) = {:.4f} %/Day'.format(i,SRM_All[i]))
            
        # Priniting Quantitative Results for Community
        print('Average Fridge Death for Community (PLP) = {:.4f} Hours/Day'.format(AC_Death_AvgPerDay_Community))

        print('Percentage of Non-Critical Loads served for Community (SLP) = {:.4f} %/Day'.format(Percentage_C_Served_Community))

        print('Percentage of All Loads served for Community (SLP) = {:.4f} %/Day'.format(Percentage_All_Served_Community))

        print(' Community (PRM) = {:.4f} Hours/Day'.format(PRM_Community))

        print(' Community (SRM_C) = {:.4f} %/Day'.format(SRM_C_Community))

        print(' Community (SRM_All) = {:.4f} %/Day'.format(SRM_All_Community))
        
        # Creating Plant_Performance

        Plant_Performance =  []

        Plant_Performance["AC_Death_AvgPerDay"] = AC_Death_AvgPerDay
        Plant_Performance["Percentage_All_Served"] = Percentage_All_Served
        Plant_Performance["Percentage_C_Served"] = Percentage_C_Served
        Plant_Performance["PRM"] = PRM_Community
        Plant_Performance["SRM_C"] = SRM_C_Community
        Plant_Performance["SRM_All"] = SRM_All

        Plant_Performance["AC_Death_AvgPerDay_Community"] = AC_Death_AvgPerDay_Community
        Plant_Performance["Percentage_All_Served_Community"] = Percentage_All_Served_Community
        Plant_Performance["Percentage_C_Served_Community"] = Percentage_C_Served_Community
        Plant_Performance["PRM_Community"] = PRM_Community
        Plant_Performance["SRM_C_Community"] = SRM_C_Community
        Plant_Performance["SRM_All_Community"] = SRM_All_Community
        
        #Finished not tested
        