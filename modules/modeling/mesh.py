import bpy
import bmesh

obj_name = 'my_shape'

mesh_data = bpy.data.meshes.new('my_data')

mesh_obj = bpy.data.objects.new(obj_name, mesh_data)

bpy.context.scene.collection.objects.link(mesh_obj)

my_bmesh = bmesh.new()

my_bmesh.to_mesh(mesh_data)
mesh_data.update()

my_bmesh.free()