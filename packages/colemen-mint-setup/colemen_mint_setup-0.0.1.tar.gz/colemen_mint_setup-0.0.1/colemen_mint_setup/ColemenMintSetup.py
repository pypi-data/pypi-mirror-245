# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import colemen_utils as c
import colemen_mint_setup.settings as _settings
from colemen_mint_setup.themeSettings import apply_theme_settings
from colemen_mint_setup.hotkeySettings import apply_hotkey_settings
from colemen_mint_setup.aliasSettings import apply_alias_settings
from colemen_mint_setup.appSettings import apply_app_settings



class ColemenMintSetup:
    def __init__(self):
        self.settings = {}
        self.data = {}
        # self.set_defaults()

    # def set_defaults(self):
    #     self.settings = c.file.import_project_settings("colemen_mint_setup.settings.json")

    def master(self):
        print("master")
        apply_theme_settings()
        apply_hotkey_settings()
        apply_app_settings()

if __name__ == '__main__':
    m = ColemenMintSetup()
    m.master()

