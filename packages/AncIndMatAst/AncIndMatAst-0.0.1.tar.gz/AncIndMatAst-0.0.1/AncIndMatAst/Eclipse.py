import math,datetime
epoch = datetime.datetime(2000, 1, 1)

# To convert angles into second 
def angleToSec(Deg):
    h,m,s=Deg
    return h*60*60+m*60+s

# To convert seconds into angle 
def secToAngle(sec):
    neg=False
    if(sec<0):
        neg=True
        sec=-1*sec
    h=sec//3600
    if neg:
        h=-1*h
    sec=sec%3600
    m=sec//60
    sec=sec%60
    s=round(sec)
    return (h,m,s)

# To convert vinadi to second
def vinadiToSec(nadi):
    return nadi*24

# To convert nadi into second 
def nadiToSec(nadi):
    return nadi*24*60

# To convert naligai into second 
def naligaiToSec(naligai):
    return (naligai*12*3600)//30

# To format time while printing
def printTime(sec):
    time=secToAngle(sec)
    return f"{round(time[0])}h {round(time[1])}m {round(time[0])}s"

# Lunar Eclipse Calculator 
def LunarEclipse(date,time,trueMoon,Rahu):
    """
    Calculate Lunar Eclipse 
    Parameters :
    date => Date to check for eclipse in (Y,M,D)
    time => Instant of opposition
    trueMoon => True Longitude of Moon
    trueRahu => True Longitude of Rahu

    Output:
    Eclipse Type
    Eclipse Magnitude
    If Eclipse Occurs
    Eclipse Beginning Time
    Eclipse Middle Time
    Eclipse End Time
    """
    date=datetime.datetime(*date)
    trueMoonInSec=angleToSec(trueMoon)
    trueRahuInSec=angleToSec(Rahu)

    diff=trueMoonInSec-trueRahuInSec

    # initially 308 but better result 
    beta=angleToSec((0,318,0))*math.sin(math.radians(diff/3600))

    daysDiff=(date-epoch).days
    gm=(134.9633964+13.06499295*daysDiff)%360
    gs=(357.5291092+0.985600231*daysDiff)%360
    mdia=(2*(939.6+61.1*math.cos(math.radians(gm))))
    shdia=(2*(2545.4+228.9*math.cos(math.radians(gm))-16.4*math.cos(math.radians(gs))))


    d=1/2*(mdia+shdia)
    ddash=1/2*(mdia-shdia)
    aLOfMoon=beta*204/205

    # Calculating Type of Eclipse
    eclipseType="no"
    if abs(aLOfMoon)<d:
        if abs(aLOfMoon)<ddash:
            eclipseType="Total"
        else:
            eclipseType="Partial"
            
    pramanam=0        
    if eclipseType != "no":
        pramanam=round((d-abs(aLOfMoon))/mdia,2)

    print(date.strftime('Lunar Eclipse Detail of %d %B %Y'))
    print("Eclipse Type : ",eclipseType)
    print("Magnitude of Eclipse : ",pramanam)


    if eclipseType!="no":
        mdm=47435+5163*math.cos(math.radians(gm))+1008*math.cos(math.radians(2*d))+906*math.cos(math.radians(gm-2*d))+351*math.cos(math.radians(2*gm))-190*math.cos(math.radians(2*d))+124*math.cos(math.radians(gm+2*d))+67*math.cos(math.radians(2*d-gs))+37*math.cos(math.radians(gm-2*d+gs))+31*math.cos(math.radians(gm-gs))-27*math.cos(math.radians(d))-27*math.cos(math.radians(gm+gs))
        sdm=3548+119*math.cos(math.radians(gs))-2*math.cos(math.radians(2*gs))
        vrk=(mdm-sdm)/60
        mdot=(vrk*206)//205
        vrch=trueMoonInSec-trueRahuInSec
        if vrch<0:
            vrch+=1296000

        # Calculating Begin,middle and end timings 
        ioo=angleToSec(time)
        if angleToSec((0,0,0)) <= vrch <= angleToSec((90,0,0)) or angleToSec((180,0,0)) <= vrch <= angleToSec((270,0,0)):
            MID=ioo-vinadiToSec((abs(aLOfMoon)*59)/(10*mdot))
        else:
            MID=ioo+vinadiToSec((abs(aLOfMoon)*59)/(10*mdot))
        start=0
        end=0
        if eclipseType=="Partial":
            HDUR=naligaiToSec(math.sqrt(d**2-aLOfMoon**2)/mdot)
            start=MID-HDUR
            end=MID+HDUR
        else:
            THDUR=naligaiToSec(math.sqrt(ddash**2-aLOfMoon**2)/mdot)
            start=MID-THDUR
            end=MID+THDUR

        print("Timings of Eclipse :")
        print("Beginnig of Eclipse : ",printTime(start))
        print("Middle of Eclipse : ",printTime(MID))
        print("End of Eclipse : ",printTime(end))


# Lunar Eclipse Calculator 
def SolarEclipse(date,time,trueMoon,Rahu):
    """
    Calculate Solar Eclipse 
    Parameters :
    date => Date to check for eclipse in (Y,M,D)
    time => Instant of New Moon
    trueMoon => True Longitude of Moon
    trueRahu => True Longitude of Rahu

    Output:
    Eclipse Type
    Eclipse Magnitude
    If Eclipse Occurs
    Eclipse Beginning Time
    Totality Beginning Time
    Eclipse Middle Time
    Totality End Time
    Eclipse End Time
    """
    date=datetime.datetime(*date)
    trueMoonInSec=angleToSec(trueMoon)
    trueRahuInSec=angleToSec(Rahu)

    daysDiff=trueMoonInSec-trueRahuInSec
    gm=(134.9633964+13.06499295*daysDiff)%360
    gs=(357.5291092+0.985600231*daysDiff)%360

    mdia=2*(939.6+61.1*math.cos(math.radians(gm)))
    sdia=2*(961.2+16.1*math.cos(math.radians(gs)))

    par=3447.9+224.4*math.cos(math.radians(gm))
    d=par+(mdia+sdia)/2
    dDash=par+(mdia-sdia)/2

    # # initially 308 but better result 
    diff=trueMoonInSec-trueRahuInSec
    chandraSara=angleToSec((0,308,0))*math.sin(math.radians(diff/3600))
    lOfMoon=(chandraSara*204)//205

    # Calculating Type of Eclipse
    eclipseType="no"
    if abs(lOfMoon)<d:
        if abs(lOfMoon)<d:
            eclipseType="Total"
        else:
            eclipseType="Partial"
            
    pramanam=0        
    if eclipseType != "no":
        pramanam=round((d-abs(lOfMoon))/mdia,2)
    print(date.strftime('Solar Eclipse Detail of %d %B %Y'))
    print("Eclipse Type : ",eclipseType)
    print("Magnitude of Eclipse : ",pramanam)

    if eclipseType!="no":
        mdm=47435+5163*math.cos(math.radians(gm))+1008*math.cos(math.radians(2*d))+906*math.cos(math.radians(gm-2*d))+351*math.cos(math.radians(2*gm))-190*math.cos(math.radians(2*d))+124*math.cos(math.radians(gm+2*d))+67*math.cos(math.radians(2*d-gs))+37*math.cos(math.radians(gm-2*d+gs))+31*math.cos(math.radians(gm-gs))-27*math.cos(math.radians(d))-27*math.cos(math.radians(gm+gs))
        sdm=3548+119*math.cos(math.radians(gs))-2*math.cos(math.radians(2*gs))
        vrk=(mdm-sdm)/60
        mdot=(vrk*206)//205
        vrch=trueMoonInSec-trueRahuInSec
        if vrch<0:
            vrch+=1296000

        # Calculating Begin,middle and end timings 
        ioo=angleToSec(time)
        if angleToSec((0,0,0)) <= vrch <= angleToSec((90,0,0)) or angleToSec((180,0,0)) <= vrch <= angleToSec((270,0,0)):
            MID=ioo-nadiToSec((99*abs(lOfMoon))/(1000*mdot))
        else:
            MID=ioo+nadiToSec((99*abs(lOfMoon))/(1000*mdot))

        HDUR=naligaiToSec(math.sqrt(d**2-lOfMoon**2)/mdot)
        THDUR=naligaiToSec(math.sqrt(dDash**2-lOfMoon**2)/mdot)
        startEclipse=MID-HDUR
        endEclipse=MID+HDUR
        startTotality=MID-THDUR
        endTotality=MID+THDUR

        print("Timings of Solar Eclipse :")
        print("Beginnig of Eclipse : ",printTime(startEclipse))
        if eclipseType=="Total":
            print("Beginnig of Totality : ",printTime(startTotality))
        print("Middle of Eclipse : ",printTime(MID))
        if eclipseType=="Total":
            print("End of Totality : ",printTime(endTotality))
        print("End of Eclipse : ",printTime(endEclipse))
       