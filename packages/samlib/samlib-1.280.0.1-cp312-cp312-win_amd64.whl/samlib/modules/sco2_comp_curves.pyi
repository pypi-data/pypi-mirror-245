
# This is a generated file

"""sco2_comp_curves - Calls sCO2 auto-design cycle function"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'comp_type': float,
    'T_comp_in': float,
    'P_comp_in': float,
    'phi_design': float,
    'psi_design': float,
    'eta_norm_design': float,
    'phi': Array,
    'phi_ND': Array,
    'psi': Array,
    'psi_ND': Array,
    'eta': Array,
    'eta_ND': Array
}, total=False)

class Data(ssc.DataDict):
    comp_type: float = INPUT(label='Integer corresponding to compressor model', units='-', type='NUMBER', required='*')
    T_comp_in: float = INPUT(label='Compressor inlet temperature', units='C', type='NUMBER', required='*')
    P_comp_in: float = INPUT(label='Compressor inlet pressure', units='MPa', type='NUMBER', required='*')
    phi_design: Final[float] = OUTPUT(label='Design flow coefficient', units='-', type='NUMBER', required='*')
    psi_design: Final[float] = OUTPUT(label='Design isentropic head coefficient', units='-', type='NUMBER', required='*')
    eta_norm_design: Final[float] = OUTPUT(label='Normalized design isentropic efficiency', units='-', type='NUMBER', required='*')
    phi: Final[Array] = OUTPUT(label='Array of flow coefficients', units='-', type='ARRAY', required='*')
    phi_ND: Final[Array] = OUTPUT(label='Array of normalized flow coefficients', units='-', type='ARRAY', required='*')
    psi: Final[Array] = OUTPUT(label='Array of isentropic head coefficients at phi', units='-', type='ARRAY', required='*')
    psi_ND: Final[Array] = OUTPUT(label='Array of normalized isentropic head coefficients at phi', units='-', type='ARRAY', required='*')
    eta: Final[Array] = OUTPUT(label='Array of efficiencies at phi', units='-', type='ARRAY', required='*')
    eta_ND: Final[Array] = OUTPUT(label='Array of normalized efficiencies at phi', units='-', type='ARRAY', required='*')

    def __init__(self, *args: Mapping[str, Any],
                 comp_type: float = ...,
                 T_comp_in: float = ...,
                 P_comp_in: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
