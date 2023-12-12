# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import colemen_utils as c
import colemen_mint_setup.settings as _settings
from colemen_mint_setup.utils import set_gsetting,dconf_write




def apply_hotkey_settings():
    label = """
# ---------------------------------------------------------------------------- #
#                           APPLYING HOTKEY SETTINGS                           #
# ---------------------------------------------------------------------------- #
"""
    print(label)


    dconf_write("/org/cinnamon/desktop/keybindings/media-keys/calculator", ['XF86Calculator', '<Primary><Alt>c'])
    dconf_write("/org/cinnamon/desktop/keybindings/media-keys/terminal",['<Primary><Alt>t', '<Primary><Shift>p'])
    dconf_write("/org/cinnamon/desktop/keybindings/wm/switch-to-workspace-left",['<Control><Alt>Left', '<Primary><Super>Left'])
    dconf_write("/org/cinnamon/desktop/keybindings/wm/switch-to-workspace-right",['<Control><Alt>Right', '<Primary><Super>Right'])
    dconf_write("/org/cinnamon/desktop/keybindings/wm/decrease-opacity",['<Primary><Super>KP_Subtract'])
    dconf_write("/org/cinnamon/desktop/keybindings/wm/increase-opacity",['<Primary><Super>KP_Add'])
    dconf_write("/org/cinnamon/desktop/keybindings/wm/lower",['<Primary>KP_Subtract'])
    dconf_write("/org/cinnamon/desktop/keybindings/media-keys/volume-mute",['XF86AudioMute', '<Alt>m'])

