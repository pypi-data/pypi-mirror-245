
# This is a generated file

"""etes_electric_resistance - Electric resistance heater charging TES from grid, discharge with power cycle"""

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
    'T_htf_cold_des': float,
    'T_htf_hot_des': float,
    'P_ref': float,
    'design_eff': float,
    'tshours': float,
    'heater_mult': float,
    'pc_config': float,
    'pb_pump_coef': float,
    'startup_time': float,
    'startup_frac': float,
    'cycle_max_frac': float,
    'cycle_cutoff_frac': float,
    'q_sby_frac': float,
    'dT_cw_ref': float,
    'T_amb_des': float,
    'CT': float,
    'T_approach': float,
    'T_ITD_des': float,
    'P_cond_ratio': float,
    'pb_bd_frac': float,
    'P_cond_min': float,
    'n_pl_inc': float,
    'tech_type': float,
    'ud_f_W_dot_cool_des': float,
    'ud_m_dot_water_cool_des': float,
    'ud_ind_od': Matrix,
    'hot_htf_code': float,
    'ud_hot_htf_props': Matrix,
    'tes_init_hot_htf_percent': float,
    'h_tank': float,
    'cold_tank_max_heat': float,
    'u_tank': float,
    'tank_pairs': float,
    'cold_tank_Thtr': float,
    'h_tank_min': float,
    'hot_tank_Thtr': float,
    'hot_tank_max_heat': float,
    'heater_efficiency': float,
    'f_q_dot_des_allowable_su': float,
    'hrs_startup_at_max_rate': float,
    'f_q_dot_heater_min': float,
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
    'pb_fixed_par': float,
    'bop_par': float,
    'bop_par_f': float,
    'bop_par_0': float,
    'bop_par_1': float,
    'bop_par_2': float,
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
    'mp_energy_market_revenue': Matrix,
    'cycle_spec_cost': float,
    'tes_spec_cost': float,
    'heater_spec_cost': float,
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
    'P_boil': float,
    'system_capacity': float,
    'nameplate': float,
    'cp_system_nameplate': float,
    'cp_battery_nameplate': float,
    'q_pb_design': float,
    'q_dot_heater_design': float,
    'tshours_heater': float,
    'Q_tes_des': float,
    'm_dot_htf_cycle_des': float,
    'cp_htf_cycle_des': float,
    'n_T_htf_pars_calc': float,
    'n_T_amb_pars_calc': float,
    'n_m_dot_pars_calc': float,
    'T_htf_ref_calc': float,
    'T_htf_low_calc': float,
    'T_htf_high_calc': float,
    'T_amb_ref_calc': float,
    'T_amb_low_calc': float,
    'T_amb_high_calc': float,
    'm_dot_htf_ND_ref_calc': float,
    'm_dot_htf_ND_low_calc': float,
    'm_dot_htf_ND_high_calc': float,
    'W_dot_gross_ND_des_calc': float,
    'Q_dot_HTF_ND_des_calc': float,
    'W_dot_cooling_ND_des_calc': float,
    'm_dot_water_ND_des_calc': float,
    'W_dot_heater_des': float,
    'E_heater_su_des': float,
    'V_tes_htf_avail': float,
    'V_tes_htf_total': float,
    'd_tank_tes': float,
    'q_dot_loss_tes_des': float,
    'dens_store_htf_at_T_ave': float,
    'W_dot_bop_design': float,
    'heater_cost_calc': float,
    'tes_cost_calc': float,
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
    'W_dot_heater': Array,
    'q_dot_heater_to_htf': Array,
    'q_dot_heater_startup': Array,
    'm_dot_htf_heater': Array,
    'T_htf_heater_in': Array,
    'T_htf_heater_out': Array,
    'q_dot_dc_tes': Array,
    'q_dot_ch_tes': Array,
    'e_ch_tes': Array,
    'q_dot_tes_losses': Array,
    'q_dot_tes_heater': Array,
    'T_tes_hot': Array,
    'T_tes_cold': Array,
    'mass_tes_cold': Array,
    'mass_tes_hot': Array,
    'eta_cycle_gross': Array,
    'q_dot_cycle': Array,
    'W_dot_cycle_gross': Array,
    'q_dot_cycle_startup': Array,
    'W_dot_cycle_cooling': Array,
    'W_dot_cycle_net': Array,
    'eta_cycle_net': Array,
    'm_dot_htf_cycle': Array,
    'T_htf_cycle_in': Array,
    'T_htf_cycle_out': Array,
    'm_dot_water_cycle': Array,
    'W_dot_cycle_htf_pump': Array,
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
    'operating_modes_a': Array,
    'operating_modes_b': Array,
    'operating_modes_c': Array,
    'annual_energy': float,
    'annual_energy_full_availability': float,
    'annual_E_heater': float,
    'annual_Q_heater_to_htf': float,
    'annual_Q_heater_startup': float,
    'annual_E_tes_heater': float,
    'annual_Q_tes_losses': float,
    'annual_E_cycle_gross': float,
    'annual_Q_cycle_thermal_in': float,
    'annual_Q_cycle_thermal_startup': float,
    'disp_objective_ann': float,
    'disp_iter_ann': float,
    'disp_presolve_nconstr_ann': float,
    'disp_presolve_nvar_ann': float,
    'disp_solve_time_ann': float,
    'disp_solve_state_ann': float,
    'avg_suboptimal_rel_mip_gap': float,
    'sim_cpu_run_time': float,
    'ppa_soln_mode': float,
    'flip_target_percent': float,
    'total_land_area': float,
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
    T_htf_cold_des: float = INPUT(label='Cold HTF inlet temperature at design conditions', units='C', type='NUMBER', group='System Design', required='*')
    T_htf_hot_des: float = INPUT(label='Hot HTF outlet temperature at design conditions', units='C', type='NUMBER', group='System Design', required='*')
    P_ref: float = INPUT(label='Reference output electric power at design condition', units='MW', type='NUMBER', group='System Design', required='*')
    design_eff: float = INPUT(label='Power cycle efficiency at design', units='none', type='NUMBER', group='System Design', required='*')
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='System Design', required='*')
    heater_mult: float = INPUT(label='Heater multiple relative to design cycle thermal power', units='-', type='NUMBER', group='System Design', required='*')
    pc_config: float = INPUT(label='PC configuration 0=Steam Rankine, 1=user defined', type='NUMBER', group='Power Cycle', required='?=0', constraints='INTEGER')
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='Power Cycle', required='*')
    startup_time: float = INPUT(label='Time needed for power block startup', units='hr', type='NUMBER', group='Power Cycle', required='*')
    startup_frac: float = INPUT(label='Fraction of design thermal power needed for startup', units='none', type='NUMBER', group='Power Cycle', required='*')
    cycle_max_frac: float = INPUT(label='Maximum turbine over design operation fraction', type='NUMBER', group='Power Cycle', required='*')
    cycle_cutoff_frac: float = INPUT(label='Minimum turbine operation fraction before shutdown', type='NUMBER', group='Power Cycle', required='*')
    q_sby_frac: float = INPUT(label='Fraction of thermal power required for standby', type='NUMBER', group='Power Cycle', required='*')
    dT_cw_ref: float = INPUT(label='Reference condenser cooling water inlet/outlet temperature difference', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    T_amb_des: float = INPUT(label='Reference ambient temperature at design point', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    CT: float = INPUT(label='Condensor type: 1=evaporative, 2=air', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    T_approach: float = INPUT(label='Cooling tower approach temperature', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    T_ITD_des: float = INPUT(label='ITD at design for dry system', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    P_cond_ratio: float = INPUT(label='Condenser pressure ratio', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    pb_bd_frac: float = INPUT(label='Power block blowdown steam fraction', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    P_cond_min: float = INPUT(label='Minimum condenser pressure', units='inHg', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    n_pl_inc: float = INPUT(label='Number of part-load increments for the heat rejection system', units='none', type='NUMBER', group='Rankine Cycle', required='pc_config=0', constraints='INTEGER')
    tech_type: float = INPUT(label='Turbine inlet pressure control 1=Fixed, 3=Sliding', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    ud_f_W_dot_cool_des: float = INPUT(label='Percent of user-defined power cycle design gross output consumed by cooling', units='%', type='NUMBER', group='User Defined Power Cycle', required='pc_config=1')
    ud_m_dot_water_cool_des: float = INPUT(label='Mass flow rate of water required at user-defined power cycle design point', units='kg/s', type='NUMBER', group='User Defined Power Cycle', required='pc_config=1')
    ud_ind_od: Matrix = INPUT(label='Off design user-defined power cycle performance as function of T_htf, m_dot_htf [ND], and T_amb', type='MATRIX', group='User Defined Power Cycle', required='pc_config=1')
    hot_htf_code: float = INPUT(label='Receiver HTF, 17=Salt (60% NaNO3, 40% KNO3) 10=Salt (46.5% LiF 11.5% NaF 42% KF) 50=Lookup tables', type='NUMBER', group='Thermal Storage', required='*')
    ud_hot_htf_props: Matrix = INPUT(label='User-defined TES fluid property data', units='-', type='MATRIX', group='Thermal Storage', required='hot_htf_code=50')
    tes_init_hot_htf_percent: float = INPUT(label='Initial fraction of available volume that is hot', units='%', type='NUMBER', group='Thermal Storage', required='*')
    h_tank: float = INPUT(label='Total height of tank (height of HTF when tank is full)', units='m', type='NUMBER', group='Thermal Storage', required='*')
    cold_tank_max_heat: float = INPUT(label='Rated heater capacity for cold tank heating', units='MW', type='NUMBER', group='Thermal Storage', required='*')
    u_tank: float = INPUT(label='Loss coefficient from the tank', units='W/m2-K', type='NUMBER', group='Thermal Storage', required='*')
    tank_pairs: float = INPUT(label='Number of equivalent tank pairs', type='NUMBER', group='Thermal Storage', required='*', constraints='INTEGER')
    cold_tank_Thtr: float = INPUT(label='Minimum allowable cold tank HTF temperature', units='C', type='NUMBER', group='Thermal Storage', required='*')
    h_tank_min: float = INPUT(label='Minimum allowable HTF height in storage tank', units='m', type='NUMBER', group='Thermal Storage', required='*')
    hot_tank_Thtr: float = INPUT(label='Minimum allowable hot tank HTF temperature', units='C', type='NUMBER', group='Thermal Storage', required='*')
    hot_tank_max_heat: float = INPUT(label='Rated heater capacity for hot tank heating', units='MW', type='NUMBER', group='Thermal Storage', required='*')
    heater_efficiency: float = INPUT(label='Heater electric to thermal efficiency', units='%', type='NUMBER', group='Heater', required='*')
    f_q_dot_des_allowable_su: float = INPUT(label='Fraction of design power allowed during startup', units='-', type='NUMBER', group='Heater', required='*')
    hrs_startup_at_max_rate: float = INPUT(label='Duration of startup at max startup power', units='hr', type='NUMBER', group='Heater', required='*')
    f_q_dot_heater_min: float = INPUT(label='Minimum allowable heater output as fraction of design', type='NUMBER', group='Heater', required='*')
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
    pb_fixed_par: float = INPUT(label="Fixed parasitic load that don't generate heat - runs at all times", units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    bop_par: float = INPUT(label='Balance of plant parasitic power fraction', units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    bop_par_f: float = INPUT(label='Balance of plant parasitic power fraction - mult frac', type='NUMBER', group='System Control', required='*')
    bop_par_0: float = INPUT(label='Balance of plant parasitic power fraction - const coeff', type='NUMBER', group='System Control', required='*')
    bop_par_1: float = INPUT(label='Balance of plant parasitic power fraction - linear coeff', type='NUMBER', group='System Control', required='*')
    bop_par_2: float = INPUT(label='Balance of plant parasitic power fraction - quadratic coeff', type='NUMBER', group='System Control', required='*')
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
    mp_energy_market_revenue: Matrix = INPUT(label='Energy market revenue input', type='MATRIX', group='Revenue', required='etes_financial_model=6&is_dispatch=1&sim_type=1', meta='Lifetime x 2[Cleared Capacity(MW),Price($/MWh)]')
    cycle_spec_cost: float = INPUT(label='Power cycle specific cost', units='$/kWe', type='NUMBER', group='System Cost', required='*')
    tes_spec_cost: float = INPUT(label='Thermal energy storage specific cost', units='$/kWht', type='NUMBER', group='System Costs', required='*')
    heater_spec_cost: float = INPUT(label='Heater specific cost', units='$/kWht', type='NUMBER', group='System Costs', required='*')
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
    P_boil: float = INPUT(label='Boiler operating pressure', units='bar', type='NUMBER', group='Rankine Cycle')
    system_capacity: Final[float] = OUTPUT(label='System capacity', units='kWe', type='NUMBER', group='System Design Calc', required='*')
    nameplate: Final[float] = OUTPUT(label='Nameplate capacity', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    cp_system_nameplate: Final[float] = OUTPUT(label='System capacity for capacity payments', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    cp_battery_nameplate: Final[float] = OUTPUT(label='Battery nameplate', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    q_pb_design: Final[float] = OUTPUT(label='Cycle thermal input at designMWt', type='NUMBER', group='*', meta='System Design Calc')
    q_dot_heater_design: Final[float] = OUTPUT(label='Heater thermal output at design', units='MWt', type='NUMBER', group='System Design Calc', required='*')
    tshours_heater: Final[float] = OUTPUT(label='Hours of TES relative to heater output', units='hr', type='NUMBER', group='System Design Calc', required='*')
    Q_tes_des: Final[float] = OUTPUT(label='TES design capacity', units='MWt-hr', type='NUMBER', group='System Design Calc', required='*')
    m_dot_htf_cycle_des: Final[float] = OUTPUT(label='Cycle htf mass flow rate at design', units='kg/s', type='NUMBER', group='Cycle Design Calc', required='*')
    cp_htf_cycle_des: Final[float] = OUTPUT(label='Cycle htf cp at T ave at design', units='kJ/kg-K', type='NUMBER', group='Cycle Design Calc', required='*')
    n_T_htf_pars_calc: Final[float] = OUTPUT(label='UDPC number of HTF parametric values', type='NUMBER', group='UDPC Design Calc', required='*')
    n_T_amb_pars_calc: Final[float] = OUTPUT(label='UDPC number of ambient temp parametric values', type='NUMBER', group='UDPC Design Calc', required='*')
    n_m_dot_pars_calc: Final[float] = OUTPUT(label='UDPC number of mass flow parametric values', type='NUMBER', group='UDPC Design Calc', required='*')
    T_htf_ref_calc: Final[float] = OUTPUT(label='UDPC reference HTF temperature', units='C', type='NUMBER', group='UDPC Design Calc', required='*')
    T_htf_low_calc: Final[float] = OUTPUT(label='UDPC low level HTF temperature', units='C', type='NUMBER', group='UDPC Design Calc', required='*')
    T_htf_high_calc: Final[float] = OUTPUT(label='UDPC high level HTF temperature', units='C', type='NUMBER', group='UDPC Design Calc', required='*')
    T_amb_ref_calc: Final[float] = OUTPUT(label='UDPC reference ambient temperature', units='C', type='NUMBER', group='UDPC Design Calc', required='*')
    T_amb_low_calc: Final[float] = OUTPUT(label='UDPC low level ambient temperature', units='C', type='NUMBER', group='UDPC Design Calc', required='*')
    T_amb_high_calc: Final[float] = OUTPUT(label='UDPC high level ambient temperature', units='C', type='NUMBER', group='UDPC Design Calc', required='*')
    m_dot_htf_ND_ref_calc: Final[float] = OUTPUT(label='UDPC reference normalized mass flow rate', type='NUMBER', group='UDPC Design Calc', required='*')
    m_dot_htf_ND_low_calc: Final[float] = OUTPUT(label='UDPC low level normalized mass flow rate', type='NUMBER', group='UDPC Design Calc', required='*')
    m_dot_htf_ND_high_calc: Final[float] = OUTPUT(label='UDPC high level normalized mass flow rate', type='NUMBER', group='UDPC Design Calc', required='*')
    W_dot_gross_ND_des_calc: Final[float] = OUTPUT(label='UDPC calculated normalized gross power at design', type='NUMBER', group='UDPC Design Calc', required='*')
    Q_dot_HTF_ND_des_calc: Final[float] = OUTPUT(label='UDPC calculated normalized heat input at design', type='NUMBER', group='UDPC Design Calc', required='*')
    W_dot_cooling_ND_des_calc: Final[float] = OUTPUT(label='UPPC calculated normalized cooling power at design', type='NUMBER', group='UDPC Design Calc', required='*')
    m_dot_water_ND_des_calc: Final[float] = OUTPUT(label='UDPC calculated water use at design', type='NUMBER', group='UDPC Design Calc', required='*')
    W_dot_heater_des: Final[float] = OUTPUT(label='Heater electricity consumption at design', units='MWe', type='NUMBER', group='Cycle Design Calc', required='*')
    E_heater_su_des: Final[float] = OUTPUT(label='Heater startup energy', units='MWt-hr', type='NUMBER', group='Cycle Design Calc', required='*')
    V_tes_htf_avail: Final[float] = OUTPUT(label='Volume of TES HTF available for heat transfer', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    V_tes_htf_total: Final[float] = OUTPUT(label='Total TES HTF volume', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    d_tank_tes: Final[float] = OUTPUT(label='Diameter of TES tank', units='m', type='NUMBER', group='TES Design Calc', required='*')
    q_dot_loss_tes_des: Final[float] = OUTPUT(label='TES thermal loss at design', units='MWt', type='NUMBER', group='TES Design Calc', required='*')
    dens_store_htf_at_T_ave: Final[float] = OUTPUT(label='Density of TES HTF at avg temps', units='kg/m3', type='NUMBER', group='TES Design Calc', required='*')
    W_dot_bop_design: Final[float] = OUTPUT(label='BOP parasitics at design', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    heater_cost_calc: Final[float] = OUTPUT(label='Heater cost', units='$', type='NUMBER', group='System Costs', required='*')
    tes_cost_calc: Final[float] = OUTPUT(label='TES cost', units='$', type='NUMBER', group='System Costs', required='*')
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
    W_dot_heater: Final[Array] = OUTPUT(label='Heater electricity consumption', units='MWe', type='ARRAY', required='sim_type=1')
    q_dot_heater_to_htf: Final[Array] = OUTPUT(label='Heater thermal power to HTF', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_heater_startup: Final[Array] = OUTPUT(label='Heater thermal power consumed during startup', units='MWt', type='ARRAY', required='sim_type=1')
    m_dot_htf_heater: Final[Array] = OUTPUT(label='Heater HTF mass flow rate', units='kg/s', type='ARRAY', required='sim_type=1')
    T_htf_heater_in: Final[Array] = OUTPUT(label='Heater HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_htf_heater_out: Final[Array] = OUTPUT(label='Heater HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    q_dot_dc_tes: Final[Array] = OUTPUT(label='TES discharge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_ch_tes: Final[Array] = OUTPUT(label='TES charge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    e_ch_tes: Final[Array] = OUTPUT(label='TES charge state', units='MWht', type='ARRAY', required='sim_type=1')
    q_dot_tes_losses: Final[Array] = OUTPUT(label='TES thermal losses', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_tes_heater: Final[Array] = OUTPUT(label='TES freeze protection power', units='MWe', type='ARRAY', required='sim_type=1')
    T_tes_hot: Final[Array] = OUTPUT(label='TES hot temperature', units='C', type='ARRAY', required='sim_type=1')
    T_tes_cold: Final[Array] = OUTPUT(label='TES cold temperature', units='C', type='ARRAY', required='sim_type=1')
    mass_tes_cold: Final[Array] = OUTPUT(label='TES cold tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    mass_tes_hot: Final[Array] = OUTPUT(label='TES hot tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    eta_cycle_gross: Final[Array] = OUTPUT(label='PC efficiency gross (no cooling parasitics)', type='ARRAY', group='powerblock', required='sim_type=1')
    q_dot_cycle: Final[Array] = OUTPUT(label='PC thermal power', units='MWt', type='ARRAY', group='powerblock', required='sim_type=1')
    W_dot_cycle_gross: Final[Array] = OUTPUT(label='PC electrical power gross (no cooling parasitics)', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
    q_dot_cycle_startup: Final[Array] = OUTPUT(label='PC startup thermal power', units='MWt', type='ARRAY', group='powerblock', required='sim_type=1')
    W_dot_cycle_cooling: Final[Array] = OUTPUT(label='PC cooling parasitics', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
    W_dot_cycle_net: Final[Array] = OUTPUT(label='PC electrical power net (with cooling parasitics)', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
    eta_cycle_net: Final[Array] = OUTPUT(label='PC efficiency net (with cooling parasitics)', type='ARRAY', group='powerblock', required='sim_type=1')
    m_dot_htf_cycle: Final[Array] = OUTPUT(label='PC HTF mass flow rate', units='kg/s', type='ARRAY', group='powerblock', required='sim_type=1')
    T_htf_cycle_in: Final[Array] = OUTPUT(label='PC HTF inlet temperature', units='C', type='ARRAY', group='powerblock', required='sim_type=1')
    T_htf_cycle_out: Final[Array] = OUTPUT(label='PC HTF outlet temperature', units='C', type='ARRAY', group='powerblock', required='sim_type=1')
    m_dot_water_cycle: Final[Array] = OUTPUT(label='PC water consumption, makeup + cooling', units='kg/s', type='ARRAY', group='powerblock', required='sim_type=1')
    W_dot_cycle_htf_pump: Final[Array] = OUTPUT(label='PC HTF pumping power', units='MWe', type='ARRAY', group='powerblock', required='sim_type=1')
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
    disp_rel_mip_gap: Final[Array] = OUTPUT(label='Dispatch relative MIP gap', type='ARRAY', required='sim_type=1')
    disp_solve_state: Final[Array] = OUTPUT(label='Dispatch solver state', type='ARRAY', required='sim_type=1')
    disp_subopt_flag: Final[Array] = OUTPUT(label='Dispatch suboptimal solution flag', type='ARRAY', required='sim_type=1')
    disp_solve_iter: Final[Array] = OUTPUT(label='Dispatch iterations count', type='ARRAY', required='sim_type=1')
    disp_objective: Final[Array] = OUTPUT(label='Dispatch objective function value', type='ARRAY', required='sim_type=1')
    disp_obj_relax: Final[Array] = OUTPUT(label='Dispatch objective function - relaxed max', type='ARRAY', required='sim_type=1')
    disp_qsfprod_expected: Final[Array] = OUTPUT(label='Dispatch expected electric heater heat generation', units='MWt', type='ARRAY', required='sim_type=1')
    disp_qsfsu_expected: Final[Array] = OUTPUT(label='Dispatch expected electric heater startup enegy', units='MWt', type='ARRAY', required='sim_type=1')
    disp_tes_expected: Final[Array] = OUTPUT(label='Dispatch expected TES charge level', units='MWht', type='ARRAY', required='sim_type=1')
    disp_pceff_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle efficiency adj.', type='ARRAY', required='sim_type=1')
    disp_qpbsu_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle startup energy', units='MWht', type='ARRAY', required='sim_type=1')
    disp_wpb_expected: Final[Array] = OUTPUT(label='Dispatch expected power generation', units='MWe', type='ARRAY', required='sim_type=1')
    disp_rev_expected: Final[Array] = OUTPUT(label='Dispatch expected revenue factor', type='ARRAY', required='sim_type=1')
    disp_presolve_nconstr: Final[Array] = OUTPUT(label='Dispatch number of constraints in problem', type='ARRAY', required='sim_type=1')
    disp_presolve_nvar: Final[Array] = OUTPUT(label='Dispatch number of variables in problem', type='ARRAY', required='sim_type=1')
    disp_solve_time: Final[Array] = OUTPUT(label='Dispatch solver time', units='sec', type='ARRAY', required='sim_type=1')
    operating_modes_a: Final[Array] = OUTPUT(label='First 3 operating modes tried', type='ARRAY', required='sim_type=1')
    operating_modes_b: Final[Array] = OUTPUT(label='Next 3 operating modes tried', type='ARRAY', required='sim_type=1')
    operating_modes_c: Final[Array] = OUTPUT(label='Final 3 operating modes tried', type='ARRAY', required='sim_type=1')
    annual_energy: Final[float] = OUTPUT(label='Annual total electric power to grid', units='kWhe', type='NUMBER', required='sim_type=1')
    annual_energy_full_availability: Final[float] = OUTPUT(label='Annual total electric power to grid w/ full availability', units='MWhe', type='NUMBER', required='sim_type=1')
    annual_E_heater: Final[float] = OUTPUT(label='Annual heater electric energy consumption', units='MWhe', type='NUMBER', required='sim_type=1')
    annual_Q_heater_to_htf: Final[float] = OUTPUT(label='Annual heater thermal power to HTF', units='MWhe', type='NUMBER', required='sim_type=1')
    annual_Q_heater_startup: Final[float] = OUTPUT(label='Annual heater thermal energy consumed by startup', units='MWht', type='NUMBER', required='sim_type=1')
    annual_E_tes_heater: Final[float] = OUTPUT(label='Annual TES freeze heater electric energy consumption', units='MWhe', type='NUMBER', required='sim_type=1')
    annual_Q_tes_losses: Final[float] = OUTPUT(label='Annual TES thermal energy lost to ambient', units='MWht', type='NUMBER', required='sim_type=1')
    annual_E_cycle_gross: Final[float] = OUTPUT(label='Annual cycle gross electric energy generation', units='MWhe', type='NUMBER', required='sim_type=1')
    annual_Q_cycle_thermal_in: Final[float] = OUTPUT(label='Annual cycle thermal energy input', units='MWht', type='NUMBER', required='sim_type=1')
    annual_Q_cycle_thermal_startup: Final[float] = OUTPUT(label='Annual cycle thermal energy consumed by startup', units='MWht', type='NUMBER', required='sim_type=1')
    disp_objective_ann: Final[float] = OUTPUT(label='Annual sum of dispatch objective function value', units='$', type='NUMBER', required='sim_type=1')
    disp_iter_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solver iterations', type='NUMBER', required='sim_type=1')
    disp_presolve_nconstr_ann: Final[float] = OUTPUT(label='Annual sum of dispatch problem constraint count', type='NUMBER', required='sim_type=1')
    disp_presolve_nvar_ann: Final[float] = OUTPUT(label='Annual sum of dispatch problem variable count', type='NUMBER', required='sim_type=1')
    disp_solve_time_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solver time', units='sec', type='NUMBER', required='sim_type=1')
    disp_solve_state_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solve state', type='NUMBER', required='sim_type=1')
    avg_suboptimal_rel_mip_gap: Final[float] = OUTPUT(label='Average suboptimal relative MIP gap', units='%', type='NUMBER', required='sim_type=1')
    sim_cpu_run_time: Final[float] = OUTPUT(label='Simulation duration clock time', units='s', type='NUMBER', required='sim_type=1')
    ppa_soln_mode: Final[float] = OUTPUT(label='PPA solution mode', units='0/1', type='NUMBER', group='Revenue', required='sim_type=1', constraints='INTEGER,MIN = 0,MAX = 1', meta='0 = solve ppa,1 = specify ppa')
    flip_target_percent: Final[float] = OUTPUT(label='After-tax IRR target', units='%', type='NUMBER', group='Revenue', required='sim_type=1', constraints='MIN=0,MAX=100')
    total_land_area: Final[float] = OUTPUT(label='Total land area', units='acre', type='NUMBER', group='System Costs', required='*')
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
                 T_htf_cold_des: float = ...,
                 T_htf_hot_des: float = ...,
                 P_ref: float = ...,
                 design_eff: float = ...,
                 tshours: float = ...,
                 heater_mult: float = ...,
                 pc_config: float = ...,
                 pb_pump_coef: float = ...,
                 startup_time: float = ...,
                 startup_frac: float = ...,
                 cycle_max_frac: float = ...,
                 cycle_cutoff_frac: float = ...,
                 q_sby_frac: float = ...,
                 dT_cw_ref: float = ...,
                 T_amb_des: float = ...,
                 CT: float = ...,
                 T_approach: float = ...,
                 T_ITD_des: float = ...,
                 P_cond_ratio: float = ...,
                 pb_bd_frac: float = ...,
                 P_cond_min: float = ...,
                 n_pl_inc: float = ...,
                 tech_type: float = ...,
                 ud_f_W_dot_cool_des: float = ...,
                 ud_m_dot_water_cool_des: float = ...,
                 ud_ind_od: Matrix = ...,
                 hot_htf_code: float = ...,
                 ud_hot_htf_props: Matrix = ...,
                 tes_init_hot_htf_percent: float = ...,
                 h_tank: float = ...,
                 cold_tank_max_heat: float = ...,
                 u_tank: float = ...,
                 tank_pairs: float = ...,
                 cold_tank_Thtr: float = ...,
                 h_tank_min: float = ...,
                 hot_tank_Thtr: float = ...,
                 hot_tank_max_heat: float = ...,
                 heater_efficiency: float = ...,
                 f_q_dot_des_allowable_su: float = ...,
                 hrs_startup_at_max_rate: float = ...,
                 f_q_dot_heater_min: float = ...,
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
                 pb_fixed_par: float = ...,
                 bop_par: float = ...,
                 bop_par_f: float = ...,
                 bop_par_0: float = ...,
                 bop_par_1: float = ...,
                 bop_par_2: float = ...,
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
                 mp_energy_market_revenue: Matrix = ...,
                 cycle_spec_cost: float = ...,
                 tes_spec_cost: float = ...,
                 heater_spec_cost: float = ...,
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
                 P_boil: float = ...,
                 adjust_constant: float = ...,
                 adjust_hourly: Array = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
