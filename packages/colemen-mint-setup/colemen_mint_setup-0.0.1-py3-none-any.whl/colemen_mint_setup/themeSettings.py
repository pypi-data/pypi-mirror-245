# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import colemen_utils as c
import colemen_mint_setup.settings as _settings
from colemen_mint_setup.utils import set_gsetting,dconf_write



def apply_general_theme_settings():
    print("Applying General Theme Settings")
    label = """
# ---------------------------------------------------------------------------- #
#                        APPLYING GENERAL THEME SETTINGS                       #
# ---------------------------------------------------------------------------- #
"""
    print(label)


    set_gsetting("org.cinnamon.theme","name","Mint-Y-Dark-Pink","   Setting Theme to $value")
    set_gsetting("org.cinnamon.desktop.interface","gtk-theme","Mint-Y-Dark-Pink")
    set_gsetting("org.cinnamon.desktop.interface","icon-theme","Yaru-dark")
    set_gsetting("x.dm.slick-greeter", "cursor-theme-name", 'Bibata-Original-Classic')


    # dconf_write("/com/linuxmint/mintmenu/applet-icon", 'mintmenu-all-applications-symbolic')
    # dconf_write("/org/cinnamon/theme/name", 'Mint-Y-Dark-Pink')
    # dconf_write("/com/linuxmint/mintmenu/applet-icon", 'mintmenu-all-applications-symbolic')
    dconf_write("/com/linuxmint/mintmenu/applet-icon-size", 22)
    dconf_write("/org/cinnamon/panels-autohide", ['1:false'])
    dconf_write("/org/cinnamon/panels-enabled",['1:0:top'])

def apply_background_settings():
    # print("Applying Background Settings")
    label = """
# ---------------------------------------------------------------------------- #
#                         APPLYING BACKGROUND SETTINGS                         #
# ---------------------------------------------------------------------------- #
"""
    print(label)


    set_gsetting("org.cinnamon.desktop.background", "picture-options", 'zoom')
    set_gsetting("org.cinnamon.desktop.background.slideshow", "delay", 1)
    set_gsetting("org.cinnamon.desktop.background.slideshow", "random-order", True)
    set_gsetting("org.cinnamon.desktop.background.slideshow", "slideshow-enabled", True)


    set_gsetting("org.cinnamon.desktop.background", "picture-uri", 'file:///home/mint/Desktop/retro_background.jpg')

    # Use scroll to set the opacity of the window.
    set_gsetting("org.cinnamon.desktop.wm.preferences", "action-scroll-titlebar", 'opacity')
    set_gsetting("org.cinnamon.desktop.wm.preferences", "min-window-opacity", 30)

def apply_file_browser_settings():
    label = """
# ---------------------------------------------------------------------------- #
#                        APPLYING FILE BROWSER SETTINGS                        #
# ---------------------------------------------------------------------------- #
"""
    print(label)

    set_gsetting("org.cinnamon.muffin", "workspace-cycle", True)
    set_gsetting("org.nemo.desktop", "desktop-layout", 'true::true')
    set_gsetting("org.nemo.preferences", "start-with-dual-pane", True)


    # dconf_write("/org/cinnamon/desktop/interface/toolbar-icons-size", "small")
    dconf_write("/org/nemo/list-view/default-column-order", ['name', 'size', 'type', 'date_modified', 'date_created_with_time', 'date_accessed', 'date_created', 'detailed_type', 'group', 'where', 'mime_type', 'date_modified_with_time', 'octal_permissions', 'owner', 'permissions'])
    dconf_write("/org/nemo/list-view/default-visible-columns", ['name', 'size', 'type', 'date_modified', 'date_accessed'])



def apply_theme_settings():
    apply_general_theme_settings()
    apply_background_settings()
    apply_file_browser_settings()

