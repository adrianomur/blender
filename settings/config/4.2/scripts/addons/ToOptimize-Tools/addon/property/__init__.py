import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)


from .main_props import TOT_Props,TOT_MatList_objectCollection,TOT_Imagelist_objectCollection,TOT_OBJBList_objectCollection
from .addon_prefs import TOT_Prefs

classes = (
    TOT_MatList_objectCollection, TOT_Imagelist_objectCollection,TOT_OBJBList_objectCollection,TOT_Props, TOT_Prefs,
)


def register_addon_properties():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.tot_props = bpy.props.PointerProperty(type= TOT_Props)

        


def unregister_addon_properties():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.tot_props