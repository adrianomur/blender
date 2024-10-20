import bpy #type: ignore

class TOT_OP_CleanUnusedMaterials(bpy.types.Operator):
    """Clean ynused materials from all objects in your scene, cannot execute in edit mode"""

    bl_idname = "tot.cleanmaterials"
    bl_label = "Clean Unused Materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    _total_slots_cleaned = 0
    _total_unused_materials_cleaned = 0
    
    @classmethod
    def poll(self, context):
        if context.active_object and context.active_object.mode == 'EDIT':
            return False
        return True
    
    def _get_all_materials_from_object(self, obj) -> set[bpy.types.Material]:
        
        mat_list = []
        for mat in obj.material_slots:              
            mat_list.append(mat.material)
            
        return set(mat_list) # Remove duplicates 
    
    def _get_all_assigned_materials_from_object(self, obj) -> set[bpy.types.Material]:
        
        mat_list = []
        for poly in obj.data.polygons:          
            mat_index = poly.material_index
            
            if not mat_index < len(obj.material_slots):
                print("WARNING: Material index out of range in " + obj.name)
                continue
                
            material_in_slot = obj.material_slots[mat_index].material
            mat_list.append(material_in_slot)
            
        return set(mat_list)
    
    def _remove_empty_material_slots(self, context, obj) -> bool:
        
        if obj.hide_viewport or obj.hide_select:
            return False
        
        context.view_layer.objects.active = obj
        total_slots = len(context.object.material_slots)
        
        context.object.active_material_index = 0
        slot_count = 0 

        for _ in range(total_slots):      
            context.object.active_material_index = slot_count 

            if context.object.active_material == None:
                bpy.ops.object.material_slot_remove() 
                self._total_slots_cleaned += 1
                continue       
                               
            slot_count += 1
            
        return True

    def execute(self, context):
                        
        objs = bpy.context.view_layer.objects
        
        self._total_slots_cleaned = 0
        self._total_unused_materials_cleaned = 0
        
        for obj in objs:           
                        
            if not obj.type == 'MESH':
                continue         
            if not len(obj.material_slots) > 0:  
                continue                                  
            
            mat_list = self._get_all_materials_from_object(obj)
            assigned_mat_list = self._get_all_assigned_materials_from_object(obj)
                                                    
            # Compare assigned materials with all materials in object, and get unused materials                                        
            unused_materials = mat_list - assigned_mat_list
                      
            for material_slot in obj.material_slots:
                if not material_slot.material:
                    continue
                if material_slot.material in unused_materials:
                    print("Removing unused material: " + material_slot.material.name)
                    print("From object: " + obj.name)

                    if material_slot.material.library:
                        print("Ignoring material from library: " + material_slot.material.name)
                        continue
                    
                    material_slot.material = None
                    self._total_unused_materials_cleaned += 1
                    
            result = self._remove_empty_material_slots(context, obj)
            if not result:
                print("WARNING: Could not remove empty material slots from " + obj.name)
                continue
                    
        self.report({'INFO'},f"Total slots cleaned: {self._total_slots_cleaned}, Total unused materials cleaned: {self._total_unused_materials_cleaned}")                     
        return {"FINISHED"}

class TOT_OP_CleanSubModifiers(bpy.types.Operator):

    """Remove All Subdivision Modifiers From Scene"""

    bl_idname = "tot.cleansubmodifiers"
    bl_label = "Remove All Subdivision Modifiers"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        
        obj_sub = []
        ob_c = bpy.context.selected_objects

        for obj in bpy.data.objects:

            if(obj.type=='MESH'):
                                
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':                       
                        obj.modifiers.remove(mod)
        
        self.report({'INFO'},"Finished") 
                                                        
        return {"FINISHED"}
    
class TOT_OP_RemoveDuplicateMaterials(bpy.types.Operator):
    """Remove Duplicate Materials"""

    bl_idname = "tot.remove_duplicate_materials"
    bl_label = "Remove Duplicate Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def get_next_original_material(self, mat: bpy.types.Material) -> bpy.types.Material:
        
        original_material_name = mat.name[:-4]
        
        current_idx = 0
        max_idx = 100
        
        while current_idx < max_idx:
            if bpy.data.materials.get(original_material_name):
                print("Found original material: " + original_material_name)
                break
            
            checking_name = original_material_name + '.' + str(current_idx).zfill(3)
            
            if bpy.data.materials.get(checking_name):
                print("Found next original material: " + checking_name)
                original_material_name = checking_name
                break
            
            current_idx += 1
                    
        return bpy.data.materials.get(original_material_name)

    def search_for_duplicate_materials(self, context) -> dict:
        
        duplicate_materials = {}
        
        for mat in bpy.data.materials:
             
            if not len(mat.name) > 4:
                continue
            
            if not mat.name[-4] == '.':
                continue
            
            if not mat.name[-3:].isdigit():
                continue
            
            original_material = self.get_next_original_material(mat) 
            
            if not original_material:
                continue
            
            if mat == original_material:
                continue
            
            duplicate_materials[mat] = original_material
                        
        return duplicate_materials
    
    def replace_duplicate_materials(self, context, duplicate_materials: dict):
        
        for obj in bpy.data.objects:   
            if hasattr(obj,'material_slots'):
                for slot in obj.material_slots:
                    if slot.material in duplicate_materials:
                        slot.material = duplicate_materials[slot.material]

    def execute(self, context):
        
        duplicate_materials = self.search_for_duplicate_materials(context)
        self.replace_duplicate_materials(context, duplicate_materials)
                             
        return {"FINISHED"}