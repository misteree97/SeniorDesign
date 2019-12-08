#########################################################
#
# DAC/ADCs Config
#
#########################################################

#ADC/DAC imports
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS
import adafruit_mcp4725
import busio
import board

#create i2c Bus
i2c = busio.I2C(board.SCL, board.SDA)

#create the ADC and DAC objects using the i2c bus
adc1 = ADS.ADS1115(i2c, address = 0x48)
adc2 = ADS.ADS1115(i2c, address = 0x49)
dac = adafruit_mcp4725.MCP4725(i2c)

#define ADC and DAC channels
ADC1Chan0 = AnalogIn(adc1, ADS.P0)
ADC1Chan1 = AnalogIn(adc1, ADS.P1)
ADC1Chan2 = AnalogIn(adc1, ADS.P2)
ADC1Chan3 = AnalogIn(adc1, ADS.P3)

ADC2Chan0 = AnalogIn(adc2, ADS.P0)
ADC2Chan1 = AnalogIn(adc2, ADS.P1)
ADC2Chan2 = AnalogIn(adc2, ADS.P2)
ADC2Chan3 = AnalogIn(adc2, ADS.P3)

#########################################################
#
# ADC/DAC Functions
#
# ADC1Chan0 - Flow Rate 
# ADC1Chan1 - 
# ADC1Chan2 - Incline Meter
# ADC1Chan3 - VALVE
# 
# ADC2Chan0 - Water Level 1 - Warning
# ADC2Chan1 - Water Level 2 - E-Stop
# ADC2Chan2 - VFD FEEDBACK
# ADC2Chan3 - 
#
#########################################################

#ADC1Chan0
class FlowRate:
    def __init__(self):
        self.prevFlowRate = 0
    
    def getGUIFlowRate(self):
        newFlowRate = ((3.829375*ADC1Chan0.voltage) -1.5175)
        flowrate = (.25*newFlowRate) + (.75*self.prevFlowRate)
        self.prevFlowRate = flowrate
        if flowrate < 0:
            flowrate = 0
        return "%05.2f F^3/s"%flowrate

def getFlowRate(): 
    return (3.829375*ADC1Chan0.voltage) - 1.5175

def getRawFlowRate(): 
    return round(ADC1Chan0.voltage, 2)

#ADC2Chan2
def getVFDFeedback():
    feedback = ((1000/33)*(ADC2Chan2.voltage))
    if feedback < 0:
        feedback = 0
    return "%04.1f %%"%feedback

#ADC1Chan2
def getInclineMeter():
    return str(round(ADC1Chan2.voltage, 2)) + ' %'

#ADC1Chan3
def getValvePos():
    valvePercent = (100000/1009*ADC1Chan3.voltage) - (44500/1009)
    if valvePercent > 100:
        valvePercent = 100
    elif valvePercent < 0:
        valvePercent = 0
    return "%04.1f %%"%valvePercent

#ADC2Chan0
def getWarningWaterLevel():
    return str(round(ADC2Chan0.voltage, 2)) + 'V'

#ADC2Chan1
def getEStopWaterLevel():
    return str(round(ADC2Chan1.voltage, 2)) + 'V'


#DAC
def setDACValue(value):
    dac.normalized_value = value
    return


#########################################################
#
# Temp Sensor - 750ms to get each reading (becuase of driver)
#
#########################################################
import os
import glob
from threading import Thread
import queue

#onewire config
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

que = queue.Queue()


def getTemp():
    thr = Thread(target=lambda q: q.put(read_temp()), args=([que]))
    thr.daemon = True
    thr.start()
    return str(' C=%3.2f  F=%3.2f'% que.get())

# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f