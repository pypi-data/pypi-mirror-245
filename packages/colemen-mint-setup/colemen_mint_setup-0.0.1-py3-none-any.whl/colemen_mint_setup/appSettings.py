# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import colemen_utils as c
import colemen_mint_setup.settings as _settings
from colemen_mint_setup.utils import install_app,execute_cmd


apps=[
    ["dconf-editor"],
    ["diodon","ppa:diodon-team/stable"],
    ["activity-log-manager"],
    ["plank","ppa:ricotz/docky"],
    ["bottles"],
    ["deluge"],
    ["obsidian"],
    ["vlc"],
    ["xdotool"],
    ["python3-pip"],
    ["sqlitebrowser"],
    ["zeit","ppa:blaze/main"],
]

def install_espanso():
    execute_cmd("cd ~/Desktop")
    execute_cmd("wget https://github.com/federico-terzi/espanso/releases/download/v2.1.8/espanso-debian-x11-amd64.deb")
    execute_cmd("sudo apt install ./espanso-debian-x11-amd64.deb")
    execute_cmd("rm ./espanso-debian-x11-amd64.deb")
    execute_cmd("espanso service register")
    execute_cmd("espanso start")

def install_drawio():
    execute_cmd("cd ~/Desktop")
    execute_cmd("wget https://github.com/jgraph/drawio-desktop/releases/download/v22.1.2/drawio-amd64-22.1.2.deb")
    execute_cmd("sudo apt install ./drawio-amd64-22.1.2.deb")
    execute_cmd("rm ./drawio-amd64-22.1.2.deb")


def apply_app_settings():
    label = """
# ---------------------------------------------------------------------------- #
#                           APPLYING HOTKEY SETTINGS                           #
# ---------------------------------------------------------------------------- #
"""
    print(label)

    for a in apps:
        if len(a) == 1:
            a.append(None)
        install_app(a[0],a[1])
    install_espanso()
    install_drawio()




