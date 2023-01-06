import os
import spidev
import RPi.GPIO as GPIO

from datetime import datetime
from time import sleep
from threading import Thread

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

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

"""This stepper definition is used in the main screen and is called with s0"""

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)

s1 = stepper(port=1, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)


class MainScreen(Screen):

    s0_rotation_direction = 0
    s1_rotation_direction = 0
    clock_control = 0
    position = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

        """Things that are actually happening when the MainScreen class is called
        These variables are only defined here so they can be altered later.
        s0_rotation_dierction controls the rotation direction and stays between 1 and 0.
        clock_control helps control the clock, as if the_dance() has been called the variable should update
        and cancel the clock until the value is returned to 0, which the_dance function does when it is finished running"""

        #initalize update freqency of values
        Clock.schedule_interval(self.speed_change, 0.5)
        Clock.schedule_interval(self.position_update, 0.5)


    def move(self, motorNumber):

        if motorNumber == 1:
            if not s0.is_busy():
                s0.go_until_press(self.s0_rotation_direction, self.ids.speed_slider_1.value)
                print("moving!")

            else:
                s0.free()
                print("s0: I'm free!!")


        if motorNumber == 3:
            if not s0.is_busy():
                s0.go_until_press(self.s0_rotation_direction, self.ids.speed_slider_1.value)
                print("moving!")

            else:
                s0.free()
                print("s0: I'm free!!")

            if not s1.is_busy():
                s1.go_until_press(self.s1_rotation_direction, self.ids.speed_slider_2.value)
                print("moving!")

            else:
                s1.free()
                print("s0: I'm free!!")

        else:
            if not s1.is_busy():
                s1.go_until_press(self.s1_rotation_direction, self.ids.speed_slider_2.value)
                print("moving!")

            else:
                s1.free()
                print("s0: I'm free!!")

    def change_direction(self, motorNumber):

        #checks what motor to run
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

    def speed_change(self, motorNumber):

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


    def soft_stop(self, motorNumber):

        if motorNumber == 1:
            "Soft Stop motor 0"

            s0.softStop()
            print("stopping!")

        else:
            "Soft Stop motor 0"

            s1.softStop()
            print("stopping!")





    @staticmethod
    def exit_program():

        s0.free_all()
        cyprus.set_servo_position(1, 0.5)
        cyprus.close()
        GPIO.cleanup()
        print("freedom!")
        quit()



#    def servo_update(self, dt):
#
#        """Function to handle the limit switch and thus the servo motor"""
#
#        if SCREEN_MANAGER.current == SERVO_SCREEN_NAME:
#           print("hah")
#            if cyprus.read_gpio() & 0b0001:  # binary bitwise AND of the value returned from read.gpio()
#
#                cyprus.set_servo_position(1, .45)
#
#            else:
#
#                cyprus.set_servo_position(1, .55)

"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))

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
