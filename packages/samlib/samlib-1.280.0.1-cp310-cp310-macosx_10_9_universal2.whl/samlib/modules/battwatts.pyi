
# This is a generated file

"""battwatts - simple battery model"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'system_use_lifetime_output': float,
    'analysis_period': float,
    'batt_simple_enable': float,
    'batt_simple_kwh': float,
    'batt_simple_kw': float,
    'batt_simple_chemistry': float,
    'batt_simple_dispatch': float,
    'batt_custom_dispatch': Array,
    'batt_simple_meter_position': float,
    'dc': Array,
    'ac': Array,
    'load': Array,
    'crit_load': Array,
    'grid_outage': Array,
    'run_resiliency_calcs': float,
    'load_escalation': Array,
    'inverter_efficiency': float,
    'batt_q0': Array,
    'batt_q1': Array,
    'batt_q2': Array,
    'batt_SOC': Array,
    'batt_DOD': Array,
    'batt_qmaxI': Array,
    'batt_qmax': Array,
    'batt_qmax_thermal': Array,
    'batt_I': Array,
    'batt_voltage_cell': Array,
    'batt_voltage': Array,
    'batt_DOD_cycle_average': Array,
    'batt_cycles': Array,
    'batt_temperature': Array,
    'batt_capacity_percent': Array,
    'batt_capacity_percent_cycle': Array,
    'batt_capacity_percent_calendar': Array,
    'batt_capacity_thermal_percent': Array,
    'batt_bank_replacement': Array,
    'batt_power': Array,
    'batt_power_dc': Array,
    'grid_power': Array,
    'system_to_load': Array,
    'batt_to_load': Array,
    'grid_to_load': Array,
    'system_to_batt': Array,
    'system_to_batt_dc': Array,
    'fuelcell_to_batt': Array,
    'grid_to_batt': Array,
    'system_to_grid': Array,
    'batt_to_grid': Array,
    'batt_to_system_load': Array,
    'interconnection_loss': Array,
    'batt_conversion_loss': Array,
    'batt_system_loss': Array,
    'batt_to_inverter_dc': Array,
    'grid_power_target': Array,
    'batt_power_target': Array,
    'batt_cost_to_cycle': Array,
    'market_sell_rate_series_yr1': Array,
    'batt_revenue_gridcharge': Array,
    'batt_revenue_charge': Array,
    'batt_revenue_clipcharge': Array,
    'batt_revenue_discharge': Array,
    'gen_without_battery': Array,
    'crit_load_unmet': Array,
    'outage_losses_unmet': Array,
    'batt_pvs_PV_ramp_interval': Array,
    'batt_pvs_forecast_pv_energy': Array,
    'batt_pvs_P_pv_ac': Array,
    'batt_pvs_outpower': Array,
    'batt_pvs_battpower': Array,
    'batt_pvs_battsoc': Array,
    'batt_pvs_curtail': Array,
    'batt_pvs_violation_list': Array,
    'batt_pvs_violation_count': float,
    'batt_pvs_violation_percent': float,
    'batt_pvs_energy_to_grid_percent': float,
    'batt_pvs_energy_to_grid_percent_sam': float,
    'monthly_system_to_load': Array,
    'monthly_batt_to_load': Array,
    'monthly_grid_to_load': Array,
    'monthly_system_to_grid': Array,
    'monthly_batt_to_grid': Array,
    'monthly_system_to_batt': Array,
    'monthly_grid_to_batt': Array,
    'monthly_interconnection_loss': Array,
    'monthly_crit_load_unmet': Array,
    'monthly_crit_load_unmet_percentage': Array,
    'monthly_crit_load': Array,
    'monthly_outage_losses_unmet': Array,
    'monthly_batt_to_system_load': Array,
    'batt_annual_charge_from_system': Array,
    'batt_annual_charge_from_grid': Array,
    'batt_annual_charge_energy': Array,
    'batt_annual_discharge_energy': Array,
    'batt_annual_energy_loss': Array,
    'batt_annual_energy_system_loss': Array,
    'annual_export_to_grid_energy': Array,
    'annual_import_to_grid_energy': Array,
    'average_battery_conversion_efficiency': float,
    'average_battery_roundtrip_efficiency': float,
    'batt_system_charge_percent': float,
    'batt_bank_installed_capacity': float,
    'annual_crit_load': float,
    'annual_crit_load_unmet': float,
    'annual_crit_load_unmet_percentage': float,
    'annual_outage_losses_unmet': float,
    'batt_dispatch_sched': Matrix,
    'gen': Array,
    'annual_energy_distribution_time': Matrix,
    'resilience_hrs': Array,
    'resilience_hrs_min': float,
    'resilience_hrs_max': float,
    'resilience_hrs_avg': float,
    'outage_durations': Array,
    'pdf_of_surviving': Array,
    'cdf_of_surviving': Array,
    'survival_function': Array,
    'avg_critical_load': float,
    'grid_curtailment': Array,
    'enable_interconnection_limit': float,
    'grid_interconnection_limit_kwac': float
}, total=False)

class Data(ssc.DataDict):
    system_use_lifetime_output: float = INPUT(label='Enable lifetime simulation', units='0/1', type='NUMBER', group='Lifetime', required='?=0', constraints='BOOLEAN', meta='0=SingleYearRepeated,1=RunEveryYear')
    analysis_period: float = INPUT(label='Lifetime analysis period', units='years', type='NUMBER', group='Lifetime', required='system_use_lifetime_output=1', meta='The number of years in the simulation')
    batt_simple_enable: float = INPUT(label='Enable Battery', units='0/1', type='NUMBER', group='Battery', required='?=0', constraints='BOOLEAN')
    batt_simple_kwh: float = INPUT(label='Battery Capacity', units='kWh', type='NUMBER', group='Battery', required='?=0')
    batt_simple_kw: float = INPUT(label='Battery Power', units='kW', type='NUMBER', group='Battery', required='?=0')
    batt_simple_chemistry: float = INPUT(label='Battery Chemistry', units='0=LeadAcid,1=Li-ion/2', type='NUMBER', group='Battery', required='?=0')
    batt_simple_dispatch: float = INPUT(label='Battery Dispatch', units='0=PeakShavingLookAhead,1=PeakShavingLookBehind,2=Custom', type='NUMBER', group='Battery', required='?=0')
    batt_custom_dispatch: Array = INPUT(label='Battery Dispatch', units='kW', type='ARRAY', group='Battery', required='batt_simple_dispatch=2')
    batt_simple_meter_position: float = INPUT(label='Battery Meter Position', units='0=BehindTheMeter,1=FrontOfMeter', type='NUMBER', group='Battery', required='?=0')
    dc: Array = INPUT(label='DC array power', units='W', type='ARRAY', group='Battery')
    ac: Array = INPUT(label='AC inverter power', units='W', type='ARRAY', group='Battery')
    load: Array = INPUT(label='Electricity load (year 1)', units='kW', type='ARRAY', group='Battery')
    crit_load: Array = INPUT(label='Critical electricity load (year 1)', units='kW', type='ARRAY', group='Battery')
    grid_outage: Array = INPUT(label='Grid outage in this time step', units='0/1', type='ARRAY', group='Load', meta='0=GridAvailable,1=GridUnavailable,Length=load')
    run_resiliency_calcs: float = INPUT(label='Enable resilence calculations for every timestep', units='0/1', type='NUMBER', group='Load', required='?=0', meta='0=DisableCalcs,1=EnableCalcs')
    load_escalation: Array = INPUT(label='Annual load escalation', units='%/year', type='ARRAY', group='Load', required='?=0')
    inverter_efficiency: float = INPUT(label='Inverter Efficiency', units='%', type='NUMBER', group='Battery', constraints='MIN=0,MAX=100')
    batt_q0: Final[Array] = OUTPUT(label='Battery total charge', units='Ah', type='ARRAY', group='Battery')
    batt_q1: Final[Array] = OUTPUT(label='Battery available charge', units='Ah', type='ARRAY', group='Battery')
    batt_q2: Final[Array] = OUTPUT(label='Battery bound charge', units='Ah', type='ARRAY', group='Battery')
    batt_SOC: Final[Array] = OUTPUT(label='Battery state of charge', units='%', type='ARRAY', group='Battery')
    batt_DOD: Final[Array] = OUTPUT(label='Battery cycle depth of discharge', units='%', type='ARRAY', group='Battery')
    batt_qmaxI: Final[Array] = OUTPUT(label='Battery maximum capacity at current', units='Ah', type='ARRAY', group='Battery')
    batt_qmax: Final[Array] = OUTPUT(label='Battery maximum charge with degradation', units='Ah', type='ARRAY', group='Battery')
    batt_qmax_thermal: Final[Array] = OUTPUT(label='Battery maximum charge at temperature', units='Ah', type='ARRAY', group='Battery')
    batt_I: Final[Array] = OUTPUT(label='Battery current', units='A', type='ARRAY', group='Battery')
    batt_voltage_cell: Final[Array] = OUTPUT(label='Battery cell voltage', units='V', type='ARRAY', group='Battery')
    batt_voltage: Final[Array] = OUTPUT(label='Battery voltage', units='V', type='ARRAY', group='Battery')
    batt_DOD_cycle_average: Final[Array] = OUTPUT(label='Battery average cycle DOD', type='ARRAY', group='Battery')
    batt_cycles: Final[Array] = OUTPUT(label='Battery number of cycles', type='ARRAY', group='Battery')
    batt_temperature: Final[Array] = OUTPUT(label='Battery temperature', units='C', type='ARRAY', group='Battery')
    batt_capacity_percent: Final[Array] = OUTPUT(label='Battery relative capacity to nameplate', units='%', type='ARRAY', group='Battery')
    batt_capacity_percent_cycle: Final[Array] = OUTPUT(label='Battery relative capacity to nameplate (cycling)', units='%', type='ARRAY', group='Battery')
    batt_capacity_percent_calendar: Final[Array] = OUTPUT(label='Battery relative capacity to nameplate (calendar)', units='%', type='ARRAY', group='Battery')
    batt_capacity_thermal_percent: Final[Array] = OUTPUT(label='Battery capacity percent for temperature', units='%', type='ARRAY', group='Battery')
    batt_bank_replacement: Final[Array] = OUTPUT(label='Battery bank replacements per year', units='number/year', type='ARRAY', group='Battery')
    batt_power: Final[Array] = OUTPUT(label='Electricity to/from battery AC', units='kW', type='ARRAY', group='Battery')
    batt_power_dc: Final[Array] = OUTPUT(label='Electricity to/from battery DC', units='kW', type='ARRAY', group='Battery')
    grid_power: Final[Array] = OUTPUT(label='Electricity to/from grid AC', units='kW', type='ARRAY', group='Battery')
    system_to_load: Final[Array] = OUTPUT(label='Electricity to load from system AC', units='kW', type='ARRAY', group='Battery')
    batt_to_load: Final[Array] = OUTPUT(label='Electricity to load from battery AC', units='kW', type='ARRAY', group='Battery')
    grid_to_load: Final[Array] = OUTPUT(label='Electricity to load from grid AC', units='kW', type='ARRAY', group='Battery')
    system_to_batt: Final[Array] = OUTPUT(label='Electricity to battery from system AC', units='kW', type='ARRAY', group='Battery')
    system_to_batt_dc: Final[Array] = OUTPUT(label='Electricity to battery from system DC', units='kW', type='ARRAY', group='Battery')
    fuelcell_to_batt: Final[Array] = OUTPUT(label='Electricity to battery from fuel cell AC', units='kW', type='ARRAY', group='Battery')
    grid_to_batt: Final[Array] = OUTPUT(label='Electricity to battery from grid AC', units='kW', type='ARRAY', group='Battery')
    system_to_grid: Final[Array] = OUTPUT(label='Electricity to grid from system AC', units='kW', type='ARRAY', group='Battery')
    batt_to_grid: Final[Array] = OUTPUT(label='Electricity to grid from battery AC', units='kW', type='ARRAY', group='Battery')
    batt_to_system_load: Final[Array] = OUTPUT(label='Electricity to system loads from battery AC', units='kW', type='ARRAY', group='Battery')
    interconnection_loss: Final[Array] = OUTPUT(label='Electricity loss due to curtailment interconnection outage', units='kW', type='ARRAY', group='Battery')
    batt_conversion_loss: Final[Array] = OUTPUT(label='Battery loss from power electronics', units='kW', type='ARRAY', group='Battery')
    batt_system_loss: Final[Array] = OUTPUT(label='Battery loss from ancillary equipment', units='kW', type='ARRAY', group='Battery')
    batt_to_inverter_dc: Final[Array] = OUTPUT(label='Electricity to inverter from battery DC', units='kW', type='ARRAY', group='Battery')
    grid_power_target: Final[Array] = OUTPUT(label='Electricity grid power target for automated dispatch', units='kW', type='ARRAY', group='Battery')
    batt_power_target: Final[Array] = OUTPUT(label='Electricity battery power target for automated dispatch', units='kW', type='ARRAY', group='Battery')
    batt_cost_to_cycle: Final[Array] = OUTPUT(label='Battery computed cycle degradation penalty', units='$/cycle-kWh', type='ARRAY', group='Battery')
    market_sell_rate_series_yr1: Final[Array] = OUTPUT(label='Power price for battery dispatch', units='$/MWh', type='ARRAY', group='Battery')
    batt_revenue_gridcharge: Final[Array] = OUTPUT(label='Revenue to charge from grid', units='$/kWh', type='ARRAY', group='Battery')
    batt_revenue_charge: Final[Array] = OUTPUT(label='Revenue to charge from system', units='$/kWh', type='ARRAY', group='Battery')
    batt_revenue_clipcharge: Final[Array] = OUTPUT(label='Revenue to charge from clipped', units='$/kWh', type='ARRAY', group='Battery')
    batt_revenue_discharge: Final[Array] = OUTPUT(label='Revenue to discharge', units='$/kWh', type='ARRAY', group='Battery')
    gen_without_battery: Final[Array] = OUTPUT(label='Power produced without the battery or curtailment', units='kW', type='ARRAY', group='Battery')
    crit_load_unmet: Final[Array] = OUTPUT(label='Critical load unmet in this timestep', units='kW', type='ARRAY', group='Battery')
    outage_losses_unmet: Final[Array] = OUTPUT(label='Battery and system losses unmet in this timestep', units='kW', type='ARRAY', group='Battery')
    batt_pvs_PV_ramp_interval: Final[Array] = OUTPUT(label='PV smoothing PV power sampled', units='kW', type='ARRAY', group='Battery')
    batt_pvs_forecast_pv_energy: Final[Array] = OUTPUT(label='PV smoothing PV power forecast', units='kW', type='ARRAY', group='Battery')
    batt_pvs_P_pv_ac: Final[Array] = OUTPUT(label='PV smoothing PV power before smoothing', units='kW', type='ARRAY', group='Battery')
    batt_pvs_outpower: Final[Array] = OUTPUT(label='PV smoothing outpower', units='kW', type='ARRAY', group='Battery')
    batt_pvs_battpower: Final[Array] = OUTPUT(label='PV smoothing battpower', units='kW', type='ARRAY', group='Battery')
    batt_pvs_battsoc: Final[Array] = OUTPUT(label='PV smoothing battery SOC', units='%', type='ARRAY', group='Battery')
    batt_pvs_curtail: Final[Array] = OUTPUT(label='PV smoothing curtailed power', units='kW', type='ARRAY', group='Battery')
    batt_pvs_violation_list: Final[Array] = OUTPUT(label='PV smoothing violation', type='ARRAY', group='Battery')
    batt_pvs_violation_count: Final[float] = OUTPUT(label='PV smoothing violation count', type='NUMBER', group='Battery')
    batt_pvs_violation_percent: Final[float] = OUTPUT(label='PV smoothing violation percent (of all intervals-including nighttime)', units='%', type='NUMBER', group='Battery')
    batt_pvs_energy_to_grid_percent: Final[float] = OUTPUT(label='PV smoothing energy to grid percent (loss due to curtail and battery loss)', units='%', type='NUMBER', group='Battery')
    batt_pvs_energy_to_grid_percent_sam: Final[float] = OUTPUT(label='PV smoothing energy to grid percent actual (loss due to curtail and battery loss)', units='%', type='NUMBER', group='Battery')
    monthly_system_to_load: Final[Array] = OUTPUT(label='Energy to load from system', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_batt_to_load: Final[Array] = OUTPUT(label='Energy to load from battery', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_grid_to_load: Final[Array] = OUTPUT(label='Energy to load from grid', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_system_to_grid: Final[Array] = OUTPUT(label='Energy to grid from system', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_batt_to_grid: Final[Array] = OUTPUT(label='Energy to grid from battery', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_system_to_batt: Final[Array] = OUTPUT(label='Energy to battery from system', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_grid_to_batt: Final[Array] = OUTPUT(label='Energy to battery from grid', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_interconnection_loss: Final[Array] = OUTPUT(label='Energy loss due to curtailment, interconnection, or outage', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH = 12')
    monthly_crit_load_unmet: Final[Array] = OUTPUT(label='Critical load energy unmet', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_crit_load_unmet_percentage: Final[Array] = OUTPUT(label='Critical load unmet percentage', units='%', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_crit_load: Final[Array] = OUTPUT(label='Critical load energy', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_outage_losses_unmet: Final[Array] = OUTPUT(label='Battery and system losses unmet energy', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    monthly_batt_to_system_load: Final[Array] = OUTPUT(label='Energy to system loads from battery', units='kWh', type='ARRAY', group='Battery', constraints='LENGTH=12')
    batt_annual_charge_from_system: Final[Array] = OUTPUT(label='Battery annual energy charged from system', units='kWh', type='ARRAY', group='Battery')
    batt_annual_charge_from_grid: Final[Array] = OUTPUT(label='Battery annual energy charged from grid', units='kWh', type='ARRAY', group='Battery')
    batt_annual_charge_energy: Final[Array] = OUTPUT(label='Battery annual energy charged', units='kWh', type='ARRAY', group='Battery')
    batt_annual_discharge_energy: Final[Array] = OUTPUT(label='Battery annual energy discharged', units='kWh', type='ARRAY', group='Battery')
    batt_annual_energy_loss: Final[Array] = OUTPUT(label='Battery annual energy loss', units='kWh', type='ARRAY', group='Battery')
    batt_annual_energy_system_loss: Final[Array] = OUTPUT(label='Battery annual system energy loss', units='kWh', type='ARRAY', group='Battery')
    annual_export_to_grid_energy: Final[Array] = OUTPUT(label='Annual energy exported to grid', units='kWh', type='ARRAY', group='Battery')
    annual_import_to_grid_energy: Final[Array] = OUTPUT(label='Annual energy imported from grid', units='kWh', type='ARRAY', group='Battery')
    average_battery_conversion_efficiency: Final[float] = OUTPUT(label='Battery average cycle conversion efficiency', units='%', type='NUMBER', group='Annual')
    average_battery_roundtrip_efficiency: Final[float] = OUTPUT(label='Battery average roundtrip efficiency', units='%', type='NUMBER', group='Annual')
    batt_system_charge_percent: Final[float] = OUTPUT(label='Battery charge energy charged from system', units='%', type='NUMBER', group='Annual')
    batt_bank_installed_capacity: Final[float] = OUTPUT(label='Battery bank installed capacity', units='kWh', type='NUMBER', group='Annual')
    annual_crit_load: Final[float] = OUTPUT(label='Critical load energy (year 1)', units='kWh', type='NUMBER', group='Battery')
    annual_crit_load_unmet: Final[float] = OUTPUT(label='Critical load energy unmet (year 1)', units='kWh', type='NUMBER', group='Battery')
    annual_crit_load_unmet_percentage: Final[float] = OUTPUT(label='Critical load unmet percentage (year 1)', units='%', type='NUMBER', group='Battery')
    annual_outage_losses_unmet: Final[float] = OUTPUT(label='Battery and system losses unmet energy (year 1)', units='kWh', type='NUMBER', group='Battery')
    batt_dispatch_sched: Final[Matrix] = OUTPUT(label='Battery dispatch schedule', type='MATRIX', group='Battery')
    gen: Final[Array] = OUTPUT(label='System power generated', units='kW', type='ARRAY', group='Time Series', required='*')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of time', units='kW', type='MATRIX', group='Heatmaps')
    resilience_hrs: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage at each timestep', units='hr', type='ARRAY', group='Resilience')
    resilience_hrs_min: Final[float] = OUTPUT(label='Hours of autonomy during grid outage minimum', units='hr', type='NUMBER', group='Resilience', constraints='MIN=0')
    resilience_hrs_max: Final[float] = OUTPUT(label='Hours of autonomy during grid outage maximum', units='hr', type='NUMBER', group='Resilience', constraints='MIN=0')
    resilience_hrs_avg: Final[float] = OUTPUT(label='Hours of autonomy during grid outage average', units='hr', type='NUMBER', group='Resilience', constraints='MIN=0')
    outage_durations: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage hour list from min to max', units='hr', type='ARRAY', group='Resilience', meta='Hours from resilience_hrs_min to resilience_hrs_max')
    pdf_of_surviving: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage probabilities', type='ARRAY', group='Resilience', constraints='MIN=0,MAX=1', meta='Hours from resilience_hrs_min to resilience_hrs_max')
    cdf_of_surviving: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage cumulative probabilities', type='ARRAY', group='Resilience', constraints='MIN=0,MAX=1', meta='Prob surviving at least x hrs; hrs from min to max')
    survival_function: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage survival function', type='ARRAY', group='Resilience', constraints='MIN=0,MAX=1', meta='Prob surviving greater than x hours; hrs from min to max')
    avg_critical_load: Final[float] = OUTPUT(label='Hours of autonomy during grid outage critical load met', units='kWh', type='NUMBER', group='Resilience', constraints='MIN=0')
    grid_curtailment: Array = INPUT(label='Grid curtailment as energy delivery limit (first year)', units='MW', type='ARRAY', group='GridLimits', required='?')
    enable_interconnection_limit: float = INPUT(label='Enable grid interconnection limit', units='0/1', type='NUMBER', group='GridLimits', meta='Enable a grid interconnection limit')
    grid_interconnection_limit_kwac: float = INPUT(label='Grid interconnection limit', units='kWac', type='NUMBER', group='GridLimits')

    def __init__(self, *args: Mapping[str, Any],
                 system_use_lifetime_output: float = ...,
                 analysis_period: float = ...,
                 batt_simple_enable: float = ...,
                 batt_simple_kwh: float = ...,
                 batt_simple_kw: float = ...,
                 batt_simple_chemistry: float = ...,
                 batt_simple_dispatch: float = ...,
                 batt_custom_dispatch: Array = ...,
                 batt_simple_meter_position: float = ...,
                 dc: Array = ...,
                 ac: Array = ...,
                 load: Array = ...,
                 crit_load: Array = ...,
                 grid_outage: Array = ...,
                 run_resiliency_calcs: float = ...,
                 load_escalation: Array = ...,
                 inverter_efficiency: float = ...,
                 grid_curtailment: Array = ...,
                 enable_interconnection_limit: float = ...,
                 grid_interconnection_limit_kwac: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
