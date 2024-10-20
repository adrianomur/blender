import bpy
import os
import sys


for arg in sys.argv:
    if arg.startswith("save_file:"):
        save_file = arg[10:]
    if arg.startswith("obname:"):
        new_ob_name = arg[7:]
    if arg.startswith("filepath:"):
        filepath = arg[9:]

for ob in bpy.data.objects:
    bpy.data.objects.remove(ob)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

innerpath = 'Object'

bpy.ops.wm.append(
    filepath=os.path.join(filepath, innerpath, new_ob_name),
    directory=os.path.join(filepath, innerpath),
    filename=new_ob_name
    )

bpy.ops.wm.save_as_mainfile(filepath = save_file)