import bpy
from modules.nodes import scene_lib


def get_view_layers(scene=None):
    current_scene = scene or scene_lib.get_current_scene()
    return current_scene.view_layers


def get_current_view_layer():
    return bpy.context.view_layer


def get_passes(layer):
    pass_attributes = [attr for attr in dir(layer) if attr.startswith("use_pass_")]
    return {pass_attr: getattr(layer, pass_attr) for pass_attr in pass_attributes}


def get_or_create_view_layer(name: str, copy_settings=True):
    scene = scene_lib.get_current_scene()
    view_layers =  get_view_layers(scene)
    view_layer = [view_layer for view_layer in view_layers if view_layer.name == name]
    view_layer = view_layer[0] if view_layer else scene.view_layers.new(name=name)
    if copy_settings:
        current_view_layer = get_current_view_layer()
        passes = get_passes(current_view_layer)
        for _pass in passes:
            print(view_layer, _pass, passes[_pass])
            setattr(view_layer, _pass, passes[_pass])
    return view_layer
