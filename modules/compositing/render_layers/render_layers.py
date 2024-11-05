import os

from modules.nodes import compositing_lib
from modules.nodes import node_lib
from modules.nodes.constants import RENDER_FOLDER


def create_output_node_from_render_layer(render_layer, clear_slots=False):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_output_node('render-layer-node-name')
    """
    output_file_node_name = render_layer.layer
    output_file_layer_slots = [output.name for output in render_layer.outputs if not output.is_unavailable]

    output_file_base_path = os.path.join(RENDER_FOLDER, output_file_node_name)
    output_file_node = compositing_lib.get_or_create_output_file_node(name=output_file_node_name,
                                                                      label=output_file_node_name,
                                                                      base_path=f'///{output_file_base_path}.',
                                                                      layer_slots=output_file_layer_slots,
                                                                      clear_slots=clear_slots)
    output_file_node.location.x = render_layer.location.x + 500
    output_file_node.location.y = render_layer.location.y

    for output_plug in render_layer.outputs:
        for index, input_plug in enumerate(output_file_node.file_slots):
            output_plug_name = output_plug.name
            if output_plug_name == input_plug.path:
                tree.links.new(output_plug, output_file_node.inputs[index])
                break

    return output_file_node


@node_lib.align_nodes
def create_outputs_from_render_layers(selected: bool = True):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_outputs_on_render_layers()
    """
    render_layer_nodes = compositing_lib.get_nodes(['R_LAYERS'], selected=selected)
    for render_layer in render_layer_nodes:
        create_output_node_from_render_layer(render_layer)

