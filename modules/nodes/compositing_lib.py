import bpy
from modules.nodes import scene_lib


def set_use_nodes():
    current_scene = scene_lib.get_current_scene()
    if not current_scene.use_nodes:
        current_scene.use_nodes = True


def get_nodes(node_filter=None, selected: bool = False):
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
    return compositing_nodes
