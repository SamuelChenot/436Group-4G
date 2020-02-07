from darksky import forecast
from api_keys import DARK_SKY_KEY
from datetime import datetime, timedelta

class Forecasts:
    # class constructor to get values
    def __init__(self, latitude, longitude):
        self.LOCATION = latitude, longitude
        self.date = datetime.now()
        self.timedelta = timedelta
        self.location = forecast(DARK_SKY_KEY, *self.LOCATION)

    def daily_forecast(self):
        """Returns a list of dictionary entries, each containing a list of weather attributes to be shown in
        daily forecast"""
        weekday = self.date
        print(self.location.daily.summary, end='\n---\n')
        week_summary_list = []
        for day in self.location.daily:
            # the %a is strftime's Weekday as locale’s abbreviated name, eg. "Mon".  See http://strftime.org/
            day = dict(day=datetime.strftime(weekday, '%a'),
                       summary=day.summary,
                       tempLow=round(day.temperatureLow),
                       tempHigh=round(day.temperatureHigh),
                       tempLowTime=day.temperatureLowTime,
                       tempeHighTime=day.temperatureHighTime,
                       windSpeed=round(day.windSpeed),
                       windBearing=degrees_to_cardinal(day.windBearing),
                       windGust=round(day.windGust),
                       precipProb=int(day.precipProbability*100),
                       uvIndex=day.uvIndex,
                       icon=day.icon
                       )
            #  print('{day}: {summary} Temp range: {tempLow} - {tempHigh}'.format(**day))
            week_summary_list.append(day)
            weekday += self.timedelta(days=1)
        # print(f"The weekly forecast is {summaryList}")
        return week_summary_list

    def hourly_forecast(self):
        """Returns a list of dictionary entries, each containing a list of weather attributes to be shown in
        hourly forecast."""
        # Set the hour to the current hour plus one, eg, if it is 10:15pm, we want the hourly forecast to begin at 11pm
        hour = self.date + self.timedelta(hours=1)
        # print(self.location.hourly.summary, end='\n---\n')
        hour_summary_list = []
        for time in self.location.hourly:
            time = dict(hour=datetime.strftime(hour, '%H'),  # The %H formats the date as the hour in 24-hour format.
                        summary=time.summary,
                        temp=round(time.temperature),
                        windSpeed=round(time.windSpeed),
                        windBearing=degrees_to_cardinal(time.windBearing),
                        windGust=round(time.windGust),
                        uvIndex=time.uvIndex
                        )
            # Add the current hour's forecast to the dictionary
            hour_summary_list.append(time)
            # Add 3 hours to the time since the user doesn't need to see the summary for every single hour
            hour += self.timedelta(hours=3)
        return hour_summary_list

    def current_conditions(self):
        """Returns the current conditions"""
        time = self.date
        #for time in self.location.currently:
        current_weather = dict(time=datetime.strftime(time, '%c'),  # The %c formats the date as the full date and time.
                               summary=self.location.currently.summary,
                               hourSummary=self.location.minutely.summary,
                               temp=round(self.location.currently.temperature),
                               feelsLike=round(self.location.currently.apparentTemperature),
                               humidity=round(self.location.currently.humidity),
                               dewPoint=round(self.location.currently.dewPoint),
                               windSpeed=round(self.location.currently.windSpeed),
                               windBearing=degrees_to_cardinal(self.location.currently.windBearing),
                               windGust=round(self.location.currently.windGust),
                               uvIndex=self.location.currently.uvIndex,
                               visibility=self.location.currently.visibility,
                               cloudCover=int((self.location.currently.cloudCover)*100),
                               ozone=self.location.currently.ozone,
                               icon=self.location.currently.icon
                               )
        return current_weather


def degrees_to_cardinal(windBearing):
    """Converts directional degrees into cardinal directions, rounding to the nearest cardinal direction"""
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    wind_direction = dirs[(round(windBearing / (360 / 8)) % 8)]

    return wind_direction


def get_weather(latitude, longitude):
    """Gets all of the weather data"""

    # creates a forecast object from the Forecasts class
    forecast = Forecasts(latitude, longitude)
    daily_forecast = forecast.daily_forecast()
    hourly_forecast = forecast.hourly_forecast()
    current_conditions = forecast.current_conditions()

    return daily_forecast, hourly_forecast, current_conditions


def print_daily_forecast(daily_forecast):
    for i in daily_forecast:
        print('{day}: {summary} Temp range: {tempLow} - {tempHigh}'.format(**i))


"""
# Main function for testing purposes:

def main(latitude, longitude):
    # sets the date to today's date
    # creates a forecast object from the Forecasts class
    forecast = Forecasts(latitude, longitude)
    #temperature, summary, dewPoint, humidity, wind, windBearing, pressure, ozone = forecast.hourly_forecast()

    daily_forecast = forecast.daily_forecast()
    #print_daily_forecast(daily_forecast)
    for i in daily_forecast:
        print("{day}: {summary} high of {tempHigh}°F and low of {tempLow}. Winds {windBearing} at {windSpeed} mph with gusts of {windGust} mph.".format(**i))

        # print("{day}: {summary} High of {round(float(tempHigh,0))}°F and low of {round(float(tempLow,0))} at {datetime.strftime(tempLowTime, '%c')}.  Winds {windBearing} at {round(float(windSpeed,0))} mph and gusts of {round(float(windGust),0)} mph.".format(**i))

    #print(daily_forecast)

    #hourly_forecast = forecast.hourly_forecast()
    #print(hourly_forecast)
    #curr = forecast.current_conditions()
    #print(curr)

    #print("-------------")
    #a1, a2, a3 = get_weather(latitude, longitude)
    #print(a1)
    #print(a2)
    #print(a3)
    #hourlyForecast__OLD()
    #print(hourly_forecast())
    #print(forecast.hourlySummary())
    #print('{day}: {sum} Temp range: {tempLow} - {tempHigh}'.format(**day))


    #return temperature, summary


main(41.431468, -71.467989)

# print(f"In {location_with_citystate[2]}, the temperature is {round(float(temperature),1)} F and it is {summary}.")

"""
