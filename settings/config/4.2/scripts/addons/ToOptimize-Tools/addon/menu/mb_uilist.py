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

class TOT_MatB_UL_items(UIList):
    filter_name   : bpy.props.StringProperty(name = "Search Term", default = '')
    invert_filter : bpy.props.BoolProperty(name="Invert", default = False)

    by_name : bpy.props.BoolProperty(name="Sort By Name", default = False)
    by_size: bpy.props.BoolProperty(name="By Size", default = False)
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)

        mat_icon = bpy.data.materials.get(item.tot_mat_name)

        if not item.missing_mat:
            if mat_icon: 
                split.label(text=item.tot_mat_name,icon_value = layout.icon(bpy.data.materials[item.tot_mat_name]))
            else:
                split.label(text=item.tot_mat_name + ' (Missing)',icon = 'ERROR')

            row=split.row()
            if item.is_linked:
                row.label(text='',icon='LINKED')
            else:
                row.label(text='',icon='BLANK1')

            row.label(text=str(round(item.tot_mat_mamory,3)) + 'M')

        else:
            split.label(text=item.tot_mat_name,icon = 'ERROR')
            row=split.row()
            row.label(text='',icon='BLANK1')
            row.label(text='Missing')

    def invoke(self, context, event):
        pass  

    def draw_filter(self, context, layout):
        row = layout.row()

        subrow = row.row(align=True)
        subrow.prop(self, 'filter_name', text='')
        subrow.separator()

        if not self.by_name:
            sort_icon = 'SORTALPHA'
        else:
            sort_icon = 'SORTSIZE'

        subrow.prop(self, "by_name", text="",icon=sort_icon)
        #icon = 'REMOVE' if self.invert_filter else 'ADD'
        #subrow.prop(self, "invert_filter", text="", icon=icon)
    
    def filter_items(self, context, data, propname):
        # This function gets the collection property (as the usual tuple (data, propname)), and must return two lists:
        # * The first one is for filtering, it must contain 32bit integers were self.bitflag_filter_item marks the
        #   matching item as filtered (i.e. to be shown), and 31 other bits are free for custom needs. Here we use the
        #   first one to mark VGROUP_EMPTY.
        # * The second one is for reordering, it must return a list containing the new indices of the items (which
        #   gives us a mapping org_idx -> new_idx).
        # Please note that the default UI_UL_list defines helper functions for common tasks (see its doc for more info).
        # If you do not make filtering and/or ordering, return empty list(s) (this will be more efficient than
        # returning full lists doing nothing!).
        material_data = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Sort by name
        if self.by_name:
            flt_neworder = helper_funcs.sort_items_by_name(material_data, 'tot_mat_name')

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, material_data, "tot_mat_name"
                                                          )
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(material_data)
        
        # Sort by name

        return flt_flags, flt_neworder

class TOT_ImageResizer_UL_items(UIList):
    filter_name   : bpy.props.StringProperty(name = "Search Term", default = '')
    invert_filter : bpy.props.BoolProperty(name="Invert", default = False)

    by_name : bpy.props.BoolProperty(name="Sort By Name", default = False)
    #by_size: bpy.props.BoolProperty(name="By Size", default = False)
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scn = context.scene.tot_props
        row = layout.row()
        row.scale_x = 1

        if scn.select_images_to:
            row.prop(item, 'image_selected', text = '', emboss=False, 
                        icon = 'CHECKBOX_HLT' if item.image_selected == True else 'CHECKBOX_DEHLT')
          
        split = row.split(factor=0.74)
        image_file = bpy.data.images.get(item.tot_image_name)
  
        split.label(text=item.tot_image_name)
        #split.label(text=item.tot_image_name,icon_value = layout.icon(image_file))

        row = split.row()
        if item.packed_img == 2:       
            row.label(text='',icon='LINKED')
        elif item.packed_img == 1:       
            row.label(text='',icon='PACKAGE')
        else:
            row.label(text='',icon='BLANK1')

        if not item.image_size == '-':
            row.label(text=str(item.image_size) + ' M')
        else:
            row.label(text='',icon='ERROR')   

    def draw_filter(self, context, layout):
        row = layout.row()

        subrow = row.row(align=True)
        subrow.prop(self, 'filter_name', text='')
        subrow.separator()

        if not self.by_name:
            sort_icon = 'SORTALPHA'
        else:
            sort_icon = 'SORTSIZE'

        subrow.prop(self, "by_name", text="",icon=sort_icon)
        #icon = 'REMOVE' if self.invert_filter else 'ADD'
        #subrow.prop(self, "invert_filter", text="", icon=icon)
    
    def filter_items(self, context, data, propname):
        # This function gets the collection property (as the usual tuple (data, propname)), and must return two lists:
        # * The first one is for filtering, it must contain 32bit integers were self.bitflag_filter_item marks the
        #   matching item as filtered (i.e. to be shown), and 31 other bits are free for custom needs. Here we use the
        #   first one to mark VGROUP_EMPTY.
        # * The second one is for reordering, it must return a list containing the new indices of the items (which
        #   gives us a mapping org_idx -> new_idx).
        # Please note that the default UI_UL_list defines helper functions for common tasks (see its doc for more info).
        # If you do not make filtering and/or ordering, return empty list(s) (this will be more efficient than
        # returning full lists doing nothing!).
        images_data = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Sort by name
        if self.by_name:
            flt_neworder = helper_funcs.sort_items_by_name(images_data, 'tot_image_name')

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, images_data, "tot_image_name"
                                                          )
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(images_data)
        
        # Sort by name

        return flt_flags, flt_neworder

class TOT_OBJB_UL_items(UIList):
    #filter_name   : bpy.props.StringProperty(name = "Search Term", default = '')
    #invert_filter : bpy.props.BoolProperty(name="Invert", default = False)

    #by_name : bpy.props.BoolProperty(name="Sort By Name", default = False)
    #by_size: bpy.props.BoolProperty(name="By Size", default = False)
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)

        #mat_icon = bpy.data.materials.get(item.tot_mat_name)

        #if not item.missing_mat:
            #if mat_icon: 
        split.label(text=item.tot_obj_name,icon=item.tot_obj_icon)
            #else:
                #split.label(text=item.tot_mat_name + ' (Missing)',icon = 'ERROR')
        
        #split = layout.split(factor=0.8)
        row = split.row()
        if item.linked_obj:
            row.label(text='',icon='LINKED')
        else:
            row.label(text='',icon='BLANK1')
            
        row.label(text=str(round(item.tot_obj_mamory,3)) + 'M')

        


        #else:
        #    split.label(text=item.tot_mat_name,icon = 'ERROR')
        #    split.label(text='???')

    def invoke(self, context, event):
        pass  
