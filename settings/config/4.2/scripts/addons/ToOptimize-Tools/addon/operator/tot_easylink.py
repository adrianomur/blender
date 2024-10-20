import bpy

from os import listdir
from os.path import isfile, join

from ..utility.functions import link_object,unlink_object
from ..utility.addon import get_prefs
class TOT_OP_EasyLink(bpy.types.Operator):

    """Easy Link Tool, Easily convert selected objects to linked"""

    bl_idname = "tot.converttolink"
    bl_label = "Convert to Linked"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scn = context.scene.tot_props
        prefs = get_prefs()

        objs = bpy.context.selected_objects

        for ob in objs:

            if not link_object(ob):
                self.report({'ERROR'},"Failed to create link")                                                    
                return {"CANCELLED"}
   
        self.report({'INFO'},"Object Linked")                                                       
        return {"FINISHED"}

class TOT_OP_UNEasyLink(bpy.types.Operator):

    """Easy Link Tool, Restore selected object (unlink)"""

    bl_idname = "tot.unconverttolink"
    bl_label = "Restore Linked Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        cn = context.scene.tot_props
        prefs = get_prefs()

        objs = bpy.context.selected_objects

        for ob in objs:
            unlink_object(ob)
        
        self.report({'INFO'},"Object Restored") 
                                                        
        return {"FINISHED"}