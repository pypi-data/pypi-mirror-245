
# This is a generated file

"""ui_udpc_checks - Calculates the levels and number of paramteric runs for 3 udpc ind variables"""

# VERSION: 0

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'ud_ind_od': Matrix,
    'T_htf_des_in': float,
    'n_T_htf_pars': float,
    'T_htf_low': float,
    'T_htf_des': float,
    'T_htf_high': float,
    'n_T_amb_pars': float,
    'T_amb_low': float,
    'T_amb_des': float,
    'T_amb_high': float,
    'n_m_dot_pars': float,
    'm_dot_low': float,
    'm_dot_des': float,
    'm_dot_high': float,
    'W_dot_gross_ND_des': float,
    'Q_dot_HTF_ND_des': float,
    'W_dot_cooling_ND_des': float,
    'm_dot_water_ND_des': float
}, total=False)

class Data(ssc.DataDict):
    ud_ind_od: Matrix = INPUT(label='Off design user-defined power cycle performance as function of T_htf, m_dot_htf [ND], and T_amb', type='MATRIX', group='User Defined Power Cycle', required='?=[[0]]')
    T_htf_des_in: float = INPUT(label='Input HTF design temperature', units='C', type='NUMBER', required='*')
    n_T_htf_pars: Final[float] = OUTPUT(label='Number of HTF parametrics', units='-', type='NUMBER', required='*')
    T_htf_low: Final[float] = OUTPUT(label='HTF low temperature', units='C', type='NUMBER', required='*')
    T_htf_des: Final[float] = OUTPUT(label='HTF design temperature', units='C', type='NUMBER', required='*')
    T_htf_high: Final[float] = OUTPUT(label='HTF high temperature', units='C', type='NUMBER', required='*')
    n_T_amb_pars: Final[float] = OUTPUT(label='Number of ambient temperature parametrics', units='-', type='NUMBER', required='*')
    T_amb_low: Final[float] = OUTPUT(label='Low ambient temperature', units='C', type='NUMBER', required='*')
    T_amb_des: Final[float] = OUTPUT(label='Design ambient temperature', units='C', type='NUMBER', required='*')
    T_amb_high: Final[float] = OUTPUT(label='High ambient temperature', units='C', type='NUMBER', required='*')
    n_m_dot_pars: Final[float] = OUTPUT(label='Number of HTF mass flow parametrics', units='-', type='NUMBER', required='*')
    m_dot_low: Final[float] = OUTPUT(label='Low ambient temperature', units='C', type='NUMBER', required='*')
    m_dot_des: Final[float] = OUTPUT(label='Design ambient temperature', units='C', type='NUMBER', required='*')
    m_dot_high: Final[float] = OUTPUT(label='High ambient temperature', units='C', type='NUMBER', required='*')
    W_dot_gross_ND_des: Final[float] = OUTPUT(label='ND cycle power output at design values of independent parameters', units='-', type='NUMBER', required='*')
    Q_dot_HTF_ND_des: Final[float] = OUTPUT(label='ND cycle heat input at design values of independent parameters', units='-', type='NUMBER', required='*')
    W_dot_cooling_ND_des: Final[float] = OUTPUT(label='ND cycle cooling power at design values of independent parameters', units='C', type='NUMBER', required='*')
    m_dot_water_ND_des: Final[float] = OUTPUT(label='ND cycle water use at design values of independent parameters', units='C', type='NUMBER', required='*')

    def __init__(self, *args: Mapping[str, Any],
                 ud_ind_od: Matrix = ...,
                 T_htf_des_in: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
