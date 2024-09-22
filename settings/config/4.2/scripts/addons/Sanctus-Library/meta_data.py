import bpy
import json
import typing
import dataclasses

from . import auto_load as al
from .auto_load.common import *

from . import base_ops
from . import dev_info
from . import library
from . import constants

FIX_META_DATA: bool = False

def fix_meta_data():
    return FIX_META_DATA and dev_info.DEVELOPER_MODE

def get_render_engine_name(engine_id: str) -> str:
    builtin_engines_map = {
        'BLENDER_EEVEE': 'Eevee',
        'BLENDER_WORKBENCH': 'Workbench',
        'CYCLES': 'Cycles'
    }
    fallback_name = engine_id.replace('_', ' ').title()
    return builtin_engines_map.get(engine_id, fallback_name)

class MetaEngine(al.BStaticEnum):

    C = dict(n='Cycles', d='Use the Cycles Render Engine', a='CYCLES')
    E = dict(n='Eevee', d='Use the Eevee Render Engine', a='BLENDER_EEVEE' if bpy.app.version < constants.EEVEE_NEXT else 'BLENDER_EEVEE_NEXT')

    def get_id(self) -> str:
        return self.value['a']
    

def meta_engine_from_id(id: str):
    return next(x for x in MetaEngine if x.get_id() == id)

def material_output_id_from_met_engines(s = set[MetaEngine]):
    if s == {MetaEngine.C}:
        return 'CYCLES'
    if s == {MetaEngine.E}:
        return 'EEVEE'
    return 'ALL'

class MetaComplexity(al.BStaticEnum):

    _0 = dict(n='Low', d='Low Complexity')
    _1 = dict(n='Medium', d='Medium Complexity')
    _2 = dict(n='High', d='High Complexity')


class GeometryNodeAssetType(al.BStaticEnum):

    ADD_NEW = dict(n='Add New', d='Any type of asset or non-GN assets')
    APPLY_MESH = dict(n='Apply to Mesh', d='Add asset as modifier to selected mesh obeject')
    APPLY_CURVE = dict(n='Apply to Curve', d='Add asset as modifier to selected curve object')
    DRAW_FREE = dict(n='Free Draw', d='New curve object with curve draw mode enabled')
    DRAW_SURFACE = dict(n='Draw on Surface', d='New curve object added to selected object to draw on surface')
    PLACE_SURFACE = dict(n='Place on Surface', d='Add asset as new object and place it on surface')

@dataclasses.dataclass
class SanctusMetaData:

    engine: list[str] = dataclasses.field(default_factory=(lambda: [x() for x in MetaEngine.all()]))

    def get_engine(self):
        return {MetaEngine.from_string(x) for x in self.engine}

    def set_engine(self, value: MetaEngine):
        self.engine = list(value())

    complexity: str = MetaComplexity._0()

    def get_complexity(self):
        return MetaComplexity.from_string(self.complexity)

    def set_complexity(self, value: MetaComplexity):
        self.complexity = value()

    gn_type: list[str] = dataclasses.field(default_factory=(lambda: [GeometryNodeAssetType.ADD_NEW()]))

    def get_gn_type(self):
        return {GeometryNodeAssetType.from_string(x) for x in self.gn_type}
    
    def set_gn_type(self, value: GeometryNodeAssetType):
        self.gn_type = list(value())

    use_displacement: bool = False
    require_uvs: bool = False

    description: str = ''
    documentation_link: str = ''

    @classmethod
    def keys(cls) -> list[str]:
        return cls.__dataclass_fields__.keys()

    def items(self) -> list[tuple[str, typing.Any]]:
        return [(k, getattr(self, k)) for k in self.keys()]

    def values(self) -> list[typing.Any]:
        return [getattr(self, k) for k in self.keys()]

    @classmethod
    def from_file(cls, filepath: Path) -> 'SanctusMetaData':
        with filepath.open('r') as openfile:
            try:
                data = json.load(openfile)
            except json.JSONDecodeError as e:
                print(f'Corrupted Meta Data in file "{str(filepath)}"')
                if fix_meta_data():
                    print('Using Default Meta Data')
                    data = SanctusMetaData().to_dict()
                else:
                    raise e
        if fix_meta_data():
            fix_json_meta_data(data)
        meta = SanctusMetaData(**data)
        if fix_meta_data():
            meta.to_file(filepath)
        return meta

    def to_dict(self):
        return {k: v for k, v in self.items()}

    def to_file(self, filepath: Path) -> None:
        data = self.to_dict()
        with filepath.open('w') as openfile:
            json.dump(data, openfile)

    def has_description(self) -> bool:
        return self.description != ''

    def get_description(self):
        real_description = self.description.replace('\\n', '\n')
        return real_description


def fix_json_meta_data(data: dict[str, typing.Any]):
    # Fix complexity being saved as int
    complexity = data['complexity']
    if isinstance(complexity, int):
        data['complexity'] = str(complexity)
    
    # Fix favorites being stores as meta data instead of preferences
    if 'favorite' in data.keys():
        del data['favorite']
    
    # Fix engine being saved as a string (enum) instead of list of strings (enum flag)
    engine = data.get('engine', None)
    if isinstance(engine, str):
        if engine == 'A':
            data['engine'] = [x() for x in MetaEngine.all()]
        else:
            data['engine'] = [engine]

    
    gn_type = data['gn_type']
    if isinstance(gn_type, str):
        data['gn_type'] = [GeometryNodeAssetType.ADD_NEW()]
    

    # remove invalid meta keys, run at end of method
    invalid_keys = [k for k in data.keys() if not k in SanctusMetaData.keys()]
    for k in invalid_keys:
        del data[k]


@al.register_operator
class SetMetaData(base_ops.SanctusOperator):
    bl_description = 'Set Meta Data on the selected Sanctus Library Item'

    engine = al.EnumFlagProperty(enum=MetaEngine, name='Engine', default=MetaEngine.all())
    complexity = al.EnumProperty(enum=MetaComplexity, name='Complexity', default=0)
    gn_type = al.EnumFlagProperty(enum=GeometryNodeAssetType, name='GN Type', default={GeometryNodeAssetType.ADD_NEW})
    use_displacement = al.BoolProperty(name='Use Displacement')
    require_uvs = al.BoolProperty(name='Require UVs')
    meta_description = al.StringProperty(name='Description', default='')
    meta_documentation_link = al.StringProperty(name='Documentation', default='')

    asset_path = al.StringProperty(options={al.BPropertyFlag.HIDDEN})

    def invoke(self, context: bt.Context, event: bt.Event) -> set[str]:
        item = self.get_item()
        meta = item.meta

        self.meta_description.value = meta.description
        self.meta_documentation_link.value = meta.documentation_link

        if event.shift:
            return self.execute(context)
        else:
            wm = al.get_wm()
            self.engine.value = meta.get_engine()
            self.complexity.value = meta.get_complexity()
            self.gn_type.value = meta.get_gn_type()
            self.use_displacement.value = meta.use_displacement
            self.require_uvs.value = meta.require_uvs
            return wm.invoke_props_dialog(self)

    def get_item(self):
        from . import library_manager
        return library_manager.MANAGER.all_assets[Path(self.asset_path())]

    def draw(self, context):
        layout: bt.UILayout = al.UI.column(self.layout)
        item = self.get_item()
        al.UI.label(layout, text=item.asset_name)
        layout.use_property_split = True

        for p in self.get_annotated_properties().values():
            if p.check_option(al.BPropertyFlag.HIDDEN):
                continue
            p.draw_ui(layout)

    def execute(self, context: bt.Context):
        from . import library_manager as lm
        md = SanctusMetaData(
            engine=[x() for x in self.engine()],
            complexity=self.complexity()(),
            gn_type=[x() for x in self.gn_type()],
            use_displacement=self.use_displacement(),
            require_uvs=self.require_uvs(),
            description=self.meta_description(),
            documentation_link=self.meta_documentation_link()
        )

        item = self.get_item()
        if item.meta_file is None:
            item.meta_file = library._create_metapath(item.directory, item.asset_name)
        if(not item.meta_file.exists()):
            item.meta_file.touch(exist_ok=False)
        md.to_file(item.meta_file)
        item.meta = md

        return {'FINISHED'}
