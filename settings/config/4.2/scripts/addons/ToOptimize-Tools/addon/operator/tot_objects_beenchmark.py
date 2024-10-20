import bpy
import os
import time
from collections import OrderedDict

from ..utility.addon import get_prefs
from ..utility.functions import material_benchmarking,find_in_group,get_size_textures
from ..utility.constants import constant_ob_types

class TOT_OP_ObjectBenchmark(bpy.types.Operator):
    """Run benchmark in materials from selected objects"""

    bl_idname = "tot.objbenchmark"
    bl_label = "Run Benchmark"
    bl_description = "Run benchmark in materials from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    #@classmethod
    #def poll(cls, context):
    #    return True

    def execute(self, context):

        if not bpy.data.is_saved:
            self.report({'ERROR'},"Save this file first!")                                                       
            return {"CANCELLED"}

        start_time = time.time()

        scn = context.scene.tot_props
        prefs = get_prefs()

        if prefs.b_auto_save:
            bpy.ops.wm.save_mainfile()

        scn.bobj_list.clear()
  
        ### Benchmark Scope

        if scn.bobj_select_mode == 's1':
            objs = bpy.data.objects
        if scn.bobj_select_mode == 's2':
            objs = bpy.context.selected_objects

        #checked_mats = []

        total_objs = []
        obj_memory = {}

        loaded_obj_data = []
        checked_obj_data = {}


        #image_sizes = {}
        ignored_objects = {}


        if prefs.auto_console:
            bpy.ops.wm.console_toggle()

        print()
        print('--------------------------------RUNNING BENCHMARK--------------------------------')
        print()

        for ob in objs:
            if ob.type in constant_ob_types:
                if ob.type == 'MESH':
                    ob_verts = ob.data.vertices.data
                    if ob_verts.name in loaded_obj_data:
                        ignored_objects[ob.name] = ob_verts.name
                        continue
            
                total_objs.append(ob.name)
                obj_memory[ob.name] = material_benchmarking(ob.name,self,'obj')

                if ob.type == 'MESH':
                    loaded_obj_data.append(ob_verts.name)
                    checked_obj_data[ob_verts.name] = obj_memory[ob.name]
        
         ##### Rendering scene with all materials
        obj_string = ''
        for ob in total_objs:
            obj_string += ob
            obj_string += '--#-##--#---##-#--'
        
        true_m_usage = material_benchmarking(obj_string,self,'obj')

        ##### Deleting empty data objects (should not happen)
        for ob in obj_memory:
            if not obj_memory[ob]:
                obj_memory[ob] = 0
        
        ##### Reordering Dict
        
        obj_memory = {k: v for k, v in sorted(obj_memory.items(), key=lambda item: item[1],reverse=True)}

        ##### Adding information to list
     
        missing_obj = False # Default

        for i in obj_memory:
            
            # getting icon
            ob = bpy.data.objects.get(i)

            if ob.type == 'MESH':
                obj_get_icon = 'MESH_CUBE'
            else:
                obj_get_icon = 'MESH_CUBE'

            if not obj_memory[i]:
                item = scn.bobj_list.add()
                item.tot_obj_name = i 
                item.tot_obj_mamory = 0
                missing_obj = True
                item.missing_obj = True
                item.tot_obj_icon = obj_get_icon
                item.linked_obj = False
                continue
     
            item = scn.bobj_list.add()
            item.tot_obj_name = i
            item.tot_obj_mamory = float(obj_memory[i])
            item.missing_obj = False
            item.tot_obj_icon = obj_get_icon
            item.linked_obj = False

        ########## Include Linked Objects 

        if scn.include_linked_obj:

            for i in ignored_objects:

                ob = bpy.data.objects.get(i)

                if ob.type == 'MESH':
                    obj_get_icon = 'MESH_CUBE'
                else:
                    obj_get_icon = 'MESH_CUBE'
                
                if not ignored_objects[i]:
                    item = scn.bobj_list.add()
                    item.tot_obj_name = i 
                    item.tot_obj_mamory = 0
                    missing_obj = True
                    item.missing_obj = True
                    item.tot_obj_icon = obj_get_icon
                    item.linked_obj = True
                    continue

                item = scn.bobj_list.add()
                item.tot_obj_name = i
                item.tot_obj_mamory = float(checked_obj_data[ignored_objects[i]])
                item.missing_obj = False
                item.tot_obj_icon = obj_get_icon
                item.linked_obj = True

        # Total Memory
        total_memory = 0
        for i in obj_memory:
            if not obj_memory[i]:
                continue
            total_memory += obj_memory[i]

        scn.obj_total_memory = total_memory

        # True total Memory              
        if not true_m_usage:
            scn.obj_true_memory_usage = 0
        else:
            scn.obj_true_memory_usage = true_m_usage
        


        print()
        print('-------------------------------BENCHMARK FINISHED--------------------------------')
        print()
        print("--- %s seconds ---" % (round(time.time() - start_time,2)))
        print()

               
        if prefs.auto_console:
            bpy.ops.wm.console_toggle()

        if not missing_obj:
            self.report({'INFO'},"Finished")                                                       
            return {"FINISHED"}
        else:
            self.report({'WARNING'},"Some objects were not in the saved blend file, please save the file and try again")                                                       
            return {"FINISHED"}
        
        return {"FINISHED"}
    
    #def invoke(self, context, event):
    #    return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scn = context.scene.tot_props

        counted_mats = []

        if scn.select_mode == 's1':
            s_objs = len(bpy.data.objects)
         
            total_mats_ui = 0
            for i in bpy.data.objects:
                if i.type in constant_ob_types:
                    for m in i.data.materials:
                        if m:
                            if not m.name in counted_mats:
                                counted_mats.append(m.name)
                                total_mats_ui += 1
       
        if scn.select_mode == 's2':
            s_objs = len(bpy.context.selected_objects)
        
            total_mats_ui = 0
            for i in bpy.context.selected_objects:
                if i.type in constant_ob_types:
                    for m in i.data.materials:
                        if m:
                            if not m.name in counted_mats:
                                counted_mats.append(m.name)
                                total_mats_ui += 1
      
        
        if s_objs == 0:
            s_objs_label = f'No Objects Selected'
        if s_objs > 0:   
            s_objs_label = f'Selected Objects: {s_objs}'

        col = layout.column(align=True)
        box = col.box()
        box.label(text=s_objs_label)
        box.label(text=f'Total Materials: {total_mats_ui}')
        row = layout.row()
        row.label(text='This process may take a while',icon='ERROR')

class TOT_OP_ClearObjectBenchmark(bpy.types.Operator):

    """Clear Material Benchmark Data"""

    bl_idname = "tot.clearobjbenchmark"
    bl_label = "Clear Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = context.scene.tot_props
        scn.bobj_list.clear()

        return {"FINISHED"}

class TOT_OP_SelectObjBenchmark(bpy.types.Operator):

    """Select objects with the select material in the list"""

    bl_idname = "tot.selectobjbenchmark"
    bl_label = "Select Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = context.scene.tot_props
        idx = scn.bobj_custom_index
        
        try:
            item = scn.bobj_list[idx]
        except IndexError:
            pass

        #print(item.tot_obj_name)

        bpy.ops.object.select_all(action='DESELECT')

        objs = bpy.data.objects

        not_in_viewlayer = False

        for ob in objs:
            if ob.type in constant_ob_types:
                if ob.name == item.tot_obj_name:
                    ob.select_set(True)
                    try:
                        bpy.context.view_layer.objects.active = ob
                    except:
                        not_in_viewlayer = True
                    
        if not_in_viewlayer:
            self.report({'WARNING'},"Some objects are not in the view layer")                                                       
            return {"FINISHED"}
        else:
            return {"FINISHED"}

class TOT_OP_VizObjBenchmark(bpy.types.Operator):
    
    """Select objects with the select material in the list"""

    bl_idname = "tot.vizobjbenchmark"
    bl_label = "Select Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = context.scene.tot_props
        idx = scn.bobj_custom_index
        
        try:
            item = scn.bobj_list[idx]
        except IndexError:
            pass

        #print(item.tot_obj_name)

        bpy.ops.object.select_all(action='DESELECT')

        objs = bpy.data.objects

        not_in_viewlayer = False

        for ob in objs:
            if ob.type in constant_ob_types:
                if ob.name == item.tot_obj_name:
                    ob.select_set(True)
                    try:
                        bpy.context.view_layer.objects.active = ob
                    except:
                        not_in_viewlayer = True
                    
        if not_in_viewlayer:
            self.report({'WARNING'},"Some objects are not in the view layer")                                                       
            return {"FINISHED"}
        else:
            return {"FINISHED"}