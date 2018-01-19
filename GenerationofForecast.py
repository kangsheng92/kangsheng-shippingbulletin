import netCDF4

import numpy

import math

import datetime

import ftplib

import sys

from xml.etree.ElementTree import Element, SubElement, tostring  
 
##functions##

# windmagnitude classification, 16 different wind directions
# according to the angles of the arctan
# take note of the directions, direction indicates where the wind is coming from
def WindDirection(angle):
    if angle > -11.25 and angle <= 11.25:
        direction = "W"
    elif angle > 11.25 and angle <= 33.75:
        direction = "WSW"
    elif angle > 33.75 and angle <= 56.25:
        direction = "SW"
    elif angle > 56.25 and angle <= 78.75:
        direction = "SSW"
    elif angle > 78.75 and angle <= 101.25:
        direction = "S"
    elif angle > 101.25 and angle <= 123.75:
        direction = "SSE"
    elif angle > 123.75 and angle <= 146.25:
        direction = "SE"
    elif angle > 146.25 and angle <= 168.75:
        direction = "ESE"
    elif angle > 168.75 and angle <= 180:
        direction = "E"
    elif angle > -180 and angle <= -168.75:
        direction = "E"
    elif angle > -168.75 and angle <= -146.25:
        direction = "ENE"
    elif angle > -146.25 and angle <= -123.75:
        direction = "NE"
    elif angle > -123.75 and angle <= -101.25:
        direction = "NNE"
    elif angle > -101.25 and angle <= -78.75:
        direction = "N"
    elif angle > -78.75 and angle <= -56.25:
        direction = "NNW"
    elif angle > -56.25 and angle <= -33.75:
        direction = "NW"
    elif angle > -33.75 and angle <= -11.25:
        direction = "WNW"
    return direction;

# seastate classification
def SeaState(waveheight):   
    if waveheight < 1.25:
        state = "Sea slight"
    elif waveheight > 1.25 and waveheight < 2.5 and (numpy.ma.sum(wave<1.25)/numpy.ma.sum(wave>0))> 0.5:
        state = "Sea slight to moderate"
    elif waveheight > 1.25 and waveheight < 2.5:
        state = "Sea moderate"
    elif waveheight > 2.5 and (numpy.ma.sum(wave<2.5)/numpy.ma.sum(wave>0))> 0.5:
        state = "Sea moderate to rough"
    elif waveheight > 2.5:
        state = "Rough"
          
    return state;

# seaswell classification
def SeaSwell(swellheight):
    if swellheight < 2:
        swell = "Swell low"
    elif swellheight > 2 and swellheight < 4 and (numpy.ma.sum(swell<2)/numpy.ma.sum(swell>0))> 0.5:
        swell = "Swell low to moderate"
    elif swellheight > 2 and swellheight < 4:
        swell = "Swell moderate"
    elif swellheight > 4 and (numpy.ma.sum(swell<4)/numpy.ma.sum(swell>0))> 0.5:
        swell = "Swell moderate to high"
    elif swellheight > 4:
        swell = "Swell high"

    return swell;     



#fetching data from the model data(this example is in local context for now, can refer to directories on the same server)
Atmospheric1 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100400001.nc","r")
Wave1 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100400001.nc","r")
Atmospheric2 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D100400001 00403001.nc","r")
Wave2 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100403001.nc","r")
Atmospheric3 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100406001.nc","r")
Wave3 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100406001.nc","r")
Atmospheric4 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100409001.nc","r")
Wave4 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100409001.nc","r")
Atmospheric5 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100412001.nc","r")
Wave5 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100412001.nc","r")
Atmospheric6 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100400001.nc","r")
Wave6 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100400001.nc","r")
Atmospheric7 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100400001.nc","r")
Wave7 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100400001.nc","r")
Atmospheric8 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1D10040000100400001.nc","r")
Wave8 = netCDF4.Dataset("C:\Users\KangSheng\Desktop\Sampledata\N1P10040000100400001.nc","r")



#getting the list of coordinates of model data, since each data in the model data has its own set of coordinates
Atmosphericlat = Atmospheric1.variables['g0_lat_0'][:]
Atmosphericlon = Atmospheric1.variables['g0_lon_1'][:] 

Wavelat = Wave1.variables['g0_lat_0'][:]
Wavelon = Wave1.variables['g0_lon_1'][:] 


   
#coordinates of the different areas that we will forecast
# boxes to represent the areas, GIS can be used to improve on this
lat1 = numpy.zeros(6)
lat2 = numpy.zeros(6)
lon1 = numpy.zeros(6)
lon2 = numpy.zeros(6)

#phuket coordinates
lat1[0] = 5.1
lat2[0] = 9.75
lon1[0] = 95.25
lon2[0] = 105

#malacca coordinates
lat1[1] = 0.3
lat2[1] = 5.1
lon1[1] = 97.67
lon2[1] = 103.25

#tioman coordinates  
lat1[2] = 0.3
lat2[2] = 5.1
lon1[2] = 103.25
lon2[2] = 105

#condore coordinates
lat1[3] = 5.1
lat2[3] = 9.75
lon1[3] = 105
lon2[3] = 110

#bunguran coordinates
lat1[4] = 0.3
lat2[4] = 5.1
lon1[4] = 105
lon2[4] = 110

#reef coordinates
lat1[5] = 0.3
lat2[5] = 9.75
lon1[5] = 110
lon2[5] = 115.3



#storing of outputs
output_winddirection = []
output_windmagnitude = []
output_weather = []
output_seastate = []
output_seaswell = []



for i in range(0,6):
#
### can use this code to find the *index of nearest lat/lon in the data* since the data has fixed lat/lon values for each grid
 lat1_at = (numpy.abs(Atmosphericlat - lat1[i])).argmin()
 lat2_at = (numpy.abs(Atmosphericlat - lat2[i])).argmin()
 lon1_at = (numpy.abs(Atmosphericlon - lon1[i])).argmin()
 lon2_at = (numpy.abs(Atmosphericlon - lon2[i])).argmin()
#
#
 lat1_wave = (numpy.abs(Wavelat - lat1[i])).argmin()
 lat2_wave = (numpy.abs(Wavelat - lat2[i])).argmin() 
 lon1_wave = (numpy.abs(Wavelon - lon1[i])).argmin()
 lon2_wave = (numpy.abs(Wavelon - lon2[i])).argmin()
#
#
#find vales of the necessary parameters
## for latitude use lat2 first as indexing goes from positive to negative for lat
 uwind1 = Atmospheric1.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind1 = Atmospheric1.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind2 = Atmospheric2.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind2 = Atmospheric2.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind3 = Atmospheric3.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind3 = Atmospheric3.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind4 = Atmospheric4.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind4 = Atmospheric4.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind5 = Atmospheric5.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind5 = Atmospheric5.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind6 = Atmospheric6.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind6 = Atmospheric6.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind7 = Atmospheric7.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind7 = Atmospheric7.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 uwind8 = Atmospheric8.variables['10U_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
 vwind8 = Atmospheric8.variables['10V_GDS0_SFC'][lat2_at:lat1_at,lon1_at:lon2_at]
#
 uwind = numpy.ma.dstack((uwind1,uwind2,uwind3,uwind4,uwind5,uwind6,uwind7,uwind8))  
 vwind = numpy.ma.dstack((vwind1,vwind2,vwind3,vwind4,vwind5,vwind6,vwind7,vwind8)) 
#
 windmagnitude = numpy.ma.sqrt((numpy.mean(uwind))**2+(numpy.ma.mean(vwind))**2)
#
# windmagnitude classification
 if windmagnitude <= 5:
     windmagnitudelow = 5
 else: 
     windmagnitudelow = int(math.floor(5*math.floor(windmagnitude/5)))
 windmagnitudecombined = numpy.zeros((len(uwind),len(uwind[0]),len(uwind[0][0])))
 for x in range(0,len(uwind)):
     for y in range(0,len(uwind[0])):
         for z in range(0,len(uwind[0][0])):
             windmagnitudecombined[x,y,z] = numpy.sqrt((uwind[x,y,z])**2+(vwind[x,y,z])**2) 
 windmagnitudehigh = numpy.max(windmagnitudecombined)
 windmagnitudehigh = int(round(5*math.ceil(windmagnitudehigh/5)))
#
 if windmagnitudehigh == 5:
     windmagnitudehigh = 10
#
 if windmagnitudelow == 5:
     windmagnitudelow = "05"
 else:
     windmagnitudelow = str(windmagnitudelow)
 windmagnitudehigh = str(windmagnitudehigh)
 winddirection = numpy.arctan(numpy.ma.mean(uwind)/numpy.ma.mean(vwind))
 winddirection = winddirection/numpy.pi*180
#
# wave data
 wave1 = Wave1.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave2 = Wave2.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave3 = Wave3.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave4 = Wave4.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave5 = Wave5.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave6 = Wave6.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave7 = Wave7.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 wave8 = Wave8.variables[“SHWW_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
#
 swell1 = Wave1.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell2 = Wave2.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell3 = Wave3.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell4 = Wave4.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell5 = Wave5.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell6 = Wave6.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell7 = Wave7.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
 swell8 = Wave8.variables[“SHTS_GDS0_MSL”][lat2_wave:lat1_wave,lon1_wave:lon2_wave]
#
 wave = numpy.ma.dstack((wave1,wave2,wave3,wave4,wave5,wave6,wave7,wave8))        
 swell = numpy.ma.dstack((swell1,swell2,swell3,swell4,swell5,swell6,swell7,swell8)) 
#
#
 waveheight = numpy.ma.max(wave)
 swellheight = numpy.ma.max(swell)
# 
 output_winddirection.append(WindDirection(winddirection))
 output_windmagnitude.append(windmagnitudelow + "/" + windmagnitudehigh)
 output_weather.append("Scattered showers/isolated thunderstorms")
 output_seastate.append(SeaState(waveheight))
 output_seaswell.append(SeaSwell(swellheight))

# end of loop


# output into XML format
root = Element("marine")
forecast1 = SubElement(root,"forecast")
area1 = SubElement(forecast1,"area")
area1.text = "phuket"
winddirection1 = SubElement(forecast1,"winddirection")
winddirection1.text = output_winddirection[0]
windmagnitude1 = SubElement(forecast1,"windmagnitude")
windmagnitude1.text = output_windmagnitude[0]
weather1 = SubElement(forecast1,"weather")
weather1.text = output_weather[0]
seastate1 = SubElement(forecast1,"seastate")
seastate1.text = output_seastate[0]
seaswell1 = SubElement(forecast1,"seaswell")
seaswell1.text = output_seaswell[0]

forecast2 = SubElement(root,"forecast")
area2 = SubElement(forecast2,"area")
area2.text = "malacca"
winddirection2 = SubElement(forecast2,"winddirection")
winddirection2.text = output_winddirection[1]
windmagnitude2 = SubElement(forecast2,"windmagnitude")
windmagnitude2.text = output_windmagnitude[1]
weather2 = SubElement(forecast2,"weather")
weather2.text = output_weather[1]
seastate2 = SubElement(forecast2,"seastate")
seastate2.text = output_seastate[1]
seaswell2 = SubElement(forecast2,"seaswell")
seaswell2.text = output_seaswell[1]

forecast3 = SubElement(root,"forecast")
area3 = SubElement(forecast3,"area")
area3.text = "tioman"
winddirection3 = SubElement(forecast3,"winddirection")
winddirection3.text = output_winddirection[2]
windmagnitude3 = SubElement(forecast3,"windmagnitude")
windmagnitude3.text = output_windmagnitude[2]
weather3 = SubElement(forecast3,"weather")
weather3.text = output_weather[2]
seastate3 = SubElement(forecast3,"seastate")
seastate3.text = output_seastate[2]
seaswell3 = SubElement(forecast3,"seaswell")
seaswell3.text = output_seaswell[2]

forecast4 = SubElement(root,"forecast")
area4 = SubElement(forecast4,"area")
area4.text = "condore"
winddirection4 = SubElement(forecast4,"winddirection")
winddirection4.text = output_winddirection[3]
windmagnitude4 = SubElement(forecast4,"windmagnitude")
windmagnitude4.text = output_windmagnitude[3]
weather4 = SubElement(forecast4,"weather")
weather4.text = output_weather[3]
seastate4 = SubElement(forecast4,"seastate")
seastate4.text = output_seastate[3]
seaswell4 = SubElement(forecast4,"seaswell")
seaswell4.text = output_seaswell[3]

forecast5 = SubElement(root,"forecast")
area5 = SubElement(forecast5,"area")
area5.text = "bunguran"
winddirection5 = SubElement(forecast5,"winddirection")
winddirection5.text = output_winddirection[4]
windmagnitude5 = SubElement(forecast5,"windmagnitude")
windmagnitude5.text = output_windmagnitude[4]
weather5 = SubElement(forecast5,"weather")
weather5.text = output_weather[4]
seastate5 = SubElement(forecast5,"seastate")
seastate5.text = output_seastate[4]
seaswell5 = SubElement(forecast5,"seaswell")
seaswell5.text = output_seaswell[4]

forecast6 = SubElement(root,"forecast")
area6 = SubElement(forecast6,"area")
area6.text = "reef"
winddirection6 = SubElement(forecast6,"winddirection")
winddirection6.text = output_winddirection[5]
windmagnitude6 = SubElement(forecast6,"windmagnitude")
windmagnitude6.text = output_windmagnitude[5]
weather6 = SubElement(forecast6,"weather")
weather6.text = output_weather[5]
seastate6 = SubElement(forecast6,"seastate")
seastate6.text = output_seastate[5]
seaswell6 = SubElement(forecast6,"seaswell")
seaswell6.text = output_seaswell[5]

mydata = tostring(root)
myfile = open("C:\Users\KangSheng\Desktop\FORECAST.xml","w")   
myfile.write(mydata)
myfile.close()









      

