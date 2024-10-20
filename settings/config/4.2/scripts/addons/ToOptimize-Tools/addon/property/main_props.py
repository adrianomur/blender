import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       FloatProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

from ..utility.functions import update_function_col, update_function_scn

class TOT_OBJBList_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    tot_obj_name: StringProperty()
    tot_obj_mamory: FloatProperty()
    missing_obj: BoolProperty()
    tot_obj_icon: StringProperty()
    linked_obj: BoolProperty()
    #missing_mat: BoolProperty()
    #obj_type: StringProperty()
    #obj_id: IntProperty()

class TOT_Imagelist_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    tot_image_name: StringProperty()
    tot_true_image_name: StringProperty()
    image_size: StringProperty()
    image_selected: BoolProperty(default=False)
    image_filepath: StringProperty()
    packed_img: IntProperty(default=0)
    #tot_mat_mamory: FloatProperty()
    #missing_mat: BoolProperty()
    #obj_type: StringProperty()
    #obj_id: IntProperty()


class TOT_MatList_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    tot_mat_name: StringProperty()
    tot_mat_mamory: FloatProperty()
    missing_mat: BoolProperty()
    is_linked: BoolProperty()
    #obj_type: StringProperty()
    #obj_id: IntProperty()

class TOT_Props(PropertyGroup):

    CA_Toggle: BoolProperty(default = False,update = update_function_col, name = "Collection Analyzer")
    AA_Toggle: BoolProperty(default = False,update = update_function_scn, name = "Scene Analyzer")

    last_shading: StringProperty()

    colA_Method: bpy.props.EnumProperty(
        name= 'Collections Analyzer Method',
        description = 'Collections Analyzer Method',
        items = [
            ('m1','Default', 'The original Collection Anaylzer method'),
            ('m2','Advanced', 'Collections Analyzer with advanced options'),
        ]        

    )  

    fix_count: IntProperty()

    ### Advanced Collection Analyzer

    mult_veryhigh: FloatProperty(default=0.9, min = 0, max = 1)
    mult_high: FloatProperty(default=0.8, min = 0, max = 1)
    mult_medium: FloatProperty(default=0.6, min = 0, max = 1)
    mult_low: FloatProperty(default=0.2, min = 0, max = 1)
    mult_very_low: FloatProperty(default=0.0, min = 0, max = 1)

    ### Scene Analyzer

    SceneA_Method: bpy.props.EnumProperty(
        name= 'Scene Analyzer Method',
        description = 'Scene Analyzer Method',
        items = [
            ('m1','Complete', 'The Scene Analyzer will run in the complete scene, including hidden and excluded objects'),
            ('m3','In View', 'The Scene Analyzer will run only in objects in view'),
            ('m2','Selected', 'The Scene Analyzer will run only in selected objects'),
        ]        

    ) 

    default_colors: StringProperty() 
    default_col_colors: StringProperty()  

    # Find in view

    fv_mode: bpy.props.EnumProperty(
        name= 'Find in Scene Method',
        description = 'Find in Scene Method',
        items = [
            ('m1','Complete', 'The Find in Scene Tool will run in the complete scene,including hidden and excluded objects'),
            ('m2','In View', 'The Find in Scene Tool will run only in objects in view'),
            ('m3','Selected', 'The Find in Scene Tool will run only in selected objects'),
        ]        

    ) 

    fv_autoselect: BoolProperty(default = True, description = 'Auto Select objects')

    fv_label_top: StringProperty(default="")

    fv_label: StringProperty(default="Select an option below")
    fv_tofind: StringProperty()
    fv_stringmode: StringProperty()

    fv_xvertices: IntProperty(default=1000)

    # Easy Link
    
    el_use_same_dic : BoolProperty(default = True, name = 'Use Same Directory',description = 'If enabled, the addon will crate a folder in the same blend file directory, and all blend files with linked objects will be placed there')
    el_make_local : BoolProperty(default = False, name = 'Make Local',description = "If enabled, after linked the object will be made local, meaning the you will be able to move it, if you don't need to move the object, just keep it disabled")                                 


    ################ Material Benchmark

    select_mode: bpy.props.EnumProperty(
        name= 'Benchmark Scope',
        description = 'Materials from',
        items = [
            ('s1','All Objects', 'Run Benchmark in Materials from all objects in the blend file data'),
            ('s2','Selected Objects', 'Run Benchmark in Materials from selected objects only'),
        ]        

    )

    mat_list: CollectionProperty(type=TOT_MatList_objectCollection)
    mat_custom_index: IntProperty(name = 'Material Name')

    total_memory: FloatProperty()
    true_memory_usage: FloatProperty()
    image_memory: FloatProperty()

    ################ OBJ benhmark

    include_linked_obj: BoolProperty(name = 'Include Linked Objects', default = True, description = 'Include linked objects in the result')

    bobj_select_mode: bpy.props.EnumProperty(
        name= 'Benchmark Scope',
        description = 'Objects in',
        items = [
            ('s1','All Objects', 'All objects in the blend file data'),
            ('s2','Selected Objects', 'Selected Objects only'),
        ]        
    )

    bobj_list: CollectionProperty(type=TOT_OBJBList_objectCollection)
    bobj_custom_index: IntProperty()

    obj_total_memory: FloatProperty()
    obj_true_memory_usage: FloatProperty() 

    ################ Image Resizer

    image_data_method : bpy.props.EnumProperty(
        name= 'Image Data',
        description = 'Get image list from',
        default='s1',
        items = [
            ('s1','Blend Data', 'Images inside Blend file data'),
            ('s2','Original Files', 'Used images'),
        ]        

    )

    selected_image_data_method: bpy.props.EnumProperty(
        name= 'Image Data',
        description = 'Image Data',
        default = 'd1',
        items = [
            ('d1','Blend File', ''),
            ('d2','Selected Material', ''),
            ('d3','Selected Objects', ''),     
        ]        
    )

    image_list: CollectionProperty(type=TOT_Imagelist_objectCollection)
    custom_index_image_list: IntProperty(name = 'Image File')

    total_image_memory: StringProperty()
    true_image_memory_usage: StringProperty()

    r_total_images: IntProperty()
    r_true_total_images: IntProperty()

    resize_size: bpy.props.EnumProperty(
        name= 'Final Resolution',
        description = 'Downsize to resolution',
        default = '1024',
        items = [
            ('128','128 px', ''),
            ('256','256 px', ''),
            ('512','512 px', ''),
            ('1024','1024 px', ''),
            ('2048','2048 px', ''),
            ('4096','4096 px', ''),
            #('3072','3072 px', ''),
            #('6144','6144 px', ''),
            #('8192','8192 px', ''),
            ('c','Custom', ''),       
        ]        
    )

    custom_resize_size: IntProperty(name='Custom size',subtype='PIXEL',default=1024,min=4)

    duplicate_images: BoolProperty(default = True, name= 'Duplicate if necessary',description = 'Create Duplicate Image files if necessary')

    use_same_directory: BoolProperty(default=True,name='Texture Folder in Blend File Directory',description = 'All resized textures will be in a folder called "Textures" in the same blend file directory')
    custom_output_path : StringProperty(
    
      name = "Custom Folder",
      default = "",
      description = "Set a custom output folder",
      subtype = 'DIR_PATH'
      )

    tog_select_all: BoolProperty(default = True)
    select_images_to: BoolProperty(default = False)
    is_clean: BoolProperty(default = False)

    