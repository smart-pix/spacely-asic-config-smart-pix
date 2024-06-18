#ExampleASIC Routines File
#
# This file contains any custom code that you want to write for your ASIC,
# for example routines to read or write to registers, or to run tests.

# python
import time

# spacely
from Master_Config import *
import Spacely_Globals as sg
from Spacely_Utils import *


#<<Registered w/ Spacely as ROUTINE 0, call as ~r0>>
def ROUTINE_basicLoopback():
    """This routine tests basic loopback from data_in to data_out"""    
    #Define the routine's purpose in a docstring like above, this will appear
    #when you call the routine in Spacely.

    '''
    1. Reset AXI interface (~S_AXI_ARESETN)
    '''
    sg.INSTR["car"].set_memory("S_AXI_ARESETN", 0)


    '''
    2. Initiate below writes in-order
    0x00000011 <--- sets superpixsel and opcode for reset
    0x00000022 <--- sets opcode for configin with data
    0x00000003 <--- sets opcode for wait
    0x00000004 <--- sets opcode for configout
    '''


    '''
    3. Snoop on reg_rddin[0] [3:0] for status
    if(4'b0001) IDLE_STATUS      <--- FSM is in IDLE state
    if(4'b0010) RESET_STATUS     <-- Superpixsel is programmed and reset is de-asserted, asserted back at following edge of ConfigClk
    if(4'b0011) CONFIGIN_STATUS  <-- bit 1 is inserted into shift register i.e asserted and de-asserted back at following edge of ConfigClk
    if(4'b0100) WAIT_STATUS      <-- FW has waited for 5164 cycles
    if(4'b1000) CONFIGOUT_STATUS <-- FW sends final value for ConfigOut
    '''
    snoop = True
    statuses = {
        "4'b0001" : "IDLE_STATUS",
        "4'b0010" : "RESET_STATUS",
        "4'b0011" : "CONFIGIN_STATUS",
        "4'b0100" : "WAIT_STATUS",
        "4'b1000" : "CONFIGOUT_STATUS",
    }
    while snoop:

        reg_rddin = sg.INSTR["car"].get_memory("reg_rddin")
        time.sleep(0.5)
        print(reg_rddin)
        
        # check status
        for key, val in statuses.items():
            if reg_rddin == key:
                print(val)
        

    '''
    4. As soon as SW sees CONFIGIN status, it can snoop upon reg_rddin[1][0] for ConfigOut 
    '''
    
    # reg_wrdout = sg.INSTR["car"].get_memory("reg_wrdout")
    # reg_wrdout = int(reg_wrdout)

    # time.sleep(0.5)
    
    # # write something
    # temp = int(not (reg_wrdout == 1))
    # write = sg.INSTR["car"].set_memory("reg_wrdout", temp)
    # time.sleep(0.5)
    
    # reg_wrdout = int(sg.INSTR["car"].get_memory("reg_wrdout"))
    # print(temp, write, reg_wrdout)
    
    pass


#<<Registered w/ Spacely as ROUTINE 1, call as ~r1>>
def ROUTINE_drivePin():

    sw_write32_0 = sg.INSTR["car"].get_memory("sw_write32_0")
    print(sw_write32_0)
    
    sw_write32_0 = sg.INSTR["car"].set_memory("sw_write32_0", 1 if sw_write32_0 == 0 else 0)
    print(sw_write32_0)

    sw_write32_0 = sg.INSTR["car"].get_memory("sw_write32_0")
    print(sw_write32_0)


# IMPORTANT! If you want to be able to run a routine easily from
# spacely, put its name in the "ROUTINES" list:
ROUTINES = [ROUTINE_basicLoopback, ROUTINE_drivePin]
