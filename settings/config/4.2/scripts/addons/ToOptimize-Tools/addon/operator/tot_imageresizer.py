import os
from collections import OrderedDict
from os import listdir
from os.path import isfile, join

import bpy

from ..utility.addon import get_prefs
from ..utility.constants import constant_ob_types
from ..utility.functions import (
    auto_purge,
    find_in_group,
    get_duplicate_file_name,
    get_materials_of_image,
    get_resolution,
    select_objects_materials,
)


class TOT_OP_UpdateimageList(bpy.types.Operator):
    """Update Image List"""

    bl_idname = "tot.updateimagelist"
    bl_label = "Update Image List"
    bl_options = {"REGISTER", "UNDO"}

    after_clean: bpy.props.BoolProperty(default=False)

    def execute(self, context):

        scn = context.scene.tot_props
        prefs = get_prefs()

        image_list = scn.image_list

        if not self.after_clean:
            scn.is_clean = False  # Clean check
        else:
            scn.is_clean = True

        image_data_method = scn.selected_image_data_method

        if image_data_method == "d1":
            image_data = bpy.data.images
        if image_data_method == "d2":

            obj = context.active_object

            if not obj:
                self.report({"ERROR"}, "No Objects Selected")
                return {"CANCELLED"}

            if not obj.type in constant_ob_types:
                self.report({"ERROR"}, "Select a valid object")
                return {"CANCELLED"}

            mat = obj.active_material

            if mat:
                if mat.use_nodes:
                    image_data = find_in_group(mat, 2)
            else:
                self.report({"ERROR"}, "No Active Material")
                return {"CANCELLED"}

        if image_data_method == "d3":

            image_data = []

            objs = context.selected_objects

            for ob in objs:
                if ob.type in constant_ob_types:
                    if ob.data.materials:
                        for mat in ob.data.materials:
                            if mat:
                                if mat.use_nodes:
                                    image_data += find_in_group(mat, 2)

        image_list.clear()
        image_dict = {}
        true_image_dict = {}

        for i in image_data:

            if not prefs.show_link_images:
                if i.library:
                    continue

            if not prefs.show_packed_images:
                if i.packed_file:
                    continue

            # if i.filepath.startswith('//'):
            #    image_path = (os.path.abspath(bpy.path.abspath(i.filepath)))

            image_path = ""
            if i.filepath:

                image_path = os.path.abspath(
                    bpy.path.abspath(i.filepath, library=i.library)
                )

            if os.path.exists(image_path):

                img_size = round(os.path.getsize(image_path) / 1000000, 6)

                # For fake image data
                image_dict[i.name] = img_size

                # For true image data
                image_name = os.path.basename(image_path)

                if not i.filepath in true_image_dict:
                    true_image_dict[i.filepath] = [img_size, image_name]

            else:
                if i.library:
                    image_dict[i.name] = 0
                    image_name = i.name

                if i.packed_file:
                    image_dict[i.name] = 0
                    image_name = i.name

                # image_dict[i.name] = 0

        ### Get total Size

        total_image_size = 0
        for i in image_dict:
            total_image_size += image_dict[i]

        ### Get true total

        true_total_image_size = 0
        for i in true_image_dict:
            true_total_image_size += true_image_dict[i][0]

        ### Reordering

        true_image_dict = {
            k: v
            for k, v in sorted(
                true_image_dict.items(), key=lambda item: item[1], reverse=True
            )
        }
        image_dict = {
            k: v
            for k, v in sorted(
                image_dict.items(), key=lambda item: item[1], reverse=True
            )
        }

        if (
            scn.image_data_method == "s2"
        ):  ######## Not used, only for true list

            for i in true_image_dict:
                new_img = image_list.add()
                new_img.tot_image_name = true_image_dict[i][1]
                new_img.image_size = "{:.2f}".format(true_image_dict[i][0])
                new_img.image_filepath = i

        if scn.image_data_method == "s1":

            for i in image_dict:

                new_img = image_list.add()
                new_img.tot_image_name = i
                new_img.image_size = "{:.2f}".format(image_dict[i])

                ## Getting Packed information
                img_data = bpy.data.images.get(i)

                if img_data:
                    if img_data.packed_file:
                        if not image_dict[i]:
                            new_img.image_size = "-"

                        new_img.packed_img = 1

                    if img_data.library:
                        if not image_dict[i]:
                            new_img.image_size = "-"
                        new_img.packed_img = 2

        scn.total_image_memory = "{:.2f}".format(total_image_size)
        scn.true_image_memory_usage = "{:.2f}".format(true_total_image_size)
        scn.r_total_images = len(image_dict)
        scn.r_true_total_images = len(true_image_dict)
        scn.tog_select_all = True

        return {"FINISHED"}


class TOT_OP_ResizeImages(bpy.types.Operator):
    """Resize Selected Images"""

    bl_idname = "tot.renderimagelist"
    bl_label = "Resize Images"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        scn = context.scene.tot_props
        selected_images = len(
            [i for i in scn.image_list if i.image_selected == True]
        )

        if selected_images and scn.select_images_to:
            return True
        else:
            return False

    def execute(self, context):

        if not bpy.data.is_saved:
            self.report({"ERROR"}, "Save this file first!")
            return {"CANCELLED"}

        scn = context.scene.tot_props
        image_list = scn.image_list

        prefs = get_prefs()

        if prefs.im_auto_save:
            bpy.ops.wm.save_mainfile()

        if prefs.auto_console:
            bpy.ops.wm.console_toggle()

        # if prefs.clearimg_beforeresize:
        #    bpy.ops.tot.clearduplicateimage(update = False)

        ### Getting Final Dict

        if scn.use_same_directory:
            final_path = (
                bpy.path.abspath(bpy.path.abspath("//"))
                + "\\"
                + "Textures"
                + "\\"
            )
        else:
            final_path = bpy.path.abspath(scn.custom_output_path)

            if not os.path.exists(final_path):
                self.report({"ERROR"}, "Select a valid folder")
                return {"CANCELLED"}

        if not os.path.exists(final_path):
            os.mkdir(final_path)

        filepath = final_path

        ### Resizing Start

        default = bpy.context.area.ui_type
        bpy.context.area.ui_type = "IMAGE_EDITOR"

        print()
        print(
            "--------------------------------RESIZING PROCESS STARTED--------------------------------"
        )
        print()

        for img in image_list:

            if img.image_selected:

                # image_filepath = filepath + '\\' + img.tot_image_name
                img_data = bpy.data.images.get(img.tot_image_name)

                if img_data:
                    pass
                else:
                    print(f"> Image data not found: {img.tot_image_name}")
                    continue

                try:
                    if img_data.size[0]:
                        pass
                    else:
                        print(f"> Invalid image file: {img.tot_image_name}")
                        continue
                except:
                    print(
                        f"> Invalid image file - Error: {img.tot_image_name}"
                    )
                    continue

                if os.path.exists(
                    bpy.path.abspath(
                        img_data.filepath, library=img_data.library
                    )
                ):
                    pass
                else:
                    print(f"> Filepath not found: {img.tot_image_name}")
                    continue

                ######### Image Pass, resizing start

                print(f"Resizing: {img_data.name}")

                img_filepath = bpy.path.abspath(img_data.filepath)

                img_filepath_2, img_extension = os.path.splitext(img_filepath)
                img_base_name = os.path.basename(img_filepath_2)
                img_true_name = os.path.basename(img_filepath)

                # Duplicate if necessary

                if scn.duplicate_images:
                    true_name_final = get_duplicate_file_name(
                        filepath, img_true_name, img_base_name, img_extension
                    )
                else:
                    true_name_final = img_true_name

                # Get resize size

                resize_size = scn.resize_size

                if resize_size == "c":
                    resize_size = scn.custom_resize_size

                size_x, size_y = get_resolution(
                    img_data.size[0], img_data.size[1], int(resize_size)
                )

                image_filepath = filepath + true_name_final
                img_data.scale(size_x, size_y)
                img_data.save_render(filepath=image_filepath)

                if not img_data:
                    print(
                        f"> Error saving image, img data is empty: {img_data.name}"
                    )
                    continue

                bpy.context.area.spaces.active.image = img_data

                try:
                    bpy.ops.image.save_as(
                        save_as_render=False,
                        filepath=image_filepath,
                        relative_path=True,
                        show_multiview=False,
                        use_multiview=False,
                    )
                except Exception as e:  # pylint: disable=broad-except
                    print(e)
                    print(f"> Exception when saving image: {img_data.name}")

        bpy.context.area.ui_type = default

        print()
        print(
            "--------------------------------RESIZING PROCESS FINISHED--------------------------------"
        )
        print()

        if prefs.auto_console:
            bpy.ops.wm.console_toggle()

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=380)

    def draw(self, context):
        scn = context.scene.tot_props
        prefs = get_prefs()

        layout = self.layout

        selected_images = len(
            [i for i in scn.image_list if i.image_selected == True]
        )

        # row=layout.row()
        # row.label(text=f'Selected Images: {str(selected_images)}')

        if selected_images == 1:
            image = "image"
        else:
            image = "images"

        box = layout.box()
        box.label(
            text=f"You are about to resize {str(selected_images)} {image}"
        )

        if not scn.is_clean:
            layout.label(
                text="Duplicate images was not cleaned!", icon="ERROR"
            )
        # layout.label(text="Don't forget to save a backup file before resizing any image in this file.",icon='ERROR')

        if prefs.im_auto_save:
            layout.label(
                text="Auto Save is Active! This file will be saved",
                icon="ERROR",
            )

        # row.prop(self, "prop2", text="Property B")


class TOT_OP_clearduplicateImages(bpy.types.Operator):
    """Clear Duplicate Images"""

    bl_idname = "tot.clearduplicateimage"
    bl_label = "Clear Duplicate Images"
    bl_options = {"REGISTER", "UNDO"}

    update: bpy.props.BoolProperty(default=True)

    def execute(self, context):

        props = context.scene.tot_props
        props.is_clean = True  # Clean check

        tex_nodes = []
        checked_paths = {}

        for i in bpy.data.materials:
            if i.use_nodes:
                tex_nodes += find_in_group(i, 1)

        for nod in reversed(tex_nodes):
            if nod.image.packed_file:
                continue
            if not nod.image.filepath in checked_paths:
                checked_paths[nod.image.filepath] = nod.image
            else:
                nod.image = checked_paths[nod.image.filepath]

        auto_purge()
        if self.update:
            bpy.ops.tot.updateimagelist(after_clean=True)

        return {"FINISHED"}


class TOT_OP_clearimagelist(bpy.types.Operator):
    """Clear all items in the Image List"""

    bl_idname = "tot.clearimagelist"
    bl_label = "Clear Image List"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        scn = context.scene.tot_props
        scn.image_list.clear()

        return {"FINISHED"}


class TOT_OP_Img_SelectAll(bpy.types.Operator):
    """Select/Deselect All images"""

    bl_idname = "tot.imglistselectall"
    bl_label = "Toggle Select All"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        scn = context.scene.tot_props

        if scn.tog_select_all:
            for img in scn.image_list:
                img.image_selected = True

            scn.tog_select_all = False

        else:
            for img in scn.image_list:
                img.image_selected = False

            scn.tog_select_all = True

        return {"FINISHED"}


class TOT_OP_Img_ImgsInformation(bpy.types.Operator):
    """Show Selected Image Information"""

    bl_idname = "tot.imginfo"
    bl_label = "Image Information"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=450)

    def draw(self, context):
        ## Getting Information
        layout = self.layout

        scn = context.scene.tot_props
        idx = scn.custom_index_image_list

        try:
            item = scn.image_list[idx]
        except IndexError:
            pass

        image_selected = bpy.data.images.get(item.tot_image_name)

        if image_selected:

            # filepath = bpy.path.abspath(image_selected.filepath)
            filepath = os.path.abspath(
                bpy.path.abspath(
                    image_selected.filepath, library=image_selected.library
                )
            )

            col = layout.column(align=True)

            box = col.box()
            box.label(text=f"Image Name:  {image_selected.name} ")
            box = col.box()
            box.label(
                text=f"Image Size:  {image_selected.size[0]} x {image_selected.size[1]} "
            )
            box = col.box()
            box.label(text=f"File Size:  {item.image_size} M")
            box = col.box()
            box.label(text=f"Original Name:  {os.path.basename(filepath)}")
            box = layout.box()

            row = box.row()
            row.label(text=f"Material List:", icon="MATERIAL")
            row.operator("tot.imgmatinfo", text="Show List")
            row = layout.row()
            row.label(text=f"Filepath:")
            box = layout.box()
            box.prop(image_selected, "filepath")

        else:
            box = layout.box()
            box.label(text="Image Not Found")


class TOT_OP_Img_MatsImgInformation(bpy.types.Operator):
    """Show all materials that uses this image"""

    bl_idname = "tot.imgmatinfo"
    bl_label = "Material List"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        ## Getting Information
        scn = context.scene.tot_props
        idx = scn.custom_index_image_list

        try:
            item = scn.image_list[idx]
        except IndexError:
            pass

        image_selected = bpy.data.images.get(item.tot_image_name)

        layout = self.layout

        if image_selected:

            materials_list = get_materials_of_image(image_selected.name)
            col_main = layout.column(align=True)

            if materials_list:

                for m in materials_list:

                    mat = bpy.data.materials.get(m)

                    if mat:
                        row = col_main.row(align=True)
                        col = row.column(align=True)
                        box = col.box()
                        box.label(text=f"{m}", icon_value=layout.icon(mat))
                        row_b = row.row(align=True)
                        row_b.scale_y = 1.5
                        row_b.scale_x = 1.2
                        row_b.operator(
                            "tot.selectimgmat",
                            text="",
                            icon="RESTRICT_SELECT_OFF",
                        ).mat_name = mat.name

            else:
                box = col_main.box()
                box.label(text="Image is not loaded in any material")


class TOT_OP_Img_MatsImgSelect(bpy.types.Operator):
    """Set Material as active, and you will be able to see it"""

    bl_idname = "tot.selectimgmat"
    bl_label = "Select Material"
    bl_options = {"REGISTER", "UNDO"}

    mat_name: bpy.props.StringProperty()

    def execute(self, context):

        mat_name = self.mat_name

        not_in_viewlayer = select_objects_materials(mat_name)

        if not_in_viewlayer:
            self.report({"WARNING"}, "Some objects are not in the view layer")
            return {"FINISHED"}
        else:
            return {"FINISHED"}


# box.label(text=f'{item.image_size} M')
