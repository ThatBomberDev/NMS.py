import logging
import json
import ctypes
from dataclasses import dataclass

from pymhf.core.hooking import disable, on_key_pressed
from pymhf.core.memutils import map_struct
from pymhf.core.mod_loader import ModState
from nmspy import NMSMod
from pymhf.core.calling import call_function
import pymhf.core.hooking
from pymhf import FUNCDEF
from pymhf.core.module_data import module_data
from pymhf.gui import FLOAT
from pymhf.gui import STRING
from nmspy.data.common import TkID 
from nmspy.data.common import cTkFixedString
from nmspy.data.common import cTkStackVector

# A utility hook mod used to log server requests. WIP

@dataclass
class serverModState(ModState): #A special class inheriting from ModState which persists between mod Hot Reloads, allowing mod developers to cache pointers, values etc.
    seasonalDataAddress = 0

@disable
class serverCaptures(NMSMod):
    #General "Nice To Have"s
    __author__ = "ThatBomberBoi"
    __description__ = "Server Captures"
    __version__ = "0.1"
    __NMSPY_required_version__ = "0.7.0"    
    
    #Create an instance of the persistant ModState Class in your mod class.
    state = serverModState()   
     

    def __init__(self):
        super().__init__()
        self.should_print = True
        

    # Hook for the HTTP::Request::POST function used by any request sent by the game. Allows for the logging of the request body, as well as the partial mapping of the endpoint (WIP)
    postFuncDef = FUNCDEF(restype=ctypes.c_ulonglong,argtypes=[ctypes.c_ulonglong,ctypes.c_ulonglong,ctypes.c_ulonglong, ctypes.c_char_p,ctypes.c_int32,ctypes.c_int32]) 
    @pymhf.core.hooking.manual_hook(name="HTTP::Request::POST", offset=None, pattern="48 89 5C 24 10 48 89 6C 24 18 48 89 74 24 20 57 48 81 EC B0 00 00 00 48 63", func_def=postFuncDef, detour_time="after")
    def updateAuth(self, result, url, postData, a4, postDataSize, postDataMime):
        logging.info(f"Post Request to {str(map_struct(postData + 0x24, cTkFixedString[0x128]))}/{str(map_struct(postData + 0xA8, cTkFixedString[0x160]))}/: {str(a4)}")

    
    #seasonRequestFD = FUNCDEF(restype=ctypes.c_ulonglong, argtypes=ctypes.c_ulonglong)
    #@pymhf.core.hooking.manual_hook(name="cGcSeasonalData::RequestCurrentSeasonData", pattern="48 89 5C 24 08 48 89 74 24 10 57 48 83 EC 40 48 8B B1", func_def=seasonRequestFD, detour_time="after")
    #def onSeasonDataRequested(self, this):
    #    self.state.seasonalDataAddress = this
    #    logging.info(f"Requested Seasonal Info For Hash: {map_struct(this+0xD15, ctypes.c_ulonglong).value}")

