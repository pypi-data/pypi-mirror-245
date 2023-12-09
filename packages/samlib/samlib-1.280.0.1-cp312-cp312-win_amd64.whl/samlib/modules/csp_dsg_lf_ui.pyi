
# This is a generated file

"""csp_dsg_lf_ui - Calculates values for all calculated values on UI TES page(s)"""

# VERSION: 0

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'P_boil': float,
    'use_quality_or_subcooled': float,
    'deltaT_subcooled': float,
    'T_saturation': float,
    'T_hot_out_target': float
}, total=False)

class Data(ssc.DataDict):
    P_boil: float = INPUT(label='Boiling pressure', units='bar', type='NUMBER', required='*')
    use_quality_or_subcooled: float = INPUT(label='0 = 2 phase outlet, 1 = subcooled', type='NUMBER', required='*')
    deltaT_subcooled: float = INPUT(label='Subcooled temperature difference from saturation temp', units='C', type='NUMBER', required='*')
    T_saturation: Final[float] = OUTPUT(label='Saturation pressure', units='C', type='NUMBER', required='*')
    T_hot_out_target: Final[float] = OUTPUT(label='Target outlet temperature', units='C', type='NUMBER', required='*')

    def __init__(self, *args: Mapping[str, Any],
                 P_boil: float = ...,
                 use_quality_or_subcooled: float = ...,
                 deltaT_subcooled: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
