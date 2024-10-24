import bpy
from modules.nodes import scene_lib
from modules.nodes import render_layer_lib

from modules.nodes.constants import FILE_OUTPUT_PREFIX
from modules.nodes.constants import RENDER_LAYER_PREFIX
from modules.nodes.scene_lib import get_node_tree, get_current_scene


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


def get_or_create_output_file_node(name: str, base_path: str = None, layer_slots: list = None):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_output_file_node('node_name', '//base_path', ['foo1', 'foo2'])
    """
    layer_slots = layer_slots or []
    tree = get_node_tree()
    node_name = f'{FILE_OUTPUT_PREFIX}_{name}'
    output_file_node = get_nodes(node_filter=['OUTPUT_FILE'], name=node_name)
    output_file_node = output_file_node[0] if output_file_node else tree.nodes.new('CompositorNodeOutputFile')
    output_file_node.name = node_name
    output_file_node.label = name
    output_file_node.file_slots.clear()
    for layer_slot in layer_slots:
        output_file_node.file_slots.new(name=layer_slot)
    if base_path:
        output_file_node.base_path = base_path
    output_file_node.width = 300
    return output_file_node


def get_or_create_render_layer_node(name: str, render_layer_name: str = None):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_render_layer_node('render-layer-node-name', 'render layer to select')
    """
    tree = get_node_tree()
    node_name = f'{RENDER_LAYER_PREFIX}_{name}'
    render_layer_node = get_nodes(node_filter=['R_LAYERS'], name=node_name)
    render_layer_node = render_layer_node[0] if render_layer_node else tree.nodes.new('CompositorNodeRLayers')
    render_layer_node.name = node_name
    render_layer_node.label = name
    render_layers_names = [node.name for node in render_layer_lib.get_view_layers()]
    if render_layer_name and render_layer_name in render_layers_names:
        render_layer_node.layer = render_layer_name
    return render_layer_node


def get_or_create_input(output_node, input_name):
    for file_slot in output_node.file_slots:
        if file_slot.name == input_name:
            return file_slot
    return output_node.file_slots.new(name=input_name)


def create_frame(node_name, nodes):
    tree = get_node_tree()
    frame_node = tree.nodes.new(type="NodeFrame")
    frame_node.name = node_name
    frame_node.label = node_name
    for node in nodes:
        node.parent = frame_node
    return frame_node
