import bpy

from .main_menu import TOT_PT_Collection_Menu, TOT_PT_View3D_Menu, TOT_PT_Find_Menu,TOT_PT_ImageAnalyzer, TOT_PT_BlenderVersion_Menu, TOT_PT_Actions_Menu,TOT_PT_EasyLink_Menu,TOT_PT_MaterialBenchmark_Menu,TOT_PT_ImageResizer_Menu,TOT_PT_SceneBenchmark_Menu,TOT_PT_ObjectsBenchmark_Menu
from .draw_out_header import draw_header_out, draw_header_3d
from .mb_uilist import TOT_MatB_UL_items,TOT_ImageResizer_UL_items,TOT_OBJB_UL_items

classes = (
    TOT_OBJB_UL_items,
    TOT_PT_Collection_Menu,
    TOT_PT_BlenderVersion_Menu,
    TOT_PT_View3D_Menu,    
    TOT_PT_SceneBenchmark_Menu,
    TOT_PT_MaterialBenchmark_Menu,
    #TOT_PT_ObjectsBenchmark_Menu,
    TOT_PT_ImageAnalyzer,
    TOT_PT_ImageResizer_Menu,
    #TOT_PT_EasyLink_Menu,
    TOT_PT_Find_Menu,
    TOT_PT_Actions_Menu,
    TOT_MatB_UL_items,
    TOT_ImageResizer_UL_items,
)

def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    if not (2, 91, 0) > bpy.app.version:
        bpy.types.OUTLINER_HT_header.append(draw_header_out) 

    bpy.types.VIEW3D_HT_header.append(draw_header_3d)


def unregister_menus():
    
    if not (2, 91, 0) > bpy.app.version:
        bpy.types.OUTLINER_HT_header.remove(draw_header_out)

    bpy.types.VIEW3D_HT_header.remove(draw_header_3d)
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)