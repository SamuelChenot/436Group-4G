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

    #put lists together for 48-hour information
    temps = []
    precips = []
    winds = []
    humids = []
    for i in range(0, 48):
        hour = curr_loc['hourly']['data'][i]
        
        #add the data for the current hour into the array
        temps.append(hour["temperature"])
        winds.append((hour["windSpeed"], hour["windBearing"]))
        humids.append(hour["humidity"])
        #if there's no probability of precipitation, there's no precipType
        if(hour['precipProbability'] != 0):
            precips.append(hour["precipType"])
        else:
            precips.append(None)

    # return necessary info for the next 48 hours
    return temps, precips, winds, humids

#put all info for all 48 hours in all mountains into a single dictionary
def assembleData(mountains):
    mountainInfo = {}
    #get the info for each mountain
    for mountain in mountains:
        temps, precips, winds, humids = getWeather(mountains[mountain][0], mountains[mountain][1])
        #put all that info into a dictionary by mountain name
        mountainInfo[mountain] = {'temperatures': temps, 'precipitations': precips, 'winds': winds, 'humidities': humids}
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
    while True:
        # #Call function on mountains every 12 hours
        if(curr_time == "12:00:00" or curr_time == "00:00:00"):
            mountainInfo = assembleData(mountains)
    print("Info:")
    print(mountainInfo)
    updateDatabase(mountainInfo)

main()