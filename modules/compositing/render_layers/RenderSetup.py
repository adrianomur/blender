from modules.nodes import scene_lib
from modules.nodes import view_layer_lib
from modules.nodes import compositing_lib
from modules.nodes.constants import VIEW_LAYER_COLLECTION_PREFIX
from modules.nodes.constants import LIGHT_VIEW_LAYER_COLLECTION_PREFIX
from modules.nodes.constants import SPACING_X, SPACING_Y
from modules.nodes.scene_lib import get_node_tree


def get_collections():
    view_layer_collections = scene_lib.get_view_layers_from_collections()
    light_view_layer_collections = scene_lib.get_light_view_layers_from_collections()
    other_collections = [collection for collection in scene_lib.get_collections() if collection not in (view_layer_collections + light_view_layer_collections)]
    return view_layer_collections, light_view_layer_collections, other_collections


class RenderItem:

    def __init__(self, name, collection, group):
        self.collection = collection
        self.name = name
        self.group = group
        self.view_layer = None
        self.render_layer = None
        self.build()
        self.plugs = self.parse_plugs()

    def build(self):
        self.view_layer = view_layer_lib.get_or_create_view_layer(name=self.name)
        self.render_layer = compositing_lib.get_or_create_render_layer_node(name=self.name,
                                                                            label=self.group.name,
                                                                            render_layer_name=self.name)

    def parse_plugs(self):
        outputs = [output for output in self.render_layer.outputs if not output.is_unavailable]
        return {f"{self.name}_{output.name.lower().replace(' ', '_')}": output for output in outputs}

    def enable_exclude_only_collections(self, collections):
        collections = collections.copy()
        _, _, other_collections = get_collections()
        collections.extend([collection for collection in other_collections + [self.collection]])
        collection_names = [collection.name for collection in collections]
        scene_lib.enable_exclude_only_collections(self.view_layer, collection_names=collection_names)

    def enable_indirect_only_collections(self, collections):
        collection_names = [collection.name for collection in collections]
        scene_lib.enable_indirect_only_collections(self.view_layer, collection_names=collection_names)

    def get_name(self, name):
        for prefix in [VIEW_LAYER_COLLECTION_PREFIX, LIGHT_VIEW_LAYER_COLLECTION_PREFIX]:
            if name.startswith(prefix):
                return name[len(prefix):]
        return name


class RenderLayer(RenderItem):

    def __init__(self, collection, group):
        name = self.get_name(collection.name)
        super().__init__(name, collection, group)
        self.enable_exclude_only_collections([self.collection])


class RenderLight(RenderItem):

    def __init__(self,
                 collection,
                 render_layer,
                 group,
                 exclude_only_collections: list = None,
                 indirect_only_collections: list = None):

        name = self.parse_name(collection, render_layer)
        super().__init__(name, collection, group)

        self.enable_exclude_only_collections(exclude_only_collections or [])
        self.enable_indirect_only_collections(indirect_only_collections or [])

    def parse_name(self, collection, render_layer):
        collection_name = self.get_name(collection.name)
        render_layer_name = render_layer.name
        return f'{render_layer_name}_{collection_name}'


class RenderGroup:

    def __init__(self, collection):
        self.collection = collection
        self.name = self.get_name(self.collection.name)
        self.render_items = []
        self.build()

        self.outputs = self.create_outputs()
        self.frame = self.create_frame()

    def get_name(self, name):
        for prefix in [VIEW_LAYER_COLLECTION_PREFIX, LIGHT_VIEW_LAYER_COLLECTION_PREFIX]:
            if name.startswith(prefix):
                return name[len(prefix):]
        return name

    def build(self):
        render_item = RenderLayer(collection=self.collection, group=self)
        self.render_items.append(render_item)

        light_view_layer_collections = scene_lib.get_light_view_layers_from_collections()
        for light_view_layer_collection in light_view_layer_collections:
            light_render_item = RenderLight(collection=light_view_layer_collection,
                                            render_layer=render_item,
                                            group=self,
                                            exclude_only_collections=[self.collection],
                                            indirect_only_collections=[self.collection])
            self.render_items.append(light_render_item)

    def create_outputs(self):
        plugs = []
        outputs = []
        for render_item in self.render_items:
            plugs.extend(render_item.plugs.keys())
        output_file_node = compositing_lib.get_or_create_output_file_node(name=self.collection.name,
                                                                          label=self.name,
                                                                          base_path=f'///{self.name}.',
                                                                          layer_slots=plugs,
                                                                          clear_slots=True)
        outputs.append(output_file_node)

        tree = get_node_tree()
        for output_socket in output_file_node.inputs:
            for render_item in self.render_items:
                render_socket = render_item.plugs.get(output_socket.name)
                if render_socket:
                    tree.links.new(output_socket, render_socket)

        return outputs

    def create_frame(self):
        for index, item in enumerate(self.render_items):
            item.render_layer.location.y = - index * SPACING_Y

        for index, item in enumerate(self.outputs):
            item.location.x = 500
            item.location.y = - index * SPACING_Y

        frame = compositing_lib.get_or_create_frame(name=self.name,
                                            label=self.name,
                                            nodes=[item.render_layer for item in self.render_items] + self.outputs)
        return frame


class RenderSetup:
    """
    from importlib import reload
    from modules.compositing.render_layers import RenderSetup
    reload(RenderSetup)
    render_setup = RenderSetup.RenderSetup()
    """
    def __init__(self):
        self.render_groups = []
        self.build()
        self.arrange_items()

    def build(self):
        view_layer_collections = scene_lib.get_view_layers_from_collections()
        for index, view_layer_collection in enumerate(view_layer_collections):
            render_group = RenderGroup(collection=view_layer_collection)
            self.render_groups.append(render_group)

    def arrange_items(self):
        previous_frame_size = (0, 0)
        previous_frame_position = (0, 0)
        for index, render_group in enumerate(self.render_groups):
            render_group.frame.location.x = previous_frame_size[0] + previous_frame_position[0] + 30
            previous_frame_size = compositing_lib.get_size(render_group.frame)
            previous_frame_position = compositing_lib.get_position(render_group.frame)
