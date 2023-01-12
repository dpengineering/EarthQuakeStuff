import os
import spidev
import RPi.GPIO as GPIO

from datetime import datetime
from time import sleep
from threading import Thread

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from pidev.stepper import stepper
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton

from Slush.Devices import L6470Registers

cyprus.initialize()
cyprus.setup_servo(1)  # sets up P4 on the RPiMIB as an RC servo style output
cyprus.set_servo_position(1, 0.5)

time = datetime
spi = spidev.SpiDev()

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'


"""

#Adjust spiral rotating disk posistion to control amplitude
#adjust disk rotate speed in sync to adjust freqency

#equation for amplitude can be calculated by manually applying a gradient along the sprial
# using that as the variable value and multiplying that by the change constant which is the
# amount the spiral shrinks in radius with each loop with max diameter of the spiral and the
# calibration to get the posistion we can use that to caculate the amplitude

def update_current_position():
    #make the color gradient corespond to apmpited then convert amplitude to poition on the spiral
    self.current_position = self.color_gradient_color*self.sclar_that_realtes_color_gradient_to_position on spiral
def sekiton_function_amplitude_control(amplitude):
    #convert desired ampliude to position on spiral and use position control to move the spiral to desired position
    self.current_amplitude = self.max_radius - (self.current_position*self.radius_decrease_per_position_change)

#increase or decrease speed to adjust the position of the disk on the spiral
def position_control(position):
    #calculate the distance traveled during the aceleration set the aceleration value constant with the stepper motor
    #set a value that increases or decreases speed by x value befre hand and increases or decreases speed when adjusting disk position
    #using the calculated distance traveled during aceleration/deceleration and convert that to am amplitude change then set that as a minimum change in amplitudeto make a change
    #set up a y = m*(x-(a+b)) function
    #where y is time, m is the distance traveled after reaching speed, x is desired distance to position on spiral,
    # a is distance change when accelerating, and b is distance change when decelerating
    
def frequency_control():
    #increase or decrease speed to increase freqency 
    
    
    
"""

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

"""This stepper definition is used everywhere stepper motors are called in this project. They are called with s0 and 
s1 and are defined as follows"""

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)

s1 = stepper(port=1, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)

global s0_rotation_direction
global s1_rotation_direction
s0_rotation_direction = 0
s1_rotation_direction = 1

class MainScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        """Things that are actually happening when the MainScreen class is called
        These variables are only defined here so they can be altered later.
        s0_rotation_dierction controls the rotation direction and stays between 1 and 0.
        clock_control helps control the clock, as if the_dance() has been called the variable should update
        and cancel the clock until the value is returned to 0, which the_dance function does when it is finished running"""

    def move(self, MotorNumber, rotation_direction):

        if not s0.is_busy() or not s1.is_busy():
            MotorNumber.go_until_press(rotation_direction, self.ids.speed_slider_1.value)
            print("moving!")

        else:
            MotorNumber.softStop()
            print("s0: I'm softStopped!")

    def move_both(self):
        # moves both motors and turns them off.

        if not s0.is_busy() or not s1.is_busy():
            self.move(s0, s0_rotation_direction)
            print("moving s0")
            self.move(s1, s1_rotation_direction)
            print("moving s1")

        else:
            s0.softStop()
            print("s0: I'm softStopped!!")
            s1.softStop()
            print("s1. I'm softStopped!")

    def speed_change(self):

        """The following is some weird old logic that Roshan wrote, it was based off of my (Rece's) old code and doesn't
        really apply to my old projects, but it's here if you need it"""

        """
            if motorNumber == 1:
                if self.clock_control == 0:
                    if s0.is_busy():
                        s0.go_until_press(self.s0_rotation_direction, self.ids.speed_slider_1.value)

            else:
                if self.s1_rotation_direction == 0:
                    self.s1_rotation_direction += 1
                    print("direction " + str(self.s1_rotation_direction))

                else:
                    if self.clock_control == 0:
                        if s0.is_busy():
                            s0.go_until_press(self.s0_rotation_direction, self.ids.speed_slider_1.value)
            """

        if s0.is_busy() or s1.is_busy():
            s0.go_until_press(s0_rotation_direction, self.ids.speed_slider_1.value)
            s1.go_until_press(s1_rotation_direction, self.ids.speed_slider_1.value)

    """The following function is currently commented out as this project should not ever need to change directions"""

    """    

    def change_direction(self, motorNumber):

            # checks what motor to run
            if motorNumber == 1:
                if s0.is_busy():
                    if self.s0_rotation_direction == 0:
                        self.s0_rotation_direction += 1
                        print("direction " + str(self.s0_rotation_direction))

                    else:
                        self.s0_rotation_direction -= 1
                        print("direction " + str(self.s0_rotation_direction))

                    s0.go_until_press(self.s0_rotation_direction, self.ids.speed_slider_1.value)

            else:
                if self.s1_rotation_direction == 0:
                   self.s1_rotation_direction += 1
                    print("direction " + str(self.s1_rotation_direction))

                else:
                    self.s1_rotation_direction -= 1
                    print("direction " + str(self.s1_rotation_direction))

                s1.go_until_press(self.s1_rotation_direction, self.ids.speed_slider_2.value) 

    """

    def soft_stop(self):
        s0.softStop()
        print("s0: stopping!")

        s1.softStop()
        print("s1: stopping!")

    @staticmethod
    def exit_program():
        s0.free_all()
        cyprus.close()
        GPIO.cleanup()
        print("freedom!")
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name='main'))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
