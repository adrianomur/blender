import bpy

from modules.nodes.constants import RENDER_LAYER_SUFFIX


def get_scenes():
    return bpy.data.scenes


def get_current_scene():
    return bpy.context.scene


def get_collections(selected: bool = False):
    collections = [collection for collection in bpy.data.collections]
    if selected:
        return [collection for collection in collections if collection.select]
    return collections


def get_render_layer_collections():
    return [collection for collection in get_collections() if collection.name.startswith(RENDER_LAYER_SUFFIX)]
