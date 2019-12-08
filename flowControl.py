import sensor
import time
from threading import Thread
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)


class Pump:
    def __init__(self):
        self.VFDPercent = 0
        self.desiredFlowRate = 0
        self.startThreadRunning = False
        self.stopThreadRunning = False
        self.maintainThreadRunning = False
        
    def setDesiredFlowRate(self, rate):
        self.desiredFlowRate = rate
    
    def startPump(self):
        self.VFDPercent = .25
        self.startThreadRunning = True
        self.stopThreadRunning = False
        self.maintainThreadRunning = False
        thr = Thread(target=self.rampUpPump, args=([lambda: self.startThreadRunning]))
        thr.daemon = True
        thr.start()
        
    def stopPump(self):
        self.startThreadRunning = False
        self.stopThreadRunning = True
        self.maintainThreadRunning = False
        thr = Thread(target=self.rampDownPump, args=([lambda: self.stopThreadRunning]))
        thr.daemon = True
        thr.start()
        
    def rampUpPump(self, run):
        GPIO.output(17,GPIO.HIGH)
        while sensor.getRawFlowRate() <= 0.75 and run():
            sensor.setDACValue(self.VFDPercent)
            if self.VFDPercent <.5:
                self.VFDPercent += .05
            time.sleep(10)
        if run():
            self.stopThreadRunning = False
            self.maintainThreadRunning = True
            thr = Thread(target=self.maintainPump, args=([lambda: self.maintainThreadRunning, lambda: sensor.getFlowRate(), lambda: self.desiredFlowRate]))
            thr.daemon = True
            thr.start()
        self.startThreadRunning = False
        
    def rampDownPump(self, run):
        while self.VFDPercent > 0 and run():
            self.VFDPercent -= .05
            if self.VFDPercent < 0:
                self.VFDPercent = 0
            sensor.setDACValue(self.VFDPercent)
            time.sleep(5)
        GPIO.output(17,GPIO.LOW)
            
    def maintainPump(self, run, currentRate, desiredRate):
        while run():
            if currentRate() < desiredRate()*.95:
                self.VFDPercent += .0025
                if self.VFDPercent >1:
                    self.VFDPercent = 1
                sensor.setDACValue(self.VFDPercent)
            elif currentRate() > desiredRate()*1.05:
                self.VFDPercent -= .0025
                if self.VFDPercent <0:
                    self.VFDPercent = 0
                sensor.setDACValue(self.VFDPercent)
            time.sleep(1)
        
