
from . import auto_load as al
from . auto_load.common import *
from . import dev_info
from . import operators
from . import baking

import json

PREFERENCES_EXTENSION: str = '.json'

KEYMAP_MANAGER: al.KeymapManager = None

class PreferencesContext(al.BStaticEnum):

    INTERFACE = dict(n="Interface", d="Interface Settings")
    SHORTCUTS = dict(n="Shortcuts", d="Shortcut settings")
    BAKING = dict(n="Baking", d="Baking Settings")
    DECALS = dict(n="Decals", d="Decal Settings")


@al.register
class CustomDecalFolder(al.PropertyGroup):

    directory = al.PathProperty(name='Custom Decals', description='Folder location where user decal images are stored', default='//', subtype=al.BPropertySubtypeString.DIR_PATH, fallback=al.BPathFallbackType.NONE)
    category_name = al.StringProperty(name='Category Name', default='', description='Name of the custom decals category that is displayed in the UI.')

    def draw_ui(self, layout: bt.UILayout, collection: al.CollectionProperty['CustomDecalFolder']):
        row = al.UI.row(layout)
        f1 = lambda l: self.category_name.draw_ui(l, al.UILabel(""))
        f2 = lambda l: self.directory.draw_ui(l, al.UILabel(""))
        al.UI.weighted_split(row, (f1, 0.4), (f2, 1), align=True)
        collection.get_remove_element(self).draw_ui(row, al.UIIcon(al.BIcon.REMOVE))

    @al.PD.update_property(directory)
    @al.PD.update_property(category_name)
    def validate_category_name(self, context: bt.Context):
        
        # force paths to be absolute
        if self.directory.is_relative and bpy.data.is_saved:
            self.directory.raw = self.directory.absolute

        from . import library_manager
        library_manager.ASSETS_UP_TO_DATE = False
        if self.category_name():
            return
        try:
            dir_str = str(self.directory.absolute)
        except OSError:
            self.category_name.value = "Custom"
            return
        if not dir_str:
            self.category_name.value = "Custom"
            return
        self.category_name.value = self.directory.absolute.name


@al.register
class InterfacePreferences(al.PropertyGroup):

    use_static_panel = al.BoolProperty(name='Display N-Panel', default=True, description='Toggle the panel on the right side of the 3D View')
    use_filters = al.BoolProperty(name='Display Filters', default=True, description='Use Filters for organizing Sanctus Assets')
    display_material_slots = al.BoolProperty(name='Diplay Material Slots', default=True, description='Display a UI element for the active material of the active object in the Material Panel')
    center_mouse_on_gizmos = al.BoolProperty(name='Center Mouse when using Gizmos', default=False, description='When using the interactive decal or GN asset gizmos, your mouse gets centered when enabled')
    asset_thumbnail_scale = al.FloatProperty(name='Asset Thumbnail Scale', default=4.0, min=1.0)


@al.register
class ShortcutsPreferences(al.PropertyGroup):
    pass

@al.register
class DecalPreferences(al.PropertyGroup):

    
    custom_decal_folders = al.CollectionProperty(type=CustomDecalFolder, name='Custom Decal Directories')

    @al.PD.set_on_add_element(custom_decal_folders)
    @al.PD.set_on_remove_element(custom_decal_folders)
    def on_custom_decal_folders_change(c: al.CollectionProperty[CustomDecalFolder], e: CustomDecalFolder):
        from . import library_manager
        library_manager.ASSETS_UP_TO_DATE = False

@al.depends_on(CustomDecalFolder, InterfacePreferences, ShortcutsPreferences, DecalPreferences, baking.settings.BakingPreferences)
@al.register
class SanctusLibraryPreferences(al.AddonPreferences):
    

    current_context = al.EnumProperty(enum=PreferencesContext, default=PreferencesContext.INTERFACE, name="Context", description="Current preferences tab")

    #contexts
    interface = al.PointerProperty(type=InterfacePreferences)
    shortcuts = al.PointerProperty(type=ShortcutsPreferences)
    baking = al.PointerProperty(type=baking.settings.BakingPreferences)
    decals = al.PointerProperty(type=DecalPreferences)

    developer_mode = al.BoolProperty(name='Developer Mode', default=False, description='Enables Developer Options. Do not touch!')

    favorites = al.JSONDataProperty(name='Favorites', default={})

    def draw(self, context: bt.Context):
        layout: bt.UILayout = self.layout

        sl_col = al.UI.column(layout.box(), align=True)
        sle_row = al.UI.row(sl_col, align=True)
        operators.preferences.ImportPreferences().draw_ui(sle_row, al.UIOptionsOperator(icon=al.BIcon.FILE_FOLDER))
        operators.preferences.ExportPreferences().draw_ui(sle_row, al.UIOptionsOperator(icon=al.BIcon.FILE))

        operators.library.InstallPillow().draw_ui(layout)

        layout.separator()

        context_col = al.UI.column(layout, align=True)
        context_row = al.UI.row(context_col, align=True)
        context_row.scale_y = 1.3

        self.current_context.draw_ui(context_row, options=al.UIOptionsProp(expand=True))
        context_layout = context_col.box()

        if self.current_context() == PreferencesContext.INTERFACE:
            interface = self.interface()
            col = al.UI.column(context_layout)
            interface.use_static_panel.draw_ui(col)
            interface.use_filters.draw_ui(col)
            interface.display_material_slots.draw_ui(col)
            interface.center_mouse_on_gizmos.draw_ui(col)
            interface.asset_thumbnail_scale.draw_ui(col)

        elif self.current_context() == PreferencesContext.SHORTCUTS:
            for shortcut in KEYMAP_MANAGER.shortcuts:
                shortcut.draw_user_binding(context_layout, expand=True, use_icons=False)
            
        elif self.current_context() == PreferencesContext.BAKING:
            baking.ui.BakingPreferencesDrawer(self.baking(), al.UI.column(context_layout), context).draw()
        
        elif self.current_context() == PreferencesContext.DECALS:
            al.UI.label(context_layout, "Custom Decal Directories:")
            self.draw_custom_decal_directories(context_layout.box())

        if dev_info.DEVELOPER_MODE:
            from . import developer_tool
            layout.separator()
            self.developer_mode.draw_ui(layout)
            developer_tool.CheckMaterialsForBakeSockets().draw_ui(layout)

    def draw_custom_decal_directories(self, layout: bt.UILayout):
        decal_settings = self.decals()
        col = al.UI.column(layout)
        decal_settings.custom_decal_folders.get_add_element().draw_ui(col, al.UIOptionsOperator(text='Add Directory', icon=al.BIcon.ADD))

        for item in decal_settings.custom_decal_folders():
            item.draw_ui(col, decal_settings.custom_decal_folders)

        from . import library_manager
        if not library_manager.ASSETS_UP_TO_DATE:
            al.UI.label(al.UI.alert(col), 'Reload the library assets in order to reflect the library changes', icon=al.BIcon.ERROR)
            operators.library.ReloadLibrary().draw_ui(col, al.UIOptionsOperator(text='Reload Library'))

    def get_developer_mode(self):
        return self.developer_mode() and dev_info.DEVELOPER_MODE
    
    def load_prefs(self):
        if not self.preference_file.exists():
            return
        print('Loading SL Preferences...')
        try:
            data = self.preference_file.read_json()
        except json.decoder.JSONDecodeError:
            print('Decoder Error when parsing SL Preferences! Cannot load preferences.')
            return
        self.deserialize(data)
        
        #TODO fix favorites
        keys = self.favorites().keys()
        if any('::' in x for x in keys):
            print('Old Favorite Keys Found')
            new_keys = [(Path(*x.split('::')[1:]) if '::' in x else x) for x in keys]
            self.favorites.value = {str(x) : True for x in new_keys}
    
    def save_prefs(self):
        print('Saving SL Preferences...')
        data = self.serialize()
        self.preference_file.write_json(data)

@al.skip_function_in_background
@al.register
def register_keymaps(register: bool):
    from . import panel_ui
    global KEYMAP_MANAGER

    kc = al.get_wm().keyconfigs.addon
    if kc and not bpy.app.background:
        if register:
            KEYMAP_MANAGER = al.KeymapManager()
            KEYMAP_MANAGER.add_shortcut_builtin(
                bo.wm.call_panel,
                {'name': panel_ui.SL_PT_View3DPanel.bl_idname},
                al.BEventType.S,
                al.BEventValue.PRESS,
                region_type=al.BRegionType.WINDOW,
                name='Floating Panel Shortcut',
                ctrl=True,
                alt=True
            )

        else:
            if KEYMAP_MANAGER is None:
                return
            KEYMAP_MANAGER.clear_shortcuts()

@al.register
def register_load_preferences(register: bool):
    prefs = SanctusLibraryPreferences()
    if register:
        prefs.load_prefs()
    else:
        prefs.save_prefs()


def get() -> SanctusLibraryPreferences:
    return al.get_prefs()
