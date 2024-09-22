
from . import auto_load as al
from .auto_load.common import *

def _import_asset(file: str, name: str, asset_type: str, link: bool = False) -> bpy.types.ID:
    with bpy.data.libraries.load(file, link=link) as (f, t):
        if not name in getattr(f, asset_type):
            raise KeyError(f'Asset "{name}" not in "{asset_type}" of source file "{file}"')
        getattr(t, asset_type).append(name)
    return getattr(bpy.data, asset_type).get(name)


def _is_ID_derived_from(id_name: str, original_name: str) -> bool:
    if id_name == original_name:
        return True

    if not id_name.startswith(original_name):  # has to start with original name
        return False
    stump = id_name.replace(original_name, '', 1)
    if not stump[0] == '.':  # stump has to have the number signature ".001"
        return False
    if not stump[1:].isnumeric():
        return False
    return True

class ImportManager:

    ASSET_TYPES = (
        'actions',
        'armatures',
        'brushes',
        'cameras',
        'collections',
        'curves',
        'fonts',
        'grease_pencils',
        'hair_curves',
        'images',
        'lattices',
        'lightprobes',
        'lights',
        'linestyles',
        'masks',
        'materials',
        'meshes',
        'metaballs',
        'movieclips',
        'node_groups',
        'objects',
        'paint_curves',
        'palettes',
        'particles',
        'pointclouds',
        'scenes',
        'shape_keys',
        'sounds',
        'speakers',
        'texts',
        'textures',
        'volumes',
        'window_managers',
        'workspaces',
        'worlds'
    )

    def __init__(self, path: Path, asset_type: str):
        self.path = path
        self.asset_type = asset_type
        self.main_asset: bt.ID = None
        self.all_imported_assets: dict[str, list[bt.ID]] = {}

        from . import library_manager
        instance = library_manager.MANAGER.runtime_library.search_hierarchy(self.path)
        if not isinstance(instance, library_manager.lib.AssetInstance):
            raise ValueError(f'Path provided for Asset Imporer "{str(self.path)}" does not lead to an asset instance')
        self.asset_instance = instance
        self.asset_name = self.asset_instance.name
    
    # @property
    # def asset_instance(self):
    #     from . import library_manager
    #     result = library_manager.MANAGER.runtime_library.search_hierarchy(self.path)
    #     if not isinstance(result, library_manager.lib.AssetInstance):
    #         raise ValueError(f'Path provided for Asset Imporer "{str(self.path)}" does not lead to an asset instance')
    #     return result

    @property
    def asset_collection(self) -> Union[bt.bpy_prop_collection, list[bt.ID]]:
        return getattr(bpy.data, self.asset_type)

    @property
    def exists_in_file(self):
        return self.asset_name in self.asset_collection.keys()

    def is_compatible(self, context: bt.Context):
        return context.scene.render.engine in [x.get_id() for x in self.asset_instance.asset.meta.get_engine()]

    def get_asset(self, reimport: bool):

        old_assets_all: dict[str, list[bt.ID]] = {k: getattr(bpy.data, k).values() for k in self.ASSET_TYPES}
        asset_name = self.asset_name
        if not asset_name in self.asset_collection.keys() or reimport:
            asset = self._load_asset()
        else:
            asset = self.asset_collection[asset_name]
        self.main_asset = asset
        for collection_key, old_collection in old_assets_all.items():
            new_collection = getattr(bpy.data, collection_key)
            self.all_imported_assets[collection_key] = [x for x in new_collection if x not in old_collection]

        return asset
    
    def _load_asset(self):
        old_assets: list[bt.ID] = list(self.asset_collection.values())
        if not self.asset_instance.asset.has_blend and self.asset_instance.asset.has_icons: # icon asset
            return bpy.data.images.load(str(self.asset_instance.asset.icon_files[self.asset_instance.preset]), check_existing=False)
        _import_asset(str(self.asset_instance.asset.blend_file), self.asset_name, self.asset_type, link=False)
        return next(x for x in self.asset_collection if not x in old_assets and _is_ID_derived_from(x.name, self.asset_name))
    
    def remove_all_imported_assets(self):
        for key, assets in self.all_imported_assets.items():
            collection: bt.bpy_prop_collection = getattr(bpy.data, key)
            for a in assets:
                try:
                    collection.remove(a)
                except ReferenceError:
                    print("Could not remove ID object. It likely has been removed already.")
