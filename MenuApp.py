#disable multitouch functionality
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

#import the required kivy dependencies
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image
import webbrowser


#import all of the local python files that the group created
import time


#weather import statements
import weather
from datetime import date, timedelta



Builder.load_file('menubar.kv')
Builder.load_file('chatwindow.kv')
Builder.load_file('screens.kv')

class MenuContainer(AnchorLayout):

    #constructor
    def __init__(self, **kwargs):
        super(MenuContainer, self).__init__(**kwargs)

        #load the login popup when the app starts
        Clock.schedule_once(self.getStartupPopup, 0)

    def getStartupPopup(self, inst):
        pop = Popup(title='Welcome to SalmonBot!', title_align='center',content=Image(source='images/MainLogo.png'),
            size_hint=(None,None), height=400, width=400)
        pop.open()


class MenuManager(ScreenManager):

    #change the current screen to the one with the specified name
    def switchScreens(self, name):
        self.current = name

# TODO split these classes up into multiple different files, for readability
# where all of the screens functions can be stored.




class WeatherScreen(Screen):

    def getWeather(self):

        # save the string from the textbox and set the textbox to empty
        location = self.location_input.text
        self.location_input.text = ""

        # convert the location into latitude and longitude
        latitude, longitude, cityname = location_to_coords.main(location)

        # if the city isn't found, let the user know of the error
        if cityname == 'Unrecognized location':
            self.location_input.hint_text = "Error, location not found"
            self.location_input.hint_color = (1, .3, .3, 1)

        # otherwise, print out the current weather for that city
        else:

            # reset the userinput hint, in case they had an error before
            self.location_input.hint_text = "Enter ZIP code, city, or city/state"
            self.location_input.hint_color = (.2, .2, .2, 1)

            # display the name of the city
            self.city_label.text = f"Weather for {cityname}:"

            # display the city's weather
            ##  i have no idea: forecast = weather.Forecasts(lat, lng, date, timedelta)
            # i think what I should do is craft the main function to return each list of dictionaries.

            #  will use daily_forecast, hourly_forecast, current_conditions = weather.getCurrentget_weather(latitude, longitude)
            daily_forecast, hourly_forecast, current_conditions = weather.get_weather(latitude, longitude)
            """
            # temp, summ, icon, humid = weather.getCurrentget_weather(latitude, longitude)
            for i in daily_forecast:
                hey = ('{day}: {summary} Temp range: {tempMin} - {tempMax}'.format(**i))

            self.temp_button.text = hey
            """


            #temp, summ, icon, humid = weather.getCurrentget_weather(latitude, longitude)
            self.currently_button.text = "Current Conditions\n\n"\
                f"{current_conditions.get('temp')} °F\n" \
                f"(Feels like {current_conditions.get('feelsLike')} °F)\n" \
                f"{current_conditions.get('hourSummary')}\n" \
                f"{current_conditions.get('windBearing')} winds at " \
                f"{current_conditions.get('windSpeed')} mph\n" \
                f"{current_conditions.get('windGust')} mph gusts\n" \
                f"Visibility: {current_conditions.get('visibility')} miles\n" \
                f"UV Index: {current_conditions.get('uvIndex')}\n " \
                f"{current_conditions.get('cloudCover')}% cloud cover" \

            # Gets the weather icon from the weatherflaticons folder
            self.currently_button.background_normal = f"images\weatherflaticons\{current_conditions.get('icon')}.png"
            self.currently_button.background_down = f"images\weatherflaticons\{current_conditions.get('icon')}.png"

            self.hourly_button.halign = "left"
            self.hourly_button.font_size = 11
            self.hourly_button.text = f"                 Hourly Forecast\n\n" \
                f"{hourly_forecast[0].get('hour')}:00 {hourly_forecast[0].get('summary')}, {hourly_forecast[0].get('temp')}°F, {hourly_forecast[0].get('windSpeed')}mph {hourly_forecast[0].get('windBearing')}\n" \
                f"{hourly_forecast[1].get('hour')}:00 {hourly_forecast[1].get('summary')}, {hourly_forecast[1].get('temp')}°F, {hourly_forecast[1].get('windSpeed')}mph {hourly_forecast[1].get('windBearing')}\n" \
                f"{hourly_forecast[2].get('hour')}:00 {hourly_forecast[2].get('summary')}, {hourly_forecast[2].get('temp')}°F, {hourly_forecast[2].get('windSpeed')}mph {hourly_forecast[2].get('windBearing')}\n" \
                f"{hourly_forecast[3].get('hour')}:00 {hourly_forecast[3].get('summary')}, {hourly_forecast[3].get('temp')}°F, {hourly_forecast[3].get('windSpeed')}mph {hourly_forecast[3].get('windBearing')}\n" \
                f"{hourly_forecast[4].get('hour')}:00 {hourly_forecast[4].get('summary')}, {hourly_forecast[4].get('temp')}°F, {hourly_forecast[4].get('windSpeed')}mph {hourly_forecast[4].get('windBearing')}\n" \
                f"{hourly_forecast[5].get('hour')}:00 {hourly_forecast[5].get('summary')}, {hourly_forecast[5].get('temp')}°F, {hourly_forecast[5].get('windSpeed')}mph {hourly_forecast[5].get('windBearing')}\n" \
                f"{hourly_forecast[6].get('hour')}:00 {hourly_forecast[6].get('summary')}, {hourly_forecast[6].get('temp')}°F, {hourly_forecast[6].get('windSpeed')}mph {hourly_forecast[6].get('windBearing')}\n" \
                f"{hourly_forecast[7].get('hour')}:00 {hourly_forecast[7].get('summary')}, {hourly_forecast[7].get('temp')}°F, {hourly_forecast[7].get('windSpeed')}mph {hourly_forecast[7].get('windBearing')}\n" \
                f"{hourly_forecast[8].get('hour')}:00 {hourly_forecast[8].get('summary')}, {hourly_forecast[8].get('temp')}°F, {hourly_forecast[8].get('windSpeed')}mph {hourly_forecast[8].get('windBearing')}\n" \
                f"{hourly_forecast[9].get('hour')}:00 {hourly_forecast[9].get('summary')}, {hourly_forecast[9].get('temp')}°F, {hourly_forecast[9].get('windSpeed')}mph {hourly_forecast[9].get('windBearing')}\n" \
                f"{hourly_forecast[10].get('hour')}:00 {hourly_forecast[10].get('summary')}, {hourly_forecast[10].get('temp')}°F, {hourly_forecast[10].get('windSpeed')}mph {hourly_forecast[10].get('windBearing')}" \

            # Fills in the Weekly Forecast section
            self.daily_button.font_size = 11.5
            self.daily_button.text = f"Tomorrow: {daily_forecast[1].get('summary')}\n    High of {daily_forecast[1].get('tempHigh')}°F and low of {daily_forecast[1].get('tempLow')}°F.  Winds {daily_forecast[1].get('windBearing')} at {daily_forecast[1].get('windSpeed')} mph with gusts of {daily_forecast[1].get('windGust')} mph.\n" \
                f"{daily_forecast[2].get('day')}: {daily_forecast[2].get('summary')}\n    High of {daily_forecast[2].get('tempHigh')}°F and low of {daily_forecast[2].get('tempLow')}°F.  Winds {daily_forecast[2].get('windBearing')} at {daily_forecast[2].get('windSpeed')} mph with gusts of {daily_forecast[2].get('windGust')} mph.\n" \
                f"{daily_forecast[3].get('day')}: {daily_forecast[3].get('summary')}\n    High of {daily_forecast[3].get('tempHigh')}°F and low of {daily_forecast[3].get('tempLow')}°F.  Winds {daily_forecast[3].get('windBearing')} at {daily_forecast[3].get('windSpeed')} mph with gusts of {daily_forecast[3].get('windGust')} mph.\n" \
                f"{daily_forecast[4].get('day')}: {daily_forecast[4].get('summary')}\n    High of {daily_forecast[4].get('tempHigh')}°F and low of {daily_forecast[4].get('tempLow')}°F.  Winds {daily_forecast[4].get('windBearing')} at {daily_forecast[4].get('windSpeed')} mph with gusts of {daily_forecast[4].get('windGust')} mph.\n" \
                f"{daily_forecast[5].get('day')}: {daily_forecast[5].get('summary')}\n    High of {daily_forecast[5].get('tempHigh')}°F and low of {daily_forecast[5].get('tempLow')}°F.  Winds {daily_forecast[5].get('windBearing')} at {daily_forecast[5].get('windSpeed')} mph with gusts of {daily_forecast[5].get('windGust')} mph.\n" \
                f"{daily_forecast[6].get('day')}: {daily_forecast[6].get('summary')}\n    High of {daily_forecast[6].get('tempHigh')}°F and low of {daily_forecast[6].get('tempLow')}°F.  Winds {daily_forecast[6].get('windBearing')} at {daily_forecast[6].get('windSpeed')} mph with gusts of {daily_forecast[6].get('windGust')} mph.\n" \
                f"{daily_forecast[7].get('day')}: {daily_forecast[7].get('summary')}\n    High of {daily_forecast[7].get('tempHigh')}°F and low of {daily_forecast[7].get('tempLow')}°F.  Winds {daily_forecast[7].get('windBearing')} at {daily_forecast[7].get('windSpeed')} mph with gusts of {daily_forecast[7].get('windGust')} mph."

            # Include precipitation with {daily_forecast[1].get('precipProb')}% chance precipitation.

class LoginPopup(Popup):

    #open the signup screen and close the current login screen
    def openSignupPopup(self):
        SignupPopup().open()
        self.dismiss()

class SignupPopup(Popup):
    pass

class MenuButton(Button):
    pass
    
class MenuApp(App):
    def build(self):
        return MenuContainer()


MenuApp().run()
