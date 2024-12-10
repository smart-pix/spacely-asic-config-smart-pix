'''
Author: Anthony Badea, Benjamin Parpillon
Date: June, 2024
'''

# python
import time
import tqdm
import h5py
from datetime import datetime
import csv

# spacely
from Master_Config import *
import Spacely_Globals as sg
from Spacely_Utils import *

superpixel = 0
# note that all functions in CMSPIX28_Subroutines.py will automatically be imported by Master_Config.py

def onstartup():

    # GLOBAL CONFIG VARIABLES
    assume_defaults = False
    
    print("====================================")
    print("=== Starting CMSPIX28 Default Setup ===")

    if not assume_defaults:
        do_setup = input("Press enter to begin or 'n' to skip >")
        if 'n' in do_setup:
            print("Skipping all setup!")
            return

    init_car =  input("Step 2: Initializing CaR Board ('n' to skip)>>>")

    if 'n' in init_car:
        print("Skipped!")
    else:

        #Basic initialization of CaR board
        sg.INSTR["car"].init_car()

        #Init CMOS I/O voltages
        print(">  Setting CMOS In/Out Voltage = 0.9 V",end='')
        if not assume_defaults: 
            set_cmos_voltage = input("('n' to skip)")
        if assume_defaults or not 'n' in set_cmos_voltage:
            sg.INSTR["car"].set_input_cmos_level(0.9)
            sg.INSTR["car"].set_output_cmos_level(0.9)
        print("finished setting CMOS")
       

    init_asic = input("Step 3: Initializing ASIC ('n' to skip)>>>")

    if 'n' in init_asic:
        print("Skipped!")
    else:
        iDVDD = V_PORT["vddd"].get_current()
        iAVDD = V_PORT["vdda"].get_current()
        print(f"DVDD current is {iDVDD}")
        print(f"AVDD current is {iAVDD}")
        print("Programming of the ASIC shift register")
        # ROUTINE_IP1_test1() -> converted to ROUTINE_ProgPixelsOnly()
        print("shift register Programmed")
        iDVDD = V_PORT["vddd"].get_current()
        iAVDD = V_PORT["vdda"].get_current()
        print(f"DVDD current is {iDVDD}")
        print(f"AVDD current is {iAVDD}")

#<<Registered w/ Spacely as ROUTINE 0, call as ~r0>>
def ROUTINE_ProgPixelsOnly():
    return ProgPixelsOnly()

#<<Registered w/ Spacely as ROUTINE 1, call as ~r1>>
def ROUTINE_ProgShiftRegs():
    return ProgShiftRegs()

#<<Registered w/ Spacely as ROUTINE 2, call as ~r2>>
def ROUTINE_ScanChainOneShot():
    return ScanChainOneShot()

#<<Registered w/ Spacely as ROUTINE 3, call as ~r3>>
def ROUTINE_PreProgSCurve():
    return PreProgSCurve()

#<<Registered w/ Spacely as ROUTINE 4, call as ~r4>>
def ROUTINE_IterMatrixSCurve():
    return IterMatrixSCurve()

#<<Registered w/ Spacely as ROUTINE 5, call as ~r5>>
def ROUTINE_DNN():
    return DNN()
