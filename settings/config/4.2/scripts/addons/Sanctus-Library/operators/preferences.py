from .. import auto_load as al
from ..auto_load.common import *
from .. import base_ops
import json

@al.register_operator
class ExportPreferences(base_ops.SanctusFilepathOperator):

    def set_defaults(self, context: bt.Context, event: bt.Event):
        prefs = preferences.SanctusLibraryPreferences(context)
        version = prefs.addon.bl_info['version']
        version_string = '_'.join([str(x) for x in version])
        self.filepath = f'{al.config.ADDON_PACKAGE}_preferences_{version_string}{preferences.PREFERENCES_EXTENSION}'
        self.filter_glob = f'*{preferences.PREFERENCES_EXTENSION}'
        self.hide_props_region = True
        self.filter_folder = False

    def draw(self, context: bt.Context) -> None:
        l = self.layout
        l = l.box()
        al.UI.label(l, 'Save the Sanctus Preferences to an external file.')
        al.UI.label(l, 'This file serves as a backup.')
        al.UI.label(l, 'Preferences get saved automatically.')

    def run(self, context: bt.Context):
        prefs = preferences.SanctusLibraryPreferences(context)
        file = Path(self.Filepath)
        file.unlink(missing_ok=True)
        file.write_text(json.dumps(prefs.serialize()))

@al.register_operator
class ImportPreferences(base_ops.SanctusFilepathOperator):

    def set_defaults(self, context: bt.Context, event: bt.Event):
        self.hide_props_region = True
        self.filter_glob = f'*{preferences.PREFERENCES_EXTENSION}'
        self.check_existing = False
        self.filter = False

    def draw(self, context: bt.Context) -> None:
        l = self.layout
        al.UI.label(l, 'Load Sanctus Preferences from a file.')


    def run(self, context: bt.Context):
        from .. import library_manager as lm
        prefs = preferences.get()
        backup = prefs.serialize()
        file = Path(self.Filepath)
        if not file.exists():
            self.report({'ERROR'}, f'Filepath "{str(file)}" does not exist')
        data = json.loads(file.read_text())
        try:
            prefs.deserialize(data)
            lm.reload_library()
        except:
            self.report({'ERROR'}, f'File content could not be used to load preferences.')
            prefs.deserialize(backup)

from .. import preferences