import bpy
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Operator, Panel, PropertyGroup, UIList

from ..utility.addon import addon_name, get_prefs


class TOT_Prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    store_colors: BoolProperty(
        default=True,
        name=" Store Original Colors",
        description="Store the original color of each object in the scene before using the Scene Analyzer Tool. (If enabled, may impact in performance when using the tool, enable it only if you need this feature)",
    )
    includ_mod: BoolProperty(
        default=True,
        name=" Include Modifiers in Vertice Count",
        description="By Default, Blender Object Data does not stores vertices with non-applied modifiers. By Enabling this option, the addon will use another method to get vertice count of objects with modifiers. (If enabled, may impact in performance when using the tool, enable it only if you need this feature)",
    )

    ### Material Bench
    auto_console: BoolProperty(
        default=True,
        name=" Auto Toggle Console if necessary",
        description="The console will be toggled before any long process starts such as Image Resizing or Scene Benchmarks, and you will be able to see the progress",
    )
    b_auto_save: BoolProperty(
        default=True,
        name=" Auto Save File Before Benchmark",
        description="The file always need to be saved for all materials be accessible in the benchmark process",
    )

    # Texture Analyzer

    show_link_images: BoolProperty(
        default=False,
        name=" Show Linked Images",
        description="Show Linked Images in Image Data Analyzer List",
    )
    show_packed_images: BoolProperty(
        default=False,
        name=" Show Packed Images",
        description="Show Packed Images in Image Data Analyzer List",
    )

    im_auto_save: BoolProperty(
        default=True,
        name=" Auto Save File Before Resizing",
        description="Auto Save File Before Resizing",
    )
    clearimg_beforeresize: BoolProperty(
        default=True,
        name=" Clear Duplicates Before Resizing",
        description=" Always clear duplicate images before resizing process",
    )

    def draw(self, context):

        prefs = get_prefs()
        layout = self.layout

        col = layout.column(align=True)
        box = col.box()
        box.label(
            text="Need help or have a feature request? Join our Discord server!"
        )
        box.operator("wm.url_open", text="Join our Discord Server").url = (
            "https://discord.gg/XGeDTUsmb4"
        )

        box = layout.box()
        box.label(text="Peformance:")
        box.prop(prefs, "store_colors")
        box.prop(prefs, "includ_mod")

        box = layout.box()
        box.label(text="Material Benchmark:")
        box.prop(prefs, "b_auto_save")

        box = layout.box()
        box.label(text="Textures Analyzer:")
        # box.prop(prefs,'clearimg_beforeresize')
        image_data_box = box.box()
        image_data_box.label(text="Image Data")
        image_data_box.prop(prefs, "show_packed_images")
        image_data_box.prop(prefs, "show_link_images")

        save_box = box.box()
        save_box.prop(prefs, "im_auto_save")

        box = layout.box()
        box.label(text="Console:")
        box.prop(prefs, "auto_console")
