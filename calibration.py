# Calibration file for the odrive using the Quanum MT5208 BLDC motor

from __future__ import print_function 

import odrive
from odrive.enums import *
import time
import math

def save_calibration(save_drive):
    print("Saving configuration")
    save_drive.save_configuration()
    save_drive.reboot()
    print("Waiting for reboot")
    save_drive = find_drive()

def find_drive():
    # Find a connected ODrive (this will block until you connect one)
    print("finding an odrive...")
    found_drive = odrive.find_any()
    # Find an ODrive that is connected on the serial port /dev/ttyUSB0
    #my_drive = odrive.find_any("serial:/dev/ttyUSB0")
    return found_drive

def startup_sequence(my_drive):
    # Startup delay
    while my_drive.axis0.current_state == AXIS_STATE_STARTUP_SEQUENCE or my_drive.axis1.current_state == AXIS_STATE_STARTUP_SEQUENCE:
        time.sleep(0.1)
    # Check current configuration
    print("axis0 state =" + str(my_drive.axis0.current_state))
    print("axis1 state =" + str(my_drive.axis1.current_state))

    print("configuring axis 0")
    if my_drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
        # we are not configured in axis0
        if my_drive.axis0.motor.is_calibrated == True:
            if my_drive.axis0.encoder.is_ready == True:
                #reset startup configuration
                print("axis 0 startup reconfiguration")
                startup_configuration_0(my_drive)
            else:
                #reconfigure encoder calibration
                print("axis 0 encoder not calibrated")
                encoder_calibrate_0(my_drive)
                #reset startup configuration
                print("axis 0 startup reconfiguration")
                startup_configuration_0(my_drive)
        else:
            # full calibration required. Motor + encoder + startup
            set_limits(my_drive, 2) # brake resistance of 2 ohms
            set_axis_limits_0(my_drive)
            print("axis 0 motor not configured")
            motor_calibrate_0(my_drive)
            #reconfigure encoder calibration
            print("axis 0 encoder not calibrated")
            encoder_calibrate_0(my_drive)
            #reset startup configuration
            print("axis 0 startup reconfiguration")
            startup_configuration_0(my_drive)
    
    print("configuring axis 1")
    if my_drive.axis1.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
        # we are not configured in axis1
        if my_drive.axis1.motor.is_calibrated == True:
            if my_drive.axis1.encoder.is_ready == True:
                #reset startup configuration
                print("axis 1 startup reconfiguration")
                startup_configuration_1(my_drive)
            else:
                #reconfigure encoder calibration
                print("axis 1 encoder not calibrated")
                encoder_calibrate_1(my_drive)
                #reset startup configuration
                print("axis 1 startup reconfiguration")
                startup_configuration_1(my_drive)
        else:
            # full calibration required. Motor + encoder + startup
            set_limits(my_drive, 2)
            set_axis_limits_1(my_drive)
            print("axis 1 motor not configured")
            motor_calibrate_1(my_drive)
            #reconfigure encoder calibration
            print("axis 1 encoder not calibrated")
            encoder_calibrate_1(my_drive)
            #reset startup configuration
            print("axis 1 startup reconfiguration")
            startup_configuration_1(my_drive)


def set_limits(my_drive, braking_resistance):
    my_drive.config.brake_resistance = braking_resistance

def set_axis_limits_0(my_drive):
    my_drive.axis0.motor.config.current_lim = 10 #[A]
    my_drive.axis0.motor.config.calibration_current = 15 #[A]
    my_drive.axis0.controller.config.vel_limit = 300000 #[counts/s]
    my_drive.axis0.motor.config.pole_pairs = 7 #[magnet poles /2]
    my_drive.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
    my_drive.axis0.encoder.config.cpr = 8192 #[counts/rev]

def set_axis_limits_1(my_drive):
    my_drive.axis1.motor.config.current_lim = 10 #[A]
    my_drive.axis1.motor.config.calibration_current = 15 #[A]
    my_drive.axis1.controller.config.vel_limit = 300000 #[counts/s]
    my_drive.axis1.motor.config.pole_pairs = 7 #[magnet poles /2]
    my_drive.axis1.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
    my_drive.axis1.encoder.config.cpr = 8192 #[counts/rev]
    
def motor_calibrate_0(my_drive):
    my_drive.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    my_drive.axis0.motor.config.pre_calibrated = True

def motor_calibrate_1(my_drive):
    my_drive.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    while my_drive.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    my_drive.axis1.motor.config.pre_calibrated = True

def encoder_calibrate_0(my_drive):
    my_drive.axis0.encoder.config.use_index = True
    my_drive.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    my_drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    my_drive.axis0.encoder.config.pre_calibrated = True
    my_drive.axis0.config.startup_encoder_index_search = True

def encoder_calibrate_1(my_drive):
    my_drive.axis1.encoder.config.use_index = True
    my_drive.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while my_drive.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    my_drive.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
    while my_drive.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    my_drive.axis1.encoder.config.pre_calibrated = True
    my_drive.axis1.config.startup_encoder_index_search = True

def startup_configuration_0(my_drive):
    my_drive.axis0.config.startup_motor_calibration = False
    my_drive.axis0.config.startup_encoder_index_search = True
    my_drive.axis0.config.startup_encoder_offset_calibration = False
    my_drive.axis0.config.startup_closed_loop_control = True
    my_drive.axis0.config.startup_sensorless_control = False

    save_calibration(my_drive)
    while my_drive.axis0.current_state == AXIS_STATE_STARTUP_SEQUENCE:
        time.sleep(0.1)
    my_drive.axis0.requested_state == AXIS_STATE_CLOSED_LOOP_CONTROL

def startup_configuration_1(my_drive):
    my_drive.axis1.config.startup_motor_calibration = False
    my_drive.axis1.config.startup_encoder_index_search = True
    my_drive.axis1.config.startup_encoder_offset_calibration = False
    my_drive.axis1.config.startup_closed_loop_control = True
    my_drive.axis1.config.startup_sensorless_control = False

    save_calibration(my_drive)
    while my_drive.axis1.current_state == AXIS_STATE_STARTUP_SEQUENCE:
        time.sleep(0.1)
    my_drive.axis1.requested_state == AXIS_STATE_CLOSED_LOOP_CONTROL
