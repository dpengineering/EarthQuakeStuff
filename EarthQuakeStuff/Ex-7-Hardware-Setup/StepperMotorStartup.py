#!/usr/bin/python3

# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()

# Init a 200 steps per revolution stepper on Port 0
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)

# get current position and print it to the screen
s0.get_position_in_units()
# this tells us that the startup position is currently setup as the "home" position

# move stepper connected to port 0, 5 rotations clockwise
s0.start_relative_move(5)

# get current position and print it to the screen
s0.get_position_in_units()
# note the current position is 5 units - in this case 5 revolutions away from home

# move stepper connected to port 0, 5 rotations counter-clockwise
s0.start_relative_move(-5)

# get current position and print it to the screen
s0.get_position_in_units()
# note we are now back at "home"

# move stepper connected to port 0, 10 rotations counter-clockwise
s0.relative_move(-10)

# get current position and print it to the screen
s0.get_position_in_units()
# note we -10 rotations from "home"
# There is another way to get back to home regardless of where we are

# Tell the motor to go home and it will go home.
s0.goHome()

# we can also set the home position
# move stepper connected to port 0, 5 rotations counter-clockwise
s0.start_relative_move(-5)
s0.get_position_in_units()
s0.set_as_home()
s0.get_position_in_units()
# notice we have set the current position as home

# Notice how it is hard to turn the stepper shaft right now?
# This is because by default the SlushEngine leaves the stepper motor stalled or ON so it could hold something
# mechanical in this position. This is good but it consumes a lot of power, and the motor can get quite hot.
# so it is best to turn off or free the motor when we dont need it to be held in its current position.
s0.free
# Frees the motor - we can also free all the motors with one command with
s0.free_all()

# we can run a stepper until it detects a input like a switch or sensor to set the home position
# here the arguments are direction 0 or 1 and steps per second - note steps here does not account for microsteps
# so if we are using 32 micro steps and a standard 200 steps per revolution stepper to get 1 rev / sec
# 32 microsteps * 200 steps / revolution * 1 revolution / second = 6400 steps / second
s0.go_until_press(0, 6400)
# this function will reset the home position to the location that the switch was activated.


# we can stop the stepper at any point in its motion by issuing the following command
s0.softStop()
# softStop() allows the motor to correctly de-accelerate
s0.hard_stop()
# hard_stop() stops immediately, does not allow the motor to de-accelerate first.
# or similarly
s0.stop()
# which is the same as hard_stop

# another option to move is to move to a specific position - the argument that is specified is the number of steps
# So if we are using 32 micro steps and a standard 200 steps per revolution stepper to move one complete rotation
# 32 microsteps * 200 steps / revolution  = 6400 steps / revolution
# the following command will rotate the stepper exactly one rotation from home.
# if the stepper is already at position 3200, the the next command wil take it to 6400 so it will add 3200 microsteps,
# or 0.5 rotations.
s0.goTo(6400)

# One thing you may have noticed is that some commands such as
# s0.relative_move()
# s0.go_to_position()
# does not complete until the command is finished - so you cant run commands such as:
# s0.stop()
# s0.get_position_in_units()
# on the stepper until the command completes. These are often called blocking commands.
# Where as command such as:
# s0.start_relative_move()
# s0.start_go_to_position()
# are non blocking and allow you to enter commands on the stepper while the command completes.
#
# You may ask yourself why would you ever use the blocking commands? Well here is the deal. MOST motion commands such as:
# s0.relative_move()
# s0.go_to_position()
# and even
# s0.start_relative_move()
# s0.start_go_to_position()
#
# The programmed motion must complete before you can give it another motion command. The real difference is that is you
# use a non blocking command such as s0.start_go_to_position() you can run other commands like get position while you
# wait. However - if you use s0.start_go_to_position() you can do other things but you cant give it other movement
# commands until s0.start_go_to_position() finishes - so you have to monitor if it is finished with s0.is_busy() which
# will return True if the motion command is still going on (if the motor is busy), or False if the motion command is
# finished (if the motor is NOT busy)
#
# The only movement commands which do not have to complete before you can issue another motion command are:
# s0.goUntilPress() # makes the motor go until a press switch event occurs
# s0.goUntilRelease() # makes the motor go until a release switch event occurs
# s0.run() # makes the motor run in a direction and speed - you can use logic such as switch events or other position
#           data to stop the run command
#
# So -why didn't I mention these commands before (goUntilPress, goUntilRelease, run)?
# Because for simple state machines,like our initial examples, we tend to use:
# s0.relative_move()
# s0.go_to_position()
# s0.start_relative_move()
# s0.start_go_to_position()


# Now it is time to try initializing additional instances of the stepper.
# For example try creating stepper instance s1
# Init a 1036 steps per revolution stepper on Port 1 - this is for a stepper with a 5.18:1 planetary transmission
# https://www.omc-stepperonline.com/economy-planetary-gearbox/nema-17-stepper-motor-bipolar-l48mm-w-gear-raio-51-planetary-gearbox-17hs19-1684s-pg5.html?mfp=161-motor-nema-size%5BNema%2017%5D

s1 = stepper(port=1, micro_steps=32, hold_current=8, run_current=10, accel_current=10, deaccel_current=10,
             steps_per_unit=1038, speed=8)
s1.setAccel(0x50)
s1.setDecel(0x100)
s1.setMaxSpeed(525)
s1.setMinSpeed(0)
s1.setThresholdSpeed(1000)
s1.setOverCurrent(2000)
s1.setStallCurrent(2187.5)
s1.setLowSpeedOpt(False)
s1.setSlope(0x562, 0x010, 0x01F, 0x01F)
s1.setParam(L6470Registers.CONFIG, 0x3688)
s1.free()

# Now try using the s1 instance to move it back and forth, and back to hose as you did with the s0 instance.

# Now it is time to try initializing additional instances of the stepper.
# For example try creating stepper instance s2
# Init a 200 steps per revolution stepper on Port 2 with a lead screw that moves 8mm per revolution
# (200 steps/1 rev)* (1 rev/8 mm) which simplifies to 25 steps/mm giving us 25 for our steps_per_unit value
# https://www.pololu.com/product/2268

s2 = stepper(port=2, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=25, speed=8)
s2.setAccel(0x50)
s2.setDecel(0x100)
s2.setMaxSpeed(525)
s2.setMinSpeed(0)
s2.setThresholdSpeed(1000)
s2.setOverCurrent(2000)
s2.setStallCurrent(2187.5)
s2.setLowSpeedOpt(False)
s2.setSlope(0x562, 0x010, 0x01F, 0x01F)
s2.setParam(L6470Registers.CONFIG, 0x3688)
s2.free()

# Now try using the s2 instance to move it back and forth, and back to hose as you did with the s0 and s1 instances.

# after using s1 and s2 - for motors that have steps_per_unit specified - do you now see why it is best to use the
# unit based movements - example:
# s0.relative_move()
# s0.start_relative_move()
# s0.get_position_in_units()
# s0.go_to_position()
# s0.start_go_to_position()
#
# versus the non unit based movements ?
# s0.move()
# s0.get_position()
# s0.goTo()
#
# So you don't have to keep track of the micro stepping and any gear reduction and linear translation!

# One last thing! Before you exit the console session (or your python script if you exit your code) you need to do
# the following: De-allocate the RPi resources that are attached to this process, we need to run the following
# commands so that the next time we want to connect a stepper to one of the ports they are free / available.
s0.free_all()
spi.close()
GPIO.cleanup()

# And if you are need to reboot your RPi or you are done working for the day and want to shutdown
# the next commands will be helpful
# reboot the system
os.system("sudo reboot")
# alternatively we can shutdown the system with
os.system("sudo shutdown now")