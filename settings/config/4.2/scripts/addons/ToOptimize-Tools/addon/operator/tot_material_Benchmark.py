import bpy
import os
import sys
import time
from collections import OrderedDict

from ..utility.addon import get_prefs
from ..utility.functions import material_benchmarking,find_in_group,get_size_textures,select_objects_materials,get_mat_count
from ..utility.constants import constant_ob_types

class TOT_OP_MaterialBenchmark(bpy.types.Operator):
    """Run benchmark in materials from selected objects"""

    bl_idname = "tot.matbenchmark"
    bl_label = "Run Benchmark"
    bl_description = "Run benchmark in materials from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True


    def execute(self, context):

        if not bpy.data.is_saved:
            self.report({'ERROR'},"Save this file first!")                                                       
            return {"CANCELLED"}

        start_time = time.time()

        scn = context.scene.tot_props
        prefs = get_prefs()

        if prefs.b_auto_save:
            bpy.ops.wm.save_mainfile()

        scn.mat_list.clear()
        scn.total_memory = 0

        ### Benchmark Scope

        if scn.select_mode == 's1':
            objs = bpy.data.objects
        if scn.select_mode == 's2':
            objs = bpy.context.selected_objects

        checked_mats = []

        total_mats = []
        mat_memory = {}
        image_sizes = {}


        if prefs.auto_console:
            bpy.ops.wm.console_toggle()

        
        print()
        print('--------------------------------RUNNING BENCHMARK--------------------------------')
        print()

        total_data_mats = get_mat_count()
        done_data_mats = 0

        for idx,ob in enumerate(objs):

            
               
            if ob.type in constant_ob_types:
                for mat in ob.data.materials:
                    if mat:
                        if not mat.name in checked_mats:
                            libray_path = ''
                            if mat.library:
                                libray_path = mat.library.filepath

                            if not mat.name in total_mats:
                                total_mats.append(mat.name)
                            
                            done_data_mats += 1
                            mat_memory[mat.name] = material_benchmarking(mat.name,self,'mat',libray_path)
                            checked_mats.append(mat.name)
                            #node_texture_list = find_in_group(mat)
                            image_sizes.update(get_size_textures(mat))

                            msg = f"Material {done_data_mats} of {total_data_mats}"
                            sys.stdout.write(msg + chr(8) * len(msg))
                            sys.stdout.flush()
                            time.sleep(0.02)
            
        
        ##### Deleting empty data materials (should not happen)
        for m in mat_memory:
            if not mat_memory[m]:
                mat_memory[m] = 0
        
        ##### Rendering scene with all materials
        print('')
        print('Running all materials...')
        print('')

        mat_string = ''
        for m in total_mats:
            mat_string += m
            mat_string += '--#-##--#---##-#--'
        
        try:
            true_m_usage = material_benchmarking(mat_string,self,'mat')
        except:
            true_m_usage = None

        ##### Reordering Dict
        
        mat_memory = {k: v for k, v in sorted(mat_memory.items(), key=lambda item: item[1])}
        mat_memory = OrderedDict(reversed(list(mat_memory.items())))

        ##### Adding information to list
     
        missing_mat = False
        for i in mat_memory:
            
            select_mat = bpy.data.materials.get(i)
            is_linked = False
            if select_mat:
                if select_mat.library:
                    is_linked = True

            if not mat_memory[i]:
                item = scn.mat_list.add()
                item.tot_mat_name = i 
                item.tot_mat_mamory = 0
                missing_mat = True
                item.missing_mat = True
                item.is_linked = is_linked

                continue
     
            item = scn.mat_list.add()
            item.tot_mat_name = i
            item.tot_mat_mamory = float(mat_memory[i])
            item.missing_mat = False
            item.is_linked = is_linked
        
        #### Getting Totals
        
        total_image_sizes = 0                    
        for i in image_sizes:
            total_image_sizes += image_sizes[i]
        
        total_memory = 0
        for i in mat_memory:
            if not mat_memory[i]:
                continue
            total_memory += mat_memory[i]
        
        scn.total_memory = total_memory
        scn.image_memory =  total_image_sizes

        if not true_m_usage:
            scn.true_memory_usage = 0
        else:
            scn.true_memory_usage = true_m_usage

        print()
        print('-------------------------------BENCHMARK FINISHED--------------------------------')
        print()
        print("--- %s seconds ---" % (round(time.time() - start_time,2)))
        print()
        
        if prefs.auto_console:
            bpy.ops.wm.console_toggle()

        if not missing_mat:
            self.report({'INFO'},"Finished")                                                       
            return {"FINISHED"}
        else:
            self.report({'WARNING'},"Some materials were not in the saved blend file, please save the file and try again")                                                       
            return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        scn = context.scene.tot_props
        prefs = get_prefs()

        if scn.select_mode == 's1':
            s_objs = len(bpy.data.objects)
                
        if scn.select_mode == 's2':
            s_objs = len(bpy.context.selected_objects)

        total_mats_ui = get_mat_count()
                
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

        if prefs.b_auto_save:
            layout.label(text="Auto Save is Active! This file will be saved",icon='ERROR')

class TOT_OP_ClearMaterialBenchmark(bpy.types.Operator):
    """Clear Material Benchmark Data"""

    bl_idname = "tot.clearmatbenchmark"
    bl_label = "Clear Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = context.scene.tot_props
        scn.mat_list.clear()

        return {"FINISHED"}

class TOT_OP_SelectMaterialBenchmark(bpy.types.Operator):
    """Select objects with the selected material in the list"""

    bl_idname = "tot.selectmatbenchmark"
    bl_label = "Select Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = context.scene.tot_props
        idx = scn.mat_custom_index
        
        try:
            item = scn.mat_list[idx]
        except IndexError:
            pass


        not_in_viewlayer = select_objects_materials(item.tot_mat_name)
                    
        if not_in_viewlayer:
            self.report({'WARNING'},"Some objects are not in the view layer")                                                       
            return {"FINISHED"}
        else:
            return {"FINISHED"}