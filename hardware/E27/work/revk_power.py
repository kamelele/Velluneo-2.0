"""Sourcing data for the Rev K power board."""

from dataclasses import replace
from pathlib import Path

import revh_power


NAME = 'Zasilacz_RevK_Moc'
DEST = Path('outputs') / NAME
PART_CODES = revh_power.PART_CODES | {'BR1': 'C7507234'}


def devices():
    return [replace(part, val='ABS10M-13', part='ABS10M-13', maker='Diodes Incorporated',
                    footprint='E27:ABS10M_SOPA-4_WX', connection={1:'P_BR', 2:'P_N', 3:'P_0', 4:'P_LR'})
            if part.ref == 'BR1' else part for part in revh_power.devices()]
