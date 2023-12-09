
# This is a generated file

"""etes_ptes - Heat pump charging two two-tank TES from grid, discharge with power cycle"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'solar_resource_file': str,
    'is_dispatch': float,
    'sim_type': float,
    'etes_financial_model': float,
    'time_start': float,
    'time_stop': float,
    'time_steps_per_hour': float,
    'vacuum_arrays': float,
    'heater_mult': float,
    'tshours': float,
    'W_dot_pc_thermo_des': float,
    'eta_pc_thermo_des': float,
    'f_pc_parasitic_des': float,
    'cop_hp_thermo_des': float,
    'f_hp_parasitic_des': float,
    'T_HT_hot_htf_des': float,
    'T_HT_cold_htf_des': float,
    'T_CT_cold_htf_des': float,
    'T_CT_hot_htf_des': float,
    'hot_htf_code': float,
    'ud_hot_htf_props': Matrix,
    'cold_htf_code': float,
    'ud_cold_htf_props': Matrix,
    'f_q_dot_des_allowable_su': float,
    'hrs_startup_at_max_rate': float,
    'f_q_dot_heater_min': float,
    'heat_pump_HT_HTF_pump_coef': float,
    'heat_pump_CT_HTF_pump_coef': float,
    'pb_pump_coef': float,
    'CT_pb_pump_coef': float,
    'startup_time': float,
    'startup_frac': float,
    'cycle_max_frac': float,
    'cycle_cutoff_frac': float,
    'q_sby_frac': float,
    'tes_init_hot_htf_percent': float,
    'h_tank': float,
    'cold_tank_max_heat': float,
    'u_tank': float,
    'tank_pairs': float,
    'cold_tank_Thtr': float,
    'h_tank_min': float,
    'hot_tank_Thtr': float,
    'hot_tank_max_heat': float,
    'CT_h_tank': float,
    'CT_u_tank': float,
    'CT_tank_pairs': float,
    'CT_h_tank_min': float,
    'disp_horizon': float,
    'disp_frequency': float,
    'disp_steps_per_hour': float,
    'disp_max_iter': float,
    'disp_timeout': float,
    'disp_mip_gap': float,
    'disp_spec_bb': float,
    'disp_reporting': float,
    'disp_spec_presolve': float,
    'disp_spec_scaling': float,
    'disp_pen_delta_w': float,
    'disp_csu_cost': float,
    'disp_hsu_cost': float,
    'disp_time_weighting': float,
    'disp_down_time_min': float,
    'disp_up_time_min': float,
    'ppa_multiplier_model': float,
    'dispatch_factors_ts': Array,
    'dispatch_sched_weekday': Matrix,
    'dispatch_sched_weekend': Matrix,
    'dispatch_factor1': float,
    'dispatch_factor2': float,
    'dispatch_factor3': float,
    'dispatch_factor4': float,
    'dispatch_factor5': float,
    'dispatch_factor6': float,
    'dispatch_factor7': float,
    'dispatch_factor8': float,
    'dispatch_factor9': float,
    'ppa_price_input': Array,
    'pb_fixed_par': float,
    'bop_par': float,
    'bop_par_f': float,
    'bop_par_0': float,
    'bop_par_1': float,
    'bop_par_2': float,
    'cycle_spec_cost': float,
    'tes_spec_cost': float,
    'CT_tes_spec_cost': float,
    'heat_pump_spec_cost': float,
    'bop_spec_cost': float,
    'contingency_rate': float,
    'sales_tax_frac': float,
    'epc_cost_perc_of_direct': float,
    'epc_cost_per_watt': float,
    'epc_cost_fixed': float,
    'land_cost_perc_of_direct': float,
    'land_cost_per_watt': float,
    'land_cost_fixed': float,
    'sales_tax_rate': float,
    'const_per_interest_rate1': float,
    'const_per_interest_rate2': float,
    'const_per_interest_rate3': float,
    'const_per_interest_rate4': float,
    'const_per_interest_rate5': float,
    'const_per_months1': float,
    'const_per_months2': float,
    'const_per_months3': float,
    'const_per_months4': float,
    'const_per_months5': float,
    'const_per_percent1': float,
    'const_per_percent2': float,
    'const_per_percent3': float,
    'const_per_percent4': float,
    'const_per_percent5': float,
    'const_per_upfront_rate1': float,
    'const_per_upfront_rate2': float,
    'const_per_upfront_rate3': float,
    'const_per_upfront_rate4': float,
    'const_per_upfront_rate5': float,
    'system_capacity': float,
    'nameplate': float,
    'cp_system_nameplate': float,
    'cp_battery_nameplate': float,
    'rte_thermo': float,
    'rte_net': float,
    'charge_capacity': float,
    'tshours_heater': float,
    'W_dot_hp_in_thermo_des': float,
    'q_dot_hp_hot_out_des': float,
    'q_dot_hp_cold_in_des': float,
    'W_dot_hp_elec_parasitic_des': float,
    'W_dot_hp_in_net_des': float,
    'COP_net_des': float,
    'm_dot_hp_HT_htf_des': float,
    'W_dot_hp_HT_htf_pump_des': float,
    'm_dot_hp_CT_htf_des': float,
    'W_dot_hp_CT_htf_pump_des': float,
    'E_hp_su_des': float,
    'q_dot_pc_hot_in_des': float,
    'q_dot_pc_cold_out_thermo_des': float,
    'W_dot_pc_elec_parasitic_des': float,
    'W_dot_pc_net_des': float,
    'eta_pc_net_des': float,
    'q_dot_pc_cold_to_CTES_des': float,
    'q_dot_pc_cold_to_surroundings_des': float,
    'm_dot_pc_HT_htf_des': float,
    'W_dot_pc_HT_htf_pump_des': float,
    'm_dot_pc_CT_htf_des': float,
    'W_dot_pc_CT_htf_pump_des': float,
    'Q_tes_des': float,
    'V_tes_htf_avail': float,
    'V_tes_htf_total': float,
    'd_tank_tes': float,
    'q_dot_loss_tes_des': float,
    'Q_CT_tes_des': float,
    'V_CT_tes_htf_avail': float,
    'V_CT_tes_htf_total': float,
    'd_CT_tank_tes': float,
    'q_dot_loss_CT_tes_des': float,
    'W_dot_bop_design': float,
    'W_dot_fixed': float,
    'heater_cost_calc': float,
    'tes_cost_calc': float,
    'CT_tes_cost_calc': float,
    'bop_cost_calc': float,
    'cycle_cost_calc': float,
    'direct_subtotal_cost_calc': float,
    'contingency_cost_calc': float,
    'total_direct_cost_calc': float,
    'epc_cost_calc': float,
    'land_cost_calc': float,
    'sales_tax_cost_calc': float,
    'total_indirect_cost_calc': float,
    'installed_per_cap_cost_calc': float,
    'total_installed_cost': float,
    'construction_financing_cost': float,
    'time_hr': Array,
    'elec_purchase_price_mult': Array,
    'tou_period': Array,
    'tdry': Array,
    'twet': Array,
    'T_hp_HT_htf_cold_in': Array,
    'T_hp_HT_htf_hot_out': Array,
    'T_hp_CT_htf_hot_in': Array,
    'T_hp_CT_htf_cold_out': Array,
    'm_dot_hp_HT_htf': Array,
    'm_dot_hp_CT_htf': Array,
    'q_dot_hp_startup': Array,
    'q_dot_hp_to_HT_htf': Array,
    'q_dot_hp_from_CT_htf': Array,
    'W_dot_hp_thermo': Array,
    'W_dot_hp_parasitics': Array,
    'W_dot_hp_HT_htf_pump': Array,
    'W_dot_hp_CT_htf_pump': Array,
    'W_dot_hp_net': Array,
    'cop_hot_hp_thermo': Array,
    'T_pc_HT_htf_hot_in': Array,
    'T_pc_HT_htf_cold_out': Array,
    'T_pc_CT_htf_cold_in': Array,
    'T_pc_CT_htf_hot_out': Array,
    'm_dot_pc_HT_htf': Array,
    'm_dot_pc_CT_htf': Array,
    'q_dot_pc_startup': Array,
    'q_dot_pc_from_HT_htf': Array,
    'q_dot_pc_thermo_out': Array,
    'q_dot_pc_to_CT_htf': Array,
    'q_dot_pc_rejected': Array,
    'W_dot_pc_thermo_out': Array,
    'W_dot_pc_parasitics': Array,
    'W_dot_pc_HT_htf_pump': Array,
    'W_dot_pc_CT_htf_pump': Array,
    'eta_pc_thermo': Array,
    'q_dot_dc_tes': Array,
    'q_dot_ch_tes': Array,
    'e_ch_tes': Array,
    'q_dot_tes_losses': Array,
    'q_dot_tes_heater': Array,
    'T_tes_hot': Array,
    'T_tes_cold': Array,
    'mass_tes_cold': Array,
    'mass_tes_hot': Array,
    'q_dot_CT_tes_losses': Array,
    'q_dot_CT_tes_heater': Array,
    'T_CT_tes_hot': Array,
    'T_CT_tes_cold': Array,
    'mass_CT_tes_cold': Array,
    'mass_CT_tes_hot': Array,
    'W_dot_fixed_parasitics': Array,
    'W_dot_bop_parasitics': Array,
    'W_dot_out_net': Array,
    'gen': Array,
    'n_op_modes': Array,
    'op_mode_1': Array,
    'op_mode_2': Array,
    'op_mode_3': Array,
    'm_dot_balance': Array,
    'q_balance': Array,
    'q_pc_target': Array,
    'disp_rel_mip_gap': Array,
    'disp_solve_state': Array,
    'disp_subopt_flag': Array,
    'disp_solve_iter': Array,
    'disp_objective': Array,
    'disp_obj_relax': Array,
    'disp_qsfprod_expected': Array,
    'disp_qsfsu_expected': Array,
    'disp_tes_expected': Array,
    'disp_pceff_expected': Array,
    'disp_qpbsu_expected': Array,
    'disp_wpb_expected': Array,
    'disp_rev_expected': Array,
    'disp_presolve_nconstr': Array,
    'disp_presolve_nvar': Array,
    'disp_solve_time': Array,
    'annual_energy': float,
    'disp_objective_ann': float,
    'disp_iter_ann': float,
    'disp_presolve_nconstr_ann': float,
    'disp_presolve_nvar_ann': float,
    'disp_solve_time_ann': float,
    'disp_solve_state_ann': float,
    'avg_suboptimal_rel_mip_gap': float,
    'ppa_soln_mode': float,
    'flip_target_percent': float,
    'adjust:constant': float,
    'adjust:hourly': Array,
    'adjust:timeindex': Array,
    'adjust:periods': Matrix,
    'annual_energy_distribution_time': Matrix
}, total=False)

class Data(ssc.DataDict):
    solar_resource_file: str = INPUT(label='Local weather file path', type='STRING', group='Solar Resource', required='?', constraints='LOCAL_FILE')
    is_dispatch: float = INPUT(label='Allow dispatch optimization?', type='NUMBER', group='System Control', required='?=0')
    sim_type: float = INPUT(label='1 (default): timeseries, 2: design only', type='NUMBER', group='System Control', required='?=1')
    etes_financial_model: float = INPUT(units='1-8', type='NUMBER', group='Financial Model', required='?=1', constraints='INTEGER,MIN=0')
    time_start: float = INPUT(label='Simulation start time', units='s', type='NUMBER', group='System Control', required='?=0')
    time_stop: float = INPUT(label='Simulation stop time', units='s', type='NUMBER', group='System Control', required='?=31536000')
    time_steps_per_hour: float = INPUT(label='Number of simulation time steps per hour', type='NUMBER', group='System Control', required='?=-1')
    vacuum_arrays: float = INPUT(label='Allocate arrays for only the required number of steps', type='NUMBER', group='System Control', required='?=0')
    heater_mult: float = INPUT(label='Heater multiple relative to design cycle thermal power', units='-', type='NUMBER', group='System Design', required='*')
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='System Design', required='*')
    W_dot_pc_thermo_des: float = INPUT(label='PC design thermodynamic power', units='MWe', type='NUMBER', group='System Design', required='*')
    eta_pc_thermo_des: float = INPUT(label='PC design thermodynamic efficiency', units='-', type='NUMBER', group='System Design', required='*')
    f_pc_parasitic_des: float = INPUT(label='PC parasitics as fraction of design thermo power out', units='-', type='NUMBER', group='System Design', required='*')
    cop_hp_thermo_des: float = INPUT(label='Heat pump design thermodynamic heat COP', units='-', type='NUMBER', group='System Design', required='*')
    f_hp_parasitic_des: float = INPUT(label='Heat pump parasitics as fraction of design thermo power in', units='-', type='NUMBER', group='System Design', required='*')
    T_HT_hot_htf_des: float = INPUT(label='HT TES hot temperature', units='C', type='NUMBER', group='System Design', required='*')
    T_HT_cold_htf_des: float = INPUT(label='HT TES cold temperature', units='C', type='NUMBER', group='System Design', required='*')
    T_CT_cold_htf_des: float = INPUT(label='CT TES cold temperature', units='C', type='NUMBER', group='System Design', required='*')
    T_CT_hot_htf_des: float = INPUT(label='CT TES hot temperature', units='C', type='NUMBER', group='System Design', required='*')
    hot_htf_code: float = INPUT(label='Hot HTF code - see htf_props.h for list', type='NUMBER', group='Thermal Storage', required='*')
    ud_hot_htf_props: Matrix = INPUT(label='User-defined Hot HTF fluid property data', units='-', type='MATRIX', group='Thermal Storage', required='hot_htf_code=50')
    cold_htf_code: float = INPUT(label='Cold HTF code - see htf_props.h for list', type='NUMBER', group='Thermal Storage', required='*')
    ud_cold_htf_props: Matrix = INPUT(label='User-defined Cold HTF fluid property data', units='-', type='MATRIX', group='Thermal Storage', required='cold_htf_code=50')
    f_q_dot_des_allowable_su: float = INPUT(label='Fraction of design power allowed during startup', units='-', type='NUMBER', group='Heater', required='*')
    hrs_startup_at_max_rate: float = INPUT(label='Duration of startup at max startup power', units='hr', type='NUMBER', group='Heater', required='*')
    f_q_dot_heater_min: float = INPUT(label='Minimum allowable heater output as fraction of design', type='NUMBER', group='Heater', required='*')
    heat_pump_HT_HTF_pump_coef: float = INPUT(label='High temp HX pumping power to move 1 kg/s', units='kW/kg/s', type='NUMBER', group='Power Cycle', required='*')
    heat_pump_CT_HTF_pump_coef: float = INPUT(label='Cold temp HX pumping power to move 1 kg/s', units='kW/kg/s', type='NUMBER', group='Power Cycle', required='*')
    pb_pump_coef: float = INPUT(label='COLD TES pumping power to move 1kg of HTF through PB loop', units='kW/kg/s', type='NUMBER', group='Power Cycle', required='*')
    CT_pb_pump_coef: float = INPUT(label='COLD TES pumping power to move 1kg of HTF through PB loop', units='kW/kg/s', type='NUMBER', group='Power Cycle', required='*')
    startup_time: float = INPUT(label='Time needed for power block startup', units='hr', type='NUMBER', group='Power Cycle', required='*')
    startup_frac: float = INPUT(label='Fraction of design thermal power needed for startup', units='none', type='NUMBER', group='Power Cycle', required='*')
    cycle_max_frac: float = INPUT(label='Maximum turbine over design operation fraction', type='NUMBER', group='Power Cycle', required='*')
    cycle_cutoff_frac: float = INPUT(label='Minimum turbine operation fraction before shutdown', type='NUMBER', group='Power Cycle', required='*')
    q_sby_frac: float = INPUT(label='Fraction of thermal power required for standby', type='NUMBER', group='Power Cycle', required='*')
    tes_init_hot_htf_percent: float = INPUT(label='HOT TES Initial fraction of available volume that is hot', units='%', type='NUMBER', group='Hot Thermal Storage', required='*')
    h_tank: float = INPUT(label='HOT TES Total height of tank (height of HTF when tank is full)', units='m', type='NUMBER', group='Hot Thermal Storage', required='*')
    cold_tank_max_heat: float = INPUT(label='HOT TES Rated heater capacity for cold tank heating', units='MW', type='NUMBER', group='Hot Thermal Storage', required='*')
    u_tank: float = INPUT(label='HOT TES Loss coefficient from the tank', units='W/m2-K', type='NUMBER', group='Hot Thermal Storage', required='*')
    tank_pairs: float = INPUT(label='HOT TES Number of equivalent tank pairs', type='NUMBER', group='Hot Thermal Storage', required='*', constraints='INTEGER')
    cold_tank_Thtr: float = INPUT(label='HOT TES Minimum allowable cold tank HTF temperature', units='C', type='NUMBER', group='Hot Thermal Storage', required='*')
    h_tank_min: float = INPUT(label='HOT TES Minimum allowable HTF height in storage tank', units='m', type='NUMBER', group='Hot Thermal Storage', required='*')
    hot_tank_Thtr: float = INPUT(label='HOT TES Minimum allowable hot tank HTF temperature', units='C', type='NUMBER', group='Hot Thermal Storage', required='*')
    hot_tank_max_heat: float = INPUT(label='HOT TES Rated heater capacity for hot tank heating', units='MW', type='NUMBER', group='Hot Thermal Storage', required='*')
    CT_h_tank: float = INPUT(label='COLD TES Total height of tank (height of HTF when tank is full)', units='m', type='NUMBER', group='Cold Thermal Storage', required='*')
    CT_u_tank: float = INPUT(label='COLD TES Loss coefficient from the tank', units='W/m2-K', type='NUMBER', group='Cold Thermal Storage', required='*')
    CT_tank_pairs: float = INPUT(label='COLD TES Number of equivalent tank pairs', type='NUMBER', group='Cold Thermal Storage', required='*', constraints='INTEGER')
    CT_h_tank_min: float = INPUT(label='COLD TES Minimum allowable HTF height in storage tank', units='m', type='NUMBER', group='Cold Thermal Storage', required='*')
    disp_horizon: float = INPUT(label='Time horizon for dispatch optimization', units='hour', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_frequency: float = INPUT(label='Frequency for dispatch optimization calculations', units='hour', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_steps_per_hour: float = INPUT(label='Time steps per hour for dispatch optimization calculations', type='NUMBER', group='System Control', required='?=1')
    disp_max_iter: float = INPUT(label='Max number of dispatch optimization iterations', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_timeout: float = INPUT(label='Max dispatch optimization solve duration', units='s', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_mip_gap: float = INPUT(label='Dispatch optimization solution tolerance', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_spec_bb: float = INPUT(label='Dispatch optimization B&B heuristic', type='NUMBER', group='System Control', required='?=-1')
    disp_reporting: float = INPUT(label='Dispatch optimization reporting level', type='NUMBER', group='System Control', required='?=-1')
    disp_spec_presolve: float = INPUT(label='Dispatch optimization presolve heuristic', type='NUMBER', group='System Control', required='?=-1')
    disp_spec_scaling: float = INPUT(label='Dispatch optimization scaling heuristic', type='NUMBER', group='System Control', required='?=-1')
    disp_pen_delta_w: float = INPUT(label='Dispatch cycle production change penalty', units='$/MWe-change', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_csu_cost: float = INPUT(label='Cycle startup cost', units='$/MWe-cycle/start', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_hsu_cost: float = INPUT(label='Heater startup cost', units='$/MWe-cycle/start', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_time_weighting: float = INPUT(label='Dispatch optimization future time discounting factor', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_down_time_min: float = INPUT(label='Minimum time requirement for cycle to not generate power', units='hr', type='NUMBER', group='System Control', required='is_dispatch=1')
    disp_up_time_min: float = INPUT(label='Minimum time requirement for cycle to generate power', units='hr', type='NUMBER', group='System Control', required='is_dispatch=1')
    ppa_multiplier_model: float = INPUT(label='PPA multiplier model', units='0/1', type='NUMBER', group='Time of Delivery Factors', required='?=0', constraints='INTEGER,MIN=0', meta='0=diurnal,1=timestep')
    dispatch_factors_ts: Array = INPUT(label='Dispatch payment factor timeseries array', type='ARRAY', group='Time of Delivery Factors', required='ppa_multiplier_model=1&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_sched_weekday: Matrix = INPUT(label='PPA pricing weekday schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_sched_weekend: Matrix = INPUT(label='PPA pricing weekend schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor1: float = INPUT(label='Dispatch payment factor 1', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor2: float = INPUT(label='Dispatch payment factor 2', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor3: float = INPUT(label='Dispatch payment factor 3', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor4: float = INPUT(label='Dispatch payment factor 4', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor5: float = INPUT(label='Dispatch payment factor 5', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor6: float = INPUT(label='Dispatch payment factor 6', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor7: float = INPUT(label='Dispatch payment factor 7', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor8: float = INPUT(label='Dispatch payment factor 8', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor9: float = INPUT(label='Dispatch payment factor 9', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    ppa_price_input: Array = INPUT(label='PPA prices - yearly', units='$/kWh', type='ARRAY', group='Revenue', required='ppa_multiplier_model=0&etes_financial_model<5&is_dispatch=1&sim_type=1')
    pb_fixed_par: float = INPUT(label="Fixed parasitic load that don't generate heat - runs at all times", units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    bop_par: float = INPUT(label='Balance of plant parasitic power fraction', units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    bop_par_f: float = INPUT(label='Balance of plant parasitic power fraction - mult frac', type='NUMBER', group='System Control', required='*')
    bop_par_0: float = INPUT(label='Balance of plant parasitic power fraction - const coeff', type='NUMBER', group='System Control', required='*')
    bop_par_1: float = INPUT(label='Balance of plant parasitic power fraction - linear coeff', type='NUMBER', group='System Control', required='*')
    bop_par_2: float = INPUT(label='Balance of plant parasitic power fraction - quadratic coeff', type='NUMBER', group='System Control', required='*')
    cycle_spec_cost: float = INPUT(label='Power cycle specific cost', units='$/kWe', type='NUMBER', group='System Costs', required='*')
    tes_spec_cost: float = INPUT(label='Hot Temp thermal energy storage specific cost', units='$/kWht', type='NUMBER', group='System Costs', required='*')
    CT_tes_spec_cost: float = INPUT(label='Cold Temp thermal energy storage specific cost', units='$/kWht', type='NUMBER', group='System Costs', required='*')
    heat_pump_spec_cost: float = INPUT(label='Heater pump specific cost', units='$/kWht', type='NUMBER', group='System Costs', required='*')
    bop_spec_cost: float = INPUT(label='Balance of plant specific cost', units='$/kWe', type='NUMBER', group='System Costs', required='*')
    contingency_rate: float = INPUT(label='Contingency for cost overrun', units='%', type='NUMBER', group='System Costs', required='*')
    sales_tax_frac: float = INPUT(label='Percent of cost to which sales tax applies', units='%', type='NUMBER', group='System Costs', required='*')
    epc_cost_perc_of_direct: float = INPUT(label='EPC cost percent of direct', units='%', type='NUMBER', group='System Costs', required='*')
    epc_cost_per_watt: float = INPUT(label='EPC cost per watt', units='$/W', type='NUMBER', group='System Costs', required='*')
    epc_cost_fixed: float = INPUT(label='EPC fixed', units='$', type='NUMBER', group='System Costs', required='*')
    land_cost_perc_of_direct: float = INPUT(label='Land cost percent of direct', units='%', type='NUMBER', group='System Costs', required='*')
    land_cost_per_watt: float = INPUT(label='Land cost per watt', units='$/W', type='NUMBER', group='System Costs', required='*')
    land_cost_fixed: float = INPUT(label='Land fixed', units='$', type='NUMBER', group='System Costs', required='*')
    sales_tax_rate: float = INPUT(label='Sales tax rate', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest_rate1: float = INPUT(label='Interest rate, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest_rate2: float = INPUT(label='Interest rate, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest_rate3: float = INPUT(label='Interest rate, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest_rate4: float = INPUT(label='Interest rate, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest_rate5: float = INPUT(label='Interest rate, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_months1: float = INPUT(label='Months prior to operation, loan 1', type='NUMBER', group='Financial Parameters', required='*')
    const_per_months2: float = INPUT(label='Months prior to operation, loan 2', type='NUMBER', group='Financial Parameters', required='*')
    const_per_months3: float = INPUT(label='Months prior to operation, loan 3', type='NUMBER', group='Financial Parameters', required='*')
    const_per_months4: float = INPUT(label='Months prior to operation, loan 4', type='NUMBER', group='Financial Parameters', required='*')
    const_per_months5: float = INPUT(label='Months prior to operation, loan 5', type='NUMBER', group='Financial Parameters', required='*')
    const_per_percent1: float = INPUT(label='Percent of total installed cost, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_percent2: float = INPUT(label='Percent of total installed cost, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_percent3: float = INPUT(label='Percent of total installed cost, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_percent4: float = INPUT(label='Percent of total installed cost, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_percent5: float = INPUT(label='Percent of total installed cost, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_upfront_rate1: float = INPUT(label='Upfront fee on principal, loan 1', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_upfront_rate2: float = INPUT(label='Upfront fee on principal, loan 2', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_upfront_rate3: float = INPUT(label='Upfront fee on principal, loan 3', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_upfront_rate4: float = INPUT(label='Upfront fee on principal, loan 4', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_upfront_rate5: float = INPUT(label='Upfront fee on principal, loan 5', units='%', type='NUMBER', group='Financial Parameters', required='*')
    system_capacity: Final[float] = OUTPUT(label='System capacity (discharge)', units='kWe', type='NUMBER', group='System Design Calc', required='*')
    nameplate: Final[float] = OUTPUT(label='Nameplate capacity (discharge)', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    cp_system_nameplate: Final[float] = OUTPUT(label='System capacity for capacity payments', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    cp_battery_nameplate: Final[float] = OUTPUT(label='Battery nameplate', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    rte_thermo: Final[float] = OUTPUT(label='Round-trip efficiency of working fluid cycles', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    rte_net: Final[float] = OUTPUT(label='Net round-trip efficiency considering all parasitics', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    charge_capacity: Final[float] = OUTPUT(label='Total electricity consumption at design-point charge', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    tshours_heater: Final[float] = OUTPUT(label='Hours of TES relative to heater output', units='hr', type='NUMBER', group='System Design Calc', required='*')
    W_dot_hp_in_thermo_des: Final[float] = OUTPUT(label='Heat pump power into working fluid', units='MWe', type='NUMBER', group='Heat Pump', required='*')
    q_dot_hp_hot_out_des: Final[float] = OUTPUT(label='Heat pump heat output', units='MWt', type='NUMBER', group='Heat Pump', required='*')
    q_dot_hp_cold_in_des: Final[float] = OUTPUT(label='Heat pump heat input', units='MWt', type='NUMBER', group='Heat Pump', required='*')
    W_dot_hp_elec_parasitic_des: Final[float] = OUTPUT(label='Heat pump parasitic power', units='MWe', type='NUMBER', group='Heat Pump', required='*')
    W_dot_hp_in_net_des: Final[float] = OUTPUT(label='Heat pump total power consumption', units='MWe', type='NUMBER', group='Heat Pump', required='*')
    COP_net_des: Final[float] = OUTPUT(label='Heat pump net COP', units='MWe', type='NUMBER', group='Heat Pump', required='*')
    m_dot_hp_HT_htf_des: Final[float] = OUTPUT(label='Heat pump HT HTF mass flow rate', units='kg/s', type='NUMBER', group='Heat Pump', required='*')
    W_dot_hp_HT_htf_pump_des: Final[float] = OUTPUT(label='Heat pump HT HTF pump power', units='MWe', type='NUMBER', group='Heat Pump', required='*')
    m_dot_hp_CT_htf_des: Final[float] = OUTPUT(label='Heat pump CT HTF mass flow rate', units='kg/s', type='NUMBER', group='Heat Pump', required='*')
    W_dot_hp_CT_htf_pump_des: Final[float] = OUTPUT(label='Heat pump CT HTF pump power', units='MWe', type='NUMBER', group='Heat Pump', required='*')
    E_hp_su_des: Final[float] = OUTPUT(label='Heat pump startup energy', units='MWt-hr', type='NUMBER', group='Heat Pump', required='*')
    q_dot_pc_hot_in_des: Final[float] = OUTPUT(label='Cycle heat input', units='MWt', type='NUMBER', group='Cycle', required='*')
    q_dot_pc_cold_out_thermo_des: Final[float] = OUTPUT(label='Cycle total heat rejection', units='MWt', type='NUMBER', group='Cycle', required='*')
    W_dot_pc_elec_parasitic_des: Final[float] = OUTPUT(label='Cycle parasitic power', units='MWe', type='NUMBER', group='Cycle', required='*')
    W_dot_pc_net_des: Final[float] = OUTPUT(label='Cycle net power generation', units='MWe', type='NUMBER', group='Cycle', required='*')
    eta_pc_net_des: Final[float] = OUTPUT(label='Cycle net efficiency', units='-', type='NUMBER', group='Cycle', required='*')
    q_dot_pc_cold_to_CTES_des: Final[float] = OUTPUT(label='Cycle heat to cold TES', units='MWt', type='NUMBER', group='Cycle', required='*')
    q_dot_pc_cold_to_surroundings_des: Final[float] = OUTPUT(label='Cycle heat to surroundings', units='MWt', type='NUMBER', group='Cycle', required='*')
    m_dot_pc_HT_htf_des: Final[float] = OUTPUT(label='Cycle HT HTF mass flow rate', units='kg/s', type='NUMBER', group='Cycle', required='*')
    W_dot_pc_HT_htf_pump_des: Final[float] = OUTPUT(label='Cycle HT HTF pump power', units='MWe', type='NUMBER', group='Cycle', required='*')
    m_dot_pc_CT_htf_des: Final[float] = OUTPUT(label='Cycle CT HTF mass flow rate', units='kg/s', type='NUMBER', group='Cycle', required='*')
    W_dot_pc_CT_htf_pump_des: Final[float] = OUTPUT(label='Cycle CT HTF pump power', units='MWe', type='NUMBER', group='Cycle', required='*')
    Q_tes_des: Final[float] = OUTPUT(label='TES design capacity', units='MWt-hr', type='NUMBER', group='TES Design Calc', required='*')
    V_tes_htf_avail: Final[float] = OUTPUT(label='Volume of TES HTF available for heat transfer', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    V_tes_htf_total: Final[float] = OUTPUT(label='Total TES HTF volume', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    d_tank_tes: Final[float] = OUTPUT(label='Diameter of TES tank', units='m', type='NUMBER', group='TES Design Calc', required='*')
    q_dot_loss_tes_des: Final[float] = OUTPUT(label='TES thermal loss at design', units='MWt', type='NUMBER', group='TES Design Calc', required='*')
    Q_CT_tes_des: Final[float] = OUTPUT(label='Cold TES design capacity', units='MWt-hr', type='NUMBER', group='TES Design Calc', required='*')
    V_CT_tes_htf_avail: Final[float] = OUTPUT(label='Volume of cold TES HTF available for heat transfer', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    V_CT_tes_htf_total: Final[float] = OUTPUT(label='Total cold TES HTF volume', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    d_CT_tank_tes: Final[float] = OUTPUT(label='Diameter of cold TES tank', units='m', type='NUMBER', group='TES Design Calc', required='*')
    q_dot_loss_CT_tes_des: Final[float] = OUTPUT(label='Cold TES thermal loss at design', units='MWt', type='NUMBER', group='TES Design Calc', required='*')
    W_dot_bop_design: Final[float] = OUTPUT(label='BOP parasitics at design', units='MWe', type='NUMBER', group='Balance of Plant', required='*')
    W_dot_fixed: Final[float] = OUTPUT(label='Fixed parasitic at design', units='MWe', type='NUMBER', group='Balance of Plant', required='*')
    heater_cost_calc: Final[float] = OUTPUT(label='Heater cost', units='$', type='NUMBER', group='System Costs', required='*')
    tes_cost_calc: Final[float] = OUTPUT(label='TES cost', units='$', type='NUMBER', group='System Costs', required='*')
    CT_tes_cost_calc: Final[float] = OUTPUT(label='Cold TES cost', units='$', type='NUMBER', group='System Costs', required='*')
    bop_cost_calc: Final[float] = OUTPUT(label='BOP cost', units='$', type='NUMBER', group='System Costs', required='*')
    cycle_cost_calc: Final[float] = OUTPUT(label='Cycle cost', units='$', type='NUMBER', group='System Costs', required='*')
    direct_subtotal_cost_calc: Final[float] = OUTPUT(label='Direct subtotal cost', units='$', type='NUMBER', group='System Costs', required='*')
    contingency_cost_calc: Final[float] = OUTPUT(label='Contingency cost', units='$', type='NUMBER', group='System Costs', required='*')
    total_direct_cost_calc: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='System Costs', required='*')
    epc_cost_calc: Final[float] = OUTPUT(label='EPC cost', units='$', type='NUMBER', group='System Costs', required='*')
    land_cost_calc: Final[float] = OUTPUT(label='Land cost', units='$', type='NUMBER', group='System Costs', required='*')
    sales_tax_cost_calc: Final[float] = OUTPUT(label='Sales tax cost', units='$', type='NUMBER', group='System Costs', required='*')
    total_indirect_cost_calc: Final[float] = OUTPUT(label='Total indirect cost', units='$', type='NUMBER', group='System Costs', required='*')
    installed_per_cap_cost_calc: Final[float] = OUTPUT(label='Installed cost per capacity', units='$/kWe', type='NUMBER', group='System Costs', required='*')
    total_installed_cost: Final[float] = OUTPUT(label='Total installed cost', units='$', type='NUMBER', group='System Costs', required='*')
    construction_financing_cost: Final[float] = OUTPUT(label='Total construction financing cost', units='$', type='NUMBER', group='Financial Parameters', required='*')
    time_hr: Final[Array] = OUTPUT(label='Time at end of timestep', units='hr', type='ARRAY', required='sim_type=1')
    elec_purchase_price_mult: Final[Array] = OUTPUT(label='Electricity purchase price multiplier', type='ARRAY', required='sim_type=1')
    tou_period: Final[Array] = OUTPUT(label='Time of use period', type='ARRAY', required='sim_type=1')
    tdry: Final[Array] = OUTPUT(label='Resource dry Bulb temperature', units='C', type='ARRAY', required='sim_type=1')
    twet: Final[Array] = OUTPUT(label='Resource wet Bulb temperature', units='C', type='ARRAY', required='sim_type=1')
    T_hp_HT_htf_cold_in: Final[Array] = OUTPUT(label='Heat pump hot tes HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_hp_HT_htf_hot_out: Final[Array] = OUTPUT(label='Heat pump hot tes HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_hp_CT_htf_hot_in: Final[Array] = OUTPUT(label='Heat pump cold tes HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_hp_CT_htf_cold_out: Final[Array] = OUTPUT(label='Heat pump cold tes HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    m_dot_hp_HT_htf: Final[Array] = OUTPUT(label='Heat pump hot tes HTF mass flow rate', units='kg/s', type='ARRAY', group='sim_type=1')
    m_dot_hp_CT_htf: Final[Array] = OUTPUT(label='Heat pump cold tes HTF mass flow rate', units='kg/s', type='ARRAY', required='sim_type=1')
    q_dot_hp_startup: Final[Array] = OUTPUT(label='Heat pump startup power', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_hp_to_HT_htf: Final[Array] = OUTPUT(label='Heat pump thermal power to hot tes HTF', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_hp_from_CT_htf: Final[Array] = OUTPUT(label='Heat pump thermal power from cold tes HTF', units='MWt', type='ARRAY', required='sim_type=1')
    W_dot_hp_thermo: Final[Array] = OUTPUT(label='Heat pump thermodynamic power in', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_hp_parasitics: Final[Array] = OUTPUT(label='Heat pump thermodynamic parasitics', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_hp_HT_htf_pump: Final[Array] = OUTPUT(label='Heat pump hot tes HTF pump power', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_hp_CT_htf_pump: Final[Array] = OUTPUT(label='Heat pump cold tes HTF pump power', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_hp_net: Final[Array] = OUTPUT(label='Heat pump total power in', units='MWe', type='ARRAY', required='sim_type=1')
    cop_hot_hp_thermo: Final[Array] = OUTPUT(label='Heat pump thermodynamic hot COP', type='ARRAY', required='sim_type=1')
    T_pc_HT_htf_hot_in: Final[Array] = OUTPUT(label='PC hot tes HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_pc_HT_htf_cold_out: Final[Array] = OUTPUT(label='PC hot tes HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_pc_CT_htf_cold_in: Final[Array] = OUTPUT(label='PC cold tes HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_pc_CT_htf_hot_out: Final[Array] = OUTPUT(label='PC cold tes HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    m_dot_pc_HT_htf: Final[Array] = OUTPUT(label='PC hot tes HTF mass flow rate', units='kg/s', type='ARRAY', group='sim_type=1')
    m_dot_pc_CT_htf: Final[Array] = OUTPUT(label='PC cold tes HTF mass flow rate', units='kg/s', type='ARRAY', required='sim_type=1')
    q_dot_pc_startup: Final[Array] = OUTPUT(label='PC startup power', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_from_HT_htf: Final[Array] = OUTPUT(label='PC thermal power from hot tes HTF', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_thermo_out: Final[Array] = OUTPUT(label='PC total heat leaving cycle', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_to_CT_htf: Final[Array] = OUTPUT(label='PC thermal power to cold tes HTF', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_rejected: Final[Array] = OUTPUT(label='PC thermal power rejected to surroundings', units='MWt', type='ARRAY', required='sim_type=1')
    W_dot_pc_thermo_out: Final[Array] = OUTPUT(label='PC thermodynamic power out', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_pc_parasitics: Final[Array] = OUTPUT(label='PC parasitics including cooling power', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_pc_HT_htf_pump: Final[Array] = OUTPUT(label='PC hot tes HTF pump power', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_pc_CT_htf_pump: Final[Array] = OUTPUT(label='PC cold tes HTF pump power', units='MWe', type='ARRAY', required='sim_type=1')
    eta_pc_thermo: Final[Array] = OUTPUT(label='PC thermodynamic efficiency', type='ARRAY', required='sim_type=1')
    q_dot_dc_tes: Final[Array] = OUTPUT(label='TES discharge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_ch_tes: Final[Array] = OUTPUT(label='TES charge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    e_ch_tes: Final[Array] = OUTPUT(label='TES charge state', units='MWht', type='ARRAY', required='sim_type=1')
    q_dot_tes_losses: Final[Array] = OUTPUT(label='TES thermal losses', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_tes_heater: Final[Array] = OUTPUT(label='TES freeze protection power', units='MWe', type='ARRAY', required='sim_type=1')
    T_tes_hot: Final[Array] = OUTPUT(label='TES hot temperature', units='C', type='ARRAY', required='sim_type=1')
    T_tes_cold: Final[Array] = OUTPUT(label='TES cold temperature', units='C', type='ARRAY', required='sim_type=1')
    mass_tes_cold: Final[Array] = OUTPUT(label='TES cold tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    mass_tes_hot: Final[Array] = OUTPUT(label='TES hot tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    q_dot_CT_tes_losses: Final[Array] = OUTPUT(label='TES thermal losses', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_CT_tes_heater: Final[Array] = OUTPUT(label='TES freeze protection power', units='MWe', type='ARRAY', required='sim_type=1')
    T_CT_tes_hot: Final[Array] = OUTPUT(label='TES hot temperature', units='C', type='ARRAY', required='sim_type=1')
    T_CT_tes_cold: Final[Array] = OUTPUT(label='TES cold temperature', units='C', type='ARRAY', required='sim_type=1')
    mass_CT_tes_cold: Final[Array] = OUTPUT(label='TES cold tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    mass_CT_tes_hot: Final[Array] = OUTPUT(label='TES hot tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    W_dot_fixed_parasitics: Final[Array] = OUTPUT(label='Parasitic power plant fixed load', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_bop_parasitics: Final[Array] = OUTPUT(label='Parasitic power plant generation-dependent laod', units='MWe', type='ARRAY', required='sim_type=1')
    W_dot_out_net: Final[Array] = OUTPUT(label='Total electric power to grid', units='MWe', type='ARRAY', required='sim_type=1')
    gen: Final[Array] = OUTPUT(label='Total electric power to grid with available derate', units='kWe', type='ARRAY', required='sim_type=1')
    n_op_modes: Final[Array] = OUTPUT(label='Operating modes in reporting timestep', type='ARRAY', required='sim_type=1')
    op_mode_1: Final[Array] = OUTPUT(label='1st operating mode', type='ARRAY', required='sim_type=1')
    op_mode_2: Final[Array] = OUTPUT(label='2nd operating mode, if applicable', type='ARRAY', required='sim_type=1')
    op_mode_3: Final[Array] = OUTPUT(label='3rd operating mode, if applicable', type='ARRAY', required='sim_type=1')
    m_dot_balance: Final[Array] = OUTPUT(label='Relative mass flow balance error', type='ARRAY', required='sim_type=1')
    q_balance: Final[Array] = OUTPUT(label='Relative energy balance error', type='ARRAY', required='sim_type=1')
    q_pc_target: Final[Array] = OUTPUT(label='Controller target pc heat input', units='MWt', type='ARRAY', required='sim_type=1')
    disp_rel_mip_gap: Final[Array] = OUTPUT(label='Dispatch relative MIP gap', type='ARRAY', required='sim_type=1')
    disp_solve_state: Final[Array] = OUTPUT(label='Dispatch solver state', type='ARRAY', required='sim_type=1')
    disp_subopt_flag: Final[Array] = OUTPUT(label='Dispatch suboptimal solution flag', type='ARRAY', required='sim_type=1')
    disp_solve_iter: Final[Array] = OUTPUT(label='Dispatch iterations count', type='ARRAY', required='sim_type=1')
    disp_objective: Final[Array] = OUTPUT(label='Dispatch objective function value', type='ARRAY', required='sim_type=1')
    disp_obj_relax: Final[Array] = OUTPUT(label='Dispatch objective function - relaxed max', type='ARRAY', required='sim_type=1')
    disp_qsfprod_expected: Final[Array] = OUTPUT(label='Dispatch expected heat pump heat generation', units='MWt', type='ARRAY', required='sim_type=1')
    disp_qsfsu_expected: Final[Array] = OUTPUT(label='Dispatch expected heat pump startup enegy', units='MWt', type='ARRAY', required='sim_type=1')
    disp_tes_expected: Final[Array] = OUTPUT(label='Dispatch expected TES charge level', units='MWht', type='ARRAY', required='sim_type=1')
    disp_pceff_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle efficiency adj.', type='ARRAY', required='sim_type=1')
    disp_qpbsu_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle startup energy', units='MWht', type='ARRAY', required='sim_type=1')
    disp_wpb_expected: Final[Array] = OUTPUT(label='Dispatch expected power generation', units='MWe', type='ARRAY', required='sim_type=1')
    disp_rev_expected: Final[Array] = OUTPUT(label='Dispatch expected revenue factor', type='ARRAY', required='sim_type=1')
    disp_presolve_nconstr: Final[Array] = OUTPUT(label='Dispatch number of constraints in problem', type='ARRAY', required='sim_type=1')
    disp_presolve_nvar: Final[Array] = OUTPUT(label='Dispatch number of variables in problem', type='ARRAY', required='sim_type=1')
    disp_solve_time: Final[Array] = OUTPUT(label='Dispatch solver time', units='sec', type='ARRAY', required='sim_type=1')
    annual_energy: Final[float] = OUTPUT(label='Annual total electric power to grid', units='kWhe', type='NUMBER', required='sim_type=1')
    disp_objective_ann: Final[float] = OUTPUT(label='Annual sum of dispatch objective function value', units='$', type='NUMBER', required='sim_type=1')
    disp_iter_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solver iterations', type='NUMBER', required='sim_type=1')
    disp_presolve_nconstr_ann: Final[float] = OUTPUT(label='Annual sum of dispatch problem constraint count', type='NUMBER', required='sim_type=1')
    disp_presolve_nvar_ann: Final[float] = OUTPUT(label='Annual sum of dispatch problem variable count', type='NUMBER', required='sim_type=1')
    disp_solve_time_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solver time', units='sec', type='NUMBER', required='sim_type=1')
    disp_solve_state_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solve state', type='NUMBER', required='sim_type=1')
    avg_suboptimal_rel_mip_gap: Final[float] = OUTPUT(label='Average suboptimal relative MIP gap', units='%', type='NUMBER', required='sim_type=1')
    ppa_soln_mode: Final[float] = OUTPUT(label='PPA solution mode', units='0/1', type='NUMBER', group='Revenue', required='sim_type=1', constraints='INTEGER,MIN = 0,MAX = 1', meta='0 = solve ppa,1 = specify ppa')
    flip_target_percent: Final[float] = OUTPUT(label='After-tax IRR target', units='%', type='NUMBER', group='Revenue', required='sim_type=1', constraints='MIN=0,MAX=100')
    adjust_constant: float = INPUT(name='adjust:constant', label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='*', constraints='MAX=100')
    adjust_hourly: Array = INPUT(name='adjust:hourly', label='Hourly Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    adjust_timeindex: Array = INPUT(name='adjust:timeindex', label='Lifetime Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    adjust_periods: Matrix = INPUT(name='adjust:periods', label='Period-based Adjustment Factors', units='%', type='MATRIX', group='Adjustment Factors', required='?', constraints='COLS=3', meta='n x 3 matrix [ start, end, loss ]')
    annual_energy_distribution_time: Final[Matrix] = OUTPUT(label='Annual energy production as function of time', units='kW', type='MATRIX', group='Heatmaps')

    def __init__(self, *args: Mapping[str, Any],
                 solar_resource_file: str = ...,
                 is_dispatch: float = ...,
                 sim_type: float = ...,
                 etes_financial_model: float = ...,
                 time_start: float = ...,
                 time_stop: float = ...,
                 time_steps_per_hour: float = ...,
                 vacuum_arrays: float = ...,
                 heater_mult: float = ...,
                 tshours: float = ...,
                 W_dot_pc_thermo_des: float = ...,
                 eta_pc_thermo_des: float = ...,
                 f_pc_parasitic_des: float = ...,
                 cop_hp_thermo_des: float = ...,
                 f_hp_parasitic_des: float = ...,
                 T_HT_hot_htf_des: float = ...,
                 T_HT_cold_htf_des: float = ...,
                 T_CT_cold_htf_des: float = ...,
                 T_CT_hot_htf_des: float = ...,
                 hot_htf_code: float = ...,
                 ud_hot_htf_props: Matrix = ...,
                 cold_htf_code: float = ...,
                 ud_cold_htf_props: Matrix = ...,
                 f_q_dot_des_allowable_su: float = ...,
                 hrs_startup_at_max_rate: float = ...,
                 f_q_dot_heater_min: float = ...,
                 heat_pump_HT_HTF_pump_coef: float = ...,
                 heat_pump_CT_HTF_pump_coef: float = ...,
                 pb_pump_coef: float = ...,
                 CT_pb_pump_coef: float = ...,
                 startup_time: float = ...,
                 startup_frac: float = ...,
                 cycle_max_frac: float = ...,
                 cycle_cutoff_frac: float = ...,
                 q_sby_frac: float = ...,
                 tes_init_hot_htf_percent: float = ...,
                 h_tank: float = ...,
                 cold_tank_max_heat: float = ...,
                 u_tank: float = ...,
                 tank_pairs: float = ...,
                 cold_tank_Thtr: float = ...,
                 h_tank_min: float = ...,
                 hot_tank_Thtr: float = ...,
                 hot_tank_max_heat: float = ...,
                 CT_h_tank: float = ...,
                 CT_u_tank: float = ...,
                 CT_tank_pairs: float = ...,
                 CT_h_tank_min: float = ...,
                 disp_horizon: float = ...,
                 disp_frequency: float = ...,
                 disp_steps_per_hour: float = ...,
                 disp_max_iter: float = ...,
                 disp_timeout: float = ...,
                 disp_mip_gap: float = ...,
                 disp_spec_bb: float = ...,
                 disp_reporting: float = ...,
                 disp_spec_presolve: float = ...,
                 disp_spec_scaling: float = ...,
                 disp_pen_delta_w: float = ...,
                 disp_csu_cost: float = ...,
                 disp_hsu_cost: float = ...,
                 disp_time_weighting: float = ...,
                 disp_down_time_min: float = ...,
                 disp_up_time_min: float = ...,
                 ppa_multiplier_model: float = ...,
                 dispatch_factors_ts: Array = ...,
                 dispatch_sched_weekday: Matrix = ...,
                 dispatch_sched_weekend: Matrix = ...,
                 dispatch_factor1: float = ...,
                 dispatch_factor2: float = ...,
                 dispatch_factor3: float = ...,
                 dispatch_factor4: float = ...,
                 dispatch_factor5: float = ...,
                 dispatch_factor6: float = ...,
                 dispatch_factor7: float = ...,
                 dispatch_factor8: float = ...,
                 dispatch_factor9: float = ...,
                 ppa_price_input: Array = ...,
                 pb_fixed_par: float = ...,
                 bop_par: float = ...,
                 bop_par_f: float = ...,
                 bop_par_0: float = ...,
                 bop_par_1: float = ...,
                 bop_par_2: float = ...,
                 cycle_spec_cost: float = ...,
                 tes_spec_cost: float = ...,
                 CT_tes_spec_cost: float = ...,
                 heat_pump_spec_cost: float = ...,
                 bop_spec_cost: float = ...,
                 contingency_rate: float = ...,
                 sales_tax_frac: float = ...,
                 epc_cost_perc_of_direct: float = ...,
                 epc_cost_per_watt: float = ...,
                 epc_cost_fixed: float = ...,
                 land_cost_perc_of_direct: float = ...,
                 land_cost_per_watt: float = ...,
                 land_cost_fixed: float = ...,
                 sales_tax_rate: float = ...,
                 const_per_interest_rate1: float = ...,
                 const_per_interest_rate2: float = ...,
                 const_per_interest_rate3: float = ...,
                 const_per_interest_rate4: float = ...,
                 const_per_interest_rate5: float = ...,
                 const_per_months1: float = ...,
                 const_per_months2: float = ...,
                 const_per_months3: float = ...,
                 const_per_months4: float = ...,
                 const_per_months5: float = ...,
                 const_per_percent1: float = ...,
                 const_per_percent2: float = ...,
                 const_per_percent3: float = ...,
                 const_per_percent4: float = ...,
                 const_per_percent5: float = ...,
                 const_per_upfront_rate1: float = ...,
                 const_per_upfront_rate2: float = ...,
                 const_per_upfront_rate3: float = ...,
                 const_per_upfront_rate4: float = ...,
                 const_per_upfront_rate5: float = ...,
                 adjust_constant: float = ...,
                 adjust_hourly: Array = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
