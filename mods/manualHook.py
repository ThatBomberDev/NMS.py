import logging
import ctypes
from dataclasses import dataclass

import pymhf.core.memutils

import nmspy.data.functions.hooks as hooks
from pymhf.core.hooking import disable, on_key_pressed, on_key_release
from pymhf.core.memutils import map_struct
import nmspy.data.structs as nms_structs
from pymhf.core.mod_loader import ModState
from nmspy import NMSMod
from nmspy.decorators import main_loop
from pymhf.core.calling import call_function
from pymhf.gui.decorators import gui_variable, gui_button, STRING
import pymhf.core.hooking
from pymhf import FUNCDEF
from nmspy.data.common import cTkFixedString

@dataclass
class hookState(ModState):
    gameStateAddress = ctypes.c_ulonglong
    modifiedUAAddress = ctypes.c_ulonglong

@disable
class manualHook(NMSMod):
    __author__ = "ThatBomberBoi"
    __description__ = "Personal Tests"
    __version__ = "0.1"
    __NMSPY_required_version__ = "0.7.2"    

    state = hookState()

    def __init__(self):
        super().__init__()
        self.should_print = True

    # Hooks to the ClassifyVoxel function which appears to iterate over every galactic voxel. Purple System Variables are mapped using offsets from LibMBIN. 
    classifyFuncDef = FUNCDEF(restype=None, argtypes=[ctypes.c_ulonglong, ctypes.c_ulonglong])
    @pymhf.core.hooking.manual_hook(name="cGcGalaxyAttributeGenerator::ClassifyVoxel", offset=None, pattern="48 89 5C 24 08 48 89 6C 24 10 48 89 74 24 18 57 48 83 EC 40 0F BF", func_def=classifyFuncDef, detour_time="after")  
    def voxelClassified(self, *args): 
        purpleSystemsCount = map_struct(args[1] + 0x78, ctypes.c_int)
        purpleSystemsStart = map_struct(args[1] + 0x7C, ctypes.c_int)
        purpleSystemsCount.value = 150 # Enables Purple Systems, setting ~ 150 to spawn per region (default: 0)
        purpleSystemsStart.value = 1000 # Changes the index from which the first purple systems can start to spawn from (default: 1000)

     
    
    