
# This is a generated file

"""mhk_wave - MHK Wave power calculation model using power distribution."""

# VERSION: 3

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'wave_resource_model_choice': float,
    'wave_resource_matrix': Matrix,
    'wave_resource_data': Table,
    'significant_wave_height': Array,
    'energy_period': Array,
    'wave_power_matrix': Matrix,
    'number_devices': float,
    'system_capacity': float,
    'number_hours': float,
    'number_records': float,
    'me_adjust:constant': float,
    'me_adjust:hourly': Array,
    'me_adjust:timeindex': Array,
    'me_adjust:periods': Matrix,
    'device_rated_power': float,
    'fixed_charge_rate': float,
    'device_costs_total': float,
    'balance_of_system_cost_total': float,
    'financial_cost_total': float,
    'total_operating_cost': float,
    'system_use_lifetime_output': float,
    'analysis_period': float,
    'generic_degradation': Array,
    'loss_array_spacing': float,
    'loss_resource_overprediction': float,
    'loss_transmission': float,
    'loss_downtime': float,
    'loss_additional': float,
    'year': Array,
    'month': Array,
    'day': Array,
    'hour': Array,
    'minute': Array,
    'device_average_power': float,
    'annual_energy': float,
    'energy_hourly_kWh': Array,
    'energy_hourly_kW': Array,
    'gen': Array,
    'sig_wave_height_index_mat': Array,
    'sig_wave_height_data': Array,
    'energy_period_index_mat': Array,
    'energy_period_data': Array,
    'wave_power_index_mat': Array,
    'capacity_factor': float,
    'numberRecords': float,
    'numberHours': float,
    'annual_energy_distribution': Matrix,
    'annual_energy_distribution_time': Matrix,
    'wave_resource_start_height': float,
    'wave_resource_start_period': float,
    'wave_resource_end_height': float,
    'wave_resource_end_period': float,
    'wave_power_start_height': float,
    'wave_power_start_period': float,
    'wave_power_end_height': float,
    'wave_power_end_period': float,
    'total_capital_cost_kwh': float,
    'total_device_cost_kwh': float,
    'total_bos_cost_kwh': float,
    'total_financial_cost_kwh': float,
    'total_om_cost_kwh': float,
    'total_capital_cost_lcoe': float,
    'total_device_cost_lcoe': float,
    'total_bos_cost_lcoe': float,
    'total_financial_cost_lcoe': float,
    'total_om_cost_lcoe': float,
    'total_capital_cost_per_kw': float,
    'total_device_cost_per_kw': float,
    'total_bos_cost_per_kw': float,
    'total_financial_cost_per_kw': float,
    'total_operations_cost_per_kw': float
}, total=False)

class Data(ssc.DataDict):
    wave_resource_model_choice: float = INPUT(label='Hourly or JPD wave resource data', units='0/1', type='NUMBER', group='MHKWave', required='?=0', constraints='INTEGER')
    wave_resource_matrix: Matrix = INPUT(label='Frequency distribution of wave resource as a function of Hs and Te', type='MATRIX', group='MHKWave', required='?')
    wave_resource_data: Table = INPUT(label='Array input of wave_resource_matrix (JPD) or time series (significant_wave_height and energy_period) data', type='TABLE', group='MHKWave', required='?')
    significant_wave_height: Array = INPUT(label='Significant wave height time series data', units='m', type='ARRAY', group='MHKWave', required='?')
    energy_period: Array = INPUT(label='Wave period time series data', units='s', type='ARRAY', group='MHKWave', required='?')
    wave_power_matrix: Matrix = INPUT(label='Wave Power Matrix', type='MATRIX', group='MHKWave', required='*')
    number_devices: float = INPUT(label='Number of wave devices in the system', type='NUMBER', group='MHKWave', required='?=1', constraints='INTEGER')
    system_capacity: float = INPUT(label='System Nameplate Capacity', units='kW', type='NUMBER', group='MHKWave', required='?=0')
    number_hours: float = INPUT(label='Number of hours in wave time series', type='NUMBER', group='MHKWave', required='?')
    number_records: float = INPUT(label='Number of records in wave time series', type='NUMBER', group='MHKWave', required='?')
    me_adjust_constant: float = INPUT(name='me_adjust:constant', label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='?', constraints='MAX=100')
    me_adjust_hourly: Array = INPUT(name='me_adjust:hourly', label='Hourly Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    me_adjust_timeindex: Array = INPUT(name='me_adjust:timeindex', label='Lifetime Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    me_adjust_periods: Matrix = INPUT(name='me_adjust:periods', label='Period-based Adjustment Factors', units='%', type='MATRIX', group='Adjustment Factors', required='?', constraints='COLS=3', meta='n x 3 matrix [ start, end, loss ]')
    device_rated_power: float = INPUT(label='Rated capacity of device', units='kW', type='NUMBER', group='MHKWave', required='*')
    fixed_charge_rate: float = INPUT(label='FCR from LCOE Cost page', type='NUMBER', group='MHKWave', required='?=1')
    device_costs_total: float = INPUT(label='Device costs', units='$', type='NUMBER', group='MHKWave', required='?=1')
    balance_of_system_cost_total: float = INPUT(label='BOS costs', units='$', type='NUMBER', group='MHKWave', required='?=1')
    financial_cost_total: float = INPUT(label='Financial costs', units='$', type='NUMBER', group='MHKWave', required='?=1')
    total_operating_cost: float = INPUT(label='O&M costs', units='$', type='NUMBER', group='MHKWave', required='?=1')
    system_use_lifetime_output: float = INPUT(label='Generic lifetime simulation', units='0/1', type='NUMBER', group='Lifetime', required='?=0', constraints='INTEGER,MIN=0,MAX=1')
    analysis_period: float = INPUT(label='Lifetime analysis period', units='years', type='NUMBER', group='Lifetime', required='system_use_lifetime_output=1')
    generic_degradation: Array = INPUT(label='Annual AC degradation', units='%/year', type='ARRAY', group='Lifetime', required='system_use_lifetime_output=1')
    loss_array_spacing: float = INPUT(label='Array spacing loss', units='%', type='NUMBER', group='MHKWave', required='*')
    loss_resource_overprediction: float = INPUT(label='Resource overprediction loss', units='%', type='NUMBER', group='MHKWave', required='*')
    loss_transmission: float = INPUT(label='Transmission losses', units='%', type='NUMBER', group='MHKWave', required='*')
    loss_downtime: float = INPUT(label='Array/WEC downtime loss', units='%', type='NUMBER', group='MHKWave', required='*')
    loss_additional: float = INPUT(label='Additional losses', units='%', type='NUMBER', group='MHKWave', required='*')
    year: Array = INPUT(label='Year', units='yr', type='ARRAY', group='MHKWave')
    month: Array = INPUT(label='Month', units='mn', type='ARRAY', group='MHKWave', meta='1-12')
    day: Array = INPUT(label='Day', units='dy', type='ARRAY', group='MHKWave', meta='1-365')
    hour: Array = INPUT(label='Hour', units='hr', type='ARRAY', group='MHKWave', meta='0-23')
    minute: Array = INPUT(label='Minute', units='min', type='ARRAY', group='MHKWave', meta='0-59')
    device_average_power: Final[float] = OUTPUT(label='Average power production of a single device', units='kW', type='NUMBER', group='MHKWave', required='*')
    annual_energy: Final[float] = OUTPUT(label='Annual energy production of array', units='kWh', type='NUMBER', group='MHKWave', required='*')
    energy_hourly_kWh: Final[Array] = OUTPUT(label='Energy production of array', units='kWh', type='ARRAY', group='Time Series', required='wave_resource_model_choice=1')
    energy_hourly_kW: Final[Array] = OUTPUT(label='Power output of array', units='kW', type='ARRAY', group='Time Series', required='wave_resource_model_choice=1')
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', group='Time Series')
    sig_wave_height_index_mat: Final[Array] = OUTPUT(label='Wave height index locations for time series', units='m', type='ARRAY', group='MHKWave', required='wave_resource_model_choice=1')
    sig_wave_height_data: Final[Array] = OUTPUT(label='Significant wave height time series data', units='m', type='ARRAY', group='MHKWave', required='wave_resource_model_choice=1')
    energy_period_index_mat: Final[Array] = OUTPUT(label='Wave period index locations for time series', units='s', type='ARRAY', group='MHKWave', required='wave_resource_model_choice=1')
    energy_period_data: Final[Array] = OUTPUT(label='Energy period time series data', units='s', type='ARRAY', group='MHKWave', required='wave_resource_model_choice=1')
    wave_power_index_mat: Final[Array] = OUTPUT(label='Wave power for time series', units='kW', type='ARRAY', group='MHKWave', required='wave_resource_model_choice=1')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='MHKWave', required='*')
    numberRecords: Final[float] = OUTPUT(label='Number of Records', type='NUMBER', group='MHKWave')
    numberHours: Final[float] = OUTPUT(label='Number of Hours', type='NUMBER', group='MHKWave')
    annual_energy_distribution: Final[Matrix] = OUTPUT(label='Annual energy production as function of Hs and Te', units='kWh', type='MATRIX', group='MHKWave')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of Time', units='kWh', type='MATRIX', group='MHKWave')
    wave_resource_start_height: Final[float] = OUTPUT(label='Wave height at which first non-zero wave resource value occurs (m)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_resource_start_period: Final[float] = OUTPUT(label='Wave period at which first non-zero wave resource value occurs (s)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_resource_end_height: Final[float] = OUTPUT(label='Wave height at which last non-zero wave resource value occurs (m)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_resource_end_period: Final[float] = OUTPUT(label='Wave period at which last non-zero wave resource value occurs (s)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_power_start_height: Final[float] = OUTPUT(label='Wave height at which first non-zero WEC power output occurs (m)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_power_start_period: Final[float] = OUTPUT(label='Wave period at which first non-zero WEC power output occurs (s)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_power_end_height: Final[float] = OUTPUT(label='Wave height at which last non-zero WEC power output occurs (m)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    wave_power_end_period: Final[float] = OUTPUT(label='Wave period at which last non-zero WEC power output occurs (s)', type='NUMBER', group='MHKWave', required='wave_resource_model_choice=0')
    total_capital_cost_kwh: Final[float] = OUTPUT(label='Capital costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKWave')
    total_device_cost_kwh: Final[float] = OUTPUT(label='Device costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKWave')
    total_bos_cost_kwh: Final[float] = OUTPUT(label='Balance of system costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKWave')
    total_financial_cost_kwh: Final[float] = OUTPUT(label='Financial costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKWave')
    total_om_cost_kwh: Final[float] = OUTPUT(label='O&M costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKWave')
    total_capital_cost_lcoe: Final[float] = OUTPUT(label='Capital cost as percentage of overall LCOE', units='%', type='NUMBER', group='MHKWave')
    total_device_cost_lcoe: Final[float] = OUTPUT(label='Device cost', units='%', type='NUMBER', group='MHKWave')
    total_bos_cost_lcoe: Final[float] = OUTPUT(label='BOS cost', units='%', type='NUMBER', group='MHKWave')
    total_financial_cost_lcoe: Final[float] = OUTPUT(label='Financial cost', units='%', type='NUMBER', group='MHKWave')
    total_om_cost_lcoe: Final[float] = OUTPUT(label='O&M cost (annual)', units='%', type='NUMBER', group='MHKWave')
    total_capital_cost_per_kw: Final[float] = OUTPUT(label='Capital cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_device_cost_per_kw: Final[float] = OUTPUT(label='Device cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_bos_cost_per_kw: Final[float] = OUTPUT(label='Balance of Systems cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_financial_cost_per_kw: Final[float] = OUTPUT(label='Financial cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_operations_cost_per_kw: Final[float] = OUTPUT(label='O&M cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')

    def __init__(self, *args: Mapping[str, Any],
                 wave_resource_model_choice: float = ...,
                 wave_resource_matrix: Matrix = ...,
                 wave_resource_data: Table = ...,
                 significant_wave_height: Array = ...,
                 energy_period: Array = ...,
                 wave_power_matrix: Matrix = ...,
                 number_devices: float = ...,
                 system_capacity: float = ...,
                 number_hours: float = ...,
                 number_records: float = ...,
                 me_adjust_constant: float = ...,
                 me_adjust_hourly: Array = ...,
                 me_adjust_timeindex: Array = ...,
                 me_adjust_periods: Matrix = ...,
                 device_rated_power: float = ...,
                 fixed_charge_rate: float = ...,
                 device_costs_total: float = ...,
                 balance_of_system_cost_total: float = ...,
                 financial_cost_total: float = ...,
                 total_operating_cost: float = ...,
                 system_use_lifetime_output: float = ...,
                 analysis_period: float = ...,
                 generic_degradation: Array = ...,
                 loss_array_spacing: float = ...,
                 loss_resource_overprediction: float = ...,
                 loss_transmission: float = ...,
                 loss_downtime: float = ...,
                 loss_additional: float = ...,
                 year: Array = ...,
                 month: Array = ...,
                 day: Array = ...,
                 hour: Array = ...,
                 minute: Array = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
