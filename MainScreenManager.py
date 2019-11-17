import time
import board
import busio
import sensor

# ADC/DAC imports
import adafruit_ads1x15.ads1115 as ADS
import adafruit_mcp4725

# Kivy imports
import kivy
from adafruit_ads1x15.analog_in import AnalogIn
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.config import Config

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

# create i2c Bus
i2c = busio.I2C(board.SCL, board.SDA)

# create the ADC and DAC objects using the i2c bus
adc1 = ADS.ADS1115(i2c, address=0x48)
adc2 = ADS.ADS1115(i2c, address=0x49)
dac = adafruit_mcp4725.MCP4725(i2c)

# define ADC and DAC channels
ADC1Chan0 = AnalogIn(adc1, ADS.P0)
ADC1Chan1 = AnalogIn(adc1, ADS.P1)
ADC1Chan2 = AnalogIn(adc1, ADS.P2)
ADC1Chan3 = AnalogIn(adc1, ADS.P3)

ADC2Chan0 = AnalogIn(adc2, ADS.P0)
ADC2Chan1 = AnalogIn(adc2, ADS.P1)
ADC2Chan2 = AnalogIn(adc2, ADS.P2)
ADC2Chan3 = AnalogIn(adc2, ADS.P3)


class MainScreen(Screen):
    pass


class AdminLoginScreen(Screen):
    def verify_credentials(self):
        if self.ids["login"].text == "username" and self.ids["passw"].text == "password":
            self.manager.current = "settings"


class Experiment1(Screen):
    voltage0 = str(ADC1Chan0.voltage)
    voltage1 = str(ADC1Chan1.voltage)
    voltage2 = str(ADC2Chan0.voltage)
    voltage3 = str(' C=%3.3f  F=%3.3f' % sensor.read_temp())

    DacVal = 1.0
    dac.normalized_value = DacVal

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_temp, 1)
        Clock.schedule_interval(self.change_DAC_val, 1)

    def change_DAC_val(self, dt):
        if self.DacVal <= 0.9:
            self.DacVal += 0.1
        else:
            self.DacVal = 0.0

    def update_temp(self, dt):
        dac.normalized_value = self.DacVal
        voltage0 = str(ADC1Chan0.voltage)
        voltage1 = str(ADC1Chan1.voltage)
        voltage2 = str(ADC2Chan0.voltage)
        voltage3 = str(' C=%3.3f  F=%3.3f' % sensor.read_temp())
        self.ids['waterTemp'].text = voltage0
        self.ids['flumeAngle'].text = voltage1
        self.ids['valvePos'].text = voltage2
        self.ids['actualflow'].text = voltage3

    def switch_color(self):
        if self.ids['start1'].text == 'Start':
            self.ids['start1'].background_color = 1, 0, 0, 1
            self.ids['start1'].text = 'Stop'
        else:
            self.ids['start1'].background_color = 0, 1, 0, 1
            self.ids['start1'].text = 'Start'


class Experiment2(Screen):
    def switch_color(self):
        if self.ids['start2'].text == 'Start':
            self.ids['start2'].background_color = 1, 0, 0, 1
            self.ids['start2'].text = 'Stop'
        else:
            self.ids['start2'].background_color = 0, 1, 0, 1
            self.ids['start2'].text = 'Start'


class OpenMode(Screen):
    def switch_color(self):
        if self.ids['openStart'].text == 'Start':
            self.ids['openStart'].background_color = 1, 0, 0, 1
            self.ids['openStart'].text = 'Stop'
        else:
            self.ids['openStart'].background_color = 0, 1, 0, 1
            self.ids['openStart'].text = 'Start'


class AdminSettingsScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


root_widget = Builder.load_string('''
MyScreenManager:
    MainScreen:
    AdminLoginScreen:   
    Experiment1:
    Experiment2:
    OpenMode:
    AdminSettingsScreen:
<MainScreen>:
    name: 'main'
    BoxLayout:
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Experiment 1'
                font_size: 40
                on_release: app.root.current = 'exper1'
            Button:
                text: 'Experiment 2'
                font_size: 40
                on_release: app.root.current = 'exper2'
            Button:
                text: 'Open Mode'
                font_size: 40
                on_release: app.root.current = 'open'
        FloatLayout:
            Button: 
                text: 'Admin Tools'
                font_size: 40
                size_hint: (.3,.15)
                pos_hint: {'x' :.7, 'center_y' :.95}
                on_release: app.root.current = 'login'
<AdminLoginScreen>:
    name: 'login'
    GridLayout:
        pos_hint: {'x' : .0, 'center_y' : .25}
        row_force_default: True
        row_default_height: 150
        cols: 2
        orientation: 'vertical'
        Label:
            text: 'UserName'
            font_size: 40
        TextInput:
            multiline: False
            id: login
            font_size: 40
        Label:
            text: 'Password'
            font_size: 40
        TextInput:
            multiline: False
            id: passw
            password: True
            font_size: 40
        Button:
            text: "Back"
            font_size: 40
            on_release: app.root.current = 'main'
        Button:
            text: "Sign In"
            font_size:40
            on_release: root.verify_credentials()
<Experiment1>:
    name: 'exper1'
    FloatLayout:
        Button:
            text: 'Back'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :0, 'center_y': .95}
            on_release: app.root.current = 'main'
    GridLayout:
        pos_hint: {'x' : .0, 'center_y' : .25}
        row_force_default: True
        row_default_height: 150
        cols:4
        Label:
            text: 'Desired Flow Rate'
            font_size : 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id : desiredflow
        Label:
            font_size: 25
            text: 'Actual Flow Rate'
        TextInput: 
            multiline: False
            size_hint_y: .1
            id : actualflow
            text: root.voltage3
        Label:
            text: 'Water Temp'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: waterTemp
            text: root.voltage0
        Label:
            text: 'Flume Angle'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: flumeAngle
            text: root.voltage1
        Label:
            text: 'Valve Positioning'
            font_size: 25
        TextInput: 
            multiline: False
            size_hint_y: .1
            id: valvePos
            text: root.voltage2
    FloatLayout:
        Button:
            size_hint_y: .2
            font_size: 40
            pos_hint:{'x' : 0, 'center_y': .10}
            text: 'Start'
            background_color: 0,1,0,1
            id: start1
            on_release: root.switch_color()
<Experiment2>:
    name: 'exper2'
    FloatLayout:
        Button:
            text: 'Back'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :0, 'center_y': .95}
            on_release: app.root.current = 'main'
    GridLayout:
        pos_hint: {'x' : .0, 'center_y' : .25}
        row_force_default: True
        row_default_height: 150
        cols:4
        Label:
            text: 'Desired Flow Rate'
            font_size : 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id : desiredflow
        Label:
            font_size: 25
            text: 'Actual Flow Rate'
        TextInput: 
            multiline: False
            size_hint_y: .1
            id : actualflow
        Label:
            text: 'Water Temp'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: waterTemp
        Label:
            text: 'Flume Angle'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: flumeAngle
        Label:
            text: 'Valve Positioning'
            font_size: 25
        TextInput: 
            multiline: False
            size_hint_y: .1
            id: valvePos
    FloatLayout:
        Button:
            size_hint_y: .2
            font_size: 40
            pos_hint:{'x' : 0, 'center_y': .10}
            text: 'Start'
            background_color: 0,1,0,1
            id: start2
            on_release: root.switch_color()
<OpenMode>:
    name: 'open'
    FloatLayout:
        Button:
            text: 'Back'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :0, 'center_y': .95}
            on_release: app.root.current = 'main'
    GridLayout:
        pos_hint: {'x' : .0, 'center_y' : .25}
        row_force_default: True
        row_default_height: 150
        cols:4
        Label:
            text: 'Desired Flow Rate'
            font_size : 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id : desiredflow
        Label:
            font_size: 25
            text: 'Actual Flow Rate'
        TextInput: 
            multiline: False
            size_hint_y: .1
            id : actualflow
        Label:
            text: 'Water Temp'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: waterTemp
        Label:
            text: 'Flume Angle'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: flumeAngle
        Label:
            text: 'Valve Positioning'
            font_size: 25
        TextInput: 
            multiline: False
            size_hint_y: .1
            id: valvePos
    FloatLayout:
        Button:
            size_hint_y: .2
            font_size: 40
            pos_hint:{'x' : 0, 'center_y': .10}
            text: 'Start'
            background_color: 0,1,0,1
            id: openStart
            on_release: root.switch_color()
<AdminSettingsScreen>:
    name: 'settings'
    FloatLayout:
        Button:
            text: 'Back'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :0, 'center_y': .95}
            on_release: app.root.current = 'main'
    GridLayout:
        cols: 2
        Label:
            text: 'Max Flow Rate'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y:.1
            id: maxFlowRate
        Label:
            text: 'Min Flow Rate'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: minFlowRate
 ''')


class ScreenManagerApp(App):
    def build(self):
        return root_widget


ScreenManagerApp().run()