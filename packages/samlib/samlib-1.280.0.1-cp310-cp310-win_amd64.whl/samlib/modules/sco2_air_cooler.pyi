
# This is a generated file

"""sco2_air_cooler - Returns air cooler dimensions given fluid and location design points"""

# VERSION: 0

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'T_amb_des': float,
    'q_dot_des': float,
    'T_co2_hot_des': float,
    'P_co2_hot_des': float,
    'deltaP_co2_des': float,
    'T_co2_cold_des': float,
    'W_dot_fan_des': float,
    'site_elevation': float,
    'd_tube_out': float,
    'd_tube_in': float,
    'depth_footprint': float,
    'width_footprint': float,
    'parallel_paths': float,
    'number_of_tubes': float,
    'length': float,
    'n_passes_series': float,
    'UA_total': float,
    'm_V_hx_material': float,
    'od_calc_W_dot_fan': Matrix,
    'od_calc_T_co2_cold': Matrix,
    'T_amb_od': Array,
    'T_co2_hot_od': Array,
    'P_co2_hot_od': Array,
    'T_co2_cold_od': Array,
    'P_co2_cold_od': Array,
    'deltaP_co2_od': Array,
    'm_dot_co2_od_ND': Array,
    'W_dot_fan_od': Array,
    'W_dot_fan_od_ND': Array,
    'q_dot_od': Array,
    'q_dot_od_ND': Array
}, total=False)

class Data(ssc.DataDict):
    T_amb_des: float = INPUT(label='Ambient temperature at design', units='C', type='NUMBER', required='*')
    q_dot_des: float = INPUT(label='Heat rejected from CO2 stream', units='MWt', type='NUMBER', required='*')
    T_co2_hot_des: float = INPUT(label='Hot temperature of CO2 at inlet to cooler', units='C', type='NUMBER', required='*')
    P_co2_hot_des: float = INPUT(label='Pressure of CO2 at inlet to cooler', units='MPa', type='NUMBER', required='*')
    deltaP_co2_des: float = INPUT(label='Pressure drop of CO2 through cooler', units='MPa', type='NUMBER', required='*')
    T_co2_cold_des: float = INPUT(label='Cold temperature of CO2 at cooler exit', units='C', type='NUMBER', required='*')
    W_dot_fan_des: float = INPUT(label='Air fan power', units='MWe', type='NUMBER', required='*')
    site_elevation: float = INPUT(label='Site elevation', units='m', type='NUMBER', required='*')
    d_tube_out: Final[float] = OUTPUT(label='CO2 tube outer diameter', units='cm', type='NUMBER', required='*')
    d_tube_in: Final[float] = OUTPUT(label='CO2 tube inner diameter', units='cm', type='NUMBER', required='*')
    depth_footprint: Final[float] = OUTPUT(label='Dimension of total air cooler in loop/air flow direction', units='m', type='NUMBER', required='*')
    width_footprint: Final[float] = OUTPUT(label='Dimension of total air cooler of parallel loops', units='m', type='NUMBER', required='*')
    parallel_paths: Final[float] = OUTPUT(label='Number of parallel flow paths', units='-', type='NUMBER', required='*')
    number_of_tubes: Final[float] = OUTPUT(label='Number of tubes (one pass)', units='-', type='NUMBER', required='*')
    length: Final[float] = OUTPUT(label='Length of tube (one pass)', units='m', type='NUMBER', required='*')
    n_passes_series: Final[float] = OUTPUT(label='Number of serial tubes in flow path', units='-', type='NUMBER', required='*')
    UA_total: Final[float] = OUTPUT(label='Total air-side conductance', units='kW/K', type='NUMBER', required='*')
    m_V_hx_material: Final[float] = OUTPUT(label='Total hx material volume - no headers', units='m^3', type='NUMBER', required='*')
    od_calc_W_dot_fan: Matrix = INPUT(label='Columns: T_co2_hot_C, P_co2_hot_MPa, T_co2_cold_C, m_dot_CO2_ND, T_amb_C. Rows: cases', type='MATRIX')
    od_calc_T_co2_cold: Matrix = INPUT(label='Columns: T_co2_hot_C, P_co2_hot_MPa, W_dot_fan_ND, m_dot_CO2_ND, T_amb_C. Rows: cases', type='MATRIX')
    T_amb_od: Final[Array] = OUTPUT(label='Off-design ambient temperature', units='C', type='ARRAY')
    T_co2_hot_od: Final[Array] = OUTPUT(label='Off-design co2 hot inlet temperature', units='C', type='ARRAY')
    P_co2_hot_od: Final[Array] = OUTPUT(label='Off-design co2 hot inlet pressure', units='MPa', type='ARRAY')
    T_co2_cold_od: Final[Array] = OUTPUT(label='Off-design co2 cold outlet temperature', units='C', type='ARRAY')
    P_co2_cold_od: Final[Array] = OUTPUT(label='Off-design co2 cold outlet pressure', units='MPa', type='ARRAY')
    deltaP_co2_od: Final[Array] = OUTPUT(label='Off-design co2 cold pressure drop', units='MPa', type='ARRAY')
    m_dot_co2_od_ND: Final[Array] = OUTPUT(label='Off-design co2 mass flow normalized design', units='-', type='ARRAY')
    W_dot_fan_od: Final[Array] = OUTPUT(label='Off-design fan power', units='MWe', type='ARRAY')
    W_dot_fan_od_ND: Final[Array] = OUTPUT(label='Off-design fan power normalized v design', units='-', type='ARRAY')
    q_dot_od: Final[Array] = OUTPUT(label='Off-design heat rejection', units='MWt', type='ARRAY')
    q_dot_od_ND: Final[Array] = OUTPUT(label='Off-design heat rejection normalized design', units='-', type='ARRAY')

    def __init__(self, *args: Mapping[str, Any],
                 T_amb_des: float = ...,
                 q_dot_des: float = ...,
                 T_co2_hot_des: float = ...,
                 P_co2_hot_des: float = ...,
                 deltaP_co2_des: float = ...,
                 T_co2_cold_des: float = ...,
                 W_dot_fan_des: float = ...,
                 site_elevation: float = ...,
                 od_calc_W_dot_fan: Matrix = ...,
                 od_calc_T_co2_cold: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
