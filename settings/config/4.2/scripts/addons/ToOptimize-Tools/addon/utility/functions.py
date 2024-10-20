import bpy
import os
import copy
import subprocess

from os import listdir
from os.path import isfile, join

from .constants import link_folder_name,constant_ob_types

def update_function_col(self, context):

    if self.CA_Toggle:
        bpy.ops.tot.collectionanalyzer('INVOKE_DEFAULT')
        return
    else:
        bpy.ops.tot.cleancolors('INVOKE_DEFAULT')
        return

def update_function_scn(self, context):

    if self.AA_Toggle:
        bpy.ops.tot.r3dviewanalyzer('INVOKE_DEFAULT')
        return
    else:
        bpy.ops.tot.clean3dviewanalyzer('INVOKE_DEFAULT')
        return

def update_label(stringmode,objs,scn):

    if stringmode == 'list':


        if len(objs) == 1:
            scn.fv_label_top = str(len(objs)) + ' Object found'
        else:
            scn.fv_label_top = str(len(objs)) + ' Objects found'

        scn.fv_label = ', '.join([str(elem) for elem in objs]) 
        scn.fv_tofind = str(objs)
        scn.fv_stringmode = stringmode
    
    if stringmode == 'single':

        scn.fv_label_top = ''
        scn.fv_label = objs
        scn.fv_tofind = objs
        scn.fv_stringmode = stringmode

'''

def get_obj_col_tree(obj_name):

    ob = bpy.data.object.get(obj_name)
    ob_col = ob.users_collection

    cols_unhide = []

    for col in bpy.data.collections:
        if ob_col in col.children:
            cols_unhide.append(col)

            for c in col.children:
                cols_unhide.append(c)
    
    for total in cols_unhide:

'''

def get_verts_mod(ob):

    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = ob.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    mesh_len = len(mesh_from_eval.vertices)
    object_eval.to_mesh_clear()

    return mesh_len

def create_new_object_file(save_file,new_ob_name,filepath):       
   
    generator = os.path.dirname(os.path.realpath(__file__)) + '\\object_file.py'

    cmd = [
        bpy.app.binary_path,
        "--background",
        "--factory-startup",
        "--python", generator,
        "--",
        "save_file:" + save_file,
        "obname:" + new_ob_name,
        "filepath:" + filepath,
        ]

    p = subprocess.Popen(cmd, universal_newlines=True,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(p.stdout.readline,''):
        print(line.rstrip())
  
    return True
 
def link_object(ob,method=2):

    bpy.ops.wm.save_as_mainfile()

    scn = bpy.context.scene.tot_props

    filepath = bpy.path.abspath("//")

    link_path = filepath + link_folder_name + '\\'

    if not os.path.exists(link_path):
        filepath = os.mkdir(link_path)
    else:
        filepath = link_path
    
    if filepath:  
        filepath = str(filepath) + str(ob.name) + '.blend'
    else:
        return False
    
    if os.path.exists(filepath):
        os.remove(filepath)

    blend_path = bpy.data.filepath

    print(ob.name + '##############')

    if method == 1:
        create_new_object_file(filepath,ob.name,blend_path)
    if method == 2:
        with open(filepath, "w") as file: # create a new empty blend file
            file.write("")
    
        data_blocks = {obl for obl in bpy.data.objects if obl.name == ob.name}      # getting material from the actual blend data
        bpy.data.libraries.write(filepath, data_blocks, fake_user=True, compress=True)
    
    new_ob_name = copy.deepcopy(ob.name)
    bpy.data.objects.remove(ob)

    if not bpy.data.materials.get(new_ob_name):

        innerpath = 'Object'
        bpy.ops.wm.link(
            filepath=os.path.join(filepath, innerpath, new_ob_name),
            directory=os.path.join(filepath, innerpath),
            filename=new_ob_name
            )

        base_object = bpy.data.objects.get(new_ob_name) 

        if scn.el_make_local:
            base_object.make_local()
  
    return True

def unlink_object(ob,mesh_method=1,material_method=1):

    print('ue')
    bpy.ops.wm.save_as_mainfile()

    filepath = bpy.path.abspath("//") + link_folder_name 

    print(filepath)
    
    if os.path.exists(filepath):
        pass
    else:
        return False

    blend_files = [f[:-6] for f in listdir(filepath) if f.endswith('.blend')]
    print(blend_files)

    if ob.name in blend_files:

        new_ob_name = copy.deepcopy(ob.name)
        mesh = ob.data.vertices.data
        bpy.data.objects.remove(ob)

        if mesh_method == 1:
            old_mesh = bpy.data.meshes.get(mesh.name)
            bpy.data.meshes.remove(old_mesh)
        
        if mesh_method == 2:
            bpy.data.meshes.remove(mesh)

        filepath = filepath + '\\' + new_ob_name + '.blend'
        innerpath = 'Object'
        bpy.ops.wm.append(
            filepath=os.path.join(filepath, innerpath, new_ob_name),
            directory=os.path.join(filepath, innerpath),
            filename=new_ob_name
            )

        base_object = bpy.data.objects.get(new_ob_name)  
        base_object.data.vertices.data.make_local()
     
        if material_method == 1:
            for mat in base_object.material_slots:
                if mat.name:
                    old_mat = copy.deepcopy(mat.name)
                    link_mat = mat.material
                    bpy.data.materials.remove(link_mat)
                    mat.material = bpy.data.materials[old_mat]
        if material_method == 2:
            for mat in base_object.data.materials:
                mat.make_local()

def get_information(line):

    string = line
    #print(string)

    ### Get Time

    time_i = string.find('| Time:')

    get_time = ''
    for w in string[time_i + 7:]:
        if w == '|':
            break
        get_time += w

    ### Used Memory

    memory_i = string.find(', Peak:')

    get_memory = ''
    for w in string[memory_i + 7:]:
        if w == '|':
            break
        get_memory += w

    float_memory = ''
    for w in get_memory:
        if not w.isdigit() and not w == '.':
            break
        float_memory += w
    
    return get_time,float(float_memory)

def material_benchmarking(mat_name,self,method,library_path = ''):

    ## mat_name is for materials and objects 
    
    if library_path:
        blend_path = bpy.path.abspath(library_path)
    else:
        blend_path = bpy.path.abspath(bpy.data.filepath)
  
    generator = os.path.dirname(os.path.realpath(__file__)) + '\\preview_config.py'

    cmd = [
        bpy.app.binary_path,
        "--background",
        "--factory-startup",
        "--python", generator,
        "--",
        "blendfile:" + blend_path,
        "matname:" + mat_name,
        "method:" + method,
        ]

    p = subprocess.Popen(cmd, universal_newlines=True,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(p.stdout.readline,''):
        if '| Finished' in line:
            #print(line.rstrip())
            time_r,memory_r = get_information(line)
            
            if not '--#-##--#---##-#--' in mat_name:
                print(f'{mat_name} - Time:{time_r} Memory:{str(memory_r)}M ')

            return memory_r
   
def find_in_group(n,method,image_name_tf = None):

    texture_nodes = []

    if type(n) == bpy.types.Material:
        if n.use_nodes:
            pass
        else:
            return texture_nodes
    
    if not n:
        return texture_nodes
    
    if not n.node_tree:
        return texture_nodes
        
    for i in n.node_tree.nodes:
        if i.type == 'TEX_IMAGE':
            if i.image:
                if method == 0:
                    texture_nodes.append(bpy.path.abspath(i.image.filepath))
                if method == 1:
                    texture_nodes.append(i)
                if method == 2:
                    texture_nodes.append(i.image)
                if method == 3:                
                    if image_name_tf:
                        if i.image.name == image_name_tf:
                            texture_nodes.append(i.image)
        if i.type == 'GROUP':
            texture_nodes = texture_nodes + find_in_group(i,method,image_name_tf = image_name_tf)
        
    return texture_nodes

def get_size_textures(material):

    textures_path = find_in_group(material,0)
    image_dict = {}

    for n in textures_path:
        
        image_path = n
        if os.path.exists(image_path):
            image_size = os.path.getsize(image_path)
            image_name = os.path.basename(image_path)
            image_dict[image_name] = round((image_size / 1000000),3)
    return image_dict

def get_size_images(image):

    image_path = image.filepath
    image_size = round(os.path.getsize(image_path),3)

    return image_size

def get_duplicate_file_name(path,true_name,img_base_name,img_extension):

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    if true_name in onlyfiles:

        dup_num = 1

        while True: 

            dup_name = img_base_name + '_' + str(dup_num) + img_extension
            #print(dup_name)

            if dup_name in onlyfiles:
                dup_num +=1
                continue
            else:
                true_name = img_base_name + '_' + str(dup_num) + img_extension
                break

    return true_name

def get_proportion(x,y,final_res):

    #scn = bpy.context.scene.textconverter

    #if x > final_res or not scn.conv_high_values or scn.corvert_method == 's2': 

    if x > final_res: 

        proportion = x - final_res
        proportion_final = 1 - (proportion/x)

        final_x = round(x - proportion)
        final_y = round(y*proportion_final)
   
    else:
        final_x = x
        final_y = y
    
    return final_x,final_y

def get_resolution(x,y,final_res):

 
    if x > y:
        final_x, final_y = get_proportion(x,y,final_res)
    else:
        final_y, final_x = get_proportion(y,x,final_res)
        
    return int(final_x),int(final_y)
    
def auto_purge():

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

def get_materials_of_image(image_name_find):

    used_materials = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            mats = find_in_group(mat,3,image_name_tf = image_name_find) 
            if mats:
                used_materials.append(mat.name)
    
    return used_materials

def select_objects_materials(mat_name):

    bpy.ops.object.select_all(action='DESELECT')
    objs = bpy.data.objects

    not_in_viewlayer = False

    for ob in objs:
        if ob.type in constant_ob_types:
            for m in ob.data.materials:
                if m:
                    if m.name == mat_name:                      
                        try:
                            ob.select_set(True)
                            bpy.context.view_layer.objects.active = ob
                        except:
                            not_in_viewlayer = True

    ac_index = -1    
    if bpy.context.active_object:
        ob = bpy.context.active_object
        if ob.type in constant_ob_types:
            if ob.data.materials:
                for i in ob.material_slots:
                    ac_index += 1
                    if i.name == mat_name:
                        break
                    else:
                        continue

        ob.active_material_index = ac_index
  
    if not_in_viewlayer:
        return True
    else:
        return False

def get_mat_count():

    scn = bpy.context.scene.tot_props
    counted_mats = []

    if scn.select_mode == 's1':

        total_mats_ui = 0
        for i in bpy.data.objects:
            if i.type in constant_ob_types:
                for m in i.data.materials:
                    if m:
                        if not m.name in counted_mats:
                            counted_mats.append(m.name)
                            total_mats_ui += 1
    
    if scn.select_mode == 's2':
            
        total_mats_ui = 0
        for i in bpy.context.selected_objects:
            if i.type in constant_ob_types:
                for m in i.data.materials:
                    if m:
                        if not m.name in counted_mats:
                            counted_mats.append(m.name)
                            total_mats_ui += 1
    
    return total_mats_ui



   
    










