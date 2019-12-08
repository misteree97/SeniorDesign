import time
import sensor
from flowControl import Pump

#Kivy imports
import kivy
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
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label

class P(FloatLayout):
    pass
class CustomDropDown(DropDown):
    pass

dropdown = CustomDropDown()
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_press=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
class drop_content(DropDown):
    pass
#from kivy.garden.graph import Graph

def show_warning_popup():
    show = P()
    box = BoxLayout(orientation = 'vertical')
    box.add_widget(Image(source='warning.jpeg'))
    closeButton = Button(text='Close')
   
    box.add_widget(closeButton)
    
    popupWindow = Popup(title="Warning Water Level Reached", content=box, size_hint = (None, None), size=(400,400))
    closeButton.bind(on_press=popupWindow.dismiss)
    popupWindow.open()
def show_panic_popup():
    show = P()
    box = BoxLayout(orientation = 'vertical')
    box.add_widget(Image(source='panic.jpeg'))
    
    closeButton = Button(text='Close')
    box.add_widget(closeButton)
    
    popupWindow = Popup(title = "PANIC WATER LEVEL REACHED", content=box, size_hint = (None, None), size=(400,400))
    closeButton.bind(on_press=popupWindow.dismiss)
    popupWindow.open()
    
class Experiment(Screen):
    #voltage3 = str(' C=%3.3f  F=%3.3f'% sensor.read_temp())
    sensor.setDACValue(0)
    def warning_btn(self):
        show_warning_popup()
    def panic_btn(self):
        show_panic_popup()
    def __init__(self, **kwargs):
        self.pump = Pump()
        self.flowRate = sensor.FlowRate()
        super(Screen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_values, .25)
        #Clock.schedule_interval(self.update_temp, 2)
        
    def update_temp(self, dt):
        pass
        
    def update_values(self, dt):
        self.pump.setDesiredFlowRate(self.ids['desiredSlider'].value)
        #self.ids['flumeAngle'].text = sensor.getInclineMeter()
        self.ids['VFDBack'].text = sensor.getVFDFeedback()
        self.ids['actualflow'].text = self.flowRate.getGUIFlowRate()
        self.ids['valvePos'].text = sensor.getValvePos()
        #self.ids['waterTemp'].text = sensor.getTemp()
                  
    #def buttonPress(self):
        #Clock.schedule_once(self.switch_color, .1)
        
    def switch_color(self):
        if self.ids['start1'].text == 'Start':
            self.pump.startPump()
            self.ids['start1'].background_color = 1, 0,0,1
            self.ids['start1'].text = 'Stop'
            print("started")
        else:
            self.pump.stopPump()
            self.ids['start1'].background_color = 0, 1, 0, 1
            self.ids['start1'].text = 'Start'
            print("stopped")
            
class AdminSettingsScreen(Screen):
    pass
                  

class MyScreenManager(ScreenManager):
    pass


class AdminLoginScreen(Screen):
    def verify_credentials(self):
        if self.ids["passw"].text == "1234":
            self.manager.current = "settings"
            

root_widget = Builder.load_string('''
MyScreenManager:
    Experiment:
    AdminLoginScreen:   
    AdminSettingsScreen:
<AdminLoginScreen>:
    name: 'login'
    on_leave: root.ids.passw.text = ""
    GridLayout:
        pos_hint: {'x' : 0, 'center_y' : .2}
        row_force_default: True
        row_default_height: 75
        cols: 2
        orientation: 'vertical'
        Label:
            text: 'PIN'
            font_size: 50
        TextInput:
            multiline: False
            id: passw
            password: True
            font_size: 50
            unfocus_on_touch: False
    GridLayout:
        pos_hint: {'x' : 0, 'center_y' : 0}
        row_force_default: True
        row_default_height: 75
        cols: 2
        orientation: 'vertical'
        Button:
            text: "Back"
            font_size: 40
            on_press:app.root.current = 'exper'
        Button:
            text: "Sign In"
            font_size:40
            on_press: root.verify_credentials()
<Experiment>:
    name: 'exper'
    RelativeLayout:
        size_hint: (.2,.15)
        pos_hint: {'center_x' : .9, 'center_y' : .95}
        Button:
            text: 'Admin Tools'
            font_size: 40
            on_press: app.root.current = 'login'
    GridLayout:
        pos_hint: {'x' : 0, 'center_y' : .3}
        row_force_default: True
        row_default_height: 100
        cols: 4
        Label:
            text: 'Desired Flow Rate'
            font_size : 25
        Slider:
            id: desiredSlider
            min: 0.00 
            max: 6.00
            step: 0.01
            value: float(desiredFlowRateTI.text)
        TextInput:
            id:desiredFlowRateTI
            foreground_color: (1,1,1,1)
            background_color: (0,0,0,0)
            text: "%05.2f"%(desiredSlider.value)
            font_size: self.height - 50
            height: 100
            unfocus_on_touch: False
            size_hint_y: None
        Button:
            text: 'F^3/s'
            id: DropDownBtn
            on_press: root.warning_btn()
            
    GridLayout:
        pos_hint: {'x' : 0, 'center_y' : .1}
        row_force_default: True
        row_default_height: 100
        cols: 4
        Label:
            font_size: 25
            text: 'Actual Flow Rate'
        Label:
            text:  ' V'
            id: actualflow
            font_size: 25
        Label:
            text: 'Valve Pos'
            font_size: 25
        Label:
            id: valvePos
            font_size: 25
        Label:
            text: 'Flume Angle'
            font_size: 25
        Label:
            id: flumeAngle
            font_size: 25
        Label:
            text: 'VFD Feedback'
            font_size: 25
        Label:
            id: VFDBack
            font_size: 25
    GridLayout:
        pos_hint: {'x' : 0, 'center_y' : -.15}
        row_force_default: True
        row_default_height: 100
        cols: 4
        Label:
        
        Label:
            font_size: 25
            text: 'Water Temp'
        Label:
            id: waterTemp
            font_size: 25
        Label:
        
    RelativeLayout:
        size_hint: (1, .14)
        pos_hint:{'center_x' : 0.5, 'center_y': 0.07}
        Button:
            font_size: 40
            text: 'Start'
            background_color: 0,1,0,1
            id: start1
            on_press: root.switch_color()
<AdminSettingsScreen>:
    name: 'settings'
    FloatLayout:
        Button:
            text: 'Back'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x' :0, 'center_y': .95}
            on_press: app.root.current = 'exper'
        Button:
            text: 'Save'
            font_size: 40
            size_hint: (.2,.15)
            pos_hint: {'x': .8, 'center_y': .95}
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
        Label:
            text: str(MaxFlowSlider.value)
            font_size: 25
            id: maxFlow
        Label:
            font_size: 25
            text: 'Set Min Flow Rate'
        Slider:
            id:MinFlowSlider
            min: 0
            max: 100
            step: 1
        Label:
            text: str(MinFlowSlider.value)
            font_size: 25
            id: minFlow
        Label:
            text: 'Set Warning Level'
            font_size: 25
        Slider:
            id:WarningSlider
            min: 0
            max: 100
            step: 1
        Label:
            text: str(WarningSlider.value)
            font_size: 25
            id: warningLevel
        Label:
            text: 'Set Panic Level'
            font_size: 25
        Slider:
            id:PanicSlider
            min: 0
            max: 100
            step: 1
        Label:
            text: str(PanicSlider.value)
            font_size: 25
            id: panicLevel
<P>:

<CustomDropDown>:
    id: drop_content
    on_select: parent.text = '{}'.format(args[1])
    Button:
        text: 'My first Item'
        size_hint_y: None
        height: 44
        on_press: root.select('item1')
    Label:
        text: 'Unselectable item'
        size_hint_y: None
        height: 44
    Button:
        text: 'My second Item'
        size_hint_y: None
        height: 44
        on_press: root.select('item2') 
 ''')


class ScreenManagerApp(App):
    def build(self):
        return root_widget

Window.fullscreen = True
ScreenManagerApp().run()
