import bpy
import sys
import os

## Functions

def material_benchmark_scene(filepath,mat_list,mat_name,append_method = 2):

    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    bpy.ops.object.shade_smooth()

    for mat_name in mat_list:
        if mat_name:
            if append_method == 1:

                innerpath = 'Material'

                bpy.ops.wm.append(
                    filepath=os.path.join(filepath, innerpath, mat_name),
                    directory=os.path.join(filepath, innerpath),
                    filename=mat_name
                    )

            if append_method == 2:
                try: 
                    material = mat_name
                    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                        assert(material in data_from.materials)
                        if material == mat_name:                     
                            data_to.materials = [mat_name]
                            material = data_to.materials[0]
                except:
                    continue

            # Applying Material

            if bpy.data.materials.get(mat_name):

                bpy.ops.material.new()
                ob = bpy.context.active_object  
                mat = bpy.data.materials[mat_name]
                bpy.context.active_object.active_material = mat
                bpy.ops.object.material_slot_add()

            else:
                continue

def obj_benchmark_scene(filepath,mat_list,mat_name):

    for mat_name in mat_list:
        if mat_name:
            innerpath = 'Object'

            bpy.ops.wm.append(
                filepath=os.path.join(filepath, innerpath, mat_name),
                directory=os.path.join(filepath, innerpath),
                filename=mat_name
                )

    for i in bpy.data.objects:
        i.location = (0,0,0)

def render_previews(save_preview=False): 

    bpy.context.scene.camera = bpy.data.objects["Camera"]

    if save_preview:
        custom_out = "C:\\Users\\T-Gamer\\Desktop\\temp6\\matbnech\\" + mat_name + ".png"
        bpy.context.scene.render.filepath = custom_out
        bpy.ops.render.render(write_still = 1)
        #bpy.ops.image.save_as(save_as_render=True, copy=True, filepath= custom_out, relative_path=True, show_multiview=False, use_multiview=False)
    else:
        bpy.ops.render.render()

def scene_pre_setup():

    bpy.context.scene.render.engine = 'CYCLES'

    # Settings

    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.cycles.film_transparent_glass = True

    # Removing Everything

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

def add_lights(scene_lights=False):

    if scene_lights:

        bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(4.11425, 4.69774, 1.78078))
        bpy.context.object.data.energy = 2500
        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(3.02968, -3.08888, 5.09294),rotation=(0,0.514181, 0.624079))
        bpy.context.object.scale[0] = 4.89
        bpy.context.object.scale[1] = 2.4
        bpy.context.object.scale[1] = 2.41
        bpy.context.object.data.energy = 400
        color_value = 0.017
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (color_value, color_value, color_value, 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 3

def camera_setup(preview_mode = False,preview_type = 'mat'):

    if preview_mode:
        
        bpy.context.scene.render.resolution_y = 500
        bpy.context.scene.render.resolution_x = 500
        bpy.context.scene.cycles.samples = 50
        
        if preview_type == 'mat':
            bpy.ops.object.camera_add(location=(0.00179, 3.3, 0), rotation=(1.570796, 0, 3.141641))
        if preview_type == 'obj':
            bpy.ops.object.camera_add(location=(0,8, 0), rotation=(1.570796, 0, 3.141641))
    
    else:

        bpy.context.scene.render.resolution_y = 4
        bpy.context.scene.render.resolution_x = 4
        bpy.context.scene.cycles.samples = 1

        bpy.ops.object.camera_add(location=(0.00179, 3.3, 0), rotation=(1.570796, 0, 3.141641))

    
## Getting Args

for arg in sys.argv:
    if arg.startswith("blendfile:"):
        filepath = arg[10:]
    if arg.startswith("matname:"):
        mat_name = arg[8:]
    if arg.startswith("method:"):
        pre_method = arg[7:]

## Getting Mat List
mat_list =  list(mat_name.split("--#-##--#---##-#--"))

scene_pre_setup() #scene pre setup

if pre_method == 'mat':
    material_benchmark_scene(filepath,mat_list,mat_name,append_method = 1) # material benchnark
if pre_method == 'obj':
    obj_benchmark_scene(filepath,mat_list,mat_name)

add_lights(scene_lights=False) #Add lights
camera_setup(preview_mode = False,preview_type = pre_method) # Camera Setup
render_previews(save_preview=False) # Rendering Previews

#bpy.ops.wm.save_mainfile() # Saving file

















