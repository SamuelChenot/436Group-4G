from darksky import forecast
from datetime import datetime
import re

#API Key
DARK_SKY_KEY = 'ce4149755b8988664a910e0ba7f9e5d1'

#pull the location data from the mountains file
def readFile(inputFile):
    #assemble the list of mountains from the data file
    mountains = {}
    infile = open(inputFile, 'r') 
    data = infile.readlines()
    for line in data:
        #split the data
        elems = line.split(",")
        #store the data into a dictionary
        mt_name = elems[0]
        mt_lat = float(elems[1])
        mt_lng = float(elems[2])
        mountains[mt_name] = (mt_lat, mt_lng)
    return mountains

#get the snowfall for both lists
def averageSnow(summary):
    if "snow" in summary:
        #find the height (in inches) of snow
        temp = re.findall(r'\d+', summary)
        #average the two if there is a comparison
        if(len(temp) == 2):
            return ((int(temp[0])+int(temp[1]))/2)
        #one measurement is given, return it
        elif(len(temp) == 1):
            return int(temp[0])
    #no snow, return 0 inches
    else:
        return 0

#Get weather information from Darksky
def getWeather(lat, lng):
    # imports the datetime library with the fields date and timedelta
    from datetime import date, timedelta

    #get the info for the current location
    curr_loc = forecast(DARK_SKY_KEY, lat, lng)
    hours = len(curr_loc.hourly)

    #lists for 48-hour info
    h_temp = []
    h_apparentTemp = []
    h_precipIntensity = []
    h_precipProb = []
    h_precipType = []
    h_windSpeed = []
    h_windGust = []
    h_windBearing = []
    h_humids = []
    h_clouds = []
    h_vis = []
    h_snow = []
    #lists for weekly info
    d_sunriseTime = []
    d_sunsetTime = []
    d_tempLow = []
    d_tempHigh = []
    d_precipIntensity = []
    d_precipMax = []
    d_precipProb = []
    d_precipType = []
    d_windSpeed = []
    d_windGust = []
    d_windGustTime = []
    d_windBearing = []
    d_humids = []
    d_clouds = []
    d_vis = []
    d_snow = []

    #get 48-hour data
    for i in range(0, 48):
        hour = curr_loc['hourly']['data'][i]
        #add the data for the current hour into the array
        h_temp.append(hour["temperature"])
        h_apparentTemp.append(hour["apparentTemperature"])
        h_precipIntensity.append(hour["precipIntensity"])
        h_precipProb.append(hour["precipProbability"])
        h_windSpeed.append(hour["windSpeed"])
        h_windGust.append(hour["windGust"])
        h_windBearing.append(hour["windBearing"])
        h_humids.append(hour["humidity"])
        h_clouds.append(hour["cloudCover"])
        h_vis.append(hour["visibility"])
        #get snow data using the summary
        h_snow.append(averageSnow(hour["summary"]))
        #if there's no probability of precipitation, there's no precipType
        if('precipType' in hour):
            h_precipType.append(hour["precipType"])
        else:
            h_precipType.append("None")
    #get weekly data
    for i in range(0, 7):
        day = curr_loc['daily']['data'][i]
        #add the data for the current day into the array
        d_precipIntensity.append(day["precipIntensity"])
        d_precipMax.append(day["precipIntensityMax"])
        d_precipProb.append(day["precipProbability"])
        d_tempLow.append(day["temperatureLow"])
        d_tempHigh.append(day["temperatureHigh"])
        d_humids.append(day["humidity"])
        d_windSpeed.append(day["windSpeed"])
        d_windGust.append(day["windGust"])
        d_windBearing.append(day["windBearing"])
        d_vis.append(day["visibility"])
        #convert time values from UNIX time to UTC time
        riseTime = datetime.utcfromtimestamp(day["sunriseTime"]).strftime("%H:%M:%S")
        setTime = datetime.utcfromtimestamp(day["sunsetTime"]).strftime("%H:%M:%S")
        gustTime = datetime.utcfromtimestamp(day["windGustTime"]).strftime("%H:%M:%S")
        d_sunriseTime.append(riseTime)
        d_sunsetTime.append(setTime)
        d_windGustTime.append(gustTime)
        #get the snow data using the summary
        d_snow.append(averageSnow(day["summary"]))
        #if there's no probability of precipitation, there's no precipType
        if('precipType' in day):
            d_precipType.append(day["precipType"])
        else:
            d_precipType.append("None")

    # return necessary info for the next 48 hours
    return h_temp, h_apparentTemp, h_precipIntensity, h_precipProb, h_precipType, h_windSpeed, h_windGust, h_windBearing, h_humids, h_clouds, h_vis, h_snow, d_sunriseTime, d_sunsetTime, d_tempLow, d_tempHigh, d_precipIntensity, d_precipMax, d_precipProb, d_precipType, d_windSpeed, d_windGust, d_windGustTime, d_windBearing, d_humids, d_clouds, d_vis, d_snow

#put all info for all 48 hours in all mountains into a single dictionary
def assembleData(mountains):
    mountainInfo = {}
    #get the info for each mountain
    for mountain in mountains:
        h_temp, h_apparentTemp, h_precipIntensity, h_precipProb, h_precipType, h_windSpeed, h_windGust, h_windBearing, h_humids, h_clouds, h_vis, h_snow, d_sunriseTime, d_sunsetTime, d_tempLow, d_tempHigh, d_precipIntensity, d_precipMax, d_precipProb, d_precipType, d_windSpeed, d_windGust, d_windGustTime, d_windBearing, d_humids, d_clouds, d_vis, d_snow = getWeather(mountains[mountain][0], mountains[mountain][1])
        #put all that info into a dictionary by mountain name
        mountainInfo[mountain] = {"hourly": {'temperature': h_temp, "apparentTemperature": h_apparentTemp, "precipIntensity": h_precipIntensity, "precipProbability": h_precipProb, "precipType": h_precipType, "windSpeed": h_windSpeed, "windGust": h_windGust, "windBearing": h_windBearing, "humidity": h_humids, "cloudCover": h_clouds, "visibility": h_vis, "averageSnowfall": h_snow}, "daily": {'sunriseTime': d_sunriseTime, "sunsetTime": d_sunsetTime, "temperatureLow": d_tempLow, "temperatureHigh": d_tempHigh, "precipIntensity": d_precipIntensity, "precipIntensityMax": d_precipMax, "precipProbability": d_precipProb, "precipType": d_precipType, "windSpeed": d_windSpeed, "windGust": d_windGust, "windGustTime": d_windGustTime, "windBearing": d_windBearing, "humidity": d_humids, "cloudCover": d_clouds, "visibility": d_vis, "averageSnowfall": d_snow}}
        print(mountain, " done.")
    print(mountainInfo)
    return mountainInfo

def updateDatabase(mountainInfo):
    #output dictionary to a CSV
    #need to do that here
    print("Database successfully updated!")

def main():
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    mountains = readFile('mountains.txt')
    #Intial call when program launches
    mountainInfo = assembleData(mountains)
    while False:
        # #Call function on mountains every 12 hours
        if(curr_time == "12:00:00" or curr_time == "00:00:00"):
            mountainInfo = assembleData(mountains)
    #add the dict data to the database
    updateDatabase(mountainInfo)

main()