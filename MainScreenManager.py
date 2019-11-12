import kivy
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider

from kivy.config import Config

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')


class AdminLoginScreen(Screen):
    def verify_credentials(self):
        if self.ids["login"].text == "username" and self.ids["passw"].text == "password":
            self.manager.current = "settings"


class Experiment(Screen):
    def verify_inputs(self):
        desiredFlow = self.ids[''].text
        if desiredFlow < 0:
            print("please enter a value > 0")

    def switch_color(self):
        if self.ids['start'].text == 'Start':
            self.ids['start'].background_color = 1, 0, 0, 1
            self.ids['start'].text = 'Stop'
            pops = PanicPopup
            pops.fire_panic_popup(self)
        else:
            self.ids['start'].background_color = 0, 1, 0, 1
            self.ids['start'].text = 'Start'
            pops = WarningPopup
            pops.fire_warning_popup(self)


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


class WarningPopup(Popup):
    text = "Warning! Water Level Has Reached Warning Level"

    def fire_warning_popup(self):
        pops = WarningPopup()
        pops.open()


class PanicPopup(Popup):
    text = "PANIC! VFD SHUTTING DOWN TURN OFF WATER"

    def fire_panic_popup(self):
        pops = PanicPopup()
        pops.open()


root_widget = Builder.load_string('''
MyScreenManager:
    Experiment:
    AdminLoginScreen:  
    OpenMode:
    AdminSettingsScreen:
<AdminLoginScreen>:
    name: 'login'
    GridLayout:
        pos_hint: {'x' : .0, 'center_y' : .25}
        row_force_default: True
        row_default_height: 100
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
            on_release: app.root.current = 'exper'
        Button:
            text: "Sign In"
            font_size:40
            on_release: root.verify_credentials()
<Experiment>:
    name: 'exper'
    FloatLayout:
        Button:
            text: 'Admin Tools'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :.8, 'center_y' :.95}
            on_release: app.root.current = 'login'        
    GridLayout:
        pos_hint: {'x' : -.05, 'center_y' : .3}
        row_force_default: True
        row_default_height:100
        cols:3
        Label:
            text: 'Desired Flow Rate'
            font_size : 25
        Slider:
            id: desiredSlider
            min: 0 
            max: 100
            step: 1
        Label:
            text: str(desiredSlider.value) + ' m/s'
            font_size: 25
    GridLayout:
        pos_hint: {'x' : -.05, 'center_y' : .1}
        row_force_default: True
        row_default_height: 100
        cols: 4
        Label:
            font_size: 25
            text: 'Actual Flow Rate'
        Label:
            text: '____ m/s'
            font_size: 25
        Label:
            text: 'Water Temp'
            font_size: 25
        Label:
            text: '____ F/C'
            font_size: 25
        Label:
            text: 'Flume Angle'
            font_size: 25
        Label:
            id: flumeAngle
            text: '_____'
            font_size: 25
        Label:
            text: 'Valve Positioning'
            font_size: 25
        Label:
            id: valvePos
            text: '______'
            font_size: 25
    FloatLayout:
        Button:
            size_hint_y: .2
            font_size: 40
            pos_hint:{'x' : 0.25, 'center_y': .10}
            size_hint: (.5, .25)
            text: 'Start'
            background_color: 0,1,0,1
            id: start
            on_release: root.switch_color()
<PanicPopup>:
    id:panicPop
    size_hint: .4, .4
    auto_dismiss: False
    title: "PANIC"
    Button:
        text: 'Click to dismiss'
        on_press: panicPop.dismiss()
<WarningPopup>:
    id: warningPop
    size_hint: .4, .4
    auto_dismiss: False
    title: 'Warning'
    text: 'Warning! Water Level Has Reached Warning Level'
    Button:
        text: 'Click to dismiss'
        on_press: warningPop.dismiss()

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
        pos_hint: {'x' : -.05, 'center_y' : .25}
        row_force_default: True
        row_default_height: 100
        cols:3
        Label:
            text: 'Desired Flow Rate'
            font_size : 25
        Slider:
            id: desiredSlider2
            min: 0
            max: 100
            step: 1
        TextInput:
            multiline: False
            size_hint_y: .1
            id : desiredflow
            text: str(desiredSlider2.value)
            font_size: 25
            input_filter: 'float'
    GridLayout:
        pos_hint: {'x' :-.05, 'center_y' : .1}
        row_force_default: True
        row_default_height: 100
        cols: 4
        Label:
            font_size: 25
            text: 'Actual Flow Rate'
        TextInput: 
            multiline: False
            size_hint_y: .1
            id : actualflow
            readonly: True
        Label:
            text: 'Water Temp'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: waterTemp
            readonly: True 
        Label:
            text: 'Flume Angle'
            font_size: 25
        TextInput:
            multiline: False
            size_hint_y: .1
            id: flumeAngle
            readonly: True
        Label:
            text: 'Valve Positioning'
            font_size: 25
        TextInput: 
            multiline: False
            size_hint_y: .1
            id: valvePos
            readonly: True
    FloatLayout:
        Button:
            size_hint_y: .2
            font_size: 40
            pos_hint:{'x' : 0, 'center_y': .10}
            text: 'Start'
            background_color: 0,1,0,1
            id: start2
            on_release: root.switch_color()
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
        Button:
            text: 'Open Mode'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :.8, 'center_y' :.95}
            on_release: app.root.current = 'open'
    GridLayout:
        pos_hint: {'x' : .0, 'center_y' : .25}
        row_force_default: True
        row_default_height: 150
        cols:3
        orientation: 'vertical'
        Label:
            text: 'Set Max Flow Rate'
            font_size : 25
        Slider:
            id:MaxFlowSlider
            min: 0
            max: 100
            step: 1
        TextInput:
            multiline: False
            size_hint_y: .1
            id : maxFlow
            text: str(MaxFlowSlider.value)
            font_size : 40
        Label:
            font_size: 25
            text: 'Set Min Flow Rate'
        Slider:
            id:MinFlowSlider
            min: 0
            max: 100
            step: 1
        TextInput: 
            multiline: False
            size_hint_y: .1
            id : minFlow
            text: str(MinFlowSlider.value)
            font_size: 40
        Label:
            text: 'Set Warning Level'
            font_size: 25
        Slider:
            id:WarningSlider
            min: 0
            max: 100
            step: 1
        TextInput:
            multiline: False
            size_hint_y: .1
            id: warningLevel
            text: str(WarningSlider.value)
            font_size: 40 
        Label:
            text: 'Set Panic Level'
            font_size: 25
        Slider:
            id:PanicSlider
            min: 0
            max: 100
            step: 1
        TextInput:
            multiline: False
            size_hint_y: .1
            id: panicLevel
            text: str(PanicSlider.value)
            font_size: 40 

 ''')


class ScreenManagerApp(App):
    def build(self):
        return root_widget


ScreenManagerApp().run()
