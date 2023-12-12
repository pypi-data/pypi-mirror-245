from typing import TYPE_CHECKING,TypeVar as _TypeVar


# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

_main_type = None

if TYPE_CHECKING:

    from colemen_mint_setup.ColemenMintSetup import ColemenMintSetup as _m
    _main_type = _TypeVar('_main_type', bound=_m)


