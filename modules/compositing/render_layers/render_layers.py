import bpy
from modules.nodes import scene_lib
from modules.nodes import compositing_lib
from modules.nodes import render_layer_lib
from modules.nodes import node_lib


def create_output_node(render_layer):
    tree = bpy.context.scene.node_tree
    output_file_node = tree.nodes.new('CompositorNodeOutputFile')
    output_file_node.location.x = render_layer.location.x + 500
    output_file_node.location.y = render_layer.location.y
    output_file_node.label = f'output_{render_layer.layer}'
    output_file_node.base_path = f'///{render_layer.layer}/'
    output_file_node.width = 300

    # connect Render Layer node to output
    index = 0
    for output in render_layer.outputs:
        if output.is_unavailable:
            continue
        if output.name not in ['Image']:
            output_file_node.file_slots.new(name=output.name)
        tree.links.new(output, output_file_node.inputs[index])
        index += 1
    return output_file_node


def create_render_layer_node(name: str, render_layer_name: str = None):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_render_layer_node('render-layer-node-name', 'render layer to select')
    """
    tree = bpy.context.scene.node_tree
    render_layer_node = tree.nodes.new('CompositorNodeRLayers')
    render_layer_node.label = name
    render_layers_names = [node.name for node in render_layer_lib.get_render_layers()]
    if render_layer_name and render_layer_name in render_layers_names:
        render_layer_node.layer = render_layer_name
    return render_layer_node


def create_outputs_from_render_layers(selected: bool = True):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_outputs_on_render_layers()
    """
    render_layer_nodes = compositing_lib.get_nodes(['R_LAYERS'], selected=selected)
    for render_layer in render_layer_nodes:
        create_output_node(render_layer)

@node_lib.align_nodes
def create_render_layers_from_collections():
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_render_layers_from_collections()
    """
    current_scene = scene_lib.get_current_scene()
    current_render_layers =  render_layer_lib.get_render_layers(current_scene)
    render_layer_collections = scene_lib.get_render_layer_collections()

    nodes = []
    for collection in render_layer_collections:

        selected_render_layer_node = None
        for render_layer in current_render_layers:
            if render_layer.name == collection.name:
                selected_render_layer_node = render_layer

        selected_render_layer_node = selected_render_layer_node or current_scene.view_layers.new(name=collection.name)
        for layer_collection in selected_render_layer_node.layer_collection.children:
            layer_collection.exclude = not (collection.name == layer_collection.name)

        selected_render_layer_node = create_render_layer_node(f'render_layer_{selected_render_layer_node.name}', selected_render_layer_node.name)
        output_node = create_output_node(selected_render_layer_node)
        nodes.append((selected_render_layer_node, output_node))
    return nodes
