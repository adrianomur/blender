import bpy


def draw_header_out(self, context):

    layout = self.layout

    scn = context.scene.tot_props   

    if bpy.context.space_data.display_mode == 'VIEW_LAYER':
        layout.prop(scn, 'CA_Toggle', text='',icon='COLLECTION_COLOR_01', toggle=True)

def draw_header_3d(self, context):

    layout = self.layout

    scn = context.scene.tot_props       
    layout.prop(scn, 'AA_Toggle', text='',icon='SCENE_DATA', toggle=True)
