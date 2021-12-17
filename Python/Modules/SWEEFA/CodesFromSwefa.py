#Module creation of CodesFromSwefa

import math
import cmath
import numpy as np
import pandas as pd

def AltiAzi(dec, L, H):
    #variable declarations
    length = len(H)
    beta = []
    azi1 = []
    azi11 = []
    azi2 = []
    azi22 = []
    phi = []
    
    #for loop that calculates and stores data
    for i in range(length):
        beta.append((180/math.pi)*(math.asin((math.cos(L*(math.pi/180))*math.cos(dec*(math.pi/180))*math.cos(H[i]*(math.pi/180)))+(math.sin(L*(math.pi/180))*math.sin(dec*(math.pi/180))))))
        azi1.append((180/math.pi)*(math.asin((math.cos(dec*(math.pi/180))*math.sin(H[i]*(math.pi/180)))/(math.cos(beta[i]*(math.pi/180))))))
        azi11.append(abs(azi1[i]))
        azi2.append(180-azi11[i])
        azi22.append(abs(azi2[i]))
        
        x = math.cos(H[i] * (math.pi/180))
        y = (math.tan(dec*(math.pi/180)))/(math.tan(L*(math.pi/180)))
        
        if x >= y:
            phi.append(azi1[i])
        else:
            if azi1[i] >= 0:
                phi.append(azi2[i])
            else:
                phi.append(-1 * azi2[i])
    dict = {'b':beta, 'p':phi}
    return dict

def ArrayIncidenceLoss(ic, cosang, bo, sf):
    Fiam = 1-(bo*((1/cosang)-1))
    Iciam = ic * Fiam
    Icsf = Iciam*(1-(sf/100))
    dict = {'Iciam':Iciam, 'Icsf':Icsf}
    return dict

def BeamDiffGHI(n, GHI, beta):
    c = 0.095+(0.04*math.sin((math.pi/180)*(360/365)*(n-100)))
    ib = GHI/(math.sin((math.pi/180)*beta)+c)
    id = c*ib
    dict = {'Ib':ib, 'Id':id, 'C':c}
    return dict

def ClockToSolarTime(n, hem, Ltm, L, CT):
    #variable declaration
    length1 = len(n)
    length2 = len(CT)
    b = []
    e = []
    st = [None] * length2   #Creates empty list of size length 2
    
    for i in range(length1):
        b.append((360/364) * (n[i]-81))
        e.append((9.87*math.sin((math.pi/180)*(2*b[i])))-(7.53*math.cos((math.pi/180)*b[i]))-(1.5*math.sin((math.pi/180)*b[i])))
        
        for j in range(length2):
            st[j] = ((CT[j])-((hem*(Ltm-L)*4)/60)+(e[i]/60))
            
    dict = {'ST':st ,'B':b ,'E':e}
    return dict

def DateTime(y,m,d,hr,minn,sec):
    date = [None]*6
    date[0] = y
    date[1] = m
    date[2] = d
    date[3] = hr
    date[4] = minn
    date[5] = sec
    
    return date

def DateTimeSeriesSlicer(OriginalDataSeries,SeriesNum3,Res,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,StartTime,EndTime):
    rows = len(OriginalDataSeries[0])
    StartIndex = 0
    EndIndex = 0
    
    Data = np.array(OriginalDataSeries)
    
    val = 0
    DayVector = []
    DayVector.append(0)
    
    while val < (24-(Res/60)):
        val += Res/60 
        DayVector.append(val)
    DayLen = len(DayVector)
        
    # DiffStartTime=(zip(StartTime, DayVector))
    # MinST = np.amin(DiffStartTime)
    # IndexST = np.where(MinST)
    
    # DiffEndTime=(zip(EndTime, DayVector))
    # MinET = np.amin(DiffEndTime)
    # IndexET = np.where(MinET)
    for i in range(rows):   #Double check this covers all values
        if (Data[i][0] == EndDay and Data[i][1] == EndMonth and Data[i][2] == EndYear and Data[i][3] == StartTime):
            StartIndex = i
    
    for i in range(rows):   #Double check this covers all values
        if (Data[i][0] == EndDay and Data[i][1] == EndMonth and Data[i][2] == EndYear and Data[i][3] == EndTime):
            EndIndex = i
    OriginalData = Data[StartIndex:EndIndex+1]
    
    dict = {'Data':OriginalData, 'StartIndex':StartIndex, 'EndIndex':EndIndex}
    return dict

def DateTimeSeriesSlicer_PecanStreetData(OriginalDataSeries,SeriesNum3,Res,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,StartTime,EndTime):
    rows = len(OriginalDataSeries)
    StartIndex = 0
    EndIndex = 0
    
    Data = np.array(OriginalDataSeries)
    
    val = 0
    DayVector = []
    DayVector.append(0)
    
    while val < (24-(Res/60)):
        val += Res/60 
        DayVector.append(val)
        
    # DiffStartTime=(zip(StartTime, DayVector))
    # MinST = np.amin(DiffStartTime)
    # IndexST = np.where(MinST)
    
    # DiffEndTime=(zip(EndTime, DayVector))
    # MinET = np.amin(DiffEndTime)
    # IndexET = np.where(MinET)
    
    for i in range(rows):   #Double check this covers all values
        if (Data[i][0] == StartDay and Data[i][1] == StartMonth and Data[i][2] == StartYear and Data[i][3] == StartTime):
            StartIndex = i
    
    for i in range(rows):   #Double check this covers all values
        if (Data[i][0] == EndDay and Data[i][1] == EndMonth and Data[i][2] == EndYear and Data[i][3] == EndTime):
            EndIndex = i
            
    try:        
        OriginalData = Data[StartIndex:EndIndex+1]
    except:
            print("Error OriginalData Series encountered String")
            OriginalData = "Error"
            
    dict = {'OriginalData':OriginalData, 'StartIndex':StartIndex, 'EndIndex':EndIndex}
    return dict

def DaysToCompute(LeapYear, StartDay, StartMonth, EndDay, EndMonth):
    StartMonthDay = 0
    EndMonthDay = 0
    
    if LeapYear == 0:
        
        if StartMonth == 1:
            StartMonthDay = 1
        elif StartMonth == 2:
            StartMonthDay = 32
        elif StartMonth == 3:
            StartMonthDay = 60
        elif StartMonth == 4:
            StartMonthDay = 91
        elif StartMonth == 5:
            StartMonthDay = 121
        elif StartMonth == 6:
            StartMonthDay = 152
        elif StartMonth == 7:
            StartMonthDay = 182
        elif StartMonth == 8:
            StartMonthDay = 213
        elif StartMonth == 9:
            StartMonthDay = 244  
        elif StartMonth == 10:
            StartMonthDay = 274
        elif StartMonth == 11:
            StartMonthDay = 305
        elif StartMonth == 12:
            StartMonthDay = 335
            
        if EndMonth == 1:
            EndMonthDay = 1
        elif EndMonth == 2:
            EndMonthDay = 32
        elif EndMonth == 3:
            EndMonthDay = 60
        elif EndMonth == 4:
            EndMonthDay = 91
        elif EndMonth == 5:
            EndMonthDay = 121
        elif EndMonth == 6:
            EndMonthDay = 152
        elif EndMonth == 7:
            EndMonthDay = 182
        elif EndMonth == 8:
            EndMonthDay = 213
        elif EndMonth == 9:
            EndMonthDay = 244  
        elif EndMonth == 10:
            EndMonthDay = 274
        elif EndMonth == 11:
            EndMonthDay = 305
        elif EndMonth == 12:
            EndMonthDay = 335     
            
            
    elif LeapYear == 1:
        
        if StartMonth == 1:
            StartMonthDay = 1
        elif StartMonth == 2:
            StartMonthDay = 32
        elif StartMonth == 3:
            StartMonthDay = 61
        elif StartMonth == 4:
            StartMonthDay = 92
        elif StartMonth == 5:
            StartMonthDay = 122
        elif StartMonth == 6:
            StartMonthDay = 153
        elif StartMonth == 7:
            StartMonthDay = 183
        elif StartMonth == 8:
            StartMonthDay = 214
        elif StartMonth == 9:
            StartMonthDay = 245
        elif StartMonth == 10:
            StartMonthDay = 275
        elif StartMonth == 11:
            StartMonthDay = 306
        elif StartMonth == 12:
            StartMonthDay = 336
          
        if EndMonth == 1:
            EndMonthDay = 1
        elif EndMonth == 2:
            EndMonthDay = 32
        elif EndMonth == 3:
            EndMonthDay = 61
        elif EndMonth == 4:
            EndMonthDay = 92
        elif EndMonth == 5:
            EndMonthDay = 122
        elif EndMonth == 6:
            EndMonthDay = 153
        elif EndMonth == 7:
            EndMonthDay = 183
        elif EndMonth == 8:
            EndMonthDay = 214
        elif EndMonth == 9:
            EndMonthDay = 245
        elif EndMonth == 10:
            EndMonthDay = 275
        elif EndMonth == 11:
            EndMonthDay = 306
        elif EndMonth == 12:
            EndMonthDay = 336
                
    StartDay = StartMonthDay+StartDay-1
    EndDay = EndMonthDay+EndDay-1
    
    dict = {'StartDay':StartDay, 'EndDay':EndDay}
    return dict

def DeciToHM(Td):
    Time = [None] * 3
    hr = math.floor(Td/1)
    mmm = Td % 1
    mm = mmm*60
    minn = math.floor(mm/1)
    sss = mm % 1
    ss = sss*60
    sec = math.floor(ss/1)
    Time[0] = hr
    Time[1] = minn
    Time[2] = sec
    return Time   

def Declination(n):
    length = len(n)
    dec = [None] * length
    
    for i in range(length):
        dec[i] = 23.45*(math.sin((360/365)*(n[i]-81)*(math.pi/180)))
        
    return dec

def FixedTilt(Ib,Id,C,beta,phi,tilt,phic,rho):
    CosIncAng = (math.cos((math.pi/180)*(beta))*math.cos((math.pi/180)*(phi-phic))*math.sin((math.pi/180)*(tilt)))+(math.sin((math.pi/180)*(beta))*math.cos((math.pi/180)*(tilt)))
    Ibc = Ib*CosIncAng
    Idc = Id*((1+math.cos((math.pi/180)*(tilt)))/(2))
    Irc = rho*Ib*(math.sin((math.pi/180)*(beta))+C)*((1-math.cos((math.pi/180)*(tilt)))/(2))
    Ic=Ibc+Idc+Irc
    dict = {'Ic':Ic, 'Ibc':Ibc, 'Idc':Idc, 'Irc':Irc, 'CosIncAng':CosIncAng}
    return dict

def HMToDeci(hr,min,sec):
    MinD=min/60
    SecD=sec/3600
    Td=hr+MinD+SecD
    return Td

def HourAngle(Hp):
    rows = len(Hp)
    col = len(Hp[0])
    H = [[None]*col] * rows
    
    for i in range(rows):
        for j in range(col):
            H[i][j] = 15*(12-(Hp[1][j]))
    return H

def ModulePower(Pmod,ModTemCF,ModNum,Tn,Gn,Icsf,T,Ic,Uo,U1,Ws):
    Tm=T+((Ic)/(Uo+(U1*Ws)))
    Pmodin=Pmod*(1+((ModTemCF/100)*(Tm-Tn)))*(Icsf/Gn)
    Pmodtot=ModNum*Pmodin
    dict = {'Pmodtot':Pmodtot, 'Pmodin':Pmodin, 'Tm':Tm}
    return dict

def JulianDay(Day, Month, Year):
    StartMonthDay = 0
    LY = LeapYearFinder(Year)
    
    if LY == 0:
        if Month == 1:
            StartMonthDay = 1
        elif Month == 2:
            StartMonthDay = 32
        elif Month == 3:
            StartMonthDay = 60
        elif Month == 4:
            StartMonthDay = 91
        elif Month == 5:
            StartMonthDay = 121
        elif Month == 6:
            StartMonthDay = 152
        elif Month == 7:
            StartMonthDay = 182
        elif Month == 8:
            StartMonthDay = 213
        elif Month == 9:
            StartMonthDay = 244
        elif Month == 10:
            StartMonthDay = 274
        elif Month == 11:
            StartMonthDay = 305
        elif Month == 12:
            StartMonthDay = 335
            
    elif LY == 1:
        if Month == 1:
            StartMonthDay = 1
        elif Month == 2:
            StartMonthDay = 32
        elif Month == 3:
            StartMonthDay = 61
        elif Month == 4:
            StartMonthDay = 92
        elif Month == 5:
            StartMonthDay = 122
        elif Month == 6:
            StartMonthDay = 153
        elif Month == 7:
            StartMonthDay = 183
        elif Month == 8:
            StartMonthDay = 214
        elif Month == 9:
            StartMonthDay = 245
        elif Month == 10:
            StartMonthDay = 275
        elif Month == 11:
            StartMonthDay = 306
        elif Month == 12:
            StartMonthDay = 336
            
    n = StartMonthDay + Day - 1
    return n

def LeapYearFinder(year):
    a = year % 4
    b = year % 100
    c = year % 400
    leap = 0
    if (a == 0 and b != 0) or c == 0:
        leap = 1
    else:
        leap = 0
    return leap

#  Detailed explanation goes here
#  LID = Light Induced Degradation (for Crystalline Modules) (1-3%; Default=2%)
#  LS = Light Soaking (For Thin Flim Modules)(3-5% or more; Default=3%)
#  Arraymismat = Array Mismatch Factor (Default=2%)
#  Crys = Is the PV Technology Crystalline (Crys==1) or Thin Film (Crys==0)??
#  Shading = Shading Loss Factor (Default=1%)
#  OhmicLoss = Array wiring loss (Default=3%)
#  INVeff = Inverter Efficiency (%; Given in Inverter Datasheet)
#  TransLoss = Transformer Loss Factor (Default=1%)

def PVoutputPower(Pmodtot, LID,LS,Arraymismat,Crys,Shading, OhmicLoss,TrackerL,INVeff,TransLoss):
    if Crys == 1:
        PVout = Pmodtot*(1-((LID+Arraymismat+Shading)/100))
    else:
        PVout = Pmodtot*(1-((Arraymismat+Shading)/100)+((LS)/100))
        
    INVpin = PVout*(1-(OhmicLoss/100))
    INVpout = INVpin*(INVeff/100)
    TrackerLossPP = INVpout*(1-(TrackerL/100))
    Pgrid=TrackerLossPP*(1-(TransLoss/100))
    ArrayMismatchLoss=Pmodtot*(Arraymismat/100)
    ShadingLoss=Pmodtot*(Shading/100)
    LIDLoss=Pmodtot*(LID/100)
    OhmicLossP=PVout*(OhmicLoss/100)
    InverterLoss=INVpin*(1-(INVeff/100))
    TrackerLossP=INVpout*(TrackerL/100)
    TransformerLossP=INVpout*(TransLoss/100)
    dict = {'Pvout':PVout, 'INVpin':INVpin, 'INVpout':INVpout, 'Pgrid':Pgrid, 'ArrayMistmatchLoss':ArrayMismatchLoss, 'ShadingLoss': ShadingLoss, 'LIDloss':LIDLoss, 'OhmicLossp':OhmicLossP, 'InverterLoss':InverterLoss, 'TransformerLossP':TransformerLossP, 'TrackerLossp':TrackerLossP}
    return dict

def SolarToClockTime(n,hem,Ltm,L,ST):
    len1 = len(n)
    len2 = len(ST)
    
    B = [None] * len1
    E = [None] * len1
    CT = [None] * len2
    
    for i in range(len1):
        B[i] = (360/364)*(n[i]-81)
        E[i] = (9.87*math.sin((math.pi/180)*(2*B[i]))-(7.53*math.cos((math.pi/180)*B[i]))-(1.5*math.sin((math.pi/180)*B[i])))
        for j in range(len2):
            CT[j] = (ST[j])+((hem*(Ltm-L)*4)/60)-(E[i]/60)
                    
    dict = {'CT':CT,'B':B, 'E':E}
    return dict

def StartEndCalendar(StartYear,StartMonth,StartDay,TotDays,Res,DataCols):
    SD=StartDay
    SM=StartMonth
    SY=StartYear
    
    DayPoints= (24.0*(60.0/Res))
    TotDataPoints=int(TotDays*DayPoints)
    
    val = 0
    Time = []
    Time.append(0)
    
    while val < (24-(Res/60)):
        val += Res/60 
        Time.append(val)
    
    TotCols=DataCols+4
    
    DateTimeMatrix = np.zeros((TotCols,TotDataPoints))
    
    Tn=0
    Th=0
    Tl=0
    Yr=0
    count = 0
    
    for i in range(TotDays):
        if SD == 31 and SM == 12:
            SY += 1
            SM = 1
            SD = 1
            Yr = 1
        
        LP = LeapYearFinder(SY)
        if SD == 31:
            SD = 1
            SM += 1
            Tn = 1
        elif SD == 30:
            l = [4, 6, 9, 11]
            for j in l:
                if SM == j:
                    SD = 1
                    SM += 1
                    Th = 1
                    break
        elif (SD == 28 and LP == 0 and SM == 2) or (SD == 29 and LP == 1 and SM == 2):
            SD = 1
            SM += 1
            Tl = 1
        
        DayIncrement = (i != 0) and (((SD != 31) and (SM==1 or SM==3 or SM==5 or SM==7 or SM==8 or SM==10 or SM==12)) or ((SD!=30) and (SM==4 or SM==6 or SM==9 or SM==11)) or (((SD!=28) and (LP==0) and (SM==2)) or ((SD!=29) and (LP==1) and (SM==2))))
        if DayIncrement:
            if Tn == 1 or Th == 1 or Tl == 1 or Yr == 1:
                SD = 1
            else:
                SD += 1
        for i in range(len(Time)):
            DateTimeMatrix[0][count] = SD
            DateTimeMatrix[1][count] = SM
            DateTimeMatrix[2][count] = SY
            DateTimeMatrix[3][count] = Time[i]
            count += 1
        
        Tn = 0
        Th = 0
        Tl = 0
        Yr = 0
        df = pd.DataFrame(DateTimeMatrix)

    dict = {'DateTimeMatrix':df.T, 'TotDataPoints':TotDataPoints, 'Time':Time}
    return dict

def SunRiseSet(L, dec):
    length = len(dec)
    Indicator = np.zeros(length)
    SunRise = [None] * length
    SunSet = [None] * length
    
    for i in range(length):
        Hsr=(180/math.pi)*(math.acos((-(math.tan(L*(math.pi/180)))*math.tan(dec[i]*(math.pi/180)))))
        hsr=abs(Hsr)
        Q=((3.467)/(math.cos((math.pi/180)*L)*math.cos((math.pi/180)*dec[i])*math.sin((math.pi/180)*Hsr)))
        
        SunRise[i]=12-(hsr/15)-(Q/60)
        SunSet[i]=12+(hsr/15)+(Q/60)
        
        Sr=abs((SunRise[i]))
        Ss=abs((SunSet[i]))
        
        if Sr > 0 and Ss > 0:
            if L > 0 and dec[i] >= 0:
                Indicator[i] = 1
                
            if (L>0) and (dec[i] <= 0):
                Indicator[i] = -1
            
            if L < 0 and dec[i] <= 0:
                Indicator[i] = 1
                
            if L < 0 and dec[i] >= 0:
                Indicator[i] = -1
        else:
            Indicator[i] = 0
            
    dict = {'SunRise':SunRise, 'SunSet':SunSet, 'Indicator':Indicator}
    return dict

def ViewFactor(beta, phi, tilt, phic):
    CosInciAngle=(math.cos((math.pi/180)*(beta))*math.cos((math.pi/180)*(phi-phic))*math.sin((math.pi/180)*(tilt)))+(math.sin((math.pi/180)*(beta))*math.cos((math.pi/180)*(tilt)))
    return CosInciAngle