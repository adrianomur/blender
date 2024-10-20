import bpy
import ast

from mathutils import Color
from ..utility.addon import get_prefs 
from ..utility.functions import get_verts_mod 

class TOT_OP_3dview_Analyzer(bpy.types.Operator):
    """Scene Analyzer"""
    bl_idname = "tot.r3dviewanalyzer"
    bl_label = "Scene Analyzer"
    bl_description = "Scene Analyzer"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scn = context.scene.tot_props
        prefs = get_prefs()

        scn.last_shading = bpy.context.space_data.shading.color_type

        scn.default_colors = '' 

        if prefs.store_colors:
            color_dict = {}
            for ob in bpy.data.objects:
                col_list = []
                if ob: 
                    for c in ob.color:
                        col_list.append(c)
                        
                    if not ob.name in color_dict:
                        color_dict[ob.name] = col_list
            
            new_dict = str(color_dict)
            scn.default_colors = new_dict     
     
        c = Color()

        if scn.SceneA_Method == 'm1':
            obj = bpy.data.objects
        if scn.SceneA_Method == 'm2':

            if not bpy.context.selected_objects:
                self.report({'WARNING'}, "No Selected Objects")
                return {'CANCELLED'}

            for ob in bpy.data.objects:  
                if ob:                                                                                          
                    ob.color = (1, 1, 1, 1)               

            obj = bpy.context.selected_objects
        
        if scn.SceneA_Method == 'm3':
            obj = [ob for ob in bpy.data.objects if ob.visible_get() == True]

        scene_vertices = 0
        high = 0

        for v in obj:           
            obj_v = 0           
            if v.type == 'MESH':   
                if prefs.includ_mod and v.modifiers:

                    obj_v = get_verts_mod(v) 

                    if obj_v > high:                   
                        high = obj_v 
                    else:
                        pass  

                    scene_vertices += obj_v  
                   
                else:
  
                    obj_v = (len(v.data.vertices))           
                    if obj_v > high:                   
                        high = obj_v 
                    else:
                        pass                                          
                    scene_vertices += obj_v                              
            else:
                pass
        
        for ob in obj:          
            if ob.type == 'MESH':
                if prefs.includ_mod and ob.modifiers :

                        col_ob = get_verts_mod(ob)
                        porcent = (high - col_ob)/high                                              
                        hue_color = 0.5 * porcent              
                        c.hsv = hue_color, 1, 1             
                        ob.color = (c[0], c[1], c[2], 1)

                else:                                                      
                    col_ob = len(ob.data.vertices)              
                    porcent = (high - col_ob)/high                                              
                    hue_color = 0.5 * porcent              
                    c.hsv = hue_color, 1, 1             
                    ob.color = (c[0], c[1], c[2], 1)                
            else:
                if ob: 
                    hue_color = 0.5
                    c.hsv = hue_color, 1, 1             
                    ob.color = (c[0], c[1], c[2], 1)  

        bpy.context.space_data.shading.type = 'SOLID'
        bpy.context.space_data.shading.color_type = 'OBJECT'

        return {"FINISHED"}
        
class TOT_OP_3dview_Analyzer_Clean(bpy.types.Operator):

    """Clean 3D View Analyzer Colors."""

    bl_idname = "tot.clean3dviewanalyzer"
    bl_label = "Clean 3D View Analyzer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        scn = context.scene.tot_props
        obj = bpy.data.objects
        prefs = get_prefs()

        if prefs.store_colors:

            if scn.default_colors:
                default_colors = eval(scn.default_colors)

            for c in default_colors:

                ob = bpy.data.objects.get(c)

                if ob: 
                    ob.color[0] = default_colors[c][0] 
                    ob.color[1] = default_colors[c][1]  
                    ob.color[2] = default_colors[c][2]  
                    ob.color[3] = default_colors[c][3] 

                    scn.default_colors = ''  

        else:
            for ob in obj:
                if ob:                                                                                            
                    ob.color = (1, 1, 1, 1)               


        bpy.context.space_data.shading.type = 'SOLID'
        bpy.context.space_data.shading.color_type = scn.last_shading

        return {"FINISHED"}
