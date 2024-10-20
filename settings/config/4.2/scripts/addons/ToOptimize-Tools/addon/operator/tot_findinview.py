import bpy

from ..utility.functions import update_label
from ..utility.addon import get_prefs 
from ..utility.functions import get_verts_mod 

class TOT_OP_FindinView_High(bpy.types.Operator):

    """Select Object With More Vertices"""

    bl_idname = "tot.findmvertices"
    bl_label = "Object With More Vertices"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scn = context.scene.tot_props
        prefs = get_prefs()
      
        scene_vertices = 0
        high = 0
        ob_high = None

        if not bpy.data.objects:
            self.report({'WARNING'},
                                    "No Objects in the scene")
            return {'CANCELLED'} 


        if scn.fv_mode == 'm1':
            ob_c = bpy.data.objects
        if scn.fv_mode == 'm2':
            ob_c = [ob for ob in bpy.data.objects if ob.visible_get() == True]
        if scn.fv_mode == 'm3':
            if not bpy.context.selected_objects:
                self.report({'WARNING'},
                                    "No Objects Selected")
                return {'CANCELLED'} 

            ob_c = bpy.context.selected_objects

        for i in ob_c:          
            i.select_set(False)
            
        for v in ob_c:           
            obj_v = 0           
            if v.type == 'MESH':  
                if prefs.includ_mod and v.modifiers:

                    obj_v = get_verts_mod(v)  

                    if obj_v > high:                   
                        high = obj_v
                        ob_high = v

                    else:
                        pass                                          
                    scene_vertices += obj_v    

                else:                     
                    obj_v = (len(v.data.vertices))           
                    if obj_v > high:                   
                        high = obj_v
                        ob_high = v

                    else:
                        pass                                          
                    scene_vertices += obj_v                              
            else:
                pass 
        
        update_label('single',ob_high.name,scn)

        if scn.fv_autoselect:
             
            try:
                ob_high.select_set(True) 
                if ob_high.visible_get() == False:
                    self.report({'WARNING'},
                                        "This object is hidden in viewport")
                    return {'CANCELLED'}
     
            except:
                self.report({'WARNING'},
                                    "Object is not in the View Layer! Maybe it was Excluded from the View Layer in the outliner tab")
                return {'CANCELLED'} 
        

        self.report({'INFO'}, ob_high.name)
          
        return {"FINISHED"}

class TOT_OP_FindinView_sub(bpy.types.Operator):

    """Select Objects With Subdivision Modifier"""

    bl_idname = "tot.findsubd"
    bl_label = "Objects With Subdivision Modifier"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scn = context.scene.tot_props

        obj_sub = []

        if scn.fv_mode == 'm1':
            ob_c = bpy.data.objects
        if scn.fv_mode == 'm2':
            ob_c = [ob for ob in bpy.data.objects if ob.visible_get() == True]
        if scn.fv_mode == 'm3':
            ob_c = bpy.context.selected_objects

        for obj in ob_c:
            if(obj.type=='MESH'):
                list1=obj.modifiers.keys()
                for i in list1:
                    if(i=='Subsurf') or (i=='Subdivision'): #Notice the first s is capital
                        obj_sub.append(obj.name)                      
                        break      

        for i in ob_c:          
            i.select_set(False)
        
        if not obj_sub:

            scn.fv_label = 'No Objects Found' 
            scn.fv_tofind = ''
            scn.fv_label_top = ''
            scn.fv_stringmode = 'list'
            
            self.report({'INFO'},
                                    "No Objects Found")
            return {'CANCELLED'} 
        
        update_label('list',obj_sub,scn)

        not_view = False
        some_hide = False
                      
        if scn.fv_autoselect:
                 
            for sub in obj_sub:
                try:
                    ob = bpy.data.objects.get(sub) 
                    if ob.visible_get() == False:
                        some_hide = True
                    else:
                        ob.select_set(True) 
                except:
                    not_view = True
     
        if not_view:
            self.report({'WARNING'},
                                "Some objects are not in the View Layer! Maybe they were Excluded from the View Layer in the Outliner tab")
            return {"FINISHED"}
        
        if some_hide:
            self.report({'WARNING'},
                                        "Some objects are hidden in viewport")
            return {'CANCELLED'} 

                      
        return {"FINISHED"}

class TOT_OP_FindinView_XVertices(bpy.types.Operator):

    """Select Objects With More than X Vertices"""

    bl_idname = "tot.findxvertices"
    bl_label = "Objects With More than X Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    x_vertices: bpy.props.IntProperty(default=1000)

    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):

        scn = context.scene.tot_props
        prefs = get_prefs()

        obj_sub = []

        if scn.fv_mode == 'm1':
            ob_c = bpy.data.objects
        if scn.fv_mode == 'm2':
            ob_c = [ob for ob in bpy.data.objects if ob.visible_get() == True]
        if scn.fv_mode == 'm3':
            ob_c = bpy.context.selected_objects
    
        
        for obj in ob_c:
            if(obj.type=='MESH'):
                if prefs.includ_mod and obj.modifiers:
                    obj_v = get_verts_mod(obj)
                    if obj_v > self.x_vertices:
                        obj_sub.append(obj.name)

                else: 
                    obj_v = (len(obj.data.vertices))  
                    if obj_v > self.x_vertices:
                        obj_sub.append(obj.name)

       
        if not obj_sub:

            scn.fv_label = 'No Objects Found' 
            scn.fv_tofind = ''
            scn.fv_label_top = ''
            scn.fv_stringmode = 'list'
            
            self.report({'INFO'},
                                    "No Objects Found")
            return {'CANCELLED'}  
        
        update_label('list',obj_sub,scn)

        not_view = False
    
        if scn.fv_autoselect:
                          
            for sub in obj_sub:
                try:  
                    ob = bpy.data.objects.get(sub) 
                    ob.select_set(True) 
                except:
                    not_view = True
  
        
        if not_view:
            self.report({'WARNING'},
                                        "Some objects are not in the View Layer! Maybe they were Excluded from the View Layer in the Outliner tab")
            return {"FINISHED"}
   
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        row.prop(self,"x_vertices",text='Vertices')

class TOT_OP_FindinView_Select(bpy.types.Operator):
    """Select Objects in the list"""

    bl_idname = "tot.findselect"
    bl_label = "Select Objects"
    bl_options = {'REGISTER', 'UNDO'}

    force_select: bpy.props.BoolProperty()

    def execute(self, context):

        scn = context.scene.tot_props
        ob_c = bpy.context.selected_objects

        if scn.fv_tofind == '':
            self.report({'WARNING'},
                                    "No Objects to Select")
            return {'CANCELLED'}

        for i in ob_c:          
            i.select_set(False)

        if scn.fv_stringmode == 'single':

            if self.force_select:
                try:
                    ob = bpy.data.objects.get(scn.fv_tofind) 
                    ob.hide_viewport = False
                    ob.hide_set(False)
                except:
                    pass

            
            try:
                ob = bpy.data.objects.get(scn.fv_tofind) 
                if ob.visible_get() == False:
                    self.report({'WARNING'},
                                    "This object is hidden in viewport")
                    return {'CANCELLED'}               
                else:

                    ob.select_set(True) 
            except:
                self.report({'WARNING'},
                                    "Some objects are not in the View Layer! Maybe they were Excluded from the View Layer in the Outliner tab")
                return {'CANCELLED'}
        
        if scn.fv_stringmode == 'list':


            new_list = scn.fv_tofind.strip('][').split(', ')

            vl_obj = False
            hide_obj = False

            if self.force_select:
                for i in new_list:
                    i = i[1:-1]
                    try:
                        ob = bpy.data.objects.get(i)
                        ob.hide_viewport = False
                        ob.hide_set(False)
                    except:
                        pass

            for i in new_list:
                i = i[1:-1]
                if i:
                    try:

                        ob = bpy.data.objects.get(i) 
                        if ob.visible_get() == False:
                            hide_obj = True              
                        else:
                            ob.select_set(True) 
                    except:
                        vl_obj = True
                else:
                    self.report({'INFO'},
                                "Nothing to Select")
                    return {'CANCELLED'} 
                        
            if vl_obj:
                self.report({'WARNING'},
                                    "Some objects are not in the View Layer! Maybe they were Excluded from the View Layer in the Outliner tab")
                return {'CANCELLED'}
            
            if hide_obj:
                self.report({'WARNING'},
                                            "Some objects are hidden in the viewport")
                return {'CANCELLED'}  

        return {"FINISHED"}

