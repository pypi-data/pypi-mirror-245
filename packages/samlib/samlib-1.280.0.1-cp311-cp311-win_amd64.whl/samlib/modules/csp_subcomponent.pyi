
# This is a generated file

"""csp_subcomponent - CSP subcomponents"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    't_step': float,
    'T_amb': Array,
    'mdot_src': Array,
    'mdot_sink': Array,
    'hot_tank_bypassed': Array,
    'T_src_out': Array,
    'T_sink_out': Array,
    'Fluid': float,
    'field_fl_props': Matrix,
    'store_fluid': float,
    'store_fl_props': Matrix,
    'P_ref': float,
    'eta_ref': float,
    'solar_mult': float,
    'tshours': float,
    'h_tank': float,
    'u_tank': float,
    'tank_pairs': float,
    'hot_tank_Thtr': float,
    'hot_tank_max_heat': float,
    'cold_tank_Thtr': float,
    'cold_tank_max_heat': float,
    'dt_hot': float,
    'T_loop_in_des': float,
    'T_loop_out': float,
    'h_tank_min': float,
    'init_hot_htf_percent': float,
    'pb_pump_coef': float,
    'tanks_in_parallel': float,
    'V_tes_des': float,
    'calc_design_pipe_vals': float,
    'tes_pump_coef': float,
    'eta_pump': float,
    'has_hot_tank_bypass': float,
    'T_tank_hot_inlet_min': float,
    'custom_tes_p_loss': float,
    'custom_tes_pipe_sizes': float,
    'k_tes_loss_coeffs': Matrix,
    'tes_diams': Matrix,
    'tes_wallthicks': Matrix,
    'tes_lengths': Matrix,
    'HDR_rough': float,
    'DP_SGS': float,
    'T_src_in': Array,
    'T_sink_in': Array,
    'T_tank_cold': Array,
    'T_tank_hot': Array
}, total=False)

class Data(ssc.DataDict):
    t_step: float = INPUT(label='Timestep duration', units='s', type='NUMBER', group='system', required='*')
    T_amb: Array = INPUT(label='Ambient temperature', units='C', type='ARRAY', group='weather', required='*')
    mdot_src: Array = INPUT(label='Mass flow from heat source', units='kg/s', type='ARRAY', group='TES', required='*')
    mdot_sink: Array = INPUT(label='Mass flow to heat sink or power block', units='kg/s', type='ARRAY', group='TES', required='*')
    hot_tank_bypassed: Array = INPUT(label='Is mass flow from source going straight to cold tank?', units='-', type='ARRAY', group='TES', required='*')
    T_src_out: Array = INPUT(label='Temperature from heat source', units='C', type='ARRAY', group='TES', required='*')
    T_sink_out: Array = INPUT(label='Temperature from heat sink or power block', units='C', type='ARRAY', group='TES', required='*')
    Fluid: float = INPUT(label='Field HTF fluid ID number', units='-', type='NUMBER', group='solar_field', required='*')
    field_fl_props: Matrix = INPUT(label='User defined field fluid property data', units='-', type='MATRIX', group='solar_field', required='*')
    store_fluid: float = INPUT(label='Material number for storage fluid', units='-', type='NUMBER', group='TES', required='*')
    store_fl_props: Matrix = INPUT(label='User defined storage fluid property data', units='-', type='MATRIX', group='TES', required='*')
    P_ref: float = INPUT(label='Rated plant capacity', units='MWe', type='NUMBER', group='powerblock', required='*')
    eta_ref: float = INPUT(label='Power cycle efficiency at design', units='none', type='NUMBER', group='powerblock', required='*')
    solar_mult: float = INPUT(label='Actual solar multiple of system', units='-', type='NUMBER', group='system', required='*')
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='TES', required='*')
    h_tank: float = INPUT(label='Total height of tank (height of HTF when tank is full', units='m', type='NUMBER', group='TES', required='*')
    u_tank: float = INPUT(label='Loss coefficient from the tank', units='W/m2-K', type='NUMBER', group='TES', required='*')
    tank_pairs: float = INPUT(label='Number of equivalent tank pairs', units='-', type='NUMBER', group='TES', required='*', constraints='INTEGER')
    hot_tank_Thtr: float = INPUT(label='Minimum allowable hot tank HTF temp', units='C', type='NUMBER', group='TES', required='*')
    hot_tank_max_heat: float = INPUT(label='Rated heater capacity for hot tank heating', units='MWe', type='NUMBER', group='TES', required='*')
    cold_tank_Thtr: float = INPUT(label='Minimum allowable cold tank HTF temp', units='C', type='NUMBER', group='TES', required='*')
    cold_tank_max_heat: float = INPUT(label='Rated heater capacity for cold tank heating', units='MWe', type='NUMBER', group='TES', required='*')
    dt_hot: float = INPUT(label='Hot side HX approach temp', units='C', type='NUMBER', group='TES', required='*')
    T_loop_in_des: float = INPUT(label='Design loop inlet temperature', units='C', type='NUMBER', group='solar_field', required='*')
    T_loop_out: float = INPUT(label='Target loop outlet temperature', units='C', type='NUMBER', group='solar_field', required='*')
    h_tank_min: float = INPUT(label='Minimum allowable HTF height in storage tank', units='m', type='NUMBER', group='TES', required='*')
    init_hot_htf_percent: float = INPUT(label='Initial fraction of avail. vol that is hot', units='%', type='NUMBER', group='TES', required='*')
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='powerblock', required='*')
    tanks_in_parallel: float = INPUT(label='Tanks are in parallel, not in series, with solar field', units='-', type='NUMBER', group='controller', required='*')
    V_tes_des: float = INPUT(label='Design-point velocity to size the TES pipe diameters', units='m/s', type='NUMBER', group='controller', required='*')
    calc_design_pipe_vals: float = INPUT(label='Calculate temps and pressures at design conditions for runners and headers', units='none', type='NUMBER', group='solar_field', required='*')
    tes_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through tes loop', units='kW/(kg/s)', type='NUMBER', group='controller', required='*')
    eta_pump: float = INPUT(label='HTF pump efficiency', units='none', type='NUMBER', group='solar_field', required='*')
    has_hot_tank_bypass: float = INPUT(label='Bypass valve connects field outlet to cold tank', units='-', type='NUMBER', group='controller', required='*')
    T_tank_hot_inlet_min: float = INPUT(label='Minimum hot tank htf inlet temperature', units='C', type='NUMBER', group='controller', required='*')
    custom_tes_p_loss: float = INPUT(label='TES pipe losses are based on custom lengths and coeffs', units='-', type='NUMBER', group='controller', required='*')
    custom_tes_pipe_sizes: float = INPUT(label='Use custom TES pipe diams, wallthks, and lengths', units='-', type='NUMBER', group='controller', required='*')
    k_tes_loss_coeffs: Matrix = INPUT(label='Minor loss coeffs for the coll, gen, and bypass loops', units='-', type='MATRIX', group='controller', required='*')
    tes_diams: Matrix = INPUT(label='Custom TES diameters', units='m', type='MATRIX', group='controller', required='*')
    tes_wallthicks: Matrix = INPUT(label='Custom TES wall thicknesses', units='m', type='MATRIX', group='controller', required='*')
    tes_lengths: Matrix = INPUT(label='Custom TES lengths', units='m', type='MATRIX', group='controller')
    HDR_rough: float = INPUT(label='Header pipe roughness', units='m', type='NUMBER', group='solar_field', required='*')
    DP_SGS: float = INPUT(label='Pressure drop within the steam generator', units='bar', type='NUMBER', group='controller', required='*')
    T_src_in: Final[Array] = OUTPUT(label='Temperature to heat source', units='C', type='ARRAY', group='TES', required='*')
    T_sink_in: Final[Array] = OUTPUT(label='Temperature to heat sink or power block', units='C', type='ARRAY', group='TES', required='*')
    T_tank_cold: Final[Array] = OUTPUT(label='Temperature of cold tank (average)', units='C', type='ARRAY', group='TES', required='*')
    T_tank_hot: Final[Array] = OUTPUT(label='Temperature of hot tank (average)', units='C', type='ARRAY', group='TES', required='*')

    def __init__(self, *args: Mapping[str, Any],
                 t_step: float = ...,
                 T_amb: Array = ...,
                 mdot_src: Array = ...,
                 mdot_sink: Array = ...,
                 hot_tank_bypassed: Array = ...,
                 T_src_out: Array = ...,
                 T_sink_out: Array = ...,
                 Fluid: float = ...,
                 field_fl_props: Matrix = ...,
                 store_fluid: float = ...,
                 store_fl_props: Matrix = ...,
                 P_ref: float = ...,
                 eta_ref: float = ...,
                 solar_mult: float = ...,
                 tshours: float = ...,
                 h_tank: float = ...,
                 u_tank: float = ...,
                 tank_pairs: float = ...,
                 hot_tank_Thtr: float = ...,
                 hot_tank_max_heat: float = ...,
                 cold_tank_Thtr: float = ...,
                 cold_tank_max_heat: float = ...,
                 dt_hot: float = ...,
                 T_loop_in_des: float = ...,
                 T_loop_out: float = ...,
                 h_tank_min: float = ...,
                 init_hot_htf_percent: float = ...,
                 pb_pump_coef: float = ...,
                 tanks_in_parallel: float = ...,
                 V_tes_des: float = ...,
                 calc_design_pipe_vals: float = ...,
                 tes_pump_coef: float = ...,
                 eta_pump: float = ...,
                 has_hot_tank_bypass: float = ...,
                 T_tank_hot_inlet_min: float = ...,
                 custom_tes_p_loss: float = ...,
                 custom_tes_pipe_sizes: float = ...,
                 k_tes_loss_coeffs: Matrix = ...,
                 tes_diams: Matrix = ...,
                 tes_wallthicks: Matrix = ...,
                 tes_lengths: Matrix = ...,
                 HDR_rough: float = ...,
                 DP_SGS: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
