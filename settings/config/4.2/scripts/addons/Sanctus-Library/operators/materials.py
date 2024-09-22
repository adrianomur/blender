
from .. import auto_load as al
from ..auto_load.common import *
from .. import base_ops

@al.register_operator
class ApplyMaterial(base_ops.SanctusAssetImportOperator):
    bl_description: str = 'Add the selected Sanctus Library Material to the selected objects.'
    asset_type = 'materials'
    use_reimport_prompt = True
    al_asserts_header: str = 'Cannot import asset:'

    al_asserts: list[al.OperatorAssert] = [
        al.OperatorAssert(lambda c: len(c.selected_objects) > 0, 'At least 1 selected object', strict=False)
    ]

    def run(self, context: bt.Context):
        importer = self.get_importer()
        mat = importer.get_asset(self.reimport_asset())
        for o in context.selected_objects:
            o.active_material = mat


@al.register_operator
class ImportMaterial(base_ops.SanctusAssetImportOperator):
    bl_description = 'Imports Material asset from library into file'
    asset_type = 'materials'
    use_reimport_prompt = True

    def run(self, context: bt.Context):
        self.get_importer().get_asset(self.reimport_asset())
