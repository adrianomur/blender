from bpy.types import Panel
import bpy

from .mb_uilist import TOT_MatB_UL_items

class TOT_PT_MainPanelOBJ:    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ToOptimize Tools'

class TOT_PT_Collection_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_label = "Collection Analyzer"

    @classmethod
    def poll(cls, context):
        if (2, 91, 0) > bpy.app.version:
            return False
        else:
            return True            
    
    def draw(self, context):
            
        layout = self.layout
        row = layout.row()              
        row.label(text= "Collection Analyzer", icon="OUTLINER_COLLECTION")
     
        scn = context.scene.tot_props  

        layout.prop(scn, 'colA_Method', expand=True)

        if scn.colA_Method == 'm2':

            row = layout.row() 
            row.label(text='Color threshold:')  
            row = layout.row() 
         
            row.label(text='',icon='COLLECTION_COLOR_01' )
            row.prop(scn, 'mult_veryhigh', text='Very Heavy',icon='COLLECTION_COLOR_01',slider=True)
            row = layout.row()   
            row.label(text='',icon='COLLECTION_COLOR_02' )
            row.prop(scn, 'mult_high', text='Heavy',icon='COLLECTION_COLOR_01',slider=True)
            row = layout.row()
            row.label(text='',icon='COLLECTION_COLOR_03' )   
            row.prop(scn, 'mult_medium', text='Medium',icon='COLLECTION_COLOR_01',slider=True)
            row = layout.row()  
            row.label(text='',icon='COLLECTION_COLOR_04' ) 
            row.prop(scn, 'mult_low', text='Light',icon='COLLECTION_COLOR_01',slider=True)
            row = layout.row() 
            row.label(text='',icon='COLLECTION_COLOR_05' ) 
            row.prop(scn, 'mult_very_low', text='Very Light',icon='COLLECTION_COLOR_01',slider=True)
            row = layout.row() 
            
        label = "Clear Analyzer" if scn.CA_Toggle else "Run Analyzer"    
        row = layout.row(align=True) 
        row.prop(scn, 'CA_Toggle', text=label,icon='COLLECTION_COLOR_01', toggle=True)
        row.operator("tot.collectionanalyzer", text='',icon='FILE_REFRESH')

class TOT_PT_BlenderVersion_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_label = "Collection Analyzer - Wrong Version"

    @classmethod
    def poll(cls, context):
        if (2, 91, 0) > bpy.app.version:
            return True
        else:
            return False            
    
    def draw(self, context):
            
        layout = self.layout
        col = layout.column()

        row = layout.row()              
        row.label(text= "This Feature Works Only In Blender 2.91 or Above")
        row = layout.row()
                          
class TOT_PT_View3D_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_label = "3D View Analyzer"        
    
    def draw(self, context):
       
        layout = self.layout
        row = layout.row()  
        
        scn = context.scene.tot_props

        row.label(text= "Scene Analyzer", icon="SCENE_DATA")
        row = layout.row()
        row.prop(scn, 'SceneA_Method', text='Very Heavy',expand=True) 

        row = layout.row(align=True)
        label = "Clear Analyzer" if scn.AA_Toggle else "Run Analyzer"   
        row.prop(scn, 'AA_Toggle', text=label,icon='SCENE_DATA', toggle=True)
        row = layout.row()

        #row.operator("tot.3dviewanalyzer", icon="MESH_CUBE") 
        #row = layout.row()
        #row.operator("tot.3dviewanalyzerselected", icon="MESH_CUBE") 
        #row = layout.row()
        #row.operator("tot.clean3dviewanalyzer", icon="CUBE") 

class TOT_PT_EasyLink_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_label = "Easy Link"
           
    def draw(self, context):
      
        layout = self.layout
        scn = context.scene.tot_props

        row = layout.row()  

        row.label(text= "Execute: ", icon="SCENE_DATA")

        col = layout.column(align=True)
        box = col.box()
        box.prop(scn,"el_use_same_dic")
        box.prop(scn,"el_make_local")
        col.operator("tot.converttolink", icon="LINKED")  
        col.operator("tot.unconverttolink", icon="UNLINKED") 

class TOT_PT_SceneBenchmark_Menu(TOT_PT_MainPanelOBJ, Panel):
    bl_label = "Scene Benchmark"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass

class TOT_PT_MaterialBenchmark_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_parent_id = "TOT_PT_SceneBenchmark_Menu"
    bl_label = "Material Benchmark"

    #bl_label = "Material Benchmark"
    #bl_idname = "tot.matbenchmarkmenu"
    #bl_space_type = 'VIEW_3D'
    #bl_region_type = 'UI'
    #bl_category = 'ToOptimize Tools'   
    #bl_options = {'DEFAULT_CLOSED'}         
    
    def draw(self, context):
      
        layout = self.layout
        scn = context.scene.tot_props

        list_exists = bpy.context.scene.tot_props.mat_list

        if scn.select_mode == 's1':
            s_objs = len(bpy.data.objects)

        if scn.select_mode == 's2':
            s_objs = len(bpy.context.selected_objects)
        
        if s_objs == 0:
            s_objs_label = f'No Objects Selected'
        if s_objs > 0:   
            s_objs_label = f'Selected Objects: {s_objs}'

        if not list_exists:
            row = layout.row()
            row.prop(scn,'select_mode',expand=True)

        col = layout.column(align=True)

        if not list_exists:
            box = col.box()
            box.label(text=s_objs_label)

        b_col = col.row(align=True)
        b_col.scale_y = 1.3

        if not list_exists:
            b_col.operator("tot.matbenchmark",text='Run Benchmark') 
        else:
            b_col.operator("tot.clearmatbenchmark",text='Clear Benchmark',icon='FILE_REFRESH') 
            b_col = b_col.column(align=True)
            b_col.scale_x=1.2
            b_col.operator("tot.selectmatbenchmark",text='',icon='RESTRICT_SELECT_OFF')

        if list_exists:

            col.template_list("TOT_MatB_UL_items", "", scn, "mat_list", scn, "mat_custom_index", rows=4)
        
            box = col.box()
            #box = box.box()
            box.label(text=f'Total Materials:  {len(scn.mat_list)}')
            box.label(text=f'Total Memory Usage:  {str(round(scn.total_memory,2))}M')
            box.label(text=f'True Memory Usage:  {str(round(scn.true_memory_usage,2))}M')
            box.label(text=f'Image Files:  {str(round(scn.image_memory,2))}M')
 
        '''
        if context.scene.tot_props.mat_list:
            row=layout.row()
            box = layout.box()
            row.label(text='Last Benchmark Results:')
            box.label(text=f'Total Memory Usage:  {str(round(scn.total_memory,2))}M')
            box.label(text=f'True Memory Usage:  {str(round(scn.true_memory_usage,2))}M')
            box.label(text=f'Image Files:  {str(round(scn.image_memory,2))}M')
            box.label(text=f'Total Materials:  {len(scn.mat_list)}')
        '''

class TOT_PT_ObjectsBenchmark_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_parent_id = "TOT_PT_SceneBenchmark_Menu"
    bl_label = "Objects Benchmark"

    def draw(self, context):
      
        layout = self.layout
        scn = context.scene.tot_props


        list_exists = bpy.context.scene.tot_props.bobj_list

        
        if scn.bobj_select_mode == 's1':
            s_objs = len(bpy.data.objects)

        if scn.bobj_select_mode == 's2':
            s_objs = len(bpy.context.selected_objects)
        
        if s_objs == 0:
            s_objs_label = f'No Objects Selected'
        if s_objs > 0:   
            s_objs_label = f'Selected Objects: {s_objs}'

        
        if not list_exists:
            row = layout.row()
            row.prop(scn,'bobj_select_mode',expand=True)
        
        row = layout.row()
        row.prop(scn,'include_linked_obj')

        col = layout.column(align=True)


        if not list_exists:
            box = col.box()
            box.label(text=s_objs_label)

        b_col = col.row(align=True)
        b_col.scale_y = 1.3

        if not list_exists:
            b_col.operator("tot.objbenchmark",text='Run Benchmark') 
        else:
            b_col.operator("tot.clearobjbenchmark",text='Clear Benchmark',icon='FILE_REFRESH') 
            b_col = b_col.column(align=True)
            b_col.scale_x=1.2
            b_col.operator("tot.selectobjbenchmark",text='',icon='RESTRICT_SELECT_OFF')

        if list_exists:

            #col = layout.column(align=True)
            col.template_list("TOT_OBJB_UL_items", "", scn, "bobj_list", scn, "bobj_custom_index", rows=4)

            box = col.box()
            #box = box.box()
            box.label(text=f'Total Objects:  {len(scn.bobj_list)}')
            box.label(text=f'Total Memory Usage:  {str(round(scn.obj_total_memory,2))}M')
            box.label(text=f'True Memory Usage:  {str(round(scn.obj_true_memory_usage,2))}M')
            #box.label(text=f'Image Files:  {str(round(scn.image_memory,2))}M')

class TOT_PT_ImageAnalyzer(TOT_PT_MainPanelOBJ, Panel):
    bl_label = "Image Data Analyzer"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self,context):
        
        layout = self.layout
        scn = context.scene.tot_props

        list_exists = scn.image_list

        row=layout.row()

    
        row.prop(scn,"selected_image_data_method")

        

        if list_exists:

            row=layout.row()

            col = row.column(align=True)
            col_b = col.row(align=True)
            col_b.scale_y = 1.3

            #col_2 = row.column(align=True)
            #col_2.scale_x = 1.2
            #col_2.scale_y = 1.2
            #col_2.operator('tot.imginfo',text='',icon='INFO')
            #col_2.operator('tot.imgmatinfo',text='',icon='MATERIAL')
            
            
            col_b.scale_x = 1.2

            if not scn.tog_select_all:
                tog_sele_icon = 'RESTRICT_SELECT_OFF'
            else:
                tog_sele_icon = 'RESTRICT_SELECT_ON'

            if scn.select_images_to:
                col_b.operator("tot.imglistselectall",text='',icon=tog_sele_icon)
            col_b.operator("tot.updateimagelist",icon='FILE_REFRESH')
            col_b.operator("tot.clearimagelist",text='',icon='TRASH')
        else:
            row=layout.row()
            col = row.column(align=True)
            col_b = col.row(align=True)
            col_b.operator("tot.updateimagelist")


        col.template_list("TOT_ImageResizer_UL_items", "", scn, "image_list", scn, "custom_index_image_list", rows=4)

        if list_exists:

            ### Show Selected Images

            idx = scn.custom_index_image_list
            try:
                item = scn.image_list[idx]
            except IndexError:
                pass

 
            box = col.box()
            row = box.row(align=True)
            box_img = row.box()
            box_img.label(text=item.tot_image_name)
            b_row = row.row(align=True)
            b_row.scale_y = 1.5
            b_row.scale_x = 1.2
            b_row.operator('tot.imginfo',text='',icon='INFO')
            #box.label(text=f'Total Memory: {str(scn.total_image_memory)} M')

            duplicate = scn.r_total_images - scn.r_true_total_images
            if duplicate < 0:
                duplicate = 0

            box.label(text=f'Image Data Total Size: {str(scn.true_image_memory_usage)} M')
            box.label(text=f'Images in Blend Data: {str(len(scn.image_list))}')
            box.label(text=f'Image Files: {str(scn.r_true_total_images)}')

            #tot.imgmatinfo 
            #
            if not scn.is_clean:  
                col = col.column(align=True)
                col.scale_y = 1.3    
                col.operator("tot.clearduplicateimage",icon='ERROR')

class TOT_PT_ImageResizer_Menu(TOT_PT_MainPanelOBJ, Panel):
    bl_parent_id = "TOT_PT_ImageAnalyzer"
    bl_label = "Image Resizer"
         
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
       
        layout = self.layout
        scn = context.scene.tot_props

        list_exists = scn.image_list
        
        #col = layout.column(align=True)
        #col_b = col.row(align=True)
        #col_b.scale_y = 1.3

        if list_exists:
            
            col = layout.column(align=True)

            selected_images = [i for i in scn.image_list if i.image_selected == True]

            
            box =  col.box()
            box_select = box.box()

            if not scn.is_clean:
                box_select.label(text=f'Clear duplicates before select images and resizing!', icon='ERROR')

            if scn.select_images_to:
                if not selected_images:
                    box_select.label(text='Select at least 1 image to resize',icon='ERROR')
                else:
                    box_select.label(text=f'Selected Images: {len(selected_images)}')
            else:
                box_select.label(text='No images selected',icon='INFO')

            box_select.prop(scn,"select_images_to",text='Select Images',icon='RESTRICT_SELECT_OFF')

            if selected_images and scn.select_images_to:

                #box.label(text=f'Selected Images: {len(selected_images)}')

                box.prop(scn,"resize_size",text='Downsize to')

                if scn.resize_size == 'c':
                    box.prop(scn,"custom_resize_size",text='Custom Size')

                box = box.box()        
                box.prop(scn,"use_same_directory")
                if not scn.use_same_directory:
                    box.prop(scn,"custom_output_path")
            
                box.prop(scn,"duplicate_images",text='Duplicate images if necessary')       
               
            #box.prop(scn,"duplicate_images")
            col = col.column(align=True)
            col.scale_y=1.3
            col.operator("tot.renderimagelist",icon='CON_SIZELIMIT')

        else:
            col = layout.column(align=True)
            col.label(text='The image list is empty, please update it.')

class TOT_PT_Find_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_label = "Find in Scene"
    bl_options = {'DEFAULT_CLOSED'}          
    
    def draw(self, context):
       
        layout = self.layout
        scn = context.scene.tot_props

        if scn.fv_label_top:
            layout.label(text=scn.fv_label_top)
 
        #row.label(text= "Select: ", icon="SCENE_DATA")
        split = layout.row(align=False)

        box = split.box()
        label = scn.fv_label
        if len(label) > 30:
            label = label[:30] + '....and More'
    
        box.label(text=label)

        row=split.row()

        row.scale_x=1.4
        row.scale_y=1.45

        row=row.row(align=True)
        row.operator("tot.findselect", text='', icon='RESTRICT_SELECT_OFF').force_select = False
        #row.operator("tot.findselect", text='', icon='ERROR').force_select = True

        row = layout.row()
        row.prop(scn,"fv_autoselect", text=" Auto Select")
        row = layout.row()
        row.prop(scn,"fv_mode",expand=True)
        row = layout.row()

        col = layout.column(align=True)
        col.operator("tot.findxvertices", icon="VERTEXSEL")
        col.operator("tot.findmvertices", icon="MESH_CUBE")   
        col.operator("tot.findsubd", icon="MOD_SUBSURF")

        row = layout.row()

class TOT_PT_Actions_Menu(TOT_PT_MainPanelOBJ, Panel):

    bl_label = "Extra Tools"
    bl_options = {'DEFAULT_CLOSED'}          
    
    def draw(self, context):
      
        layout = self.layout
        row = layout.row()  

        row.label(text= "Execute: ", icon="SCENE_DATA")
        col = layout.column(align=True)
        col.operator("tot.cleanmaterials", icon="NODE_MATERIAL") 
        col.operator("tot.remove_duplicate_materials", icon="MATERIAL_DATA")        
        col.operator("tot.cleansubmodifiers", icon="MOD_SUBSURF")
        col.operator("tot.collectioncleaner", icon="TRASH")  
        
         
        
        

        