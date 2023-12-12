# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import colemen_utils as c
import colemen_mint_setup.settings as _settings
from colemen_mint_setup.utils import set_gsetting,dconf_write



default_bash_aliases="""

alias boobs="echo ( • )( • )ԅ(‾⌣‾ԅ)"

alias desktop="cd Desktop"
alias desk="cd Desktop"

alias bc="bc -l"

alias sai="sudo apt-get install"
alias sau="sudo apt update"
alias executable="chmod +x"
alias exe="chmod +x"

alias :q="exit"
alias ext="exit"
alias xt="exit"
alias by="exit"
alias bye="exit"
alias die="exit"
alias quit="exit"

alias taskscheduler="nohup zeit &"
alias zeit="nohup zeit &"
alias guake="nohup guake &"
alias dconf="nohup dconf-editor &"

alias listwindows="wmctrl -l"
alias listwins="wmctrl -l"

alias minimizeTerminals="$scripts_path/minimizeTerminals.sh"
alias killTerminals="$scripts_path/killTerminals.sh"

"""

def create_bash_aliases():
    file_path = "/home/mint/.bash_aliases"
    aliases = default_bash_aliases.replace("$scripts_path","~/Desktop/scripts")
    f = open(file_path, "w")
    f.write(aliases)
    f.close()

