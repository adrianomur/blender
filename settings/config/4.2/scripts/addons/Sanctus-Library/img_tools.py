import bpy
import threading
import time
import bpy.types as bt
import numpy as np
from numpy import ndarray
from pathlib import Path

from . import image_processing as ip


BLENDER_PREVIEW_SIZE: tuple[int, int] = (128, 128)

def make_icon_favorite(base_icon: bt.ImagePreview, star_icon: bt.ImagePreview):

    star_image = ip.get_image_from_preview(star_icon)
    base_image = ip.get_image_from_preview(base_icon)

    if ip.bs(base_image) != ip.bs(star_image):
        base_image = ip.square_image(base_image)
        base_image = ip.resize_image(base_image, ip.bs(star_image), bilinear=False)
    
    new_image = ip.overlay_image(base_image, star_image)
    ip.set_preview_image(base_icon, new_image)

def ensure_previews():
    bpy.ops.wm.previews_clear('EXEC_DEFAULT', id_type={'MATERIAL'})
    bpy.ops.wm.previews_ensure('EXEC_DEFAULT')


def capture_material_preview(mat: bt.Material) -> ndarray:
    ensure_previews()
    pixels: np.ndarray = np.zeros(len(mat.preview_ensure().image_pixels_float), dtype='float32')
    mat.preview_ensure().image_pixels_float.foreach_get(pixels)

    return pixels.reshape([*BLENDER_PREVIEW_SIZE, 4])


def save_pixels_as_image(pixels: ndarray, file: Path):
    temp_image = bpy.data.images.new('.temp_sanctus_preview_image', width=pixels.shape[1], height=pixels.shape[0], alpha=True)
    temp_image.pixels.foreach_set(pixels.flatten())
    temp_image.pixels.update()
    temp_image.update()
    temp_image.filepath_raw = str(file)
    temp_image.file_format = 'PNG'
    temp_image.save()
    bpy.data.images.remove(temp_image)


def convert_linear_to_srgb(image: bt.Image) -> None:
    buffer = ip.read_image(image)
    ip.set_image(image, ip.linear_to_srgb(buffer))
    image.pixels.update()

def convert_srgb_to_linear(image: bt.Image) -> None:
    buffer = ip.read_image(image)
    ip.set_image(image, ip.srgb_to_linear(buffer))
    image.pixels.update()

def un_premul_alpha(image: bt.Image):
    buffer = ip.read_image(image)
    buffer = ip.divide_by_alpha(buffer)
    ip.set_image(image, buffer)
    image.pixels.update()

def replace_image(old: bt.Image, new: bt.Image):
    old_name = old.name
    old.user_remap(new)
    bpy.data.images.remove(old)
    new.name = old_name
