from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Label

from kivy.lang import Builder


Builder.load_file("snow.kv")

class SnowApp(App, BoxLayout):

    def build(self):
        
        return self
            
SnowApp().run()
