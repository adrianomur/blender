import bpy

from modules.nodes.constants import VIEW_LAYER_COLLECTION_PREFIX
from modules.nodes.constants import LIGHT_VIEW_LAYER_COLLECTION_PREFIX


def get_scenes():
    return bpy.data.scenes


def get_current_scene():
    return bpy.context.scene


def get_node_tree():
    return get_current_scene().node_tree


def get_collections(selected: bool = False):
    collections = [collection for collection in bpy.data.collections]
    if selected:
        return [collection for collection in collections if collection.select]
    return collections


def enable_exclude_only_collections(view_layer, collection_names):
    for collection in view_layer.layer_collection.children:
        collection.exclude = collection.name not in collection_names


def enable_indirect_only_collections(view_layer, collection_names):
    for collection in view_layer.layer_collection.children:
        collection.indirect_only = collection.name not in collection_names


def get_view_layers_from_collections():
    return [collection for collection in get_collections() if collection.name.startswith(VIEW_LAYER_COLLECTION_PREFIX)]


def get_light_view_layers_from_collections():
    return [collection for collection in get_collections() if collection.name.startswith(LIGHT_VIEW_LAYER_COLLECTION_PREFIX)]
