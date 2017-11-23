#!/usr/bin/env python

# niryo_one_rpi_node.py
# Copyright (C) 2017 Niryo
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# All nodes related to Raspberry Pi are running here with only one node
# ( lower RAM usage )
#
#

import rospy
import RPi.GPIO as GPIO

from ros_log_manager import RosLogManager
from led_manager import LEDManager
from niryo_one_button import NiryoButton
from digital_io_panel import DigitalIOPanel
from wifi_connection import WifiConnectionManager
from niryo_one_ros_setup import *

FAN_1_GPIO = 23
FAN_2_GPIO = 27

class NiryoOneRpi:

    def setup_fans(self):
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FAN_1_GPIO, GPIO.OUT)
        GPIO.setup(FAN_2_GPIO, GPIO.OUT)
        rospy.sleep(0.1)
        GPIO.output(FAN_1_GPIO, GPIO.HIGH)
        GPIO.output(FAN_2_GPIO, GPIO.HIGH)
        rospy.loginfo("------ RPI FANS ON ------")

    def __init__(self):
        self.wifi_manager_enabled = rospy.get_param("~wifi_manager_enabled")
        self.launch_ros_processes = rospy.get_param("~launch_ros_processes")
        self.niryo_one_ros_setup = None

        if self.launch_ros_processes:
            self.niryo_one_ros_setup = NiryoOneRosSetup()
            rospy.sleep(10) # let some time for other processes to launch (does not affect total launch time)
        
        # Start wifi manager
        if self.wifi_manager_enabled:
            self.wifi_manager = WifiConnectionManager()
        
        self.setup_fans()
        self.ros_log_manager = RosLogManager()
        self.led_manager = LEDManager()
        self.niryo_one_button = NiryoButton()
        self.digital_io_panel = DigitalIOPanel()


if __name__ == '__main__':
    rospy.init_node('niryo_one_rpi')
    NiryoOneRpi()
    rospy.spin()
