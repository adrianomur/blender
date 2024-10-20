"""
import sys
import importlib
sys.path.append('/Users/adriano/dev/blender')
import compositing
importlib.reload(compositing)
from compositing.render_layers import render_layers
render_layers.create_outputs_on_selected()
"""
import bpy
from ..utilities import node


def create_outputs_on_selected():
    render_layer_nodes = node.get_selected_nodes(['R_LAYERS'])
    tree = bpy.context.scene.node_tree
    for render_layer in render_layer_nodes:
        
        # create new output node
        output_file_node = tree.nodes.new('CompositorNodeOutputFile')
        output_file_node.location.x = render_layer.location.x + 500
        output_file_node.location.y = render_layer.location.y
        output_file_node.label = render_layer.layer
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
