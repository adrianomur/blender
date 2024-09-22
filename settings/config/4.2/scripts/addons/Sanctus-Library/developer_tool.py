import subprocess

import bpy.types as bt
from . import library
from . import auto_load as al
from .auto_load.common import *
from . import asset
from . import meta_data
from . import node_utils

def draw_meta_data_preview(layout: bt.UILayout, name: str, meta: meta_data.SanctusMetaData):
    c = layout.column(align=True)
    c.scale_y = 0.8
    al.UI.label(c, f'Current Item Meta: ({name})')
    for v, k in meta.items():
        al.UI.label(c, f'{v}: {k}')


def _correction_args(blend_file: Path, subtask_file_name: str):
    return [
        bpy.app.binary_path,
        str(blend_file),
        '-b',
        '--factory-startup',
        '--python',
        str(Path(__file__).parent.joinpath('developer_tools', subtask_file_name))
    ]

def _run_background(args: list, shell: bool = True):
    # subprocess.run(args, stdout=sys.stdout, shell=shell)
    output = subprocess.check_output(args, shell=True)
    return output.decode('UTF-8')

def _print_output(output: str):
    parts = output.splitlines()
    ignore_prefixes = [
        'Blender ',
        'Read blend: ',
        'Blender quit'
    ]
    end = '==================='
    custom_prints = [p for p in parts if not any(p.startswith(x) for x in ignore_prefixes)]
    custom_prints.insert(0, '')
    print('\n    '.join(custom_prints))
    print(end)

def _get_all_material_items():
    from . import library_manager as lm
    return [v for k, v in lm.MANAGER.all_assets.items() if lm.AssetClasses.MATERIALS in k.parts]

@al.register_operator
class CorrrectNormalBakeNodes(al.Operator):

    def run(self, context: bt.Context):
        material_items = _get_all_material_items()
        valid_items: list[library.Asset] = []
        for i in material_items:
            with bpy.data.libraries.load(str(i.blend_file), link=False, relative=False) as (from_data, to_data):
                if any('normal_bake' in x for x in from_data.node_groups):
                    valid_items.append(i)
        
        for i in valid_items:
            
            print(f'Running file: {i.asset_name}')
            output = _run_background(_correction_args(i.blend_file, '_fix_normal_bake.py'))
            _print_output(output)
            

@al.register_operator
class CorrectDisplacementMaterials(al.Operator):

    al_asserts = [
        al.OperatorAssert(lambda c: bpy.app.version >= (4,0,0), 'Blender 4.0 or higher required', strict=False)
    ]

    def run(self, context: bt.Context):
        valid_items = [x for x in _get_all_material_items() if x.meta.use_displacement]
        
        for i in valid_items:
            
            print(f'Running file: {i.asset_name}')
            output = _run_background(_correction_args(i.blend_file, '_fix_displacement_materials.py'))
            _print_output(output)

@al.register_operator
class CheckMaterialsForBakeSockets(al.Operator):

    def run(self, context: bt.Context):
        valid_items = [x for x in _get_all_material_items()]

        for i in valid_items:
            print(f'Running file: {i.asset_name}')
            output = _run_background(_correction_args(i.blend_file, '_check_material_bake_sockets.py'))
            _print_output(output)

class DocText:
    TODO_TEXT = 'TODO'
    CATEGORY_SYMBOL = '▼'
    BOOL_TEXT_VALUES = ('Yes', 'No')

    _lines: list[str]

    def __init__(self, text: str = ''):
        self.text = text

    @property
    def text(self):
        return '\n'.join(self._lines) + '\n'
    
    @text.setter
    def text(self, new_text: str):
        self._lines = new_text.splitlines()
    
    def add_line(self, line: str):
        self._lines.append(line)

    def pop_line(self, index: int = -1):
        return self._lines.pop(index)

    def add_header(self, text: str, bold: bool = True):
        if bold:
            text = DocText.bold(text)
        self.add_line(f'h3. {text}')
    
    def add_parameter(self, title: str, description: str = TODO_TEXT):
        title = DocText.bold(title + ':')
        self.add_line(f'{title} {description}')
    
    def add_category(self, name: str):
        self.add_line(f'{DocText.CATEGORY_SYMBOL} {name}')

    def add_newline(self):
        self.add_line('')

    def copy(self):
        new = type(self)()
        new._lines = self._lines.copy()
        return new
    
    def clear(self):
        self._lines = []

    def __add__(self, other):
        new = type(self)()
        new._lines = self._lines
        new._lines += self.to_doctext(other)._lines
        return new
    
    def __iadd__(self, other):
        self._lines += self.to_doctext(other)._lines
        return self
    
    @classmethod
    def to_doctext(cls, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(value)
        return cls(str(value))
    
    def is_empty(self):
        return len(self._lines) < 1
    
    def is_whitespace(self):
        return all(x.removesuffix('\n').isspace() for x in self._lines)
    
    @staticmethod
    def bool_text(value: bool):
        return DocText.BOOL_TEXT_VALUES[0] if value else DocText.BOOL_TEXT_VALUES[1]

    @staticmethod
    def complexity_text(complexity: str):
        value = int(complexity) + 1
        return f'{value}/3'

    @staticmethod
    def gn_type_text(meta: meta_data.SanctusMetaData):
        if len(meta.gn_type) == 1:
            return meta_data.GeometryNodeAssetType.from_string(meta.gn_type[0]).get_name()
        l = [meta_data.GeometryNodeAssetType.from_string(x).get_name() for x in meta.gn_type]
        return '[' + ', '.join(l) + ']'
    
    @staticmethod
    def wrap(text: str, symbol: str):
        return symbol + text + symbol

    @staticmethod
    def bold(text: str):
        return DocText.wrap(text, '*')
    
    @staticmethod
    def link(type: str, link_id: str, link_name: str = '', insert: str = 'blank'):
        prefix = f'({insert})'
        if link_name != '':
            prefix = f'"({insert}){link_name}":'
        return prefix + '{' + f'{type}-LINK+{link_id}' + '}'


@al.register_operator
class CopyItemTemplateDocumentation(al.Operator):

    asset_path = al.StringProperty()
    
    def get_material_documentation(self, asset_item: library.Asset):

        from .panel_ui_sections import SanctusMaterialSection
        engines = list(asset_item.meta.get_engine())

        result = DocText()
        result.add_header('Technical Details')
        result.add_newline()
        engines_text = ', '.join([x.get_name() for x in engines])
        result.add_parameter('Render Engines Compatibility', engines_text)
        result.add_parameter(
            'Requires Displacement', 
            DocText.bool_text(asset_item.meta.use_displacement) 
            + (f' ({DocText.link("TOPIC", "displacement", "working with Displacement")})' if asset_item.meta.use_displacement else '')
        )
        result.add_parameter('Requires UVs', DocText.bool_text(asset_item.meta.require_uvs))
        result.add_parameter('Processing/Complexity', DocText.complexity_text(asset_item.meta.complexity))
        result.add_parameter('Can be baked', f'Yes ({DocText.link("TOPIC", "baking-procedural-materials", "How to bake materials")})')
        result.add_newline()
            
        
        import_manager = asset.ImportManager(asset_item.instance_path(0), asset_type='materials')
        material: bt.Material = import_manager.get_asset(reimport=True)

        nt: bt.ShaderNodeTree = material.node_tree
            
        def get_material_parameters():
            from . import meta_data
            params_text = DocText()
            parameter_count = 0
            try:
                output = SanctusMaterialSection.get_shader_output_node(nt, meta_data.material_output_id_from_met_engines(asset_item.meta.get_engine()))
                node = SanctusMaterialSection.get_first_material_node(output)
            except SanctusMaterialSection.ShaderNodeFindError:
                return DocText()
            for i in node.inputs:
                if SanctusMaterialSection.shader_input_is_category(i):
                    if parameter_count > 1:
                        params_text.add_newline()
                    params_text.add_category(i.name[2:-2])
                    parameter_count += 1
                    continue
                hidden_text = ' (Only visible in the Shader Editor)' if i.hide_value else ''
                params_text.add_parameter(f'{i.name}{hidden_text}')
                parameter_count += 1

            return params_text

        material_params_text = get_material_parameters()
        if not material_params_text.is_empty():
            result.add_header('Parameters')
            result.add_newline()
            result += material_params_text
        
        import_manager.remove_all_imported_assets()
        return result

    def get_gn_documentation(self, asset_item: library.Asset):

        result = DocText()
        result.add_header('Technical Parameters')
        result.add_newline()
        result.add_parameter('Asset Type', DocText.gn_type_text(asset_item.meta))
        
        result.add_newline()
        result.add_header('Parameters')
        result.add_newline()

        import_manager = asset.ImportManager(asset_item.instance_path(0), 'node_groups')
        node_group: bt.GeometryNodeTree = import_manager.get_asset(reimport=True)
        parameter_count = 0
        for i in node_utils.get_node_tree_inputs(node_group):
            if isinstance(i, bt.NodeTreeInterfaceSocketString) and node_utils.input_name_is_category(i.name):
               if parameter_count > 0:
                   result.add_newline()
               result.add_category(node_utils.category_name_reduced(i.name))
               parameter_count += 1
               continue
            result.add_parameter(i.name)
            parameter_count += 1
        
        if parameter_count < 1:
            result.pop_line()
            result.pop_line()
            result.pop_line()

        import_manager.remove_all_imported_assets()
        return result 
    
    def get_decal_documentation(self, asset_item: library.Asset):
        return DocText()
    
    def get_shader_documentation(self, asset_item: library.Asset):
        result = DocText()

        result.add_header('Parameters')
        result.add_newline()

        import_manager = asset.ImportManager(asset_item.instance_path(0), 'node_groups')
        node_group: bt.ShaderNodeTree = import_manager.get_asset(reimport=True)

        inputs = node_utils.get_node_tree_inputs(node_group)
        if len(inputs) == 0:
            return result

        parameter_count = 0
        for i in node_utils.get_node_tree_inputs(node_group):
            if isinstance(i, bt.NodeTreeInterfaceSocket) and node_utils.input_name_is_category(i.name):
                if parameter_count > 0:
                    result.add_newline()
                result.add_category(node_utils.category_name_reduced(i.name))
                parameter_count += 1
                continue
            result.add_parameter(i.name)
            parameter_count += 1
        
        import_manager.remove_all_imported_assets()
        return result
    
    def get_compositor_documentation(self, asset_item: library.Asset):
        return self.get_shader_documentation(asset_item)

    def get_smodules_documentation(self, asset_item: library.Asset):
        return self.get_shader_documentation(asset_item)

    def run(self, context: bt.Context):
        from . import library_manager as lm

        asset_item = lm.MANAGER.all_assets[Path(self.asset_path())]

        result: DocText = DocText()
        path_parts = asset_item.asset_path.parts
        if lm.AssetClasses.MATERIALS in path_parts:
            result = self.get_material_documentation(asset_item)
        elif lm.AssetClasses.GNTOOLS in path_parts:
            result = self.get_gn_documentation(asset_item)
        elif lm.AssetClasses.DECALS in path_parts:
            result = self.get_decal_documentation(asset_item)
        elif lm.AssetClasses.SHADER in path_parts:
            result = self.get_shader_documentation(asset_item)
        elif lm.AssetClasses.COMPOSITOR in path_parts:
            result = self.get_compositor_documentation(asset_item)
        elif lm.AssetClasses.SMODULES in path_parts:
            result = self.get_smodules_documentation(asset_item)
        
        al.get_wm().clipboard = result.text
        self.report({'INFO'}, 'Copied Template Documentation to Clipboard')

def copy_gn_modifier_values_to_group(mod: bt.NodesModifier):
    DEFAULT_VALUE = 'default_value'
    node_tree: bt.GeometryNodeTree = mod.node_group
    inputs = [x for x in node_utils.get_node_tree_inputs(node_tree) if hasattr(x, DEFAULT_VALUE)]

    for i in inputs:
        setattr(i, DEFAULT_VALUE, mod[i.identifier])


@al.register_operator
class CopyNodesModifierValuesToGroup(al.Operator):

    obj = al.ContextProperty[bt.Object]()
    modifier_name = al.StringProperty()

    def get_modifier(self) -> bt.NodesModifier:
        return self.obj().modifiers[self.modifier_name()]
    
    def run(self, context: bt.Context):
        copy_gn_modifier_values_to_group(self.get_modifier())

@al.register_draw_function(bt.DATA_PT_modifiers)
def draw_copy_modifier_values_interface(self: bt.Panel, context: al.BContext[bt.SpaceProperties]):
    from . import preferences
    if not preferences.get().get_developer_mode():
        return
    layout = self.layout
    obj = context.space_data.pin_id if context.space_data.use_pin_id else context.object
    if obj is None:
        return
    valid_mods = [x for x in obj.modifiers if isinstance(x, bt.NodesModifier) and x.node_group is not None]
    if len(valid_mods) == 0:
        return
    layout = layout.box().column(align=True)
    al.UI.label(layout, 'Copy Modifier Values to Group')
    for mod in valid_mods:
        CopyNodesModifierValuesToGroup(obj=obj, modifier_name=mod.name).draw_ui(layout, al.UIOptionsOperator(text=mod.name))


def copy_group_node_vaues_to_node_group(node: bt.ShaderNodeGroup):
    DEFAULT_VALUE = 'default_value'
    inputs = [x for x in node_utils.get_node_tree_inputs(node.node_tree)if hasattr(x, DEFAULT_VALUE)]

    for i in inputs:
        node_input = next(x for x in node.inputs if x.identifier == i.identifier)
        setattr(i, DEFAULT_VALUE, node_input.default_value)


@al.register_operator
class CopyGroupNodeValuesToNodeGroup(al.Operator):

    al_asserts = [
        al.OperatorAssert(lambda c: isinstance(c.active_node, bt.ShaderNodeGroup), "Active node is node group", strict=False)
    ]

    def run(self, context: bt.Context):
        copy_group_node_vaues_to_node_group(context.active_node)
