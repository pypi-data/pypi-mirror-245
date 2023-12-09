
# This is a generated file

"""battery - Battery storage standalone model ."""

# VERSION: 10

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'percent_complete': float,
    'system_use_lifetime_output': float,
    'analysis_period': float,
    'en_batt': float,
    'en_standalone_batt': float,
    'en_wave_batt': float,
    'energy_hourly_kW': Array,
    'gen': Array,
    'load': Array,
    'crit_load': Array,
    'load_escalation': Array,
    'crit_load_escalation': Array,
    'grid_outage': Array,
    'run_resiliency_calcs': float,
    'capacity_factor': float,
    'capacity_factor_sales': float,
    'annual_energy': float,
    'batt_chem': float,
    'inverter_model': float,
    'inverter_count': float,
    'inv_snl_eff_cec': float,
    'inv_snl_paco': float,
    'inv_ds_eff': float,
    'inv_ds_paco': float,
    'inv_pd_eff': float,
    'inv_pd_paco': float,
    'inv_cec_cg_eff_cec': float,
    'inv_cec_cg_paco': float,
    'batt_ac_or_dc': float,
    'batt_dc_dc_efficiency': float,
    'dcoptimizer_loss': float,
    'batt_dc_ac_efficiency': float,
    'batt_ac_dc_efficiency': float,
    'batt_meter_position': float,
    'batt_inverter_efficiency_cutoff': float,
    'batt_losses': Array,
    'batt_losses_charging': Array,
    'batt_losses_discharging': Array,
    'batt_losses_idle': Array,
    'batt_loss_choice': float,
    'batt_current_choice': float,
    'batt_computed_strings': float,
    'batt_computed_series': float,
    'batt_computed_bank_capacity': float,
    'batt_current_charge_max': float,
    'batt_current_discharge_max': float,
    'batt_power_charge_max_kwdc': float,
    'batt_power_discharge_max_kwdc': float,
    'batt_power_charge_max_kwac': float,
    'batt_power_discharge_max_kwac': float,
    'batt_voltage_choice': float,
    'batt_Vfull': float,
    'batt_Vexp': float,
    'batt_Vnom': float,
    'batt_Vnom_default': float,
    'batt_Qfull': float,
    'batt_Qfull_flow': float,
    'batt_Qexp': float,
    'batt_Qnom': float,
    'batt_Vcut': float,
    'batt_C_rate': float,
    'batt_resistance': float,
    'batt_voltage_matrix': Matrix,
    'LeadAcid_q20_computed': float,
    'LeadAcid_q10_computed': float,
    'LeadAcid_qn_computed': float,
    'LeadAcid_tn': float,
    'batt_initial_SOC': float,
    'batt_minimum_SOC': float,
    'batt_minimum_outage_SOC': float,
    'batt_maximum_SOC': float,
    'batt_minimum_modetime': float,
    'batt_life_model': float,
    'batt_lifetime_matrix': Matrix,
    'batt_calendar_choice': float,
    'batt_calendar_lifetime_matrix': Matrix,
    'batt_calendar_q0': float,
    'batt_calendar_a': float,
    'batt_calendar_b': float,
    'batt_calendar_c': float,
    'batt_replacement_capacity': float,
    'batt_replacement_option': float,
    'batt_replacement_schedule_percent': Array,
    'om_replacement_cost1': Array,
    'batt_mass': float,
    'batt_surface_area': float,
    'batt_Cp': float,
    'batt_h_to_ambient': float,
    'batt_room_temperature_celsius': Array,
    'cap_vs_temp': Matrix,
    'dispatch_manual_charge': Array,
    'dispatch_manual_fuelcellcharge': Array,
    'dispatch_manual_discharge': Array,
    'dispatch_manual_btm_discharge_to_grid': Array,
    'dispatch_manual_gridcharge': Array,
    'dispatch_manual_percent_discharge': Array,
    'dispatch_manual_percent_gridcharge': Array,
    'dispatch_manual_sched': Matrix,
    'dispatch_manual_sched_weekend': Matrix,
    'dispatch_manual_system_charge_first': float,
    'batt_target_power': Array,
    'batt_target_power_monthly': Array,
    'batt_target_choice': float,
    'batt_custom_dispatch': Array,
    'batt_dispatch_choice': float,
    'batt_dispatch_auto_can_fuelcellcharge': float,
    'batt_dispatch_auto_can_gridcharge': float,
    'batt_dispatch_auto_can_charge': float,
    'batt_dispatch_auto_can_clipcharge': float,
    'batt_dispatch_auto_btm_can_discharge_to_grid': float,
    'batt_dispatch_charge_only_system_exceeds_load': float,
    'batt_dispatch_discharge_only_load_exceeds_system': float,
    'batt_look_ahead_hours': float,
    'batt_dispatch_update_frequency_hours': float,
    'batt_dispatch_pvs_nameplate_ac': float,
    'batt_dispatch_pvs_ac_lb_enable': float,
    'batt_dispatch_pvs_ac_lb': float,
    'batt_dispatch_pvs_ac_ub_enable': float,
    'batt_dispatch_pvs_ac_ub': float,
    'batt_dispatch_pvs_curtail_as_control': float,
    'batt_dispatch_pvs_curtail_if_violation': float,
    'batt_dispatch_pvs_short_forecast_enable': float,
    'batt_dispatch_pvs_forecast_shift_periods': float,
    'batt_dispatch_pvs_timestep_multiplier': float,
    'batt_dispatch_pvs_max_ramp': float,
    'batt_dispatch_pvs_soc_rest': float,
    'batt_dispatch_pvs_kp': float,
    'batt_dispatch_pvs_ki': float,
    'batt_dispatch_pvs_kf': float,
    'batt_dispatch_wf_forecast_choice': float,
    'batt_dispatch_load_forecast_choice': float,
    'batt_pv_clipping_forecast': Array,
    'batt_pv_ac_forecast': Array,
    'batt_load_ac_forecast': Array,
    'batt_load_ac_forecast_escalation': Array,
    'batt_cycle_cost_choice': float,
    'batt_cycle_cost': Array,
    'inflation_rate': float,
    'om_batt_replacement_cost': Array,
    'om_replacement_cost_escal': float,
    'om_batt_variable_cost': Array,
    'om_production_escal': float,
    'fuelcell_power': Array,
    'forecast_price_signal_model': float,
    'ppa_price_input': Array,
    'ppa_multiplier_model': float,
    'ppa_escalation': float,
    'dispatch_factors_ts': Array,
    'dispatch_tod_factors': Array,
    'dispatch_sched_weekday': Matrix,
    'dispatch_sched_weekend': Matrix,
    'mp_enable_energy_market_revenue': float,
    'mp_energy_market_revenue': Matrix,
    'mp_enable_ancserv1': float,
    'mp_ancserv1_revenue': Matrix,
    'mp_enable_ancserv2': float,
    'mp_ancserv2_revenue': Matrix,
    'mp_enable_ancserv3': float,
    'mp_ancserv3_revenue': Matrix,
    'mp_enable_ancserv4': float,
    'mp_ancserv4_revenue': Matrix,
    'mp_energy_market_revenue_single': Matrix,
    'mp_ancserv1_revenue_single': Matrix,
    'mp_ancserv2_revenue_single': Matrix,
    'mp_ancserv3_revenue_single': Matrix,
    'mp_ancserv4_revenue_single': Matrix,
    'mp_enable_market_percent_gen': float,
    'mp_enable_ancserv1_percent_gen': float,
    'mp_enable_ancserv2_percent_gen': float,
    'mp_enable_ancserv3_percent_gen': float,
    'mp_enable_ancserv4_percent_gen': float,
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
    'resilience_hrs': Array,
    'resilience_hrs_min': float,
    'resilience_hrs_max': float,
    'resilience_hrs_avg': float,
    'outage_durations': Array,
    'pdf_of_surviving': Array,
    'cdf_of_surviving': Array,
    'survival_function': Array,
    'avg_critical_load': float,
    'en_electricity_rates': float,
    'rate_escalation': Array,
    'ur_metering_option': float,
    'ur_nm_yearend_sell_rate': float,
    'ur_nm_credit_month': float,
    'ur_nm_credit_rollover': float,
    'ur_monthly_fixed_charge': float,
    'ur_sell_eq_buy': float,
    'ur_monthly_min_charge': float,
    'ur_annual_min_charge': float,
    'ur_en_ts_sell_rate': float,
    'ur_ts_sell_rate': Array,
    'ur_en_ts_buy_rate': float,
    'ur_ts_buy_rate': Array,
    'ur_ec_sched_weekday': Matrix,
    'ur_ec_sched_weekend': Matrix,
    'ur_ec_tou_mat': Matrix,
    'ur_dc_enable': float,
    'ur_dc_sched_weekday': Matrix,
    'ur_dc_sched_weekend': Matrix,
    'ur_dc_tou_mat': Matrix,
    'ur_dc_flat_mat': Matrix,
    'ur_enable_billing_demand': float,
    'ur_billing_demand_minimum': float,
    'ur_billing_demand_lookback_period': float,
    'ur_billing_demand_lookback_percentages': Matrix,
    'ur_dc_billing_demand_periods': Matrix,
    'ur_yearzero_usage_peaks': Array,
    'grid_curtailment': Array,
    'enable_interconnection_limit': float,
    'grid_interconnection_limit_kwac': float
}, total=False)

class Data(ssc.DataDict):
    percent_complete: float = INOUT(label='Estimated simulation status', units='%', type='NUMBER', group='Simulation')
    system_use_lifetime_output: float = INPUT(label='Lifetime simulation', units='0/1', type='NUMBER', group='Lifetime', required='?=0', constraints='BOOLEAN', meta='0=SingleYearRepeated,1=RunEveryYear')
    analysis_period: float = INPUT(label='Lifetime analysis period', units='years', type='NUMBER', group='Lifetime', required='system_use_lifetime_output=1', meta='The number of years in the simulation')
    en_batt: float = INPUT(label='Enable battery storage model', units='0/1', type='NUMBER', group='BatterySystem', required='?=0')
    en_standalone_batt: float = INPUT(label='Enable standalone battery storage model', units='0/1', type='NUMBER', group='BatterySystem', required='?=0')
    en_wave_batt: float = INPUT(label='Enable wave battery storage model', units='0/1', type='NUMBER', group='BatterySystem', required='?=0')
    energy_hourly_kW: Array = INOUT(label='Power output of array', units='kW', type='ARRAY', group='System Output', required='en_wave_batt=1', meta='Lifetime system generation')
    gen: Array = INOUT(label='System power generated', units='kW', type='ARRAY', group='System Output')
    load: Array = INPUT(label='Electricity load (year 1)', units='kW', type='ARRAY', group='Load')
    crit_load: Array = INPUT(label='Critical electricity load (year 1)', units='kW', type='ARRAY', group='Load')
    load_escalation: Array = INPUT(label='Annual load escalation', units='%/year', type='ARRAY', group='Load', required='?=0')
    crit_load_escalation: Array = INPUT(label='Annual critical load escalation', units='%/year', type='ARRAY', group='Load', required='?=0')
    grid_outage: Array = INPUT(label='Grid outage in this time step', units='0/1', type='ARRAY', group='Load', meta='0=GridAvailable,1=GridUnavailable,Length=load')
    run_resiliency_calcs: float = INPUT(label='Enable resilence calculations for every timestep', units='0/1', type='NUMBER', group='Load', required='?=0', meta='0=DisableCalcs,1=EnableCalcs')
    capacity_factor: float = INOUT(label='Capacity factor', units='%', type='NUMBER', group='System Output')
    capacity_factor_sales: Final[float] = OUTPUT(label='Capacity factor based on AC electricity to grid', units='%', type='NUMBER', group='System Output')
    annual_energy: float = INOUT(label='Annual Energy', units='kWh', type='NUMBER', group='System Output', required='?=0')
    batt_chem: float = INPUT(label='Battery chemistry', type='NUMBER', group='BatteryCell', meta='0=LeadAcid,1=LiIon')
    inverter_model: float = INPUT(label='Inverter model specifier', type='NUMBER', group='Inverter', required='?=4', constraints='INTEGER,MIN=0,MAX=4', meta='0=cec,1=datasheet,2=partload,3=coefficientgenerator,4=generic')
    inverter_count: float = INPUT(label='Number of inverters', type='NUMBER', group='Inverter')
    inv_snl_eff_cec: float = INPUT(label='Inverter Sandia CEC Efficiency', units='%', type='NUMBER', group='Inverter')
    inv_snl_paco: float = INPUT(label='Inverter Sandia Maximum AC Power', units='Wac', type='NUMBER', group='Inverter')
    inv_ds_eff: float = INPUT(label='Inverter Datasheet Efficiency', units='%', type='NUMBER', group='Inverter')
    inv_ds_paco: float = INPUT(label='Inverter Datasheet Maximum AC Power', units='Wac', type='NUMBER', group='Inverter')
    inv_pd_eff: float = INPUT(label='Inverter Partload Efficiency', units='%', type='NUMBER', group='Inverter')
    inv_pd_paco: float = INPUT(label='Inverter Partload Maximum AC Power', units='Wac', type='NUMBER', group='Inverter')
    inv_cec_cg_eff_cec: float = INPUT(label='Inverter Coefficient Generator CEC Efficiency', units='%', type='NUMBER', group='Inverter')
    inv_cec_cg_paco: float = INPUT(label='Inverter Coefficient Generator Max AC Power', units='Wac', type='NUMBER', group='Inverter')
    batt_ac_or_dc: float = INPUT(label='Battery interconnection (AC or DC)', type='NUMBER', group='BatterySystem', meta='0=DC_Connected,1=AC_Connected')
    batt_dc_dc_efficiency: float = INPUT(label='System DC to battery DC efficiency', type='NUMBER', group='BatterySystem')
    dcoptimizer_loss: float = INPUT(label='DC optimizer loss', type='NUMBER', group='Losses')
    batt_dc_ac_efficiency: float = INPUT(label='Battery DC to AC efficiency', type='NUMBER', group='BatterySystem')
    batt_ac_dc_efficiency: float = INPUT(label='Inverter AC to battery DC efficiency', type='NUMBER', group='BatterySystem')
    batt_meter_position: float = INPUT(label='Position of battery relative to electric meter', type='NUMBER', group='BatterySystem', meta='0=BehindTheMeter,1=FrontOfMeter')
    batt_inverter_efficiency_cutoff: float = INPUT(label='Inverter efficiency at which to cut battery charge or discharge off', units='%', type='NUMBER', group='BatterySystem')
    batt_losses: Array = INPUT(label='Battery system losses at each timestep (kW DC for DC connected, AC for AC connected)', units='kW', type='ARRAY', group='BatterySystem', required='?=0')
    batt_losses_charging: Array = INPUT(label='Battery system losses when charging (kW DC for DC connected, AC for AC connected)', units='kW', type='ARRAY', group='BatterySystem', required='?=0')
    batt_losses_discharging: Array = INPUT(label='Battery system losses when discharging (kW DC for DC connected, AC for AC connected)', units='kW', type='ARRAY', group='BatterySystem', required='?=0')
    batt_losses_idle: Array = INPUT(label='Battery system losses when idle (kW DC for DC connected, AC for AC connected)', units='kW', type='ARRAY', group='BatterySystem', required='?=0')
    batt_loss_choice: float = INPUT(label='Loss power input option', units='0/1', type='NUMBER', group='BatterySystem', required='?=0', meta='0=Monthly,1=TimeSeries')
    batt_current_choice: float = INPUT(label='Limit cells by current or power', type='NUMBER', group='BatterySystem')
    batt_computed_strings: float = INOUT(label='Battery number of strings of cells', type='NUMBER', group='BatterySystem')
    batt_computed_series: float = INOUT(label='Battery number of cells in series', type='NUMBER', group='BatterySystem')
    batt_computed_bank_capacity: float = INOUT(label='Battery computed bank capacity', units='kWh', type='NUMBER', group='BatterySystem')
    batt_current_charge_max: float = INOUT(label='Battery maximum charge current', units='A', type='NUMBER', group='BatterySystem')
    batt_current_discharge_max: float = INOUT(label='Battery maximum discharge current', units='A', type='NUMBER', group='BatterySystem')
    batt_power_charge_max_kwdc: float = INOUT(label='Battery maximum charge power (DC)', units='kWdc', type='NUMBER', group='BatterySystem')
    batt_power_discharge_max_kwdc: float = INOUT(label='Battery maximum discharge power (DC)', units='kWdc', type='NUMBER', group='BatterySystem')
    batt_power_charge_max_kwac: float = INOUT(label='Battery maximum charge power (AC)', units='kWac', type='NUMBER', group='BatterySystem')
    batt_power_discharge_max_kwac: float = INOUT(label='Battery maximum discharge power (AC)', units='kWac', type='NUMBER', group='BatterySystem')
    batt_voltage_choice: float = INPUT(label='Battery voltage input option', units='0/1', type='NUMBER', group='BatteryCell', required='?=0', meta='0=UseVoltageModel,1=InputVoltageTable')
    batt_Vfull: float = INPUT(label='Fully charged cell voltage', units='V', type='NUMBER', group='BatteryCell')
    batt_Vexp: float = INPUT(label='Cell voltage at end of exponential zone', units='V', type='NUMBER', group='BatteryCell')
    batt_Vnom: float = INPUT(label='Cell voltage at end of nominal zone', units='V', type='NUMBER', group='BatteryCell')
    batt_Vnom_default: float = INPUT(label='Default nominal cell voltage', units='V', type='NUMBER', group='BatteryCell')
    batt_Qfull: float = INPUT(label='Fully charged cell capacity', units='Ah', type='NUMBER', group='BatteryCell')
    batt_Qfull_flow: float = INPUT(label='Fully charged flow battery capacity', units='Ah', type='NUMBER', group='BatteryCell')
    batt_Qexp: float = INPUT(label='Cell capacity at end of exponential zone', units='Ah', type='NUMBER', group='BatteryCell')
    batt_Qnom: float = INPUT(label='Cell capacity at end of nominal zone', units='Ah', type='NUMBER', group='BatteryCell')
    batt_Vcut: float = INPUT(label='Cutoff voltage for battery rated capacity', units='V', type='NUMBER', group='BatteryCell', required='?=0')
    batt_C_rate: float = INPUT(label='Rate at which voltage vs. capacity curve input', type='NUMBER', group='BatteryCell')
    batt_resistance: float = INPUT(label='Internal resistance', units='Ohm', type='NUMBER', group='BatteryCell')
    batt_voltage_matrix: Matrix = INPUT(label='Battery voltage vs. depth-of-discharge', type='MATRIX', group='BatteryCell')
    LeadAcid_q20_computed: float = INPUT(label='Capacity at 20-hour discharge rate', units='Ah', type='NUMBER', group='BatteryCell')
    LeadAcid_q10_computed: float = INPUT(label='Capacity at 10-hour discharge rate', units='Ah', type='NUMBER', group='BatteryCell')
    LeadAcid_qn_computed: float = INPUT(label='Capacity at discharge rate for n-hour rate', units='Ah', type='NUMBER', group='BatteryCell')
    LeadAcid_tn: float = INPUT(label='Time to discharge', units='h', type='NUMBER', group='BatteryCell')
    batt_initial_SOC: float = INPUT(label='Initial state-of-charge', units='%', type='NUMBER', group='BatteryCell')
    batt_minimum_SOC: float = INPUT(label='Minimum allowed state-of-charge during nominal operation', units='%', type='NUMBER', group='BatteryCell')
    batt_minimum_outage_SOC: float = INPUT(label='Minimum allowed state-of-charge during an outage', units='%', type='NUMBER', group='BatteryCell')
    batt_maximum_SOC: float = INPUT(label='Maximum allowed state-of-charge', units='%', type='NUMBER', group='BatteryCell')
    batt_minimum_modetime: float = INPUT(label='Minimum time at charge state', units='min', type='NUMBER', group='BatteryCell')
    batt_life_model: float = INPUT(label='Battery life model specifier', units='0/1/2', type='NUMBER', group='BatteryCell', required='?=0', meta='0=calendar/cycle,1=NMC,2=LMO/LTO')
    batt_lifetime_matrix: Matrix = INPUT(label='Cycles vs capacity at different depths-of-discharge', type='MATRIX', group='BatteryCell', required='en_batt=1&batt_life_model=0')
    batt_calendar_choice: float = INPUT(label='Calendar life degradation input option', units='0/1/2', type='NUMBER', group='BatteryCell', required='en_batt=1&batt_life_model=0', meta='0=NoCalendarDegradation,1=LithiomIonModel,2=InputLossTable')
    batt_calendar_lifetime_matrix: Matrix = INPUT(label='Days vs capacity', type='MATRIX', group='BatteryCell', required='en_batt=1&batt_life_model=0&batt_calendar_choice=2')
    batt_calendar_q0: float = INPUT(label='Calendar life model initial capacity cofficient', type='NUMBER', group='BatteryCell', required='en_batt=1&batt_life_model=0&batt_calendar_choice=1')
    batt_calendar_a: float = INPUT(label='Calendar life model coefficient', units='1/sqrt(day)', type='NUMBER', group='BatteryCell', required='en_batt=1&batt_life_model=0&batt_calendar_choice=1')
    batt_calendar_b: float = INPUT(label='Calendar life model coefficient', units='K', type='NUMBER', group='BatteryCell', required='en_batt=1&batt_life_model=0&batt_calendar_choice=1')
    batt_calendar_c: float = INPUT(label='Calendar life model coefficient', units='K', type='NUMBER', group='BatteryCell', required='en_batt=1&batt_life_model=0&batt_calendar_choice=1')
    batt_replacement_capacity: float = INPUT(label='Capacity degradation at which to replace battery', units='%', type='NUMBER', group='BatterySystem')
    batt_replacement_option: float = INPUT(label='Enable battery replacement?', units='0=none,1=capacity based,2=user schedule', type='NUMBER', group='BatterySystem', required='?=0', constraints='INTEGER,MIN=0,MAX=2')
    batt_replacement_schedule_percent: Array = INPUT(label='Percentage of battery capacity to replace in each year', units='%', type='ARRAY', group='BatterySystem', required='batt_replacement_option=2', meta='length <= analysis_period')
    om_replacement_cost1: Array = INPUT(label='Cost to replace battery per kWh', units='$/kWh', type='ARRAY', group='BatterySystem')
    batt_mass: float = INPUT(label='Battery mass', units='kg', type='NUMBER', group='BatterySystem')
    batt_surface_area: float = INPUT(label='Battery surface area', units='m^2', type='NUMBER', group='BatterySystem')
    batt_Cp: float = INPUT(label='Battery specific heat capacity', units='J/KgK', type='NUMBER', group='BatteryCell')
    batt_h_to_ambient: float = INPUT(label='Heat transfer between battery and environment', units='W/m2K', type='NUMBER', group='BatteryCell')
    batt_room_temperature_celsius: Array = INPUT(label='Temperature of storage room', units='C', type='ARRAY', group='BatteryCell', meta='length=1 for fixed, # of weatherfile records otherwise')
    cap_vs_temp: Matrix = INPUT(label='Effective capacity as function of temperature', units='C,%', type='MATRIX', group='BatteryCell')
    dispatch_manual_charge: Array = INPUT(label='Periods 1-6 charging from system allowed?', type='ARRAY', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_dispatch_choice=3')
    dispatch_manual_fuelcellcharge: Array = INPUT(label='Periods 1-6 charging from fuel cell allowed?', type='ARRAY', group='BatteryDispatch')
    dispatch_manual_discharge: Array = INPUT(label='Periods 1-6 discharging allowed?', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3')
    dispatch_manual_btm_discharge_to_grid: Array = INPUT(label='Periods 1-6 behind the meter discharging to grid allowed?', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3&batt_meter_position=0')
    dispatch_manual_gridcharge: Array = INPUT(label='Periods 1-6 grid charging allowed?', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3')
    dispatch_manual_percent_discharge: Array = INPUT(label='Periods 1-6 discharge percent', units='%', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3')
    dispatch_manual_percent_gridcharge: Array = INPUT(label='Periods 1-6 gridcharge percent', units='%', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3')
    dispatch_manual_sched: Matrix = INPUT(label='Battery dispatch schedule for weekday', type='MATRIX', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3')
    dispatch_manual_sched_weekend: Matrix = INPUT(label='Battery dispatch schedule for weekend', type='MATRIX', group='BatteryDispatch', required='en_batt=1&batt_dispatch_choice=3')
    dispatch_manual_system_charge_first: float = INPUT(label='System charges battery before meeting load', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=0&batt_dispatch_choice=3&batt_dispatch_charge_only_system_exceeds_load=0', meta='0=LoadFirst,1=ChargeFirst')
    batt_target_power: Array = INPUT(label='Grid target power for every time step', units='kW', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_meter_position=0&batt_dispatch_choice=1')
    batt_target_power_monthly: Array = INPUT(label='Grid target power on monthly basis', units='kW', type='ARRAY', group='BatteryDispatch', required='en_batt=1&batt_meter_position=0&batt_dispatch_choice=1')
    batt_target_choice: float = INPUT(label='Target power input option', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=0&batt_dispatch_choice=1', meta='0=InputMonthlyTarget,1=InputFullTimeSeries')
    batt_custom_dispatch: Array = INPUT(label='Custom battery power for every time step', units='kW', type='ARRAY', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_dispatch_choice=2', meta='kWAC if AC-connected, else kWDC')
    batt_dispatch_choice: float = INPUT(label='Battery dispatch algorithm', units='0/1/2/3/4', type='NUMBER', group='BatteryDispatch', required='en_batt=1', meta='If behind the meter: 0=PeakShaving,1=InputGridTarget,2=InputBatteryPower,3=ManualDispatch,4=PriceSignalForecast if front of meter: 0=AutomatedEconomic,1=PV_Smoothing,2=InputBatteryPower,3=ManualDispatch')
    batt_dispatch_auto_can_fuelcellcharge: float = INPUT(label='Charging from fuel cell allowed for automated dispatch?', units='0/1', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_auto_can_gridcharge: float = INPUT(label='Grid charging allowed for automated dispatch?', units='0/1', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_auto_can_charge: float = INPUT(label='System charging allowed for automated dispatch?', units='0/1', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_auto_can_clipcharge: float = INPUT(label='Battery can charge from clipped power?', units='0/1', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_auto_btm_can_discharge_to_grid: float = INPUT(label='Behind the meter battery can discharge to grid?', units='0/1', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_charge_only_system_exceeds_load: float = INPUT(label='Battery can charge from system only when system output exceeds load', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=0')
    batt_dispatch_discharge_only_load_exceeds_system: float = INPUT(label='Battery can discharge battery only when load exceeds system output', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=0')
    batt_look_ahead_hours: float = INPUT(label='Hours to look ahead in automated dispatch', units='hours', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_update_frequency_hours: float = INPUT(label='Frequency to update the look-ahead dispatch', units='hours', type='NUMBER', group='BatteryDispatch')
    batt_dispatch_pvs_nameplate_ac: float = INPUT(label='Nameplate for pv smoothing', units='kWac', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_ac_lb_enable: float = INPUT(label='Enable AC lower bound', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_ac_lb: float = INPUT(label='AC lower bound', units='fraction of nameplate', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_ac_ub_enable: float = INPUT(label='Enable AC upper bound', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_ac_ub: float = INPUT(label='AC upper bound', units='fraction of nameplate', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_curtail_as_control: float = INPUT(label='Correct up-ramp violations', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_curtail_if_violation: float = INPUT(label='Curtail violations', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_short_forecast_enable: float = INPUT(label='Enable short term power forecast', units='0/1', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_forecast_shift_periods: float = INPUT(label='Forecasting window', units='periods of ramp intervals', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_timestep_multiplier: float = INPUT(label='Ramp timestep multiplier', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_max_ramp: float = INPUT(label='Maximum ramp rate', units='% of nameplate per ramp interval', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_soc_rest: float = INPUT(label='Battery resting SOC', units='%', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_kp: float = INPUT(label='Track PV power multiplier (kp)', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_ki: float = INPUT(label='Return to rest SOC multiplier (ki)', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_pvs_kf: float = INPUT(label='Forecast accumulation error multiplier (kf)', type='NUMBER', group='BatteryDispatch', required='en_batt=1&en_standalone_batt=0&batt_meter_position=1&batt_dispatch_choice=1')
    batt_dispatch_wf_forecast_choice: float = INPUT(label='Weather forecast choice for automatic dispatch', units='0/1/2', type='NUMBER', group='BatteryDispatch', required='?=0', meta='0=LookAhead,1=LookBehind,2=InputForecast')
    batt_dispatch_load_forecast_choice: float = INPUT(label='Load forecast choice for automatic dispatch', units='0/1/2', type='NUMBER', group='BatteryDispatch', required='?=0', meta='0=LookAhead,1=LookBehind,2=InputForecast')
    batt_pv_clipping_forecast: Array = INPUT(label='PV clipping forecast', units='kW', type='ARRAY', group='BatteryDispatch', meta='Length either 8760 * steps per hour (values repeat each year) or 8760 * steps per hour * analysis period')
    batt_pv_ac_forecast: Array = INPUT(label='PV ac power forecast', units='kW', type='ARRAY', group='BatteryDispatch', meta='Length either 8760 * steps per hour (values repeat each year) or 8760 * steps per hour * analysis period')
    batt_load_ac_forecast: Array = INPUT(label='Load ac power forecast', units='kW', type='ARRAY', group='BatteryDispatch', meta='Length either 8760 or 8760 * steps per hour')
    batt_load_ac_forecast_escalation: Array = INPUT(label='Annual load escalation for ac power forecast', units='kW', type='ARRAY', group='BatteryDispatch', meta='length <= analysis_period')
    batt_cycle_cost_choice: float = INPUT(label='Use SAM cost model for degradaton penalty or input custom via batt_cycle_cost', units='0/1', type='NUMBER', group='BatteryDispatch', required='?=0', meta='0=UseCostModel,1=InputCost')
    batt_cycle_cost: Array = INPUT(label='Input battery cycle degradaton penalty per year', units='$/cycle-kWh', type='ARRAY', group='BatteryDispatch', required='batt_cycle_cost_choice=1', meta='length 1 or analysis_period, length 1 will be extended using inflation')
    inflation_rate: float = INPUT(label='Inflation rate', units='%', type='NUMBER', group='Lifetime', required='?=0', constraints='MIN=-99')
    om_batt_replacement_cost: Array = INPUT(label='Replacement cost 1', units='$/kWh', type='ARRAY', group='System Costs', required='?=0.0')
    om_replacement_cost_escal: float = INPUT(label='Replacement cost escalation', units='%/year', type='NUMBER', group='System Costs', required='?=0.0')
    om_batt_variable_cost: Array = INPUT(label='Battery production-based System Costs amount', units='$/MWh', type='ARRAY', group='System Costs', required='?=0.0')
    om_production_escal: float = INPUT(label='Production-based O&M escalation', units='%/year', type='NUMBER', group='System Costs', required='?=0.0')
    fuelcell_power: Array = INPUT(label='Electricity from fuel cell AC', units='kW', type='ARRAY', group='FuelCell')
    forecast_price_signal_model: float = INPUT(label='Forecast price signal model selected', units='0/1', type='NUMBER', group='Price Signal', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=PPA based,1=Merchant Plant')
    ppa_price_input: Array = INPUT(label='PPA Price Input', units='$/kWh', type='ARRAY', group='Price Signal', required='forecast_price_signal_model=0&en_batt=1&batt_meter_position=1')
    ppa_multiplier_model: float = INPUT(label='PPA multiplier model', units='0/1', type='NUMBER', group='Price Signal', required='forecast_price_signal_model=0&en_batt=1&batt_meter_position=1', constraints='INTEGER,MIN=0', meta='0=diurnal,1=timestep')
    ppa_escalation: float = INPUT(label='PPA escalation rate', units='%/year', type='NUMBER', group='Price Signal', required='forecast_price_signal_model=0&en_batt=1&batt_meter_position=1')
    dispatch_factors_ts: Array = INPUT(label='Dispatch payment factor time step', type='ARRAY', group='Price Signal', required='forecast_price_signal_model=0&en_batt=1&batt_meter_position=1&ppa_multiplier_model=1')
    dispatch_tod_factors: Array = INPUT(label='TOD factors for periods 1-9', type='ARRAY', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=0&ppa_multiplier_model=0')
    dispatch_sched_weekday: Matrix = INPUT(label='Diurnal weekday TOD periods', units='1..9', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=0&ppa_multiplier_model=0', meta='12 x 24 matrix')
    dispatch_sched_weekend: Matrix = INPUT(label='Diurnal weekend TOD periods', units='1..9', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=0&ppa_multiplier_model=0', meta='12 x 24 matrix')
    mp_enable_energy_market_revenue: float = INPUT(label='Enable energy market revenue', units='0/1', type='NUMBER', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1', meta='0=false,1=true')
    mp_energy_market_revenue: Matrix = INPUT(label='Energy market revenue input', units=' [MW, $/MW]', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=1')
    mp_enable_ancserv1: float = INPUT(label='Enable ancillary services 1 revenue', units='0/1', type='NUMBER', group='Price Signal', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_ancserv1_revenue: Matrix = INPUT(label='Ancillary services 1 revenue input', units=' [MW, $/MW]', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=1')
    mp_enable_ancserv2: float = INPUT(label='Enable ancillary services 2 revenue', units='0/1', type='NUMBER', group='Price Signal', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_ancserv2_revenue: Matrix = INPUT(label='Ancillary services 2 revenue input', units=' [MW, $/MW]', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=1')
    mp_enable_ancserv3: float = INPUT(label='Enable ancillary services 3 revenue', units='0/1', type='NUMBER', group='Price Signal', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_ancserv3_revenue: Matrix = INPUT(label='Ancillary services 3 revenue input', units=' [MW, $/MW]', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=1')
    mp_enable_ancserv4: float = INPUT(label='Enable ancillary services 4 revenue', units='0/1', type='NUMBER', group='Price Signal', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_ancserv4_revenue: Matrix = INPUT(label='Ancillary services 4 revenue input', units=' [MW, $/MW]', type='MATRIX', group='Price Signal', required='en_batt=1&batt_meter_position=1&forecast_price_signal_model=1')
    mp_energy_market_revenue_single: Matrix = INPUT(label='Energy market revenue input', type='MATRIX', group='Revenue', required='forecast_price_signal_model=1&mp_enable_market_percent_gen=1', meta='Lifetime x 1 [Price($/MWh)]')
    mp_ancserv1_revenue_single: Matrix = INPUT(label='Ancillary services 1 revenue input', type='MATRIX', group='Revenue', required='forecast_price_signal_model=1&mp_enable_ancserv1_percent_gen=1', meta='Lifetime x 1[Price($/MWh)]')
    mp_ancserv2_revenue_single: Matrix = INPUT(label='Ancillary services 2 revenue input', type='MATRIX', group='Revenue', required='forecast_price_signal_model=1&mp_enable_ancserv2_percent_gen=1', meta='Lifetime x 1[Price($/MWh)]')
    mp_ancserv3_revenue_single: Matrix = INPUT(label='Ancillary services 3 revenue input', type='MATRIX', group='Revenue', required='forecast_price_signal_model=1&mp_enable_ancserv3_percent_gen=1', meta='Lifetime x 1[Price($/MWh)]')
    mp_ancserv4_revenue_single: Matrix = INPUT(label='Ancillary services 4 revenue input', type='MATRIX', group='Revenue', required='forecast_price_signal_model=1&mp_enable_ancserv4_percent_gen=1', meta='Lifetime x 1[Price($/MWh)]')
    mp_enable_market_percent_gen: float = INPUT(label='Enable percent demand cleared capacity option for market revenue', units='0/1', type='NUMBER', group='Revenue', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_enable_ancserv1_percent_gen: float = INPUT(label='Enable percent demand cleared capacity option for ancillary service 1', units='0/1', type='NUMBER', group='Revenue', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_enable_ancserv2_percent_gen: float = INPUT(label='Enable percent demand cleared capacity option for ancillary service 2', units='0/1', type='NUMBER', group='Revenue', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_enable_ancserv3_percent_gen: float = INPUT(label='Enable percent demand cleared capacity option for ancillary service 3', units='0/1', type='NUMBER', group='Revenue', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
    mp_enable_ancserv4_percent_gen: float = INPUT(label='Enable percent demand cleared capacity option for ancillary service 4', units='0/1', type='NUMBER', group='Revenue', required='forecast_price_signal_model=1', constraints='INTEGER,MIN=0,MAX=1')
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
    resilience_hrs: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage at each timestep', units='hr', type='ARRAY', group='Resilience')
    resilience_hrs_min: Final[float] = OUTPUT(label='Hours of autonomy during grid outage minimum', units='hr', type='NUMBER', group='Resilience', constraints='MIN=0')
    resilience_hrs_max: Final[float] = OUTPUT(label='Hours of autonomy during grid outage maximum', units='hr', type='NUMBER', group='Resilience', constraints='MIN=0')
    resilience_hrs_avg: Final[float] = OUTPUT(label='Hours of autonomy during grid outage average', units='hr', type='NUMBER', group='Resilience', constraints='MIN=0')
    outage_durations: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage hour list from min to max', units='hr', type='ARRAY', group='Resilience', meta='Hours from resilience_hrs_min to resilience_hrs_max')
    pdf_of_surviving: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage probabilities', type='ARRAY', group='Resilience', constraints='MIN=0,MAX=1', meta='Hours from resilience_hrs_min to resilience_hrs_max')
    cdf_of_surviving: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage cumulative probabilities', type='ARRAY', group='Resilience', constraints='MIN=0,MAX=1', meta='Prob surviving at least x hrs; hrs from min to max')
    survival_function: Final[Array] = OUTPUT(label='Hours of autonomy during grid outage survival function', type='ARRAY', group='Resilience', constraints='MIN=0,MAX=1', meta='Prob surviving greater than x hours; hrs from min to max')
    avg_critical_load: Final[float] = OUTPUT(label='Hours of autonomy during grid outage critical load met', units='kWh', type='NUMBER', group='Resilience', constraints='MIN=0')
    en_electricity_rates: float = INPUT(label='Optionally enable/disable electricity_rate', units='years', type='NUMBER', group='Electricity Rates', constraints='INTEGER,MIN=0,MAX=1')
    rate_escalation: Array = INPUT(label='Annual electricity rate escalation', units='%/year', type='ARRAY', group='Electricity Rates', required='?=0')
    ur_metering_option: float = INPUT(label='Metering options', units='0=net energy metering,1=net energy metering with $ credits,2=net billing,3=net billing with carryover to next month,4=buy all - sell all', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=4', meta='Net metering monthly excess')
    ur_nm_yearend_sell_rate: float = INPUT(label='Net metering true-up credit sell rate', units='$/kWh', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_nm_credit_month: float = INPUT(label='Month of year end payout (true-up)', units='mn', type='NUMBER', group='Electricity Rates', required='?=11', constraints='INTEGER,MIN=0,MAX=11')
    ur_nm_credit_rollover: float = INPUT(label='Apply net metering true-up credits to future bills', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=disable,1=enable')
    ur_monthly_fixed_charge: float = INPUT(label='Monthly fixed charge', units='$', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_sell_eq_buy: float = INPUT(label='Set sell rate equal to buy rate', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='Optional override')
    ur_monthly_min_charge: float = INPUT(label='Monthly minimum charge', units='$', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_annual_min_charge: float = INPUT(label='Annual minimum charge', units='$', type='NUMBER', group='Electricity Rates', required='?=0.0')
    ur_en_ts_sell_rate: float = INPUT(label='Enable time step sell rates', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='0=disable,1=enable')
    ur_ts_sell_rate: Array = INPUT(label='Time step sell rates', units='$/kWh', type='ARRAY', group='Electricity Rates')
    ur_en_ts_buy_rate: float = INPUT(label='Enable time step buy rates', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='0=disable,1=enable')
    ur_ts_buy_rate: Array = INPUT(label='Time step buy rates', units='$/kWh', type='ARRAY', group='Electricity Rates')
    ur_ec_sched_weekday: Matrix = INPUT(label='Energy charge weekday schedule', units='Periods defined in ur_ec_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_ec_sched_weekend: Matrix = INPUT(label='Energy charge weekend schedule', units='Periods defined in ur_ec_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_ec_tou_mat: Matrix = INPUT(label='Energy rates table', units='col 0=period no, col 1=tier no, col 2=max usage, col 3=max usage units (0=kWh, 1=kWh/kW, 2=kWh daily, 3=kWh/kW daily), col 4=buy rate ($/kWh), col 5=sell rate ($/kWh)', type='MATRIX', group='Electricity Rates', meta='nx6')
    ur_dc_enable: float = INPUT(label='Enable demand charge', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='BOOLEAN', meta='0=disable,1=enable')
    ur_dc_sched_weekday: Matrix = INPUT(label='Demand charge weekday schedule', units='Periods defined in ur_dc_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_dc_sched_weekend: Matrix = INPUT(label='Demand charge weekend schedule', units='Periods defined in ur_dc_tou_mat', type='MATRIX', group='Electricity Rates', meta='12x24')
    ur_dc_tou_mat: Matrix = INPUT(label='Demand rates (TOU) table', units='col 0=period no, col 1=tier no, col 2=tier peak (kW), col 3=charge ($/kW)', type='MATRIX', group='Electricity Rates', required='ur_dc_enable=1', meta='nx4')
    ur_dc_flat_mat: Matrix = INPUT(label='Demand rates (flat) table', units='col 0=month, col 1=tier no, col 2=tier peak (kW), col 3=charge ($/kW)', type='MATRIX', group='Electricity Rates', required='ur_dc_enable=1', meta='nx4')
    ur_enable_billing_demand: float = INPUT(label='Enable billing demand ratchets', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0', constraints='INTEGER,MIN=0,MAX=1', meta='0=disable,1=enable')
    ur_billing_demand_minimum: float = INPUT(label='Minimum billing demand', units='kW', type='NUMBER', group='Electricity Rates', required='ur_enable_billing_demand=1')
    ur_billing_demand_lookback_period: float = INPUT(label='Billing demand lookback period', units='mn', type='NUMBER', group='Electricity Rates', required='ur_enable_billing_demand=1', constraints='INTEGER,MIN=0,MAX=12')
    ur_billing_demand_lookback_percentages: Matrix = INPUT(label='Billing demand lookback percentages by month and consider actual peak demand', units='%', type='MATRIX', group='Electricity Rates', required='ur_enable_billing_demand=1', meta='12x2')
    ur_dc_billing_demand_periods: Matrix = INPUT(label='Billing demand applicability to a given demand charge time of use period', type='MATRIX', group='Electricity Rates', required='ur_enable_billing_demand=1')
    ur_yearzero_usage_peaks: Array = INPUT(label='Peak usage by month for year zero', units='kW', type='ARRAY', group='Electricity Rates', required='ur_enable_billing_demand=1', meta='12')
    grid_curtailment: Array = INPUT(label='Grid curtailment as energy delivery limit (first year)', units='MW', type='ARRAY', group='GridLimits', required='?')
    enable_interconnection_limit: float = INPUT(label='Enable grid interconnection limit', units='0/1', type='NUMBER', group='GridLimits', meta='Enable a grid interconnection limit')
    grid_interconnection_limit_kwac: float = INPUT(label='Grid interconnection limit', units='kWac', type='NUMBER', group='GridLimits')

    def __init__(self, *args: Mapping[str, Any],
                 percent_complete: float = ...,
                 system_use_lifetime_output: float = ...,
                 analysis_period: float = ...,
                 en_batt: float = ...,
                 en_standalone_batt: float = ...,
                 en_wave_batt: float = ...,
                 energy_hourly_kW: Array = ...,
                 gen: Array = ...,
                 load: Array = ...,
                 crit_load: Array = ...,
                 load_escalation: Array = ...,
                 crit_load_escalation: Array = ...,
                 grid_outage: Array = ...,
                 run_resiliency_calcs: float = ...,
                 capacity_factor: float = ...,
                 annual_energy: float = ...,
                 batt_chem: float = ...,
                 inverter_model: float = ...,
                 inverter_count: float = ...,
                 inv_snl_eff_cec: float = ...,
                 inv_snl_paco: float = ...,
                 inv_ds_eff: float = ...,
                 inv_ds_paco: float = ...,
                 inv_pd_eff: float = ...,
                 inv_pd_paco: float = ...,
                 inv_cec_cg_eff_cec: float = ...,
                 inv_cec_cg_paco: float = ...,
                 batt_ac_or_dc: float = ...,
                 batt_dc_dc_efficiency: float = ...,
                 dcoptimizer_loss: float = ...,
                 batt_dc_ac_efficiency: float = ...,
                 batt_ac_dc_efficiency: float = ...,
                 batt_meter_position: float = ...,
                 batt_inverter_efficiency_cutoff: float = ...,
                 batt_losses: Array = ...,
                 batt_losses_charging: Array = ...,
                 batt_losses_discharging: Array = ...,
                 batt_losses_idle: Array = ...,
                 batt_loss_choice: float = ...,
                 batt_current_choice: float = ...,
                 batt_computed_strings: float = ...,
                 batt_computed_series: float = ...,
                 batt_computed_bank_capacity: float = ...,
                 batt_current_charge_max: float = ...,
                 batt_current_discharge_max: float = ...,
                 batt_power_charge_max_kwdc: float = ...,
                 batt_power_discharge_max_kwdc: float = ...,
                 batt_power_charge_max_kwac: float = ...,
                 batt_power_discharge_max_kwac: float = ...,
                 batt_voltage_choice: float = ...,
                 batt_Vfull: float = ...,
                 batt_Vexp: float = ...,
                 batt_Vnom: float = ...,
                 batt_Vnom_default: float = ...,
                 batt_Qfull: float = ...,
                 batt_Qfull_flow: float = ...,
                 batt_Qexp: float = ...,
                 batt_Qnom: float = ...,
                 batt_Vcut: float = ...,
                 batt_C_rate: float = ...,
                 batt_resistance: float = ...,
                 batt_voltage_matrix: Matrix = ...,
                 LeadAcid_q20_computed: float = ...,
                 LeadAcid_q10_computed: float = ...,
                 LeadAcid_qn_computed: float = ...,
                 LeadAcid_tn: float = ...,
                 batt_initial_SOC: float = ...,
                 batt_minimum_SOC: float = ...,
                 batt_minimum_outage_SOC: float = ...,
                 batt_maximum_SOC: float = ...,
                 batt_minimum_modetime: float = ...,
                 batt_life_model: float = ...,
                 batt_lifetime_matrix: Matrix = ...,
                 batt_calendar_choice: float = ...,
                 batt_calendar_lifetime_matrix: Matrix = ...,
                 batt_calendar_q0: float = ...,
                 batt_calendar_a: float = ...,
                 batt_calendar_b: float = ...,
                 batt_calendar_c: float = ...,
                 batt_replacement_capacity: float = ...,
                 batt_replacement_option: float = ...,
                 batt_replacement_schedule_percent: Array = ...,
                 om_replacement_cost1: Array = ...,
                 batt_mass: float = ...,
                 batt_surface_area: float = ...,
                 batt_Cp: float = ...,
                 batt_h_to_ambient: float = ...,
                 batt_room_temperature_celsius: Array = ...,
                 cap_vs_temp: Matrix = ...,
                 dispatch_manual_charge: Array = ...,
                 dispatch_manual_fuelcellcharge: Array = ...,
                 dispatch_manual_discharge: Array = ...,
                 dispatch_manual_btm_discharge_to_grid: Array = ...,
                 dispatch_manual_gridcharge: Array = ...,
                 dispatch_manual_percent_discharge: Array = ...,
                 dispatch_manual_percent_gridcharge: Array = ...,
                 dispatch_manual_sched: Matrix = ...,
                 dispatch_manual_sched_weekend: Matrix = ...,
                 dispatch_manual_system_charge_first: float = ...,
                 batt_target_power: Array = ...,
                 batt_target_power_monthly: Array = ...,
                 batt_target_choice: float = ...,
                 batt_custom_dispatch: Array = ...,
                 batt_dispatch_choice: float = ...,
                 batt_dispatch_auto_can_fuelcellcharge: float = ...,
                 batt_dispatch_auto_can_gridcharge: float = ...,
                 batt_dispatch_auto_can_charge: float = ...,
                 batt_dispatch_auto_can_clipcharge: float = ...,
                 batt_dispatch_auto_btm_can_discharge_to_grid: float = ...,
                 batt_dispatch_charge_only_system_exceeds_load: float = ...,
                 batt_dispatch_discharge_only_load_exceeds_system: float = ...,
                 batt_look_ahead_hours: float = ...,
                 batt_dispatch_update_frequency_hours: float = ...,
                 batt_dispatch_pvs_nameplate_ac: float = ...,
                 batt_dispatch_pvs_ac_lb_enable: float = ...,
                 batt_dispatch_pvs_ac_lb: float = ...,
                 batt_dispatch_pvs_ac_ub_enable: float = ...,
                 batt_dispatch_pvs_ac_ub: float = ...,
                 batt_dispatch_pvs_curtail_as_control: float = ...,
                 batt_dispatch_pvs_curtail_if_violation: float = ...,
                 batt_dispatch_pvs_short_forecast_enable: float = ...,
                 batt_dispatch_pvs_forecast_shift_periods: float = ...,
                 batt_dispatch_pvs_timestep_multiplier: float = ...,
                 batt_dispatch_pvs_max_ramp: float = ...,
                 batt_dispatch_pvs_soc_rest: float = ...,
                 batt_dispatch_pvs_kp: float = ...,
                 batt_dispatch_pvs_ki: float = ...,
                 batt_dispatch_pvs_kf: float = ...,
                 batt_dispatch_wf_forecast_choice: float = ...,
                 batt_dispatch_load_forecast_choice: float = ...,
                 batt_pv_clipping_forecast: Array = ...,
                 batt_pv_ac_forecast: Array = ...,
                 batt_load_ac_forecast: Array = ...,
                 batt_load_ac_forecast_escalation: Array = ...,
                 batt_cycle_cost_choice: float = ...,
                 batt_cycle_cost: Array = ...,
                 inflation_rate: float = ...,
                 om_batt_replacement_cost: Array = ...,
                 om_replacement_cost_escal: float = ...,
                 om_batt_variable_cost: Array = ...,
                 om_production_escal: float = ...,
                 fuelcell_power: Array = ...,
                 forecast_price_signal_model: float = ...,
                 ppa_price_input: Array = ...,
                 ppa_multiplier_model: float = ...,
                 ppa_escalation: float = ...,
                 dispatch_factors_ts: Array = ...,
                 dispatch_tod_factors: Array = ...,
                 dispatch_sched_weekday: Matrix = ...,
                 dispatch_sched_weekend: Matrix = ...,
                 mp_enable_energy_market_revenue: float = ...,
                 mp_energy_market_revenue: Matrix = ...,
                 mp_enable_ancserv1: float = ...,
                 mp_ancserv1_revenue: Matrix = ...,
                 mp_enable_ancserv2: float = ...,
                 mp_ancserv2_revenue: Matrix = ...,
                 mp_enable_ancserv3: float = ...,
                 mp_ancserv3_revenue: Matrix = ...,
                 mp_enable_ancserv4: float = ...,
                 mp_ancserv4_revenue: Matrix = ...,
                 mp_energy_market_revenue_single: Matrix = ...,
                 mp_ancserv1_revenue_single: Matrix = ...,
                 mp_ancserv2_revenue_single: Matrix = ...,
                 mp_ancserv3_revenue_single: Matrix = ...,
                 mp_ancserv4_revenue_single: Matrix = ...,
                 mp_enable_market_percent_gen: float = ...,
                 mp_enable_ancserv1_percent_gen: float = ...,
                 mp_enable_ancserv2_percent_gen: float = ...,
                 mp_enable_ancserv3_percent_gen: float = ...,
                 mp_enable_ancserv4_percent_gen: float = ...,
                 en_electricity_rates: float = ...,
                 rate_escalation: Array = ...,
                 ur_metering_option: float = ...,
                 ur_nm_yearend_sell_rate: float = ...,
                 ur_nm_credit_month: float = ...,
                 ur_nm_credit_rollover: float = ...,
                 ur_monthly_fixed_charge: float = ...,
                 ur_sell_eq_buy: float = ...,
                 ur_monthly_min_charge: float = ...,
                 ur_annual_min_charge: float = ...,
                 ur_en_ts_sell_rate: float = ...,
                 ur_ts_sell_rate: Array = ...,
                 ur_en_ts_buy_rate: float = ...,
                 ur_ts_buy_rate: Array = ...,
                 ur_ec_sched_weekday: Matrix = ...,
                 ur_ec_sched_weekend: Matrix = ...,
                 ur_ec_tou_mat: Matrix = ...,
                 ur_dc_enable: float = ...,
                 ur_dc_sched_weekday: Matrix = ...,
                 ur_dc_sched_weekend: Matrix = ...,
                 ur_dc_tou_mat: Matrix = ...,
                 ur_dc_flat_mat: Matrix = ...,
                 ur_enable_billing_demand: float = ...,
                 ur_billing_demand_minimum: float = ...,
                 ur_billing_demand_lookback_period: float = ...,
                 ur_billing_demand_lookback_percentages: Matrix = ...,
                 ur_dc_billing_demand_periods: Matrix = ...,
                 ur_yearzero_usage_peaks: Array = ...,
                 grid_curtailment: Array = ...,
                 enable_interconnection_limit: float = ...,
                 grid_interconnection_limit_kwac: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
