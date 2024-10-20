import bpy

from .collection_analyzer import TOT_OP_Collection_Analyzer, TOT_OP_Collection_Analyzer_Clean, TOT_OP_Collection_Cleaner
from .tot_3dview_analyzer import TOT_OP_3dview_Analyzer, TOT_OP_3dview_Analyzer_Clean
from .tot_findinview import TOT_OP_FindinView_High, TOT_OP_FindinView_sub, TOT_OP_FindinView_Select, TOT_OP_FindinView_XVertices
from .tot_execute import TOT_OP_CleanUnusedMaterials, TOT_OP_CleanSubModifiers, TOT_OP_RemoveDuplicateMaterials
from .tot_easylink import TOT_OP_EasyLink,TOT_OP_UNEasyLink
from .tot_material_Benchmark import TOT_OP_MaterialBenchmark,TOT_OP_ClearMaterialBenchmark,TOT_OP_SelectMaterialBenchmark
from .tot_imageresizer import TOT_OP_UpdateimageList,TOT_OP_ResizeImages,TOT_OP_clearduplicateImages,TOT_OP_clearimagelist,TOT_OP_Img_SelectAll,TOT_OP_Img_ImgsInformation,TOT_OP_Img_MatsImgInformation,TOT_OP_Img_MatsImgSelect
from .tot_objects_beenchmark import TOT_OP_ObjectBenchmark,TOT_OP_ClearObjectBenchmark,TOT_OP_SelectObjBenchmark

classes = (
    TOT_OP_Collection_Analyzer,
    TOT_OP_3dview_Analyzer,
    TOT_OP_Collection_Analyzer_Clean,
    TOT_OP_3dview_Analyzer_Clean,
    TOT_OP_FindinView_High,
    TOT_OP_FindinView_sub,
    TOT_OP_CleanUnusedMaterials,
    TOT_OP_CleanSubModifiers,
    TOT_OP_Collection_Cleaner,
    TOT_OP_FindinView_Select,
    TOT_OP_FindinView_XVertices,
    TOT_OP_EasyLink,
    TOT_OP_UNEasyLink,
    TOT_OP_MaterialBenchmark,
    TOT_OP_ClearMaterialBenchmark,
    TOT_OP_SelectMaterialBenchmark,
    TOT_OP_UpdateimageList,
    TOT_OP_ResizeImages,
    TOT_OP_clearduplicateImages,
    TOT_OP_clearimagelist,
    TOT_OP_Img_SelectAll,
    TOT_OP_ObjectBenchmark,
    TOT_OP_ClearObjectBenchmark,
    TOT_OP_SelectObjBenchmark,
    TOT_OP_Img_ImgsInformation,
    TOT_OP_Img_MatsImgInformation,
    TOT_OP_Img_MatsImgSelect,
    TOT_OP_RemoveDuplicateMaterials
)

def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)