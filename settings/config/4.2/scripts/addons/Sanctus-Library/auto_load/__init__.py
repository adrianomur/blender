from . geo import *
from . enums import *
from . ops import *
from . props import *
from . reg import *
from . shortcuts import *
from . ui import *
from . utils import *
from . prefs import *
from . property_ui import *

from . import config

def configure(prefix: str, package: str, version_str: str, debug: bool = False):
    config.ADDON_PREFIX = prefix
    config.ADDON_PACKAGE = package
    config.ADDON_VERSION = version_str
    config.DEBUG = debug
    if config.DEBUG:
        print('='*50)
        print(f'Configured Auto-Load: \nOperator Prefix={repr(config.ADDON_PREFIX)}, \nPackage={repr(config.ADDON_PACKAGE)}')
        print('='*50)
    setattr(get_addon_module(), config.REGISTER_MANAGER_NAME, RegisterManager())
    
    from . import property_operators
    GenericUIList.bl_idname = f'{config.ADDON_PREFIX}_UL_generic'
    register(GenericUIList)
    register(AL_PT_property_drawer_popover)
