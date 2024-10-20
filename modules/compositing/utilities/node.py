import bpy


def set_use_nodes():
    scene = bpy.context.scene
    if not scene.use_nodes:
        scene.use_nodes = True


def get_nodes(node_filter=None):
    set_use_nodes()
    scene = bpy.context.scene
    node_filter = node_filter or []
    all_compositing_nodes = scene.node_tree.nodes
    if not node_filter:
        return [node for node in all_compositing_nodes]
    compositing_nodes = []
    for node in all_compositing_nodes:
        for node_type in node_filter:
            if node.type == node_type:
                compositing_nodes.append(node)
                break
    return compositing_nodes


def get_selected_nodes(node_filter=None):
    set_use_nodes()
    node_filter = node_filter or []
    return [node for node in get_nodes(node_filter=node_filter) if node.select]

