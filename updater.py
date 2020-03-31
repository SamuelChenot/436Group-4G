from darksky import forecast
from datetime import datetime

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

#Get weather information from Darksky
def getWeather(lat, lng):
    # imports the datetime library with the fields date and timedelta
    from datetime import date, timedelta

    #get the info for the current location
    curr_loc = forecast(DARK_SKY_KEY, lat, lng)
    hours = len(curr_loc.hourly)

    #lists for 48-hour info
    h_temps = []
    h_precips = []
    h_winds = []
    h_humids = []
    #lists for weekly info
    w_temps = []
    w_precips = []
    w_winds = []
    w_humids = []
    # print((curr_loc['daily']['data']))
    #get 48-hour data
    for i in range(0, 48):
        hour = curr_loc['hourly']['data'][i]
        #add the data for the current hour into the array
        h_temps.append(hour["temperature"])
        h_winds.append((hour["windSpeed"], hour["windBearing"]))
        h_humids.append(hour["humidity"])
        #if there's no probability of precipitation, there's no precipType
        if('precipType' in hour):
            h_precips.append(hour["precipType"])
        else:
            h_precips.append(None)

    for i in range(0, 7):
        day = curr_loc['daily']['data'][i]
        #add the data for the current day into the array
        w_temps.append((day["temperatureLow"], day["temperatureHigh"]))
        w_winds.append((day["windSpeed"], day["windBearing"]))
        w_humids.append(day["humidity"])
        #if there's no probability of precipitation, there's no precipType
        if('precipType' in day):
            w_precips.append(day["precipType"])
        else:
            w_precips.append(None)

    # return necessary info for the next 48 hours
    return h_temps, h_precips, h_winds, h_humids, w_temps, w_precips, w_winds, w_humids

#put all info for all 48 hours in all mountains into a single dictionary
def assembleData(mountains):
    mountainInfo = {}
    #get the info for each mountain
    for mountain in mountains:
        h_temps, h_precips, h_winds, h_humids, w_temps, w_precips, w_winds, w_humids = getWeather(mountains[mountain][0], mountains[mountain][1])
        #put all that info into a dictionary by mountain name
        mountainInfo[mountain] = {"daily": {'temperatures': h_temps, 'precipitations': h_precips, 'winds': h_winds, 'humidities': h_humids}, "weekly": {'temperatures': w_temps, 'precipitations': w_precips, 'winds': w_winds, 'humidities': w_humids}}
        print(mountain, " done.")
    return mountainInfo

def updateDatabase(mountainInfo):
    print("Database successfully updated")

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