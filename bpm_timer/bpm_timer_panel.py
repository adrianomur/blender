import bpy
from bpy.types import Operator

from bpy.utils import register_class, unregister_class


bl_info = {
    "name": "BPM keyframe",
    "description": "Set keyframe based on the BPM",
    "author": "Adriano Muraca",
    "version": (0, 0, 1),
    "blender": (2, 9, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object"}


class BPM_Keyframe_Panel(bpy.types.Panel):
    bl_label = "BPM Keyframe Panel"
    bl_idname = "OBJECT_PT_BPM_Keyframe"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Keyframes"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.operator(BPM_Keyframe_Operator.bl_idname, text="BPM Keyframe", icon="KEYTYPE_KEYFRAME_VEC")


class BPM_Keyframe_Operator(Operator):
    bl_idname = 'bpm_keyframe.1'
    bl_label = "BPM Keyframe"

    def execute(self, context):
        print('executed')
        return ('Finished')


_classes = {
    BPM_Keyframe_Operator, 
    BPM_Keyframe_Panel
}


def register():
    for _cls in _classes:
        register_class(_cls)


def unregister():
    for _cls in _classes:
        unregister_class(_cls)


if __name__ == "__main__":
    register()