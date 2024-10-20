import bpy

from ..utility.addon import get_prefs 
from ..utility.functions import get_verts_mod 

class TOT_OP_Collection_Analyzer(bpy.types.Operator):

    """Update Collection Analyzer"""

    bl_idname = "tot.collectionanalyzer"
    bl_label = "Update"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (2, 91, 0) > bpy.app.version:
            return False
        else:
            return True


    def execute(self, context):

        prefs = get_prefs()

        scn = context.scene.tot_props
        scn.default_col_colors = ''
        default_colors = {}
        
        #scn.CA_Toggle = True

        if scn.colA_Method == 'm1':
                       
            #  Parameters to define:        
            mult_veryhigh = 0.9
            mult_high = 0.8
            mult_medium = 0.6
            mult_low = 0.2
            mult_very_low = 0

        if scn.colA_Method == 'm2':

            mult_veryhigh = scn.mult_veryhigh
            mult_high = scn.mult_high
            mult_medium = scn.mult_medium
            mult_low = scn.mult_low
            mult_very_low = scn.mult_very_low
      
        scene_total = 0        
        scene_objects = bpy.data.objects        
        
        highest_col = 0 

        for collection in bpy.data.collections:
            
            default_colors[collection.name] = collection.color_tag

            collection.color_tag = 'NONE'            
            if collection.name[-1] == '%':               
               c_name_clean = collection.name[:-10]             
               collection.name = c_name_clean.strip()                          
            else:
               continue  

        scn.default_col_colors = str(default_colors)    
        
        #  Check number of objects in the scene        
        for objs in scene_objects:           
            #  in case that that is something that is not an object with vertices           
            if objs.type == 'MESH':   
                if prefs.includ_mod and objs.modifiers:
                    scene_total += get_verts_mod(objs)                  
                else:
                    scene_total += len(objs.data.vertices)                              
            else:
                continue                                                  
        
        # Start checking each collection vertices, to get a list of vertices per objects, to get the highest value                           
        for i in bpy.data.collections:          
           col_total_vert = 0                                             
           for i_obj in i.all_objects:                                       
               if i_obj.type == 'MESH': 
                    if prefs.includ_mod and i_obj.modifiers: 
                        col_total_vert += get_verts_mod(i_obj) 
                    else:
                        col_total_vert += len(i_obj.data.vertices)                                                                                                                                                       
               else:                  
                   continue              
           if col_total_vert > highest_col:             
               highest_col = col_total_vert              
           else:
               pass                           
       
        #  defines the low, medium and high, based in the highest collection value       
        veryhigh = highest_col * mult_veryhigh
        low = highest_col * mult_low
        medium = highest_col * mult_medium
        high = highest_col * mult_high 
               
        #  start to check each collection, to set the color to the correct icon                                                  
        for collection in bpy.data.collections:
                        
           vertice_counter = 0 
           c_name = collection.name          
                 
           for obj in collection.all_objects:              
               if obj.type == 'MESH': 
                   if prefs.includ_mod and obj.modifiers: 
                        vertice_counter += get_verts_mod(obj) 
                   else:
                        vertice_counter += len(obj.data.vertices)                                                                                                                                                                                                       
               else:                                     
                   vertice_counter += 0
                         
           # if the collection as a number of vertices                  
           if vertice_counter > 0:                                
               c_porcent = (vertice_counter/scene_total)*100.                                   
               if c_name[-1] != '%':              
                  collection.name = f'{c_name}  |  {c_porcent:.2f}%' 
                  
           else: 
               pass         
                         
           if vertice_counter >= veryhigh:             
             collection.color_tag = 'COLOR_01'            
           elif vertice_counter >= high and vertice_counter <= veryhigh:          
             collection.color_tag = 'COLOR_02'                   
           elif vertice_counter >= medium and vertice_counter <= high :               
             collection.color_tag = 'COLOR_03'             
           elif vertice_counter >= low and vertice_counter <= medium :          
             collection.color_tag = 'COLOR_04'             
           elif vertice_counter > mult_very_low and vertice_counter <= low :             
             collection.color_tag = 'COLOR_05'          
           else:             
             collection.color_tag = 'NONE'
                                    
        return {"FINISHED"}

class TOT_OP_Collection_Analyzer_Clean(bpy.types.Operator):

    """Clear analyses result"""
    
    bl_idname = "tot.cleancolors"
    bl_label = "Clear Information"
    bl_options = {"REGISTER"}   

    @classmethod
    def poll(cls, context):
        if (2, 91, 0) > bpy.app.version:
            return False
        else:
            return True
   
    def execute(self, context):

        scn = context.scene.tot_props

        if scn.default_col_colors:
            default_col_colors = eval(scn.default_col_colors)
    
        for collection in bpy.data.collections:    
        
            if collection.name[-1] == '%':               
               c_name_clean = collection.name[:-10]             
               collection.name = c_name_clean.strip()                          
            #else:
               #continue 

            #print(default_col_colors[collection.name.strip()])

            if collection.name in default_col_colors:
                #print(collection.name)
                collection.color_tag = default_col_colors[collection.name]
            else:
                collection.color_tag = 'NONE' 

        #scn.CA_Toggle = False          
            
        return {"FINISHED"}   

class TOT_OP_Collection_Cleaner(bpy.types.Operator):

    """Delete Empty Collections"""

    bl_idname = "tot.collectioncleaner"
    bl_label = "Delete Empty Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = context.scene.tot_props

        for collection in bpy.data.collections:
                                           
            object_counter = 0 
            c_name = collection.name          
                    
            for obj in collection.all_objects:              
                if obj.type:  
                    object_counter += 1

                else:                                     
                    object_counter += 0
                                                        
            if object_counter == 0:    
                    print(collection)         
                    bpy.data.collections.remove(collection)         
            else:             
                continue

        self.report({'INFO'},"Finished") 
                                    
        return {"FINISHED"}

        

        

