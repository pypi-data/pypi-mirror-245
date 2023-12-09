
# This is a generated file

"""ptes_design_point - PTES Design Point"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'hx_eff': float,
    'eta': float,
    'eta_pump': float,
    'ploss_working': float,
    'ploss_air': float,
    'ploss_liquid': float,
    'motor_eff': float,
    'gen_eff': float,
    'T0': float,
    'P0': float,
    'P1': float,
    'T_compressor_inlet': float,
    'T_compressor_outlet': float,
    'power_output': float,
    'charge_time_hr': float,
    'discharge_time_hr': float,
    'alpha': float,
    'working_fluid_type': str,
    'hot_fluid_id': float,
    'cold_fluid_id': float,
    'hot_ud_fluid_props': Matrix,
    'cold_ud_fluid_props': Matrix,
    'hp_COP': float,
    'cycle_eff': float,
    'Th_hot': float,
    'Th_cold': float,
    'Tc_hot': float,
    'Tc_cold': float,
    'hp_parasitic_fraction': float,
    'hp_hot_pump_power': float,
    'hp_cold_pump_power': float,
    'pc_parasitic_fraction': float,
    'pc_hot_pump_power': float,
    'pc_cold_pump_power': float,
    'N_pts_charge': float,
    'temp_series_charge': Array,
    's_series_charge': Array,
    'N_pts_discharge': float,
    'temp_series_discharge': Array,
    's_series_discharge': Array
}, total=False)

class Data(ssc.DataDict):
    hx_eff: float = INPUT(label='hx effectiveness', type='NUMBER', required='*')
    eta: float = INPUT(label='polytropic efficiency of compressors and expanders', type='NUMBER', required='*')
    eta_pump: float = INPUT(label='polytropic efficiency of air pump', type='NUMBER', required='*')
    ploss_working: float = INPUT(label='Fractional pressure loss in each heat exchanger', type='NUMBER', required='*')
    ploss_air: float = INPUT(label='Fractional pressure loss (air)', type='NUMBER', required='*')
    ploss_liquid: float = INPUT(label='Fractional pressure loss (liquid)', type='NUMBER', required='*')
    motor_eff: float = INPUT(label='Motor Efficiency', type='NUMBER', required='*')
    gen_eff: float = INPUT(label='Generator Efficiency', type='NUMBER', required='*')
    T0: float = INPUT(label='Ambient Temperature', units='C', type='NUMBER', required='*')
    P0: float = INPUT(label='Ambient Pressure', units='Pa', type='NUMBER', required='*')
    P1: float = INPUT(label='Lowest Pressure in cycle', units='Pa', type='NUMBER', required='*')
    T_compressor_inlet: float = INPUT(label='Charging compressor inlet temperature', units='C', type='NUMBER', required='*')
    T_compressor_outlet: float = INPUT(label='Charging compressor outlet temperature', units='C', type='NUMBER', required='*')
    power_output: float = INPUT(label='Power Output', units='MW', type='NUMBER', required='*')
    charge_time_hr: float = INPUT(label='charging time', units='hr', type='NUMBER', required='*')
    discharge_time_hr: float = INPUT(label='discharge time', units='hr', type='NUMBER', required='*')
    alpha: float = INPUT(label='Ratio of mdot cp     AIR/WF', type='NUMBER', required='*')
    working_fluid_type: str = INPUT(label='Working Fluid Type', type='STRING')
    hot_fluid_id: float = INPUT(label='Hot Reservoir Fluid ID', type='NUMBER')
    cold_fluid_id: float = INPUT(label='Cold Reservoir Fluid ID', type='NUMBER')
    hot_ud_fluid_props: Matrix = INPUT(label='User Defined Hot Resevior Fluid Properties', type='MATRIX')
    cold_ud_fluid_props: Matrix = INPUT(label='User Defined Cold Resevior Fluid Properties', type='MATRIX')
    hp_COP: Final[float] = OUTPUT(label='Heat Pump COP', type='NUMBER', group='SAM')
    cycle_eff: Final[float] = OUTPUT(label='Cycle Efficiency', type='NUMBER', group='SAM')
    Th_hot: Final[float] = OUTPUT(label='Hot Storage Hot Temp', units='C', type='NUMBER', group='SAM')
    Th_cold: Final[float] = OUTPUT(label='Hot Storage Cold Temp', units='C', type='NUMBER', group='SAM')
    Tc_hot: Final[float] = OUTPUT(label='Cold Storage Hot Temp', units='C', type='NUMBER', group='SAM')
    Tc_cold: Final[float] = OUTPUT(label='Cold Storage Cold Temp', units='C', type='NUMBER', group='SAM')
    hp_parasitic_fraction: Final[float] = OUTPUT(label='Heat Pump Parasitics Fraction', type='NUMBER', group='SAM')
    hp_hot_pump_power: Final[float] = OUTPUT(label='Heat Pump Hot HX Pump Power', units='kW/kg/s', type='NUMBER', group='SAM')
    hp_cold_pump_power: Final[float] = OUTPUT(label='Heat Pump Cold HX Pump Power', units='kW/kg/s', type='NUMBER', group='SAM')
    pc_parasitic_fraction: Final[float] = OUTPUT(label='Power Cycle Parasitics Fraction', type='NUMBER', group='SAM')
    pc_hot_pump_power: Final[float] = OUTPUT(label='Power Cycle Hot HX Pump Power', units='kW/kg/s', type='NUMBER', group='SAM')
    pc_cold_pump_power: Final[float] = OUTPUT(label='Power Cycle Cold HX Pump Power', units='kW/kg/s', type='NUMBER', group='SAM')
    N_pts_charge: Final[float] = OUTPUT(label='Number data points on plot', type='NUMBER')
    temp_series_charge: Final[Array] = OUTPUT(label='Temperature Values', units='C', type='ARRAY')
    s_series_charge: Final[Array] = OUTPUT(label='Entropy Values', units='kJ/kg K', type='ARRAY')
    N_pts_discharge: Final[float] = OUTPUT(label='Number data points on plot', type='NUMBER')
    temp_series_discharge: Final[Array] = OUTPUT(label='Temperature Values', units='C', type='ARRAY')
    s_series_discharge: Final[Array] = OUTPUT(label='Entropy Values', units='kJ/kg K', type='ARRAY')

    def __init__(self, *args: Mapping[str, Any],
                 hx_eff: float = ...,
                 eta: float = ...,
                 eta_pump: float = ...,
                 ploss_working: float = ...,
                 ploss_air: float = ...,
                 ploss_liquid: float = ...,
                 motor_eff: float = ...,
                 gen_eff: float = ...,
                 T0: float = ...,
                 P0: float = ...,
                 P1: float = ...,
                 T_compressor_inlet: float = ...,
                 T_compressor_outlet: float = ...,
                 power_output: float = ...,
                 charge_time_hr: float = ...,
                 discharge_time_hr: float = ...,
                 alpha: float = ...,
                 working_fluid_type: str = ...,
                 hot_fluid_id: float = ...,
                 cold_fluid_id: float = ...,
                 hot_ud_fluid_props: Matrix = ...,
                 cold_ud_fluid_props: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
