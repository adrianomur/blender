
from modules.nodes.scene_lib import get_current_scene


def get_render_layers(scene=None):
    current_scene = scene or get_current_scene()
    return current_scene.view_layers