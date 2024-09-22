bl_info = {
    "name":         "Sanctus-Library",
    "author":       "Sanctus, Kolupsy",
    "version":      (3, 1, 0),
    "blender":      (4, 0, 0),
    "location":     "",
    "description":  "Sanctus Material Library",
    "warning":      "",
    "doc_url":      "http://sanctuslibrary.xyz",
    "category":     "Material",
}

from . import auto_load as al
from . import dev_info

al.configure(
    prefix='SL', 
    package=__package__,
    version_str=f'Addon: {bl_info["version"]}, git:{dev_info.GIT_VERSION}',
    debug=dev_info.DEBUG,
)

al.import_modules(__file__, __package__)

al.register_addon()