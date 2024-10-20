import bpy
from bpy.types import Object, RenderSettings, ViewLayer
from mathutils import Vector


def project_3d_point(
    view_layer: ViewLayer,
    camera: Object,
    point: Vector,
    render: RenderSettings,
) -> Vector:
    """Project a 3D point into 2D pixel coordinates"""

    modelview_matrix = camera.matrix_world.inverted()
    projection_matrix = camera.calc_matrix_camera(
        view_layer.depsgraph,
        x=render.resolution_x,
        y=render.resolution_y,
        scale_x=render.pixel_aspect_x,
        scale_y=render.pixel_aspect_y,
    )

    p1 = (
        projection_matrix
        @ modelview_matrix  # type:ignore
        @ Vector((point.x, point.y, point.z, 1))
    )
    p2 = Vector(((p1.x / p1.w, p1.y / p1.w)))

    return p2


def check_if_object_is_in_camera_view(
    view_layer: ViewLayer, render: RenderSettings, camera: Object, obj: Object
) -> bool:
    """Check if an object is in the camera view"""

    for v in obj.data.vertices:
        p = obj.matrix_world @ v.co
        p2 = project_3d_point(view_layer, camera, p, render)
        if -1 <= p2.x <= 1 and -1 <= p2.y <= 1:
            return True

    return False


def main():

    camera = bpy.data.objects["Camera"]  # or bpy.context.active_object
    render = bpy.context.scene.render
    view_layer = bpy.context.view_layer

    # hides if not in camera view
    for obj in bpy.data.objects:
        if not obj.type == "MESH":
            continue

        obj.hide_set(True)
        obj.hide_render = True

        in_camera_view = check_if_object_is_in_camera_view(
            view_layer, render, camera, obj
        )

        if in_camera_view:
            obj.hide_set(False)
            obj.hide_render = False


main()
