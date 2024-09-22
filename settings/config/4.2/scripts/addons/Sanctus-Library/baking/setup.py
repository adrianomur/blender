from ..auto_load.common import *
from . import utils

class BakeSetup:

    @property
    def node_tree(self):
        return self.material.node_tree
    
    @property
    def nodes(self):
        return self.material.node_tree.nodes

    def __init__(self, material: bt.Material, image: bt.Image, bake_socket: Optional[bt.NodeSocket] = None):
        self.temp_nodes: list[bt.Node] = []
        self.material = material
        self.image = image
        self.bake_socket = bake_socket
        self.output_socket = utils.get_shader_output_socket(self.node_tree)
        
        self.former_active_node = self.nodes.active
        self.former_connected_socket = None
        if len(self.output_socket.links) > 0:
            self.former_connected_socket: bt.NodeSocket = self.output_socket.links[0].from_socket

        image_node: bt.ShaderNodeTexImage = self.nodes.new('ShaderNodeTexImage') #change in nt
        self.image_node = image_node
        image_node.image = image
        self.nodes.active = image_node #change in nt

        if self.bake_socket is not None:
            self.link_to_material(self.bake_socket) #change in nt

    def link_to_material(self, socket: bt.NodeSocket):
        self.node_tree.links.new(socket, self.output_socket)

    def set_image(self, image: bt.Image):
        self.image = image
        self.image_node.image = image

    def register_node(self, node: bt.Node):
        self.temp_nodes.append(node)

    def register_and_connect_node(self, node: bt.Node, output_socket: Optional[bt.NodeSocket] = None):
        if output_socket is None:
            output_socket = node.outputs[0]
        self.register_node(node)
        self.link_to_material(output_socket)

    def connect_default_value(self, value: Union[float, tuple[float, float, float]]):
        rgb_value = value
        if isinstance(value, float):
            rgb_value = (value, value, value)
            
        node: bt.ShaderNodeRGB = self.nodes.new('ShaderNodeRGB')
        output: bt.NodeSocketColor = node.outputs[0]
        output.default_value = (rgb_value[0], rgb_value[1], rgb_value[2], 0)
        
        self.register_and_connect_node(node, output)

    def clean_up(self):
        for n in self.temp_nodes + [self.image_node]:
            self.nodes.remove(n)
        self.nodes.active = self.former_active_node
        self.node_tree.links.new(self.former_connected_socket, self.output_socket)
