
from .. import auto_load as al
from ..auto_load.common import *

from .. import base_ops
from . import modals

from .. import meta_data as md
from .. import node_utils


@al.register_operator
class GNAddNew(base_ops.SanctusAssetImportOperator):
    bl_label = md.GeometryNodeAssetType.ADD_NEW.get_name()
    bl_description = md.GeometryNodeAssetType.ADD_NEW.get_description()
    asset_type = 'objects'
    use_reimport_prompt = False

    def run(self, context: bt.Context):
        obj = self.get_importer().get_asset(reimport=True)
        base_ops.link_and_select_object(context, obj)


@al.register_operator
class GNApplyMesh(base_ops.SanctusAssetImportOperator):
    bl_label = md.GeometryNodeAssetType.APPLY_MESH.get_name()
    bl_description = md.GeometryNodeAssetType.APPLY_MESH.get_description()
    asset_type = 'node_groups'
    use_reimport_prompt = False
    al_asserts: list[al.OperatorAssert] = [
        al.OperatorAssert(lambda c: c.active_object in c.selected_objects, 'Active object available and selected', strict=False),
        al.OperatorAssert(lambda c: c.object.type == 'MESH', 'Active objec type has to be "MESH"'),
    ]

    def run(self, context: bt.Context):
        nt: bt.GeometryNodeTree = self.get_importer().get_asset(self.reimport_asset())
        obj: bt.Object = context.object
        mod: bt.NodesModifier = obj.modifiers.new(nt.name, 'NODES')
        mod.node_group = nt

@al.register_operator
class GNApplyCurve(base_ops.SanctusAssetImportOperator):
    bl_label = md.GeometryNodeAssetType.APPLY_CURVE.get_name()
    bl_description = md.GeometryNodeAssetType.APPLY_CURVE.get_description()
    asset_type = 'node_groups'
    use_reimport_prompt = False
    al_asserts: list[al.OperatorAssert] = [
        al.OperatorAssert(lambda c: c.active_object in c.selected_objects, 'Active object available and selected', strict=False),
        al.OperatorAssert(lambda c: c.object.type == 'CURVE', 'Active objec type has to be "CURVE"'),
    ]

    def run(self, context: bt.Context):
        nt: bt.GeometryNodeTree = self.get_importer().get_asset(self.reimport_asset())
        obj: bt.Object = context.object
        mod: bt.NodesModifier = obj.modifiers.new(nt.name, 'NODES')
        mod.node_group = nt

def _create_new_object(context: bt.Context, name: str, data: bt.ID):

    obj = bpy.data.objects.new(name, data)
    obj.matrix_world = context.scene.cursor.matrix
    base_ops.link_and_select_object(context, obj)
    return obj

def _create_new_gn_curve_object(context: bt.Context, nt: bt.GeometryNodeTree, name: str):
    
    new_curve = bpy.data.curves.new(name, al.BObjectTypeCurve.CURVE())
    obj = _create_new_object(context, name, new_curve)
    mod: bt.NodesModifier = obj.modifiers.new(nt.name, 'NODES')
    mod.node_group = nt
    return (obj, mod)

def _try_assign_gn_properties(modifier: bt.NodesModifier, *parameters: tuple[tuple[str, Any]]):
        
    for attr, value in parameters:
        try:
            identifier = node_utils.gn_input_identifier(modifier.node_group, attr)
            modifier[identifier] = value
        except StopIteration:
            pass

@al.register_operator
class GNDrawFree(base_ops.SanctusAssetImportOperator):
    bl_label = md.GeometryNodeAssetType.DRAW_FREE.get_name()
    bl_description = md.GeometryNodeAssetType.DRAW_FREE.get_description()
    asset_type = 'objects'
    use_reimport_prompt = False

    def run(self, context: bt.Context):
        importer = self.get_importer()
        new_name = f'{importer.asset_instance.display_name} Drawing'
        obj: bt.Object = importer.get_asset(True)
        base_ops.link_and_select_object(context, obj)
        obj.name = new_name
        obj.data.name = new_name
        
        context.scene.tool_settings.curve_paint_settings.depth_mode = 'CURSOR'
        bo.object.mode_set(mode='EDIT')
        bo.wm.tool_set_by_id(name='builtin.draw')

@al.register_operator
class GNDrawSurface(base_ops.SanctusAssetImportOperator):
    bl_label = md.GeometryNodeAssetType.DRAW_SURFACE.get_name()
    bl_description = md.GeometryNodeAssetType.DRAW_SURFACE.get_description()
    asset_type = 'objects'
    use_reimport_prompt = False

    al_asserts = [
        al.OperatorAssert(lambda c: c.active_object in c.selected_objects, 'Object is active and selected', strict=False)
    ]

    def run(self, context: bt.Context):
        active_obj = context.active_object

        importer = self.get_importer()
        new_name = f'{importer.asset_instance.display_name} Drawing'
        obj: bt.Object = importer.get_asset(True)
        obj.name = new_name
        obj.data.name = new_name
        base_ops.link_and_select_object(context, obj)
        mod: bt.NodesModifier = obj.modifiers[0]

        obj.parent = active_obj
        
        _try_assign_gn_properties(mod, ('Target Object', active_obj))
        
        context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
        bo.object.mode_set(mode='EDIT')
        bo.wm.tool_set_by_id(name='builtin.draw')


class GNPlaceAsset(base_ops.SanctusAssetImportOperator):
    bl_label = md.GeometryNodeAssetType.PLACE_SURFACE.get_name()
    bl_description = md.GeometryNodeAssetType.PLACE_SURFACE.get_description()
    bl_options = {'UNDO'}
    asset_type = 'objects'
    use_reimport_prompt = False


    def invoke(self, context: bt.Context, event: bt.Event):
        from .. import preferences

        modals.SET_GIZMO_RUNNING(True)

        importer = self.get_importer()
        obj: bt.Object = importer.get_asset(True)
        base_ops.link_and_select_object(context, obj)
        obj.scale = Vector((0,0,0))
        mod = next(x for x in obj.modifiers if isinstance(x, bt.NodesModifier))

        self.asset_object = obj
        self.modifier = mod
        self.raycast_hit = al.geo.FAILED_RAYHIT
        self.target_is_valid = False


        if preferences.get().interface().center_mouse_on_gizmos():
            al.geo.center_mouse_in_window(context)
        
        bt.WindowManager.modal_handler_add(self)

        return {al.BOperatorReturn.RUNNING_MODAL()}
    
    def modal(self, context: bt.Context, event: bt.Event):
        context.area.tag_redraw()
        if modals.ModalHelper.is_event_cancel(event):
            self.raycast_hit = al.geo.FAILED_RAYHIT
            self.target_is_valid = False
            return self.execute(context)

        self.raycast_hit = al.geo.raycast_scene_view(context, context.evaluated_depsgraph_get(), al.geo.mouse_vector_from_event(event))
        self.target_is_valid = self.raycast_hit.is_hit
        if(self.raycast_hit.obj == self.asset_object):
            self.target_is_valid = False

        if self.target_is_valid:
            
            self.asset_object.parent = self.raycast_hit.obj

            _try_assign_gn_properties(self.modifier, ('Target Object', self.raycast_hit.obj))

            self.asset_object.matrix_world = al.geo.trs_matrix(self.raycast_hit.location, self.raycast_hit.normal)
        else:
            self.asset_object.scale = Vector((0,0,0))

        if modals.ModalHelper.is_event_confirm(event):
            if self.target_is_valid:
                return self.execute(context)
            else:
                self.report({'WARNING'}, 'Asset has to be placed on the surface of an object. [ESC] to cancel placement.')
                {al.BOperatorReturn.RUNNING_MODAL()}
        
        return {'PASS_THROUGH'}
    
    def run(self, context: bt.Context):
        modals.SET_GIZMO_RUNNING(False)
        if not self.target_is_valid:
            bpy.data.objects.remove(self.asset_object)
            return {al.BOperatorReturn.CANCELLED()}


@al.register_operator
class GNPlaceSurface(GNPlaceAsset):
    
    al_asserts = [
        modals.GIZMO_RUNNING_ASSERT,
        al.OperatorAssert(lambda c: c.object in c.selected_objects, 'Active object available and selected', strict=False),
        al.OperatorAssert(lambda c: c.object.type == 'MESH', 'Active object has to be "MESH"')
    ]
