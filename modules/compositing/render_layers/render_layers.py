import os
import bpy
from numpy.exceptions import VisibleDeprecationWarning

from modules.nodes import scene_lib
from modules.nodes import compositing_lib
from modules.nodes import render_layer_lib
from modules.nodes import node_lib
from modules.nodes.scene_lib import get_node_tree

from modules.nodes.constants import RENDER_FOLDER
from modules.nodes.constants import VIEW_LAYER_COLLECTION_PREFIX
from modules.nodes.constants import LIGHT_VIEW_LAYER_COLLECTION_PREFIX


def create_output_node_from_render_layer(render_layer):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_output_node('render-layer-node-name')
    """
    tree = get_node_tree()
    output_file_node_name = render_layer.layer
    output_file_layer_slots = [output.name for output in render_layer.outputs if not output.is_unavailable]
    output_file_base_path = os.path.join(RENDER_FOLDER, output_file_node_name)
    output_file_node = compositing_lib.get_or_create_output_file_node(name=output_file_node_name,
                                                                      base_path=f'///{output_file_base_path}/',
                                                                      layer_slots=output_file_layer_slots)
    output_file_node.location.x = render_layer.location.x + 500
    output_file_node.location.y = render_layer.location.y

    for output_plug in render_layer.outputs:
        for index, input_plug in enumerate(output_file_node.file_slots):
            if output_plug.name == input_plug.path:
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


def get_or_create_view_layer(view_layer_name):
    scene = scene_lib.get_current_scene()
    view_layers =  render_layer_lib.get_view_layers(scene)
    view_layer = [view_layer for view_layer in view_layers if view_layer.name == view_layer_name]
    return view_layer[0] if view_layer else scene.view_layers.new(name=view_layer_name)


def create_view_layer_and_render_layer_node(name):
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_render_layers_setup()
    """
    view_layer = get_or_create_view_layer(name)
    render_layer_node = compositing_lib.get_or_create_render_layer_node(name=name, render_layer_name=name)
    return view_layer, render_layer_node


@node_lib.align_nodes
def create_view_layers_from_collections():
    """
    from importlib import reload
    import modules.compositing.render_layers.render_layers as render_layers
    reload(render_layers)
    render_layers.create_view_layers_from_collections()
    """
    view_layer_collections = scene_lib.get_view_layers_from_collections()
    light_view_layer_collections = scene_lib.get_light_view_layers_from_collections()
    non_view_layer_collections = [collection for collection in scene_lib.get_collections() if collection not in (view_layer_collections + light_view_layer_collections)]

    nodes = []
    for view_layer_collection in view_layer_collections:
        view_layer_collection_name = view_layer_collection.name.lstrip(VIEW_LAYER_COLLECTION_PREFIX)
        view_layer, render_layer_node = create_view_layer_and_render_layer_node(view_layer_collection_name)

        collection_names = [collection.name for collection in non_view_layer_collections + [view_layer_collection]]
        scene_lib.enable_exclude_only_collections(view_layer, collection_names=collection_names)

        output_node = create_output_node_from_render_layer(render_layer_node)
        nodes.append((render_layer_node, output_node))

        frame_nodes = []
        frame_nodes.extend((render_layer_node, output_node))

        for light_view_layer_collection in light_view_layer_collections:
            light_view_layer_collection_name = light_view_layer_collection.name.lstrip(LIGHT_VIEW_LAYER_COLLECTION_PREFIX)
            view_layer, render_layer_light_setup_node = create_view_layer_and_render_layer_node(f'{view_layer_collection_name}_{light_view_layer_collection_name}')

            collection_names = [collection.name for collection in non_view_layer_collections + [view_layer_collection, light_view_layer_collection]]
            scene_lib.enable_exclude_only_collections(view_layer, collection_names=collection_names)
            scene_lib.enable_indirect_only_collections(view_layer, collection_names=[view_layer_collection.name])

            light_setup_output_node = create_output_node_from_render_layer(render_layer_light_setup_node)

            nodes.append((render_layer_light_setup_node, light_setup_output_node))
            frame_nodes.extend((render_layer_light_setup_node, light_setup_output_node))

        compositing_lib.create_frame(view_layer_collection_name, frame_nodes)

    return nodes
