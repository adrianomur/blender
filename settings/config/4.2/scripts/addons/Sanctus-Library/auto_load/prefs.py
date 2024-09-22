import bpy
import sys
import json
import typing
import bpy.types as bt

from pathlib import Path

from . import props
from . import config
from . import utils

class PreferenceFile:

    @classmethod
    def get(cls):
        addon_name = config.ADDON_PACKAGE
        addons_directory = Path(sys.modules[addon_name].__file__).parent.parent
        return addons_directory.joinpath(f'.{bpy.path.clean_name(addon_name)}_preferences.json')

    @classmethod
    def exists(cls):
        return cls.get().exists()

    @classmethod
    def read_json(cls) -> typing.Union[utils.JSONSerializable, None]:
        filepath = cls.get()
        data = filepath.read_text(encoding='utf-8')
        return json.loads(data)
    
    @classmethod
    def write_json(cls, data: utils.JSONSerializable):
        filepath = cls.get()
        filepath.unlink(missing_ok=True)
        filepath.write_text(json.dumps(data))

class AddonPreferences(props.AnnotatedObject, bt.AddonPreferences):
    bl_idname = ''

    @property
    def addon(self):
        import importlib
        return importlib.import_module(config.ADDON_PACKAGE)
    
    preference_file = PreferenceFile

    def __new__(cls, context: bt.Context = None):
        if context is None:
            context = bpy.context
        p: cls = context.preferences.addons[cls.bl_idname].preferences
        return p

    def __init__(self, context: bt.Context = None):
        pass  # Skipped because instantiating the class will not return a newly created object

def get_prefs() -> AddonPreferences:
    return bpy.context.preferences.addons[config.ADDON_PACKAGE].preferences