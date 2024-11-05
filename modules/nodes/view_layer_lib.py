from modules.nodes import scene_lib


def get_view_layers(scene=None):
    current_scene = scene or scene_lib.get_current_scene()
    return current_scene.view_layers


def get_or_create_view_layer(name: str):
    scene = scene_lib.get_current_scene()
    view_layers =  get_view_layers(scene)
    view_layer = [view_layer for view_layer in view_layers if view_layer.name == name]
    view_layer = view_layer[0] if view_layer else scene.view_layers.new(name=name)
    return view_layer
