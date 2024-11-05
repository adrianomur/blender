import bpy
from modules.nodes import scene_lib
from modules.nodes import view_layer_lib

from modules.nodes.constants import NODE_TYPES
from modules.nodes.constants import FILE_OUTPUT_PREFIX
from modules.nodes.constants import RENDER_LAYER_PREFIX
from modules.nodes.constants import FRAME_PREFIX

from modules.nodes.scene_lib import get_node_tree


def set_use_nodes():
    current_scene = scene_lib.get_current_scene()
    if not current_scene.use_nodes:
        current_scene.use_nodes = True


def get_nodes(node_filter=None, name: str = None, selected: bool = False):
    set_use_nodes()
    current_scene = bpy.context.scene
    node_filter = node_filter or []
    node_tree_nodes = current_scene.node_tree.nodes
    compositing_nodes = []
    if node_filter:
        for node in node_tree_nodes:
            for node_type in node_filter:
                if node.type == node_type:
                    compositing_nodes.append(node)
                    break
    else:
        compositing_nodes = [node for node in node_tree_nodes]
    if selected:
        compositing_nodes = [node for node in compositing_nodes if node.select]
    if name:
        compositing_nodes = [node for node in compositing_nodes if node.name == name]
    return compositing_nodes


def get_or_create_node(node_name: str, node_type: str):
    tree = get_node_tree()
    nodes = get_nodes(node_filter=[node_type], name=node_name)
    node_type = NODE_TYPES.get(node_type)
    if not node_type:
        raise RuntimeError
    if nodes:
        return nodes[0]
    new_node = tree.nodes.new(node_type)
    new_node.name = node_name
    new_node.width = 300
    return new_node


def get_or_create_output_file_node(name: str,
                                   label: str,
                                   base_path: str = None,
                                   layer_slots: list = None,
                                   clear_slots=False):
    """
    from importlib import reload
    import modules.compositing.nodes import compositing_lib
    reload(compositing_lib)
    compositing_lib.create_output_file_node('node_name', '//base_path', ['foo1', 'foo2'])
    """
    layer_slots = layer_slots or []
    output_file_node = get_or_create_node(node_name=f'{FILE_OUTPUT_PREFIX}{name}', node_type='OUTPUT_FILE')
    output_file_node.label = label
    if clear_slots:
        output_file_node.file_slots.clear()
    for layer_slot in layer_slots:
        output_file_node.file_slots.new(name=layer_slot)
    if base_path:
        output_file_node.base_path = base_path
    return output_file_node


def get_or_create_render_layer_node(name: str,
                                    label: str,
                                    render_layer_name: str = None):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_render_layer_node('render-layer-node-name', 'render layer to select')
    """
    render_layer_node = get_or_create_node(node_name=f'{RENDER_LAYER_PREFIX}{name}', node_type='R_LAYERS')
    render_layer_node.label = label
    render_layers_names = [node.name for node in view_layer_lib.get_view_layers()]
    if render_layer_name and render_layer_name in render_layers_names:
        render_layer_node.layer = render_layer_name
    return render_layer_node


def get_or_create_frame(name: str,
                        label: str = None,
                        nodes: list = None):
    frame_node = get_or_create_node(node_name=f'{FRAME_PREFIX}_{name}', node_type='FRAME')
    frame_node.label = label
    for node in nodes:
        node.parent = frame_node
    return frame_node


def get_or_create_input(output_node, input_name):
    for index, file_slot in enumerate(output_node.file_slots):
        if file_slot.name == input_name:
            return file_slot
    return output_node.file_slots.new(name=input_name)


def get_size(node):
    return node.width, node.height


def get_position(node):
    return node.location.x, node.location.y
