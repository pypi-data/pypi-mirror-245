
# This is a generated file

"""mhk_tidal - MHK Tidal power calculation model using power distribution."""

# VERSION: 3

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'tidal_resource': Matrix,
    'tidal_power_curve': Matrix,
    'number_devices': float,
    'fixed_charge_rate': float,
    'device_costs_total': float,
    'balance_of_system_cost_total': float,
    'financial_cost_total': float,
    'total_operating_cost': float,
    'system_capacity': float,
    'loss_array_spacing': float,
    'loss_resource_overprediction': float,
    'loss_transmission': float,
    'loss_downtime': float,
    'loss_additional': float,
    'device_rated_capacity': float,
    'device_average_power': float,
    'annual_energy': float,
    'capacity_factor': float,
    'annual_energy_distribution': Array,
    'annual_cumulative_energy_distribution': Array,
    'tidal_resource_start_velocity': float,
    'tidal_resource_end_velocity': float,
    'tidal_power_start_velocity': float,
    'tidal_power_end_velocity': float,
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
    tidal_resource: Matrix = INPUT(label='Frequency distribution of resource as a function of stream speeds', type='MATRIX', group='MHKTidal', required='*')
    tidal_power_curve: Matrix = INPUT(label='Power curve of tidal energy device as function of stream speeds', units='kW', type='MATRIX', group='MHKTidal', required='*')
    number_devices: float = INPUT(label='Number of tidal devices in the system', type='NUMBER', group='MHKTidal', required='?=1', constraints='INTEGER')
    fixed_charge_rate: float = INPUT(label='FCR from LCOE Cost page', type='NUMBER', group='MHKTidal', required='?=1')
    device_costs_total: float = INPUT(label='Device costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    balance_of_system_cost_total: float = INPUT(label='BOS costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    financial_cost_total: float = INPUT(label='Financial costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    total_operating_cost: float = INPUT(label='O&M costs', units='$', type='NUMBER', group='MHKTidal', required='?=1')
    system_capacity: float = INPUT(label='System Nameplate Capacity', units='kW', type='NUMBER', group='MHKTidal', required='?=0')
    loss_array_spacing: float = INPUT(label='Array spacing loss', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_resource_overprediction: float = INPUT(label='Resource overprediction loss', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_transmission: float = INPUT(label='Transmission losses', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_downtime: float = INPUT(label='Array/WEC downtime loss', units='%', type='NUMBER', group='MHKTidal', required='*')
    loss_additional: float = INPUT(label='Additional losses', units='%', type='NUMBER', group='MHKTidal', required='*')
    device_rated_capacity: Final[float] = OUTPUT(label='Rated capacity of device', units='kW', type='NUMBER', group='MHKTidal')
    device_average_power: Final[float] = OUTPUT(label='Average power production of a single device', units='kW', type='NUMBER', group='MHKTidal', required='*')
    annual_energy: Final[float] = OUTPUT(label='Annual energy production of array', units='kWh', type='NUMBER', group='MHKTidal', required='*')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', group='MHKTidal', required='*')
    annual_energy_distribution: Final[Array] = OUTPUT(label='Annual energy production of array as function of speed', units='kWh', type='ARRAY', group='MHKTidal', required='*')
    annual_cumulative_energy_distribution: Final[Array] = OUTPUT(label='Cumulative annual energy production of array as function of speed', units='kWh', type='ARRAY', group='MHKTidal', required='*')
    tidal_resource_start_velocity: Final[float] = OUTPUT(label='First tidal velocity where probability distribution is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    tidal_resource_end_velocity: Final[float] = OUTPUT(label='Last tidal velocity where probability distribution is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    tidal_power_start_velocity: Final[float] = OUTPUT(label='First tidal velocity where power curve is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    tidal_power_end_velocity: Final[float] = OUTPUT(label='Last tidal velocity where power curve is greater than 0 ', units='m/s', type='NUMBER', group='MHKTidal', required='*')
    total_capital_cost_kwh: Final[float] = OUTPUT(label='Capital costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_device_cost_kwh: Final[float] = OUTPUT(label='Device costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_bos_cost_kwh: Final[float] = OUTPUT(label='Balance of system costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_financial_cost_kwh: Final[float] = OUTPUT(label='Financial costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_om_cost_kwh: Final[float] = OUTPUT(label='O&M costs per unit annual energy', units='$/kWh', type='NUMBER', group='MHKTidal', required='*')
    total_capital_cost_lcoe: Final[float] = OUTPUT(label='Capital cost as percentage of overall LCOE', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_device_cost_lcoe: Final[float] = OUTPUT(label='Device cost', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_bos_cost_lcoe: Final[float] = OUTPUT(label='BOS cost', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_financial_cost_lcoe: Final[float] = OUTPUT(label='Financial cost', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_om_cost_lcoe: Final[float] = OUTPUT(label='O&M cost (annual)', units='%', type='NUMBER', group='MHKTidal', required='*')
    total_capital_cost_per_kw: Final[float] = OUTPUT(label='Capital cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_device_cost_per_kw: Final[float] = OUTPUT(label='Device cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_bos_cost_per_kw: Final[float] = OUTPUT(label='Balance of Systems cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_financial_cost_per_kw: Final[float] = OUTPUT(label='Financial cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')
    total_operations_cost_per_kw: Final[float] = OUTPUT(label='O&M cost per kW', units='$/kW', type='NUMBER', group='MHKCosts')

    def __init__(self, *args: Mapping[str, Any],
                 tidal_resource: Matrix = ...,
                 tidal_power_curve: Matrix = ...,
                 number_devices: float = ...,
                 fixed_charge_rate: float = ...,
                 device_costs_total: float = ...,
                 balance_of_system_cost_total: float = ...,
                 financial_cost_total: float = ...,
                 total_operating_cost: float = ...,
                 system_capacity: float = ...,
                 loss_array_spacing: float = ...,
                 loss_resource_overprediction: float = ...,
                 loss_transmission: float = ...,
                 loss_downtime: float = ...,
                 loss_additional: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
