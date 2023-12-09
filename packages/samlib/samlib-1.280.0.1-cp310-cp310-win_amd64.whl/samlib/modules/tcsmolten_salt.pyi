
# This is a generated file

"""tcsmolten_salt - CSP molten salt power tower with hierarchical controller and dispatch optimization"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'solar_resource_file': str,
    'solar_resource_data': Table,
    'is_dispatch': float,
    'sim_type': float,
    'csp_financial_model': float,
    'time_start': float,
    'time_stop': float,
    'time_steps_per_hour': float,
    'vacuum_arrays': float,
    'is_parallel_htr': float,
    'T_htf_cold_des': float,
    'T_htf_hot_des': float,
    'P_ref': float,
    'design_eff': float,
    'tshours': float,
    'solarm': float,
    'dni_des': float,
    'field_model_type': float,
    'helio_width': float,
    'helio_height': float,
    'helio_optical_error_mrad': float,
    'helio_active_fraction': float,
    'dens_mirror': float,
    'helio_reflectance': float,
    'rec_absorptance': float,
    'rec_hl_perm2': float,
    'land_max': float,
    'land_min': float,
    'land_bound_table': Matrix,
    'land_bound_list': Array,
    'p_start': float,
    'p_track': float,
    'hel_stow_deploy': float,
    'v_wind_max': float,
    'interp_nug': float,
    'interp_beta': float,
    'helio_aim_points': Matrix,
    'eta_map': Matrix,
    'eta_map_aod_format': float,
    'flux_maps': Matrix,
    'c_atm_0': float,
    'c_atm_1': float,
    'c_atm_2': float,
    'c_atm_3': float,
    'n_facet_x': float,
    'n_facet_y': float,
    'focus_type': float,
    'cant_type': float,
    'n_flux_days': float,
    'delta_flux_hrs': float,
    'water_usage_per_wash': float,
    'washing_frequency': float,
    'check_max_flux': float,
    'sf_excess': float,
    'A_sf_in': float,
    'total_land_area_before_rad_cooling_in': float,
    'N_hel': float,
    'flux_max': float,
    'opt_init_step': float,
    'opt_max_iter': float,
    'opt_conv_tol': float,
    'opt_flux_penalty': float,
    'opt_algorithm': float,
    'receiver_type': float,
    'N_panels': float,
    'd_tube_out': float,
    'th_tube': float,
    'mat_tube': float,
    'rec_htf': float,
    'field_fl_props': Matrix,
    'Flow_type': float,
    'crossover_shift': float,
    'epsilon': float,
    'hl_ffact': float,
    'f_rec_min': float,
    'rec_su_delay': float,
    'rec_qf_delay': float,
    'csp.pt.rec.max_oper_frac': float,
    'eta_pump': float,
    'piping_length_mult': float,
    'piping_length_const': float,
    'n_cav_rec_panels': float,
    'cav_rec_span': float,
    'cav_rec_passive_abs': float,
    'cav_rec_passive_eps': float,
    'piping_loss_coefficient': float,
    'rec_clearsky_model': float,
    'rec_clearsky_dni': Array,
    'rec_clearsky_fraction': float,
    'is_rec_model_trans': float,
    'is_rec_startup_trans': float,
    'rec_tm_mult': float,
    'riser_tm_mult': float,
    'downc_tm_mult': float,
    'u_riser': float,
    'th_riser': float,
    'heat_trace_power': float,
    'preheat_flux': float,
    'min_preheat_time': float,
    'min_fill_time': float,
    'startup_ramp_time': float,
    'startup_target_Tdiff': float,
    'is_rec_startup_from_T_soln': float,
    'is_rec_enforce_min_startup': float,
    'helio_positions': Matrix,
    'rec_height': float,
    'D_rec': float,
    'h_tower': float,
    'cav_rec_height': float,
    'cav_rec_width': float,
    'heater_mult': float,
    'heater_efficiency': float,
    'f_q_dot_des_allowable_su': float,
    'hrs_startup_at_max_rate': float,
    'f_q_dot_heater_min': float,
    'disp_hsu_cost_rel': float,
    'heater_spec_cost': float,
    'allow_heater_no_dispatch_opt': float,
    'tes_init_hot_htf_percent': float,
    'h_tank': float,
    'cold_tank_max_heat': float,
    'u_tank': float,
    'tank_pairs': float,
    'cold_tank_Thtr': float,
    'h_tank_min': float,
    'hot_tank_Thtr': float,
    'hot_tank_max_heat': float,
    'tanks_in_parallel': float,
    'h_ctes_tank_min': float,
    'ctes_tshours': float,
    'ctes_field_fl': float,
    'h_ctes_tank': float,
    'u_ctes_tank': float,
    'ctes_tankpairs': float,
    'T_ctes_cold_design': float,
    'T_ctes_warm_design': float,
    'T_ctes_warm_ini': float,
    'T_ctes_cold_ini': float,
    'f_ctes_warm_ini': float,
    'rad_multiplier': float,
    'm_dot_radpanel': float,
    'n_rad_tubes': float,
    'W_rad_tubes': float,
    'L_rad': float,
    'th_rad_panel': float,
    'D_rad_tubes': float,
    'k_panel': float,
    'epsilon_radtop': float,
    'epsilon_radbot': float,
    'epsilon_radgrnd': float,
    'L_rad_sections': float,
    'epsilon_radHX': float,
    'ctes_type': float,
    'radiator_unitcost': float,
    'radiator_installcost': float,
    'radiator_fluidcost': float,
    'radfluid_vol_ratio': float,
    'ctes_cost': float,
    'rad_pressuredrop': float,
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
    'F_wc': Array,
    'tech_type': float,
    'ud_f_W_dot_cool_des': float,
    'ud_m_dot_water_cool_des': float,
    'ud_ind_od': Matrix,
    'pb_fixed_par': float,
    'aux_par': float,
    'aux_par_f': float,
    'aux_par_0': float,
    'aux_par_1': float,
    'aux_par_2': float,
    'bop_par': float,
    'bop_par_f': float,
    'bop_par_0': float,
    'bop_par_1': float,
    'bop_par_2': float,
    'timestep_load_fractions': Array,
    'f_turb_tou_periods': Array,
    'weekday_schedule': Matrix,
    'weekend_schedule': Matrix,
    'is_tod_pc_target_also_pc_max': float,
    'can_cycle_use_standby': float,
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
    'disp_time_weighting': float,
    'is_write_ampl_dat': float,
    'ampl_data_dir': str,
    'is_ampl_engine': float,
    'ampl_exec_call': str,
    'disp_rsu_cost_rel': float,
    'disp_csu_cost_rel': float,
    'disp_pen_ramping': float,
    'disp_inventory_incentive': float,
    'q_rec_standby': float,
    'q_rec_heattrace': float,
    'is_wlim_design': float,
    'disp_wlim_maxspec': float,
    'is_wlim_series': float,
    'wlim_series': Array,
    'ppa_multiplier_model': float,
    'ppa_soln_mode': float,
    'dispatch_factors_ts': Array,
    'en_electricity_rates': float,
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
    'is_dispatch_series': float,
    'dispatch_series': Array,
    'ppa_price_input': Array,
    'mp_energy_market_revenue': Matrix,
    'tower_fixed_cost': float,
    'tower_exp': float,
    'rec_ref_cost': float,
    'rec_ref_area': float,
    'rec_cost_exp': float,
    'site_spec_cost': float,
    'heliostat_spec_cost': float,
    'plant_spec_cost': float,
    'bop_spec_cost': float,
    'tes_spec_cost': float,
    'land_spec_cost': float,
    'contingency_rate': float,
    'sales_tax_rate': float,
    'sales_tax_frac': float,
    'cost_sf_fixed': float,
    'fossil_spec_cost': float,
    'csp.pt.cost.epc.per_acre': float,
    'csp.pt.cost.epc.percent': float,
    'csp.pt.cost.epc.per_watt': float,
    'csp.pt.cost.epc.fixed': float,
    'csp.pt.cost.plm.percent': float,
    'csp.pt.cost.plm.per_watt': float,
    'csp.pt.cost.plm.fixed': float,
    'csp.pt.sf.fixed_land_area': float,
    'csp.pt.sf.land_overhead_factor': float,
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
    'piping_loss': float,
    'disp_csu_cost': float,
    'disp_rsu_cost': float,
    'disp_pen_delta_w': float,
    'P_boil': float,
    'csp.pt.tes.init_hot_htf_percent': float,
    'total_land_area': float,
    'system_capacity': float,
    'cp_system_nameplate': float,
    'cp_battery_nameplate': float,
    'N_hel_calc': float,
    'refl_image_error': float,
    'heliostat_area': float,
    'average_attenuation': float,
    'helio_positions_calc': Matrix,
    'A_sf': float,
    'land_min_abs': float,
    'land_max_abs': float,
    'land_area_base_calc': float,
    'total_land_area_before_rad_cooling_calc': float,
    'W_dot_col_tracking_des': float,
    'rec_height_calc': float,
    'D_rec_calc': float,
    'h_tower_calc': float,
    'ext_rec_area': float,
    'ext_rec_aspect': float,
    'cav_rec_height_calc': float,
    'cav_rec_width_calc': float,
    'cav_rec_area': float,
    'cav_panel_width': float,
    'cav_radius': float,
    'A_rec': float,
    'L_tower_piping_calc': float,
    'q_dot_rec_des': float,
    'eta_rec_thermal_des': float,
    'W_dot_rec_pump_des': float,
    'W_dot_rec_pump_tower_share_des': float,
    'W_dot_rec_pump_rec_share_des': float,
    'vel_rec_htf_des': float,
    'm_dot_htf_rec_des': float,
    'm_dot_htf_rec_max': float,
    'q_dot_piping_loss_des': float,
    'q_dot_heater_des': float,
    'W_dot_heater_des': float,
    'E_heater_su_des': float,
    'm_dot_htf_cycle_des': float,
    'q_dot_cycle_des': float,
    'W_dot_cycle_pump_des': float,
    'W_dot_cycle_cooling_des': float,
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
    'Q_tes_des': float,
    'V_tes_htf_avail_des': float,
    'V_tes_htf_total_des': float,
    'd_tank_tes': float,
    'q_dot_loss_tes_des': float,
    'tshours_rec': float,
    'tshours_heater': float,
    'dens_store_htf_at_T_ave': float,
    'nameplate': float,
    'W_dot_bop_design': float,
    'W_dot_fixed': float,
    'h_rec_input_to_cost_model': float,
    'csp.pt.cost.site_improvements': float,
    'csp.pt.cost.heliostats': float,
    'csp.pt.cost.tower': float,
    'csp.pt.cost.receiver': float,
    'csp.pt.cost.storage': float,
    'csp.pt.cost.power_block': float,
    'heater_cost': float,
    'csp.pt.cost.rad_field': float,
    'csp.pt.cost.rad_fluid': float,
    'csp.pt.cost.rad_storage': float,
    'csp.pt.cost.bop': float,
    'csp.pt.cost.fossil': float,
    'ui_direct_subtotal': float,
    'csp.pt.cost.contingency': float,
    'total_direct_cost': float,
    'csp.pt.cost.epc.total': float,
    'csp.pt.cost.plm.total': float,
    'csp.pt.cost.sales_tax.total': float,
    'total_indirect_cost': float,
    'total_installed_cost': float,
    'csp.pt.cost.installed_per_capacity': float,
    'const_per_principal1': float,
    'const_per_principal2': float,
    'const_per_principal3': float,
    'const_per_principal4': float,
    'const_per_principal5': float,
    'const_per_interest1': float,
    'const_per_interest2': float,
    'const_per_interest3': float,
    'const_per_interest4': float,
    'const_per_interest5': float,
    'const_per_total1': float,
    'const_per_total2': float,
    'const_per_total3': float,
    'const_per_total4': float,
    'const_per_total5': float,
    'const_per_percent_total': float,
    'const_per_principal_total': float,
    'const_per_interest_total': float,
    'construction_financing_cost': float,
    'time_hr': Array,
    'solzen': Array,
    'solaz': Array,
    'beam': Array,
    'tdry': Array,
    'twet': Array,
    'rh': Array,
    'wspd': Array,
    'eta_map_out': Matrix,
    'flux_maps_for_import': Matrix,
    'flux_maps_out': Matrix,
    'q_sf_inc': Array,
    'eta_field': Array,
    'defocus': Array,
    'sf_adjust_out': Array,
    'rec_defocus': Array,
    'q_dot_rec_inc': Array,
    'eta_therm': Array,
    'Q_thermal': Array,
    'pparasi': Array,
    'm_dot_rec': Array,
    'q_startup': Array,
    'T_rec_in': Array,
    'T_rec_out': Array,
    'q_piping_losses': Array,
    'q_thermal_loss': Array,
    'q_dot_reflection_loss': Array,
    'P_tower_pump': Array,
    'T_rec_out_end': Array,
    'T_rec_out_max': Array,
    'T_panel_out_max': Array,
    'T_wall_rec_inlet': Array,
    'T_wall_rec_outlet': Array,
    'T_wall_riser': Array,
    'T_wall_downcomer': Array,
    'clearsky': Array,
    'Q_thermal_ss': Array,
    'Q_thermal_ss_csky': Array,
    'W_dot_heater': Array,
    'q_dot_heater_to_htf': Array,
    'q_dot_heater_startup': Array,
    'm_dot_htf_heater': Array,
    'T_htf_heater_in': Array,
    'T_htf_heater_out': Array,
    'eta': Array,
    'q_pb': Array,
    'm_dot_pc': Array,
    'q_pc_startup': Array,
    'q_dot_pc_startup': Array,
    'P_cycle': Array,
    'T_pc_in': Array,
    'T_pc_out': Array,
    'm_dot_water_pc': Array,
    'T_cond_out': Array,
    'T_cold': Array,
    'm_cold': Array,
    'm_warm': Array,
    'T_warm': Array,
    'T_rad_out': Array,
    'A_radfield': float,
    'P_cond': Array,
    'P_cond_iter_err': Array,
    'radcool_control': Array,
    'cycle_htf_pump_power': Array,
    'P_cooling_tower_tot': Array,
    'tank_losses': Array,
    'q_heater': Array,
    'T_tes_hot': Array,
    'T_tes_cold': Array,
    'mass_tes_cold': Array,
    'mass_tes_hot': Array,
    'q_dc_tes': Array,
    'q_ch_tes': Array,
    'e_ch_tes': Array,
    'm_dot_cr_to_tes_hot': Array,
    'm_dot_tes_hot_out': Array,
    'm_dot_pc_to_tes_cold': Array,
    'm_dot_tes_cold_out': Array,
    'm_dot_field_to_cycle': Array,
    'm_dot_cycle_to_field': Array,
    'tes_htf_pump_power': Array,
    'P_fixed': Array,
    'P_plant_balance_tot': Array,
    'P_rec_heattrace': Array,
    'P_out_net': Array,
    'tou_value': Array,
    'pricing_mult': Array,
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
    'disp_qsf_expected': Array,
    'disp_qsfprod_expected': Array,
    'disp_qsfsu_expected': Array,
    'disp_tes_expected': Array,
    'disp_pceff_expected': Array,
    'disp_thermeff_expected': Array,
    'disp_qpbsu_expected': Array,
    'disp_wpb_expected': Array,
    'disp_rev_expected': Array,
    'disp_presolve_nconstr': Array,
    'disp_presolve_nvar': Array,
    'disp_solve_time': Array,
    'q_dot_pc_sb': Array,
    'q_dot_pc_min': Array,
    'q_dot_pc_max': Array,
    'q_dot_pc_target': Array,
    'is_rec_su_allowed': Array,
    'is_pc_su_allowed': Array,
    'is_pc_sb_allowed': Array,
    'is_PAR_HTR_allowed': Array,
    'q_dot_elec_to_PAR_HTR': Array,
    'q_dot_est_cr_su': Array,
    'q_dot_est_cr_on': Array,
    'q_dot_est_tes_dc': Array,
    'q_dot_est_tes_ch': Array,
    'operating_modes_a': Array,
    'operating_modes_b': Array,
    'operating_modes_c': Array,
    'gen': Array,
    'annual_energy': float,
    'annual_W_cycle_gross': float,
    'annual_W_cooling_tower': float,
    'annual_q_rec_inc': float,
    'annual_q_rec_loss': float,
    'annual_eta_rec_th': float,
    'annual_eta_rec_th_incl_refl': float,
    'conversion_factor': float,
    'capacity_factor': float,
    'sales_energy_capacity_factor': float,
    'kwh_per_kw': float,
    'annual_total_water_use': float,
    'capacity_factor_highest_1000_ppas': float,
    'capacity_factor_highest_2000_ppas': float,
    'disp_objective_ann': float,
    'disp_iter_ann': float,
    'disp_presolve_nconstr_ann': float,
    'disp_presolve_nvar_ann': float,
    'disp_solve_time_ann': float,
    'disp_solve_state_ann': float,
    'avg_suboptimal_rel_mip_gap': float,
    'sim_cpu_run_time': float,
    'adjust:constant': float,
    'adjust:hourly': Array,
    'adjust:timeindex': Array,
    'adjust:periods': Matrix,
    'sf_adjust:constant': float,
    'sf_adjust:hourly': Array,
    'sf_adjust:timeindex': Array,
    'sf_adjust:periods': Matrix
}, total=False)

class Data(ssc.DataDict):
    solar_resource_file: str = INPUT(label='Local weather file path', type='STRING', group='Solar Resource', required='?', constraints='LOCAL_FILE')
    solar_resource_data: Table = INPUT(label='Weather resource data in memory', type='TABLE', group='Solar Resource', required='?')
    is_dispatch: float = INPUT(label='Allow dispatch optimization?', type='NUMBER', group='System Control', required='?=0')
    sim_type: float = INPUT(label='1 (default): timeseries, 2: design only', type='NUMBER', group='System Control', required='?=1')
    csp_financial_model: float = INPUT(units='1-8', type='NUMBER', group='Financial Model', required='?=1', constraints='INTEGER,MIN=0')
    time_start: float = INPUT(label='Simulation start time', units='s', type='NUMBER', group='System Control', required='?=0')
    time_stop: float = INPUT(label='Simulation stop time', units='s', type='NUMBER', group='System Control', required='?=31536000')
    time_steps_per_hour: float = INPUT(label='Number of simulation time steps per hour', type='NUMBER', group='System Control', required='?=-1')
    vacuum_arrays: float = INPUT(label='Allocate arrays for only the required number of steps', type='NUMBER', group='System Control', required='?=0')
    is_parallel_htr: float = INPUT(label='Does plant include a HTF heater parallel to solar field?', type='NUMBER', group='System Control', required='?=0')
    T_htf_cold_des: float = INPUT(label='Cold HTF inlet temperature at design conditions', units='C', type='NUMBER', group='System Design', required='*')
    T_htf_hot_des: float = INPUT(label='Hot HTF outlet temperature at design conditions', units='C', type='NUMBER', group='System Design', required='*')
    P_ref: float = INPUT(label='Reference output electric power at design condition', units='MW', type='NUMBER', group='System Design', required='*')
    design_eff: float = INPUT(label='Power cycle efficiency at design', units='none', type='NUMBER', group='System Design', required='*')
    tshours: float = INPUT(label='Equivalent full-load thermal storage hours', units='hr', type='NUMBER', group='System Design', required='*')
    solarm: float = INPUT(label='Solar multiple', units='-', type='NUMBER', group='System Design', required='*')
    dni_des: float = INPUT(label='Design-point DNI', units='W/m2', type='NUMBER', group='System Design', required='*')
    field_model_type: float = INPUT(label='0=design field and tower/receiver geometry, 1=design field, 2=user specified field, 3=user flux and eta map, pass heliostat_positions to SolarPILOT for layout, 4=user flux and eta maps, no SolarPILOT, input A_sf_in, total_land_area_before_rad_cooling_in, and N_hel', type='NUMBER', group='Heliostat Field', required='*')
    helio_width: float = INPUT(label='Heliostat width', units='m', type='NUMBER', group='Heliostat Field', required='field_model_type<4')
    helio_height: float = INPUT(label='Heliostat height', units='m', type='NUMBER', group='Heliostat Field', required='field_model_type<4')
    helio_optical_error_mrad: float = INPUT(label='Heliostat optical error', units='mrad', type='NUMBER', group='Heliostat Field', required='*')
    helio_active_fraction: float = INPUT(label='Heliostat active fraction', type='NUMBER', group='Heliostat Field', required='*')
    dens_mirror: float = INPUT(label='Ratio of heliostat reflective area to profile', type='NUMBER', group='Heliostat Field', required='field_model_type<4')
    helio_reflectance: float = INPUT(label='Heliostat reflectance', type='NUMBER', group='Heliostat Field', required='*')
    rec_absorptance: float = INPUT(label='Receiver absorptance', type='NUMBER', group='Tower and Receiver', required='*')
    rec_hl_perm2: float = INPUT(label='Receiver design heatloss', units='kW/m2', type='NUMBER', group='Tower and Receiver', required='*')
    land_max: float = INPUT(label='Land max boundary', units='-ORm', type='NUMBER', group='Heliostat Field', required='?=7.5')
    land_min: float = INPUT(label='Land min boundary', units='-ORm', type='NUMBER', group='Heliostat Field', required='?=0.75')
    land_bound_table: Matrix = INPUT(label='Land boundary table', units='m', type='MATRIX', group='Heliostat Field', required='?')
    land_bound_list: Array = INPUT(label='Land boundary table listing', type='ARRAY', group='Heliostat Field', required='?')
    p_start: float = INPUT(label='Heliostat startup energy', units='kWe-hr', type='NUMBER', group='Heliostat Field', required='*')
    p_track: float = INPUT(label='Heliostat tracking energy', units='kWe', type='NUMBER', group='Heliostat Field', required='*')
    hel_stow_deploy: float = INPUT(label='Stow/deploy elevation angle', units='deg', type='NUMBER', group='Heliostat Field', required='*')
    v_wind_max: float = INPUT(label='Heliostat max wind velocity', units='m/s', type='NUMBER', group='Heliostat Field', required='*')
    interp_nug: float = INPUT(label='Interpolation nugget', units='-', type='NUMBER', group='Heliostat Field', required='?=0')
    interp_beta: float = INPUT(label='Interpolation beta coef.', units='-', type='NUMBER', group='Heliostat Field', required='?=1.99')
    helio_aim_points: Matrix = INPUT(label='Heliostat aim point table', units='m', type='MATRIX', group='Heliostat Field', required='?')
    eta_map: Matrix = INPUT(label='Field efficiency array', type='MATRIX', group='Heliostat Field', required='field_model_type>2')
    eta_map_aod_format: float = INPUT(label='Use 3D AOD format field efficiency array', type='NUMBER', group='Heliostat Field', required='field_model_type>2', meta='heliostat')
    flux_maps: Matrix = INPUT(label='Flux map intensities', type='MATRIX', group='Heliostat Field', required='field_model_type>2')
    c_atm_0: float = INPUT(label='Attenuation coefficient 0', type='NUMBER', group='Heliostat Field', required='?=0.006789')
    c_atm_1: float = INPUT(label='Attenuation coefficient 1', type='NUMBER', group='Heliostat Field', required='?=0.1046')
    c_atm_2: float = INPUT(label='Attenuation coefficient 2', type='NUMBER', group='Heliostat Field', required='?=-0.0107')
    c_atm_3: float = INPUT(label='Attenuation coefficient 3', type='NUMBER', group='Heliostat Field', required='?=0.002845')
    n_facet_x: float = INPUT(label='Number of heliostat facets - X', type='NUMBER', group='Heliostat Field', required='*')
    n_facet_y: float = INPUT(label='Number of heliostat facets - Y', type='NUMBER', group='Heliostat Field', required='*')
    focus_type: float = INPUT(label='Heliostat focus method', type='NUMBER', group='Heliostat Field', required='*')
    cant_type: float = INPUT(label='Heliostat canting method', type='NUMBER', group='Heliostat Field', required='*')
    n_flux_days: float = INPUT(label='Number of days in flux map lookup', type='NUMBER', group='Tower and Receiver', required='?=8')
    delta_flux_hrs: float = INPUT(label='Hourly frequency in flux map lookup', type='NUMBER', group='Tower and Receiver', required='?=1')
    water_usage_per_wash: float = INPUT(label='Water usage per wash', units='L/m2_aper', type='NUMBER', group='Heliostat Field', required='*')
    washing_frequency: float = INPUT(label='Mirror washing frequency', units='none', type='NUMBER', group='Heliostat Field', required='*')
    check_max_flux: float = INPUT(label='Check max flux at design point', type='NUMBER', group='Heliostat Field', required='?=0')
    sf_excess: float = INPUT(label='Heliostat field multiple', type='NUMBER', group='System Design', required='?=1.0')
    A_sf_in: float = INPUT(label='Solar field area', units='m^2', type='NUMBER', group='Heliostat Field', required='field_model_type>3')
    total_land_area_before_rad_cooling_in: float = INPUT(label='Total land area not including radiative cooling - in', units='acre', type='NUMBER', group='Heliostat Field', required='field_model_type>3')
    N_hel: float = INPUT(label='Number of heliostats - in', type='NUMBER', group='Heliostat Field', required='field_model_type>3')
    flux_max: float = INPUT(label='Maximum allowable flux', type='NUMBER', group='Tower and Receiver', required='?=1000')
    opt_init_step: float = INPUT(label='Optimization initial step size', type='NUMBER', group='Heliostat Field', required='?=0.05')
    opt_max_iter: float = INPUT(label='Max number iteration steps', type='NUMBER', group='Heliostat Field', required='?=200')
    opt_conv_tol: float = INPUT(label='Optimization convergence tolerance', type='NUMBER', group='Heliostat Field', required='?=0.001')
    opt_flux_penalty: float = INPUT(label='Optimization flux overage penalty', type='NUMBER', group='Heliostat Field', required='*')
    opt_algorithm: float = INPUT(label='Optimization algorithm', type='NUMBER', group='Heliostat Field', required='?=1')
    receiver_type: float = INPUT(label='0: external (default), 1; cavity', type='NUMBER', group='Heliostat Field', required='?=0')
    N_panels: float = INPUT(label='Number of individual panels on the receiver', type='NUMBER', group='Tower and Receiver', required='*', constraints='INTEGER')
    d_tube_out: float = INPUT(label='The outer diameter of an individual receiver tube', units='mm', type='NUMBER', group='Tower and Receiver', required='*')
    th_tube: float = INPUT(label='The wall thickness of a single receiver tube', units='mm', type='NUMBER', group='Tower and Receiver', required='*')
    mat_tube: float = INPUT(label='Receiver tube material, 2=Stainless AISI316', type='NUMBER', group='Tower and Receiver', required='*')
    rec_htf: float = INPUT(label='Receiver HTF, 17=Salt (60% NaNO3, 40% KNO3) 10=Salt (46.5% LiF 11.5% NaF 42% KF) 50=Lookup tables', type='NUMBER', group='Tower and Receiver', required='*')
    field_fl_props: Matrix = INPUT(label='User defined field fluid property data', units='-', type='MATRIX', group='Tower and Receiver', required='*')
    Flow_type: float = INPUT(label='Receiver flow pattern: see figure on SAM Receiver page', type='NUMBER', group='Tower and Receiver', required='*')
    crossover_shift: float = INPUT(label='Number of panels shift in receiver crossover position', type='NUMBER', group='Tower and Receiver', required='?=0')
    epsilon: float = INPUT(label='The emissivity of the receiver surface coating', type='NUMBER', group='Tower and Receiver', required='*')
    hl_ffact: float = INPUT(label='The heat loss factor (thermal loss fudge factor)', type='NUMBER', group='Tower and Receiver', required='*')
    f_rec_min: float = INPUT(label='Minimum receiver mass flow rate turn down fraction', type='NUMBER', group='Tower and Receiver', required='*')
    rec_su_delay: float = INPUT(label='Fixed startup delay time for the receiver', units='hr', type='NUMBER', group='Tower and Receiver', required='*')
    rec_qf_delay: float = INPUT(label='Energy-based receiver startup delay (fraction of rated thermal power)', type='NUMBER', group='Tower and Receiver', required='*')
    csp_pt_rec_max_oper_frac: float = INPUT(name='csp.pt.rec.max_oper_frac', label='Maximum receiver mass flow rate fraction', type='NUMBER', group='Tower and Receiver', required='*')
    eta_pump: float = INPUT(label='Receiver HTF pump efficiency', type='NUMBER', group='Tower and Receiver', required='*')
    piping_length_mult: float = INPUT(label='Piping length multiplier', type='NUMBER', group='Tower and Receiver', required='*')
    piping_length_const: float = INPUT(label='Piping constant length', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    n_cav_rec_panels: float = INPUT(label='Cavity receiver number of panels', type='NUMBER', group='Tower and Receiver', required='receiver_type=1')
    cav_rec_span: float = INPUT(label='Cavity receiver span angle', units='deg', type='NUMBER', group='Tower and Receiver', required='receiver_type=1')
    cav_rec_passive_abs: float = INPUT(label='Cavity receiver passive surface solar absorptance', type='NUMBER', group='Tower and Receiver', required='receiver_type=1')
    cav_rec_passive_eps: float = INPUT(label='Cavity receiver passive surface thermal emissivity', type='NUMBER', group='Tower and Receiver', required='receiver_type=1')
    piping_loss_coefficient: float = INPUT(label='Thermal loss per meter of piping', units='Wt/m2-K', type='NUMBER', group='Tower and Receiver')
    rec_clearsky_model: float = INPUT(label='Clearsky model: None = -1, User-defined data = 0, Meinel = 1; Hottel = 2; Allen = 3; Moon = 4', type='NUMBER', group='Tower and Receiver', required='?=-1')
    rec_clearsky_dni: Array = INPUT(label='User-defined clear-sky DNI', units='W/m2', type='ARRAY', group='Tower and Receiver', required='rec_clearsky_model=0')
    rec_clearsky_fraction: float = INPUT(label='Weighting fraction on clear-sky DNI for receiver flow control', type='NUMBER', group='Tower and Receiver', required='?=0.0')
    is_rec_model_trans: float = INPUT(label='Formulate receiver model as transient?', type='NUMBER', group='Tower and Receiver', required='?=0')
    is_rec_startup_trans: float = INPUT(label='Formulate receiver startup model as transient?', type='NUMBER', group='Tower and Receiver', required='?=0')
    rec_tm_mult: float = INPUT(label='Receiver thermal mass multiplier', type='NUMBER', group='Tower and Receiver', required='?=1.0')
    riser_tm_mult: float = INPUT(label='Riser thermal mass multiplier', type='NUMBER', group='Tower and Receiver', required='?=1.0')
    downc_tm_mult: float = INPUT(label='Downcomer thermal mass multiplier', type='NUMBER', group='Tower and Receiver', required='?=1.0')
    u_riser: float = INPUT(label='Design point HTF velocity in riser', units='m/s', type='NUMBER', group='Tower and Receiver', required='?=4.0')
    th_riser: float = INPUT(label='Riser or downcomer tube wall thickness', units='mm', type='NUMBER', group='Tower and Receiver', required='?=15.0')
    heat_trace_power: float = INPUT(label='Riser/downcomer heat trace power during startup', units='kW/m', type='NUMBER', group='Tower and Receiver', required='?=500.0')
    preheat_flux: float = INPUT(label='Tube absorbed solar flux during preheat', units='kW/m2', type='NUMBER', group='Tower and Receiver', required='?=50.0')
    min_preheat_time: float = INPUT(label='Minimum time required in preheat startup stage', units='hr', type='NUMBER', group='Tower and Receiver', required='?=0.0')
    min_fill_time: float = INPUT(label='Startup time delay for filling the receiver/piping', units='hr', type='NUMBER', group='Tower and Receiver', required='?=0.1333')
    startup_ramp_time: float = INPUT(label='Time required to reach full flux during receiver startup', units='hr', type='NUMBER', group='Tower and Receiver', required='?=0.1333')
    startup_target_Tdiff: float = INPUT(label='Target HTF T at end of startup - steady state hot HTF temperature', units='C', type='NUMBER', group='Tower and Receiver', required='?=-5.0')
    is_rec_startup_from_T_soln: float = INPUT(label='Begin receiver startup from solved temperature profiles?', type='NUMBER', group='Tower and Receiver', required='?=0')
    is_rec_enforce_min_startup: float = INPUT(label='Always enforce minimum startup time', type='NUMBER', group='Tower and Receiver', required='?=1')
    helio_positions: Matrix = INPUT(label='Heliostat position table - in', type='MATRIX', group='Heliostat Field', required='field_model_type=2|field_model_type=3')
    rec_height: float = INPUT(label='Receiver height - in', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    D_rec: float = INPUT(label='The overall outer diameter of the receiver - in', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    h_tower: float = INPUT(label='Tower height - in', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    cav_rec_height: float = INPUT(label='Cavity receiver height - in', units='m', type='NUMBER', group='Tower and Receiver', required='receiver_type=1')
    cav_rec_width: float = INPUT(label='Cavity receiver aperture width - in', units='m', type='NUMBER', group='Tower and Receiver', required='receiver_type=1')
    heater_mult: float = INPUT(label='Heater multiple relative to design cycle thermal power', units='-', type='NUMBER', group='Parallel Heater', required='is_parallel_htr=1')
    heater_efficiency: float = INPUT(label='Heater electric to thermal efficiency', units='%', type='NUMBER', group='Parallel Heater', required='is_parallel_htr=1')
    f_q_dot_des_allowable_su: float = INPUT(label='Fraction of design power allowed during startup', units='-', type='NUMBER', group='Parallel Heater', required='is_parallel_htr=1')
    hrs_startup_at_max_rate: float = INPUT(label='Duration of startup at max startup power', units='hr', type='NUMBER', group='Parallel Heater', required='is_parallel_htr=1')
    f_q_dot_heater_min: float = INPUT(label='Minimum allowable heater output as fraction of design', type='NUMBER', group='Parallel Heater', required='is_parallel_htr=1')
    disp_hsu_cost_rel: float = INPUT(label='Heater startup cost', units='$/MWt/start', type='NUMBER', group='System Control', required='is_dispatch=1&is_parallel_htr=1')
    heater_spec_cost: float = INPUT(label='Heater specific cost', units='$/kWht', type='NUMBER', group='System Costs', required='is_parallel_htr=1')
    allow_heater_no_dispatch_opt: float = INPUT(label='Allow heater with no dispatch optimization? SAM UI relies on cmod default', type='NUMBER', group='System Costs', required='?=0')
    tes_init_hot_htf_percent: float = INPUT(label='Initial fraction of available volume that is hot', units='%', type='NUMBER', group='Thermal Storage')
    h_tank: float = INPUT(label='Total height of tank (height of HTF when tank is full)', units='m', type='NUMBER', group='Thermal Storage', required='*')
    cold_tank_max_heat: float = INPUT(label='Rated heater capacity for cold tank heating', units='MW', type='NUMBER', group='Thermal Storage', required='*')
    u_tank: float = INPUT(label='Loss coefficient from the tank', units='W/m2-K', type='NUMBER', group='Thermal Storage', required='*')
    tank_pairs: float = INPUT(label='Number of equivalent tank pairs', type='NUMBER', group='Thermal Storage', required='*', constraints='INTEGER')
    cold_tank_Thtr: float = INPUT(label='Minimum allowable cold tank HTF temperature', units='C', type='NUMBER', group='Thermal Storage', required='*')
    h_tank_min: float = INPUT(label='Minimum allowable HTF height in storage tank', units='m', type='NUMBER', group='Thermal Storage', required='*')
    hot_tank_Thtr: float = INPUT(label='Minimum allowable hot tank HTF temperature', units='C', type='NUMBER', group='Thermal Storage', required='*')
    hot_tank_max_heat: float = INPUT(label='Rated heater capacity for hot tank heating', units='MW', type='NUMBER', group='Thermal Storage', required='*')
    tanks_in_parallel: float = INPUT(label='Tanks are in parallel, not in series, with solar field', units='-', type='NUMBER', group='Thermal Storage', required='*')
    h_ctes_tank_min: float = INPUT(label='Minimum allowable water height in storage tank', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    ctes_tshours: float = INPUT(label='Equivalent full load storage hours', units='hr', type='NUMBER', group='RADCOOL', required='?=0')
    ctes_field_fl: float = INPUT(label='Fluid in radiator field. 3=liquid water. Other = Glycol.', units='-', type='NUMBER', group='RADCOOL', required='?=3')
    h_ctes_tank: float = INPUT(label='Total height of cold storage tank when full', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    u_ctes_tank: float = INPUT(label='Loss coefficient from cold storage tank', units='W/m2-K', type='NUMBER', group='RADCOOL', required='?=0')
    ctes_tankpairs: float = INPUT(label='Number of equivalent tank pairs', units='-', type='NUMBER', group='RADCOOL', required='?=0')
    T_ctes_cold_design: float = INPUT(label='Design value of cooled water to power block', units='C', type='NUMBER', group='RADCOOL', required='?=0')
    T_ctes_warm_design: float = INPUT(label='Design value of warm water returning from power block', units='C', type='NUMBER', group='RADCOOL', required='?=0')
    T_ctes_warm_ini: float = INPUT(label='Initial value of warm tank', units='C', type='NUMBER', group='RADCOOL', required='?=0')
    T_ctes_cold_ini: float = INPUT(label='Initial value of cold tank', units='C', type='NUMBER', group='RADCOOL', required='?=0')
    f_ctes_warm_ini: float = INPUT(label='Initial fraction of avail. volume that is warm', units='-', type='NUMBER', group='RADCOOL', required='?=0')
    rad_multiplier: float = INPUT(label='Ratio of radiator field area to solar aperature area', units='-', type='NUMBER', group='RADCOOL', required='?=0')
    m_dot_radpanel: float = INPUT(label='Mass flow rate through single radiator panel', units='kg/sec', type='NUMBER', group='RADCOOL', required='?=0')
    n_rad_tubes: float = INPUT(label='Number of parallel tubes in single radiator panel', units='-', type='NUMBER', group='RADCOOL', required='?=0')
    W_rad_tubes: float = INPUT(label='Center-to-center distance between tubes in radiator panel', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    L_rad: float = INPUT(label='Length of radiator panel row', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    th_rad_panel: float = INPUT(label='Thickness of radiator panel', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    D_rad_tubes: float = INPUT(label='Inner diameter of tubes in radiator panel', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    k_panel: float = INPUT(label='Thermal conductivity of radiator panel material', units='W/m-K', type='NUMBER', group='RADCOOL', required='?=235')
    epsilon_radtop: float = INPUT(label='Emmissivity of top of radiator panel', units='-', type='NUMBER', group='RADCOOL', required='?=.95')
    epsilon_radbot: float = INPUT(label='Emmissivity of top of radiator panel bottom (facing ground)', units='-', type='NUMBER', group='RADCOOL', required='?=.07')
    epsilon_radgrnd: float = INPUT(label='Emmissivity of ground underneath radiator panel', units='-', type='NUMBER', group='RADCOOL', required='?=.90')
    L_rad_sections: float = INPUT(label='Length of individual radiator panel', units='m', type='NUMBER', group='RADCOOL', required='?=0')
    epsilon_radHX: float = INPUT(label='Effectiveness of HX between radiative field and cold storage', units='-', type='NUMBER', group='RADCOOL', required='?=.8')
    ctes_type: float = INPUT(label='Type of cold storage (2=two tank, 3= three node)', units='-', type='NUMBER', group='RADCOOL', required='?=0')
    radiator_unitcost: float = INPUT(label='Cost of radiative panels', units='$/m^2', type='NUMBER', group='RADCOOL', required='?=0')
    radiator_installcost: float = INPUT(label='Installation cost of radiative panels', units='$/m^2', type='NUMBER', group='RADCOOL', required='?=0')
    radiator_fluidcost: float = INPUT(label='Cost of circulating fluid in radiative panels', units='$/L', type='NUMBER', group='RADCOOL', required='?=0')
    radfluid_vol_ratio: float = INPUT(label='Ratio of fluid in distribution to fluid in panels', units='-', type='NUMBER', group='RADCOOL', required='?=0')
    ctes_cost: float = INPUT(label='Cost of cold storage construction', units='$/L', type='NUMBER', group='RADCOOL', required='?=0')
    rad_pressuredrop: float = INPUT(label='Average pressure drop through a radiative panel & distribution', units='kPa', type='NUMBER', group='RADCOOL', required='?=0')
    pc_config: float = INPUT(label='PC configuration 0=Steam Rankine (224), 1=user defined', type='NUMBER', group='Power Cycle', required='?=0', constraints='INTEGER')
    pb_pump_coef: float = INPUT(label='Pumping power to move 1kg of HTF through PB loop', units='kW/kg', type='NUMBER', group='Power Cycle', required='*')
    startup_time: float = INPUT(label='Time needed for power block startup', units='hr', type='NUMBER', group='Power Cycle', required='*')
    startup_frac: float = INPUT(label='Fraction of design thermal power needed for startup', units='none', type='NUMBER', group='Power Cycle', required='*')
    cycle_max_frac: float = INPUT(label='Maximum turbine over design operation fraction', type='NUMBER', group='Power Cycle', required='*')
    cycle_cutoff_frac: float = INPUT(label='Minimum turbine operation fraction before shutdown', type='NUMBER', group='Power Cycle', required='*')
    q_sby_frac: float = INPUT(label='Fraction of thermal power required for standby', type='NUMBER', group='Power Cycle', required='*')
    dT_cw_ref: float = INPUT(label='Reference condenser cooling water inlet/outlet temperature difference', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    T_amb_des: float = INPUT(label='Reference ambient temperature at design point', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    CT: float = INPUT(label='Condensor type: 1=evaporative, 2=air, 3=hybrid', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    T_approach: float = INPUT(label='Cooling tower approach temperature', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    T_ITD_des: float = INPUT(label='ITD at design for dry system', units='C', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    P_cond_ratio: float = INPUT(label='Condenser pressure ratio', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    pb_bd_frac: float = INPUT(label='Power block blowdown steam fraction', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    P_cond_min: float = INPUT(label='Minimum condenser pressure', units='inHg', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    n_pl_inc: float = INPUT(label='Number of part-load increments for the heat rejection system', units='none', type='NUMBER', group='Rankine Cycle', required='pc_config=0', constraints='INTEGER')
    F_wc: Array = INPUT(label='TOU array of fractions indicating wet cooling share for hybrid cooling', type='ARRAY', group='System Control', required='pc_config=0')
    tech_type: float = INPUT(label='Turbine inlet pressure control 1=Fixed, 3=Sliding', type='NUMBER', group='Rankine Cycle', required='pc_config=0')
    ud_f_W_dot_cool_des: float = INPUT(label='Percent of user-defined power cycle design gross output consumed by cooling', units='%', type='NUMBER', group='User Defined Power Cycle', required='pc_config=1')
    ud_m_dot_water_cool_des: float = INPUT(label='Mass flow rate of water required at user-defined power cycle design point', units='kg/s', type='NUMBER', group='User Defined Power Cycle', required='pc_config=1')
    ud_ind_od: Matrix = INPUT(label='Off design user-defined power cycle performance as function of T_htf, m_dot_htf [ND], and T_amb', type='MATRIX', group='User Defined Power Cycle', required='pc_config=1')
    pb_fixed_par: float = INPUT(label='Fixed parasitic load - runs at all times', units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    aux_par: float = INPUT(label='Aux heater, boiler parasitic', units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    aux_par_f: float = INPUT(label='Aux heater, boiler parasitic - multiplying fraction', type='NUMBER', group='System Control', required='*')
    aux_par_0: float = INPUT(label='Aux heater, boiler parasitic - constant coefficient', type='NUMBER', group='System Control', required='*')
    aux_par_1: float = INPUT(label='Aux heater, boiler parasitic - linear coefficient', type='NUMBER', group='System Control', required='*')
    aux_par_2: float = INPUT(label='Aux heater, boiler parasitic - quadratic coefficient', type='NUMBER', group='System Control', required='*')
    bop_par: float = INPUT(label='Balance of plant parasitic power fraction', units='MWe/MWcap', type='NUMBER', group='System Control', required='*')
    bop_par_f: float = INPUT(label='Balance of plant parasitic power fraction - mult frac', type='NUMBER', group='System Control', required='*')
    bop_par_0: float = INPUT(label='Balance of plant parasitic power fraction - const coeff', type='NUMBER', group='System Control', required='*')
    bop_par_1: float = INPUT(label='Balance of plant parasitic power fraction - linear coeff', type='NUMBER', group='System Control', required='*')
    bop_par_2: float = INPUT(label='Balance of plant parasitic power fraction - quadratic coeff', type='NUMBER', group='System Control', required='*')
    timestep_load_fractions: Array = INPUT(label='Turbine load fraction for each timestep, alternative to block dispatch', type='ARRAY', group='System Control', required='?')
    f_turb_tou_periods: Array = INPUT(label='Dispatch logic for turbine load fraction', type='ARRAY', group='System Control', required='*')
    weekday_schedule: Matrix = INPUT(label='12x24 CSP operation Time-of-Use Weekday schedule', type='MATRIX', group='System Control', required='*')
    weekend_schedule: Matrix = INPUT(label='12x24 CSP operation Time-of-Use Weekend schedule', type='MATRIX', group='System Control', required='*')
    is_tod_pc_target_also_pc_max: float = INPUT(label='Is the TOD target cycle heat input also the max cycle heat input?', type='NUMBER', group='System Control', required='?=0')
    can_cycle_use_standby: float = INPUT(label='Can the cycle use standby operation?', type='NUMBER', group='System Control', required='?=0')
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
    disp_time_weighting: float = INPUT(label='Dispatch optimization future time discounting factor', type='NUMBER', group='System Control', required='?=0.99')
    is_write_ampl_dat: float = INPUT(label='Write AMPL data files for dispatch run', type='NUMBER', group='System Control', required='?=0')
    ampl_data_dir: str = INPUT(label='AMPL data file directory', type='STRING', group='System Control', required="?=''")
    is_ampl_engine: float = INPUT(label='Run dispatch optimization with external AMPL engine', type='NUMBER', group='System Control', required='?=0')
    ampl_exec_call: str = INPUT(label='System command to run AMPL code', type='STRING', group='System Control', required="?='ampl sdk_solution.run'")
    disp_rsu_cost_rel: float = INPUT(label='Receiver startup cost', units='$/MWt/start', type='NUMBER', group='System Control')
    disp_csu_cost_rel: float = INPUT(label='Cycle startup cost', units='$/MWe-cycle/start', type='NUMBER', group='System Control')
    disp_pen_ramping: float = INPUT(label='Dispatch cycle production change penalty', units='$/MWe-change', type='NUMBER', group='System Control')
    disp_inventory_incentive: float = INPUT(label='Dispatch storage terminal inventory incentive multiplier', type='NUMBER', group='System Control', required='?=0.0')
    q_rec_standby: float = INPUT(label='Receiver standby energy consumption', units='kWt', type='NUMBER', group='System Control', required='?=9e99')
    q_rec_heattrace: float = INPUT(label='Receiver heat trace energy consumption during startup', units='kWe-hr', type='NUMBER', group='System Control', required='?=0.0')
    is_wlim_design: float = INPUT(label='Use fixed design-point net electricity generation limits (dispatch opt only)', type='NUMBER', group='System Control', required='?=0')
    disp_wlim_maxspec: float = INPUT(label='Fixed design-point max net power to the grid (dispatch opt only)', type='NUMBER', group='System Control', required='is_wlim_design=1')
    is_wlim_series: float = INPUT(label='Use time-series net electricity generation limits (dispatch opt only)', type='NUMBER', group='System Control', required='?=0')
    wlim_series: Array = INPUT(label='Time series net electicity generation limits (dispatch opt only)', units='kWe', type='ARRAY', group='System Control', required='is_wlim_series=1')
    ppa_multiplier_model: float = INPUT(label='PPA multiplier model 0: dispatch factors dispatch_factorX, 1: hourly multipliers dispatch_factors_ts', units='0/1', type='NUMBER', group='Time of Delivery Factors', required='?=0', constraints='INTEGER,MIN=0', meta='0=diurnal,1=timestep')
    ppa_soln_mode: float = INPUT(label='PPA solution mode (0=Specify IRR target, 1=Specify PPA price)', type='NUMBER', group='Financial Solution Mode', required='sim_type=1&ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factors_ts: Array = INPUT(label='Dispatch payment factor array', type='ARRAY', group='Time of Delivery Factors', required='ppa_multiplier_model=1&csp_financial_model<5&is_dispatch=1&sim_type=1')
    en_electricity_rates: float = INPUT(label='Enable electricity rates for grid purchase', units='0/1', type='NUMBER', group='Electricity Rates', required='?=0')
    dispatch_sched_weekday: Matrix = INPUT(label='PPA pricing weekday schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_sched_weekend: Matrix = INPUT(label='PPA pricing weekend schedule, 12x24', type='MATRIX', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor1: float = INPUT(label='Dispatch payment factor 1', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor2: float = INPUT(label='Dispatch payment factor 2', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor3: float = INPUT(label='Dispatch payment factor 3', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor4: float = INPUT(label='Dispatch payment factor 4', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor5: float = INPUT(label='Dispatch payment factor 5', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor6: float = INPUT(label='Dispatch payment factor 6', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor7: float = INPUT(label='Dispatch payment factor 7', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor8: float = INPUT(label='Dispatch payment factor 8', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    dispatch_factor9: float = INPUT(label='Dispatch payment factor 9', type='NUMBER', group='Time of Delivery Factors', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    is_dispatch_series: float = INPUT(label='Use time-series dispatch factors', type='NUMBER', group='System Control', required='?=0')
    dispatch_series: Array = INPUT(label='Time series dispatch factors', type='ARRAY', group='System Control')
    ppa_price_input: Array = INPUT(label='PPA prices - yearly', units='$/kWh', type='ARRAY', group='Revenue', required='ppa_multiplier_model=0&csp_financial_model<5&is_dispatch=1&sim_type=1')
    mp_energy_market_revenue: Matrix = INPUT(label='Energy market revenue input', type='MATRIX', group='Revenue', required='csp_financial_model=6&is_dispatch=1&sim_type=1', meta='Lifetime x 2[Cleared Capacity(MW),Price($/MWh)]')
    tower_fixed_cost: float = INPUT(label='Tower fixed cost', units='$', type='NUMBER', group='System Costs', required='*')
    tower_exp: float = INPUT(label='Tower cost scaling exponent', type='NUMBER', group='System Costs', required='*')
    rec_ref_cost: float = INPUT(label='Receiver reference cost', units='$', type='NUMBER', group='System Costs', required='*')
    rec_ref_area: float = INPUT(label='Receiver reference area for cost scale', type='NUMBER', group='System Costs', required='*')
    rec_cost_exp: float = INPUT(label='Receiver cost scaling exponent', type='NUMBER', group='System Costs', required='*')
    site_spec_cost: float = INPUT(label='Site improvement cost', units='$/m2', type='NUMBER', group='System Costs', required='*')
    heliostat_spec_cost: float = INPUT(label='Heliostat field cost', units='$/m2', type='NUMBER', group='System Costs', required='*')
    plant_spec_cost: float = INPUT(label='Power cycle specific cost', units='$/kWe', type='NUMBER', group='System Costs', required='*')
    bop_spec_cost: float = INPUT(label='BOS specific cost', units='$/kWe', type='NUMBER', group='System Costs', required='*')
    tes_spec_cost: float = INPUT(label='Thermal energy storage cost', units='$/kWht', type='NUMBER', group='System Costs', required='*')
    land_spec_cost: float = INPUT(label='Total land area cost', units='$/acre', type='NUMBER', group='System Costs', required='*')
    contingency_rate: float = INPUT(label='Contingency for cost overrun', units='%', type='NUMBER', group='System Costs', required='*')
    sales_tax_rate: float = INPUT(label='Sales tax rate', units='%', type='NUMBER', group='Financial Parameters', required='*')
    sales_tax_frac: float = INPUT(label='Percent of cost to which sales tax applies', units='%', type='NUMBER', group='System Costs', required='*')
    cost_sf_fixed: float = INPUT(label='Solar field fixed cost', units='$', type='NUMBER', group='System Costs', required='*')
    fossil_spec_cost: float = INPUT(label='Fossil system specific cost', units='$/kWe', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_epc_per_acre: float = INPUT(name='csp.pt.cost.epc.per_acre', label='EPC cost per acre', units='$/acre', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_epc_percent: float = INPUT(name='csp.pt.cost.epc.percent', label='EPC cost percent of direct', units='%', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_epc_per_watt: float = INPUT(name='csp.pt.cost.epc.per_watt', label='EPC cost per watt', units='$/W', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_epc_fixed: float = INPUT(name='csp.pt.cost.epc.fixed', label='EPC fixed', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_plm_percent: float = INPUT(name='csp.pt.cost.plm.percent', label='PLM cost percent of direct', units='%', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_plm_per_watt: float = INPUT(name='csp.pt.cost.plm.per_watt', label='PLM cost per watt', units='$/W', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_plm_fixed: float = INPUT(name='csp.pt.cost.plm.fixed', label='PLM fixed', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_sf_fixed_land_area: float = INPUT(name='csp.pt.sf.fixed_land_area', label='Fixed land area', units='acre', type='NUMBER', group='Heliostat Field', required='*')
    csp_pt_sf_land_overhead_factor: float = INPUT(name='csp.pt.sf.land_overhead_factor', label='Land overhead factor', type='NUMBER', group='Heliostat Field', required='*')
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
    piping_loss: float = INPUT(label='Thermal loss per meter of piping', units='Wt/m', type='NUMBER', group='Deprecated')
    disp_csu_cost: float = INPUT(label='Cycle startup cost', units='$', type='NUMBER', group='Deprecated')
    disp_rsu_cost: float = INPUT(label='Receiver startup cost', units='$', type='NUMBER', group='Deprecated')
    disp_pen_delta_w: float = INPUT(label='Dispatch cycle production change penalty', units='$/kWe-change', type='NUMBER', group='Deprecated')
    P_boil: float = INPUT(label='Boiler operating pressure', units='bar', type='NUMBER', group='Deprecated')
    csp_pt_tes_init_hot_htf_percent: float = INPUT(name='csp.pt.tes.init_hot_htf_percent', label='Initial fraction of available volume that is hot', units='%', type='NUMBER', group='Deprecated')
    total_land_area: Final[float] = OUTPUT(label='Total land area', units='acre', type='NUMBER', group='System Costs', required='*')
    system_capacity: Final[float] = OUTPUT(label='System capacity', units='kWe', type='NUMBER', group='System Costs', required='*')
    cp_system_nameplate: Final[float] = OUTPUT(label='System capacity for capacity payments', units='MWe', type='NUMBER', group='System Costs', required='*')
    cp_battery_nameplate: Final[float] = OUTPUT(label='Battery nameplate', units='MWe', type='NUMBER', group='System Costs', required='*')
    N_hel_calc: Final[float] = OUTPUT(label='Number of heliostats - out', type='NUMBER', group='Heliostat Field', required='*')
    refl_image_error: Final[float] = OUTPUT(label='Reflected image error', units='mrad', type='NUMBER', group='Heliostat Field', required='*')
    heliostat_area: Final[float] = OUTPUT(label='Active area of heliostat', units='m^2', type='NUMBER', group='Heliostat Field', required='*')
    average_attenuation: Final[float] = OUTPUT(label='Average solar field attenuation', units='%', type='NUMBER', group='Heliostat Field', required='*')
    helio_positions_calc: Final[Matrix] = OUTPUT(label='Heliostat position table - out', type='MATRIX', group='Heliostat Field', required='*')
    A_sf: Final[float] = OUTPUT(label='Solar field area', units='m^2', type='NUMBER', group='Heliostat Field', required='*')
    land_min_abs: Final[float] = OUTPUT(label='Min distance from tower to heliostat', units='m', type='NUMBER', group='Heliostat Field', required='*')
    land_max_abs: Final[float] = OUTPUT(label='Max distance from tower to heliostat', units='m', type='NUMBER', group='Heliostat Field', required='*')
    land_area_base_calc: Final[float] = OUTPUT(label='Land area occupied by heliostats', units='acre', type='NUMBER', group='Heliostat Field', required='*')
    total_land_area_before_rad_cooling_calc: Final[float] = OUTPUT(label='Total land area not including radiative cooling - out', units='acre', type='NUMBER', group='Heliostat Field', required='*')
    W_dot_col_tracking_des: Final[float] = OUTPUT(label='Collector tracking power at design', units='MWe', type='NUMBER', group='Heliostat Field', required='*')
    rec_height_calc: Final[float] = OUTPUT(label='Receiver height - out', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    D_rec_calc: Final[float] = OUTPUT(label='The overall outer diameter of the receiver - out', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    h_tower_calc: Final[float] = OUTPUT(label='Tower height - out', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    ext_rec_area: Final[float] = OUTPUT(label='External receiver area - out', units='m2', type='NUMBER', group='Tower and Receiver', required='*')
    ext_rec_aspect: Final[float] = OUTPUT(label='External receiver aspect ratio - out', type='NUMBER', group='Tower and Receiver', required='*')
    cav_rec_height_calc: Final[float] = OUTPUT(label='Cavity receiver height - out', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    cav_rec_width_calc: Final[float] = OUTPUT(label='Cavity receiver aperture width - out', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    cav_rec_area: Final[float] = OUTPUT(label='Cavity receiver area', units='m2', type='NUMBER', group='Tower and Receiver', required='*')
    cav_panel_width: Final[float] = OUTPUT(label='Cavity panel width', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    cav_radius: Final[float] = OUTPUT(label='Cavity radius', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    A_rec: Final[float] = OUTPUT(label='Receiver area - planar', units='m2', type='NUMBER', group='Tower and Receiver', required='*')
    L_tower_piping_calc: Final[float] = OUTPUT(label='Tower piping length', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    q_dot_rec_des: Final[float] = OUTPUT(label='Receiver thermal output at design', units='MWt', type='NUMBER', group='Tower and Receiver', required='*')
    eta_rec_thermal_des: Final[float] = OUTPUT(label='Receiver estimated thermal efficiency at design', type='NUMBER', group='Tower and Receiver', required='*')
    W_dot_rec_pump_des: Final[float] = OUTPUT(label='Receiver estimated pump power at design', units='MWe', type='NUMBER', group='Tower and Receiver', required='*')
    W_dot_rec_pump_tower_share_des: Final[float] = OUTPUT(label='Receiver estimated pump power due to tower height at design', units='MWe', type='NUMBER', group='Tower and Receiver', required='*')
    W_dot_rec_pump_rec_share_des: Final[float] = OUTPUT(label='Receiver estimated pump power due to rec tubes at design', units='MWe', type='NUMBER', group='Tower and Receiver', required='*')
    vel_rec_htf_des: Final[float] = OUTPUT(label='Receiver estimated tube HTF velocity at design', units='m/s', type='NUMBER', group='Tower and Receiver', required='*')
    m_dot_htf_rec_des: Final[float] = OUTPUT(label='Receiver HTF mass flow rate at design', units='kg/s', type='NUMBER', group='Tower and Receiver', required='*')
    m_dot_htf_rec_max: Final[float] = OUTPUT(label='Receiver max HTF mass flow rate', units='kg/s', type='NUMBER', group='Tower and Receiver', required='*')
    q_dot_piping_loss_des: Final[float] = OUTPUT(label='Receiver estimated piping loss at design', units='MWt', type='NUMBER', group='Tower and Receiver', required='*')
    q_dot_heater_des: Final[float] = OUTPUT(label='Heater design thermal power', units='MWt', type='NUMBER', group='Heater', required='*')
    W_dot_heater_des: Final[float] = OUTPUT(label='Heater electricity consumption at design', units='MWe', type='NUMBER', group='Heater', required='*')
    E_heater_su_des: Final[float] = OUTPUT(label='Heater startup energy', units='MWt-hr', type='NUMBER', group='Heater', required='*')
    m_dot_htf_cycle_des: Final[float] = OUTPUT(label='PC HTF mass flow rate at design', units='kg/s', type='NUMBER', group='Power Cycle', required='*')
    q_dot_cycle_des: Final[float] = OUTPUT(label='PC thermal input at design', units='MWt', type='NUMBER', group='Power Cycle', required='*')
    W_dot_cycle_pump_des: Final[float] = OUTPUT(label='PC HTF pump power at design', units='MWe', type='NUMBER', group='Power Cycle', required='*')
    W_dot_cycle_cooling_des: Final[float] = OUTPUT(label='PC cooling power at design', units='MWe', type='NUMBER', group='Power Cycle', required='*')
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
    Q_tes_des: Final[float] = OUTPUT(label='TES design capacity', units='MWt-hr', type='NUMBER', group='TES Design Calc', required='*')
    V_tes_htf_avail_des: Final[float] = OUTPUT(label='TES volume of HTF available for heat transfer', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    V_tes_htf_total_des: Final[float] = OUTPUT(label='TES total HTF volume', units='m3', type='NUMBER', group='TES Design Calc', required='*')
    d_tank_tes: Final[float] = OUTPUT(label='TES tank diameter', units='m', type='NUMBER', group='TES Design Calc', required='*')
    q_dot_loss_tes_des: Final[float] = OUTPUT(label='TES thermal loss at design', units='MWt', type='NUMBER', group='TES Design Calc', required='*')
    tshours_rec: Final[float] = OUTPUT(label='TES duration at receiver design output', units='hr', type='NUMBER', group='TES Design Calc', required='*')
    tshours_heater: Final[float] = OUTPUT(label='TES duration at heater design output', units='hr', type='NUMBER', group='TES Design Calc', required='*')
    dens_store_htf_at_T_ave: Final[float] = OUTPUT(label='TES density of HTF at avg temps', units='kg/m3', type='NUMBER', group='TES Design Calc', required='*')
    nameplate: Final[float] = OUTPUT(label='Nameplate capacity', units='MWe', type='NUMBER', group='System Design Calc', required='*')
    W_dot_bop_design: Final[float] = OUTPUT(label='BOP parasitics at design', units='MWe', type='NUMBER', group='Balance of Plant', required='*')
    W_dot_fixed: Final[float] = OUTPUT(label='Fixed parasitic at design', units='MWe', type='NUMBER', group='Balance of Plant', required='*')
    h_rec_input_to_cost_model: Final[float] = OUTPUT(label='Receiver height for cost model selected from receiver type', units='m', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_site_improvements: Final[float] = OUTPUT(name='csp.pt.cost.site_improvements', label='Site improvement cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_heliostats: Final[float] = OUTPUT(name='csp.pt.cost.heliostats', label='Heliostat cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_tower: Final[float] = OUTPUT(name='csp.pt.cost.tower', label='Tower cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_receiver: Final[float] = OUTPUT(name='csp.pt.cost.receiver', label='Receiver cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_storage: Final[float] = OUTPUT(name='csp.pt.cost.storage', label='TES cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_power_block: Final[float] = OUTPUT(name='csp.pt.cost.power_block', label='Power cycle cost', units='$', type='NUMBER', group='System Costs', required='*')
    heater_cost: Final[float] = OUTPUT(label='Heater cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_rad_field: Final[float] = OUTPUT(name='csp.pt.cost.rad_field', label='Radiative field cost$', type='NUMBER', group='*', meta='System Costs')
    csp_pt_cost_rad_fluid: Final[float] = OUTPUT(name='csp.pt.cost.rad_fluid', label='Radiative fluid cost$', type='NUMBER', group='*', meta='System Costs')
    csp_pt_cost_rad_storage: Final[float] = OUTPUT(name='csp.pt.cost.rad_storage', label='Cold storage cost$', type='NUMBER', group='*', meta='System Costs')
    csp_pt_cost_bop: Final[float] = OUTPUT(name='csp.pt.cost.bop', label='BOP cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_fossil: Final[float] = OUTPUT(name='csp.pt.cost.fossil', label='Fossil backup cost', units='$', type='NUMBER', group='System Costs', required='*')
    ui_direct_subtotal: Final[float] = OUTPUT(label='Direct capital precontingency cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_contingency: Final[float] = OUTPUT(name='csp.pt.cost.contingency', label='Contingency cost', units='$', type='NUMBER', group='System Costs', required='*')
    total_direct_cost: Final[float] = OUTPUT(label='Total direct cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_epc_total: Final[float] = OUTPUT(name='csp.pt.cost.epc.total', label='EPC and owner cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_plm_total: Final[float] = OUTPUT(name='csp.pt.cost.plm.total', label='Total land cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_sales_tax_total: Final[float] = OUTPUT(name='csp.pt.cost.sales_tax.total', label='Sales tax cost', units='$', type='NUMBER', group='System Costs', required='*')
    total_indirect_cost: Final[float] = OUTPUT(label='Total indirect cost', units='$', type='NUMBER', group='System Costs', required='*')
    total_installed_cost: Final[float] = OUTPUT(label='Total installed cost', units='$', type='NUMBER', group='System Costs', required='*')
    csp_pt_cost_installed_per_capacity: Final[float] = OUTPUT(name='csp.pt.cost.installed_per_capacity', label='Estimated installed cost per cap', units='$', type='NUMBER', group='System Costs', required='*')
    const_per_principal1: Final[float] = OUTPUT(label='Principal, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_principal2: Final[float] = OUTPUT(label='Principal, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_principal3: Final[float] = OUTPUT(label='Principal, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_principal4: Final[float] = OUTPUT(label='Principal, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_principal5: Final[float] = OUTPUT(label='Principal, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest1: Final[float] = OUTPUT(label='Interest cost, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest2: Final[float] = OUTPUT(label='Interest cost, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest3: Final[float] = OUTPUT(label='Interest cost, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest4: Final[float] = OUTPUT(label='Interest cost, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest5: Final[float] = OUTPUT(label='Interest cost, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_total1: Final[float] = OUTPUT(label='Total financing cost, loan 1', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_total2: Final[float] = OUTPUT(label='Total financing cost, loan 2', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_total3: Final[float] = OUTPUT(label='Total financing cost, loan 3', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_total4: Final[float] = OUTPUT(label='Total financing cost, loan 4', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_total5: Final[float] = OUTPUT(label='Total financing cost, loan 5', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_percent_total: Final[float] = OUTPUT(label='Total percent of installed costs, all loans', units='%', type='NUMBER', group='Financial Parameters', required='*')
    const_per_principal_total: Final[float] = OUTPUT(label='Total principal, all loans', units='$', type='NUMBER', group='Financial Parameters', required='*')
    const_per_interest_total: Final[float] = OUTPUT(label='Total interest costs, all loans', units='$', type='NUMBER', group='Financial Parameters', required='*')
    construction_financing_cost: Final[float] = OUTPUT(label='Total construction financing cost', units='$', type='NUMBER', group='Financial Parameters', required='*')
    time_hr: Final[Array] = OUTPUT(label='Time at end of timestep', units='hr', type='ARRAY', required='sim_type=1')
    solzen: Final[Array] = OUTPUT(label='Resource solar zenith', units='deg', type='ARRAY', required='sim_type=1')
    solaz: Final[Array] = OUTPUT(label='Resource solar azimuth', units='deg', type='ARRAY', required='sim_type=1')
    beam: Final[Array] = OUTPUT(label='Resource beam normal irradiance', units='W/m2', type='ARRAY', required='sim_type=1')
    tdry: Final[Array] = OUTPUT(label='Resource dry Bulb temperature', units='C', type='ARRAY', required='sim_type=1')
    twet: Final[Array] = OUTPUT(label='Resource wet Bulb temperature', units='C', type='ARRAY', required='sim_type=1')
    rh: Final[Array] = OUTPUT(label='Resource relative humidity', units='%', type='ARRAY', required='sim_type=1')
    wspd: Final[Array] = OUTPUT(label='Resource wind velocity', units='m/s', type='ARRAY', required='sim_type=1')
    eta_map_out: Final[Matrix] = OUTPUT(label='Solar field optical efficiencies', type='MATRIX', required='sim_type=1')
    flux_maps_for_import: Final[Matrix] = OUTPUT(label='Flux map for import', type='MATRIX', required='sim_type=1')
    flux_maps_out: Final[Matrix] = OUTPUT(label='Flux map intensities', type='MATRIX', required='sim_type=1')
    q_sf_inc: Final[Array] = OUTPUT(label='Field incident thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    eta_field: Final[Array] = OUTPUT(label='Field optical efficiency', type='ARRAY', required='sim_type=1')
    defocus: Final[Array] = OUTPUT(label='Field optical focus fraction', type='ARRAY', required='sim_type=1')
    sf_adjust_out: Final[Array] = OUTPUT(label='Field availability adjustment factor', type='ARRAY', required='sim_type=1')
    rec_defocus: Final[Array] = OUTPUT(label='Receiver component defocus', type='ARRAY', required='sim_type=1')
    q_dot_rec_inc: Final[Array] = OUTPUT(label='Receiver incident thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    eta_therm: Final[Array] = OUTPUT(label='Receiver thermal efficiency', type='ARRAY', required='sim_type=1')
    Q_thermal: Final[Array] = OUTPUT(label='Receiver thermal power to HTF less piping loss', units='MWt', type='ARRAY', required='sim_type=1')
    pparasi: Final[Array] = OUTPUT(label='Field tracking power', units='MWe', type='ARRAY', required='sim_type=1')
    m_dot_rec: Final[Array] = OUTPUT(label='Receiver mass flow rate', units='kg/s', type='ARRAY', required='sim_type=1')
    q_startup: Final[Array] = OUTPUT(label='Receiver startup thermal energy consumed', units='MWt', type='ARRAY', required='sim_type=1')
    T_rec_in: Final[Array] = OUTPUT(label='Receiver HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_rec_out: Final[Array] = OUTPUT(label='Receiver HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    q_piping_losses: Final[Array] = OUTPUT(label='Receiver header/tower piping losses', units='MWt', type='ARRAY', required='sim_type=1')
    q_thermal_loss: Final[Array] = OUTPUT(label='Receiver convection and emission losses', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_reflection_loss: Final[Array] = OUTPUT(label='Receiver reflection losses', units='MWt', type='ARRAY', required='sim_type=1&receiver_type=1')
    P_tower_pump: Final[Array] = OUTPUT(label='Receiver and tower HTF pumping power', units='MWe', type='ARRAY', required='sim_type=1')
    T_rec_out_end: Final[Array] = OUTPUT(label='Receiver HTF outlet temperature at end of timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    T_rec_out_max: Final[Array] = OUTPUT(label='Receiver maximum HTF outlet temperature during timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    T_panel_out_max: Final[Array] = OUTPUT(label='Receiver panel maximum HTF outlet temperature during timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    T_wall_rec_inlet: Final[Array] = OUTPUT(label='Receiver inlet panel wall temperature at end of timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    T_wall_rec_outlet: Final[Array] = OUTPUT(label='Receiver outlet panel wall temperature at end of timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    T_wall_riser: Final[Array] = OUTPUT(label='Receiver riser wall temperature at end of timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    T_wall_downcomer: Final[Array] = OUTPUT(label='Receiver downcomer wall temperature at end of timestep', units='C', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    clearsky: Final[Array] = OUTPUT(label='Predicted clear-sky beam normal irradiance', units='W/m2', type='ARRAY', group='CR', required='sim_type=1&rec_clearsky_fraction>0')
    Q_thermal_ss: Final[Array] = OUTPUT(label='Receiver thermal power to HTF less piping loss (steady state)', units='MWt', type='ARRAY', group='CR', required='sim_type=1&is_rec_model_trans=1')
    Q_thermal_ss_csky: Final[Array] = OUTPUT(label='Receiver thermal power to HTF less piping loss under clear-sky conditions (steady state)', units='MWt', type='ARRAY', group='CR', required='sim_type=1&rec_clearsky_fraction>0')
    W_dot_heater: Final[Array] = OUTPUT(label='Parallel heater electricity consumption', units='MWe', type='ARRAY', group='Parallel Heater', required='sim_type=1&is_parallel_htr=1')
    q_dot_heater_to_htf: Final[Array] = OUTPUT(label='Parallel heater thermal power to HTF', units='MWt', type='ARRAY', group='Parallel Heater', required='sim_type=1&is_parallel_htr=1')
    q_dot_heater_startup: Final[Array] = OUTPUT(label='Parallel heater thermal power consumed during startup', units='MWt', type='ARRAY', group='Parallel Heater', required='sim_type=1&is_parallel_htr=1')
    m_dot_htf_heater: Final[Array] = OUTPUT(label='Parallel heater HTF mass flow rate', units='kg/s', type='ARRAY', group='Parallel Heater', required='sim_type=1&is_parallel_htr=1')
    T_htf_heater_in: Final[Array] = OUTPUT(label='Parallel heater HTF inlet temperature', units='C', type='ARRAY', group='Parallel Heater', required='sim_type=1&is_parallel_htr=1')
    T_htf_heater_out: Final[Array] = OUTPUT(label='Parallel heater HTF outlet temperature', units='C', type='ARRAY', group='Parallel Heater', required='sim_type=1&is_parallel_htr=1')
    eta: Final[Array] = OUTPUT(label='PC efficiency, gross', type='ARRAY', required='sim_type=1')
    q_pb: Final[Array] = OUTPUT(label='PC input energy', units='MWt', type='ARRAY', required='sim_type=1')
    m_dot_pc: Final[Array] = OUTPUT(label='PC HTF mass flow rate', units='kg/s', type='ARRAY', required='sim_type=1')
    q_pc_startup: Final[Array] = OUTPUT(label='PC startup thermal energy', units='MWht', type='ARRAY', required='sim_type=1')
    q_dot_pc_startup: Final[Array] = OUTPUT(label='PC startup thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    P_cycle: Final[Array] = OUTPUT(label='PC electrical power output, gross', units='MWe', type='ARRAY', required='sim_type=1')
    T_pc_in: Final[Array] = OUTPUT(label='PC HTF inlet temperature', units='C', type='ARRAY', required='sim_type=1')
    T_pc_out: Final[Array] = OUTPUT(label='PC HTF outlet temperature', units='C', type='ARRAY', required='sim_type=1')
    m_dot_water_pc: Final[Array] = OUTPUT(label='PC water consumption, makeup + cooling', units='kg/s', type='ARRAY', required='sim_type=1')
    T_cond_out: Final[Array] = OUTPUT(label='PC condenser water outlet temperature', units='C', type='ARRAY', group='PC', required='sim_type=1')
    T_cold: Final[Array] = OUTPUT(label='Cold storage cold temperature', units='C', type='ARRAY', group='PC', required='?')
    m_cold: Final[Array] = OUTPUT(label='Cold storage cold tank mass', units='kg', type='ARRAY', group='PC', required='?')
    m_warm: Final[Array] = OUTPUT(label='Cold storage warm tank mass', units='kg', type='ARRAY', group='PC', required='?')
    T_warm: Final[Array] = OUTPUT(label='Cold storage warm tank temperature', units='C', type='ARRAY', group='PC', required='?')
    T_rad_out: Final[Array] = OUTPUT(label='Radiator outlet temperature', units='C', type='ARRAY', group='PC', required='?')
    A_radfield: Final[float] = OUTPUT(label='Radiator field surface area', units='m^2', type='NUMBER', group='PC', required='?')
    P_cond: Final[Array] = OUTPUT(label='PC condensing presssure', units='Pa', type='ARRAY', group='PC', required='?')
    P_cond_iter_err: Final[Array] = OUTPUT(label='PC condenser presure iteration error', type='ARRAY', group='PC', required='?')
    radcool_control: Final[Array] = OUTPUT(label='Radiative cooling status code', units='-', type='ARRAY', group='PC', required='?')
    cycle_htf_pump_power: Final[Array] = OUTPUT(label='Cycle HTF pump power', units='MWe', type='ARRAY', required='sim_type=1')
    P_cooling_tower_tot: Final[Array] = OUTPUT(label='Parasitic power condenser operation', units='MWe', type='ARRAY', required='sim_type=1')
    tank_losses: Final[Array] = OUTPUT(label='TES thermal losses', units='MWt', type='ARRAY', required='sim_type=1')
    q_heater: Final[Array] = OUTPUT(label='TES freeze protection power', units='MWe', type='ARRAY', required='sim_type=1')
    T_tes_hot: Final[Array] = OUTPUT(label='TES hot temperature', units='C', type='ARRAY', required='sim_type=1')
    T_tes_cold: Final[Array] = OUTPUT(label='TES cold temperature', units='C', type='ARRAY', required='sim_type=1')
    mass_tes_cold: Final[Array] = OUTPUT(label='TES cold tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    mass_tes_hot: Final[Array] = OUTPUT(label='TES hot tank mass (end)', units='kg', type='ARRAY', required='sim_type=1')
    q_dc_tes: Final[Array] = OUTPUT(label='TES discharge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    q_ch_tes: Final[Array] = OUTPUT(label='TES charge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    e_ch_tes: Final[Array] = OUTPUT(label='TES charge state', units='MWht', type='ARRAY', required='sim_type=1')
    m_dot_cr_to_tes_hot: Final[Array] = OUTPUT(label='Mass flow: field to hot TES', units='kg/s', type='ARRAY', required='sim_type=1')
    m_dot_tes_hot_out: Final[Array] = OUTPUT(label='Mass flow: TES hot out', units='kg/s', type='ARRAY', required='sim_type=1')
    m_dot_pc_to_tes_cold: Final[Array] = OUTPUT(label='Mass flow: cycle to cold TES', units='kg/s', type='ARRAY', required='sim_type=1')
    m_dot_tes_cold_out: Final[Array] = OUTPUT(label='Mass flow: TES cold out', units='kg/s', type='ARRAY', required='sim_type=1')
    m_dot_field_to_cycle: Final[Array] = OUTPUT(label='Mass flow: field to cycle', units='kg/s', type='ARRAY', required='sim_type=1')
    m_dot_cycle_to_field: Final[Array] = OUTPUT(label='Mass flow: cycle to field', units='kg/s', type='ARRAY', required='sim_type=1')
    tes_htf_pump_power: Final[Array] = OUTPUT(label='TES HTF pump power', units='MWe', type='ARRAY', required='sim_type=1')
    P_fixed: Final[Array] = OUTPUT(label='Parasitic power fixed load', units='MWe', type='ARRAY', required='sim_type=1')
    P_plant_balance_tot: Final[Array] = OUTPUT(label='Parasitic power generation-dependent load', units='MWe', type='ARRAY', required='sim_type=1')
    P_rec_heattrace: Final[Array] = OUTPUT(label='Receiver heat trace parasitic load', units='MWe', type='ARRAY', group='System', required='sim_type=1&is_rec_model_trans=1')
    P_out_net: Final[Array] = OUTPUT(label='Total electric power to grid', units='MWe', type='ARRAY', required='sim_type=1')
    tou_value: Final[Array] = OUTPUT(label='CSP operating time-of-use value', type='ARRAY', required='sim_type=1')
    pricing_mult: Final[Array] = OUTPUT(label='PPA price multiplier', type='ARRAY', required='sim_type=1')
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
    disp_qsf_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field available energy', units='MWt', type='ARRAY', required='sim_type=1')
    disp_qsfprod_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field generation', units='MWt', type='ARRAY', required='sim_type=1')
    disp_qsfsu_expected: Final[Array] = OUTPUT(label='Dispatch expected solar field startup enegy', units='MWt', type='ARRAY', required='sim_type=1')
    disp_tes_expected: Final[Array] = OUTPUT(label='Dispatch expected TES charge level', units='MWht', type='ARRAY', required='sim_type=1')
    disp_pceff_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle efficiency adj.', type='ARRAY', required='sim_type=1')
    disp_thermeff_expected: Final[Array] = OUTPUT(label='Dispatch expected SF thermal efficiency adj.', type='ARRAY', required='sim_type=1')
    disp_qpbsu_expected: Final[Array] = OUTPUT(label='Dispatch expected power cycle startup energy', units='MWht', type='ARRAY', required='sim_type=1')
    disp_wpb_expected: Final[Array] = OUTPUT(label='Dispatch expected power generation', units='MWe', type='ARRAY', required='sim_type=1')
    disp_rev_expected: Final[Array] = OUTPUT(label='Dispatch expected revenue factor', type='ARRAY', required='sim_type=1')
    disp_presolve_nconstr: Final[Array] = OUTPUT(label='Dispatch number of constraints in problem', type='ARRAY', required='sim_type=1')
    disp_presolve_nvar: Final[Array] = OUTPUT(label='Dispatch number of variables in problem', type='ARRAY', required='sim_type=1')
    disp_solve_time: Final[Array] = OUTPUT(label='Dispatch solver time', units='sec', type='ARRAY', required='sim_type=1')
    q_dot_pc_sb: Final[Array] = OUTPUT(label='Thermal power for PC standby', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_min: Final[Array] = OUTPUT(label='Thermal power for PC min operation', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_max: Final[Array] = OUTPUT(label='Max thermal power to PC', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_pc_target: Final[Array] = OUTPUT(label='Target thermal power to PC', units='MWt', type='ARRAY', required='sim_type=1')
    is_rec_su_allowed: Final[Array] = OUTPUT(label='Is receiver startup allowed', type='ARRAY', required='sim_type=1')
    is_pc_su_allowed: Final[Array] = OUTPUT(label='Is power cycle startup allowed', type='ARRAY', required='sim_type=1')
    is_pc_sb_allowed: Final[Array] = OUTPUT(label='Is power cycle standby allowed', type='ARRAY', required='sim_type=1')
    is_PAR_HTR_allowed: Final[Array] = OUTPUT(label='Is parallel electric heater operation allowed', type='ARRAY', required='sim_type=1')
    q_dot_elec_to_PAR_HTR: Final[Array] = OUTPUT(label='Electric heater thermal power target', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_est_cr_su: Final[Array] = OUTPUT(label='Estimated receiver startup thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_est_cr_on: Final[Array] = OUTPUT(label='Estimated receiver thermal power TO HTF', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_est_tes_dc: Final[Array] = OUTPUT(label='Estimated max TES discharge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    q_dot_est_tes_ch: Final[Array] = OUTPUT(label='Estimated max TES charge thermal power', units='MWt', type='ARRAY', required='sim_type=1')
    operating_modes_a: Final[Array] = OUTPUT(label='First 3 operating modes tried', type='ARRAY', required='sim_type=1')
    operating_modes_b: Final[Array] = OUTPUT(label='Next 3 operating modes tried', type='ARRAY', required='sim_type=1')
    operating_modes_c: Final[Array] = OUTPUT(label='Final 3 operating modes tried', type='ARRAY', required='sim_type=1')
    gen: Final[Array] = OUTPUT(label='Total electric power to grid with available derate', units='kWe', type='ARRAY', required='sim_type=1')
    annual_energy: Final[float] = OUTPUT(label='Annual total electric power to grid', units='kWhe', type='NUMBER', required='sim_type=1')
    annual_W_cycle_gross: Final[float] = OUTPUT(label='Electrical source - power cycle gross output', units='kWhe', type='NUMBER', required='sim_type=1')
    annual_W_cooling_tower: Final[float] = OUTPUT(label='Total of condenser operation parasitics', units='kWhe', type='NUMBER', group='PC', required='sim_type=1')
    annual_q_rec_inc: Final[float] = OUTPUT(label='Annual receiver incident thermal power after reflective losses', units='MWt-hr', type='NUMBER', group='Tower and Receiver', required='sim_type=1')
    annual_q_rec_loss: Final[float] = OUTPUT(label='Annual receiver convective and radiative losses', units='MWt-hr', type='NUMBER', group='Tower and Receiver', required='sim_type=1')
    annual_eta_rec_th: Final[float] = OUTPUT(label='Annual receiver thermal efficiency ignoring rec reflective loss', type='NUMBER', group='Tower and Receiver', required='sim_type=1')
    annual_eta_rec_th_incl_refl: Final[float] = OUTPUT(label='Annual receiver thermal efficiency including reflective loss', type='NUMBER', group='Tower and Receiver', required='sim_type=1')
    conversion_factor: Final[float] = OUTPUT(label='Gross to net conversion factor', units='%', type='NUMBER', required='sim_type=1')
    capacity_factor: Final[float] = OUTPUT(label='Capacity factor', units='%', type='NUMBER', required='sim_type=1')
    sales_energy_capacity_factor: Final[float] = OUTPUT(label='Capacity factor considering only positive net generation periods', units='%', type='NUMBER', required='sim_type=1')
    kwh_per_kw: Final[float] = OUTPUT(label='First year kWh/kW', units='kWh/kW', type='NUMBER', required='sim_type=1')
    annual_total_water_use: Final[float] = OUTPUT(label='Total annual water usage, cycle + mirror washing', units='m3', type='NUMBER', required='sim_type=1')
    capacity_factor_highest_1000_ppas: Final[float] = OUTPUT(label='Capacity factor at 1000 highest ppa timesteps', units='-', type='NUMBER', required='sim_type=1')
    capacity_factor_highest_2000_ppas: Final[float] = OUTPUT(label='Capacity factor at 2000 highest ppa timesteps', units='-', type='NUMBER', required='sim_type=1')
    disp_objective_ann: Final[float] = OUTPUT(label='Annual sum of dispatch objective function value', type='NUMBER', required='sim_type=1')
    disp_iter_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solver iterations', type='NUMBER', required='sim_type=1')
    disp_presolve_nconstr_ann: Final[float] = OUTPUT(label='Annual sum of dispatch problem constraint count', type='NUMBER', required='sim_type=1')
    disp_presolve_nvar_ann: Final[float] = OUTPUT(label='Annual sum of dispatch problem variable count', type='NUMBER', required='sim_type=1')
    disp_solve_time_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solver time', type='NUMBER', required='sim_type=1')
    disp_solve_state_ann: Final[float] = OUTPUT(label='Annual sum of dispatch solve state', type='NUMBER', required='sim_type=1')
    avg_suboptimal_rel_mip_gap: Final[float] = OUTPUT(label='Average suboptimal relative MIP gap', units='%', type='NUMBER', required='sim_type=1')
    sim_cpu_run_time: Final[float] = OUTPUT(label='Simulation duration clock time', units='s', type='NUMBER', required='sim_type=1')
    adjust_constant: float = INPUT(name='adjust:constant', label='Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='*', constraints='MAX=100')
    adjust_hourly: Array = INPUT(name='adjust:hourly', label='Hourly Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    adjust_timeindex: Array = INPUT(name='adjust:timeindex', label='Lifetime Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    adjust_periods: Matrix = INPUT(name='adjust:periods', label='Period-based Adjustment Factors', units='%', type='MATRIX', group='Adjustment Factors', required='?', constraints='COLS=3', meta='n x 3 matrix [ start, end, loss ]')
    sf_adjust_constant: float = INPUT(name='sf_adjust:constant', label='SF Constant loss adjustment', units='%', type='NUMBER', group='Adjustment Factors', required='*', constraints='MAX=100')
    sf_adjust_hourly: Array = INPUT(name='sf_adjust:hourly', label='SF Hourly Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    sf_adjust_timeindex: Array = INPUT(name='sf_adjust:timeindex', label='SF Lifetime Adjustment Factors', units='%', type='ARRAY', group='Adjustment Factors', required='?', constraints='LENGTH=8760')
    sf_adjust_periods: Matrix = INPUT(name='sf_adjust:periods', label='SF Period-based Adjustment Factors', units='%', type='MATRIX', group='Adjustment Factors', required='?', constraints='COLS=3', meta='n x 3 matrix [ start, end, loss ]')

    def __init__(self, *args: Mapping[str, Any],
                 solar_resource_file: str = ...,
                 solar_resource_data: Table = ...,
                 is_dispatch: float = ...,
                 sim_type: float = ...,
                 csp_financial_model: float = ...,
                 time_start: float = ...,
                 time_stop: float = ...,
                 time_steps_per_hour: float = ...,
                 vacuum_arrays: float = ...,
                 is_parallel_htr: float = ...,
                 T_htf_cold_des: float = ...,
                 T_htf_hot_des: float = ...,
                 P_ref: float = ...,
                 design_eff: float = ...,
                 tshours: float = ...,
                 solarm: float = ...,
                 dni_des: float = ...,
                 field_model_type: float = ...,
                 helio_width: float = ...,
                 helio_height: float = ...,
                 helio_optical_error_mrad: float = ...,
                 helio_active_fraction: float = ...,
                 dens_mirror: float = ...,
                 helio_reflectance: float = ...,
                 rec_absorptance: float = ...,
                 rec_hl_perm2: float = ...,
                 land_max: float = ...,
                 land_min: float = ...,
                 land_bound_table: Matrix = ...,
                 land_bound_list: Array = ...,
                 p_start: float = ...,
                 p_track: float = ...,
                 hel_stow_deploy: float = ...,
                 v_wind_max: float = ...,
                 interp_nug: float = ...,
                 interp_beta: float = ...,
                 helio_aim_points: Matrix = ...,
                 eta_map: Matrix = ...,
                 eta_map_aod_format: float = ...,
                 flux_maps: Matrix = ...,
                 c_atm_0: float = ...,
                 c_atm_1: float = ...,
                 c_atm_2: float = ...,
                 c_atm_3: float = ...,
                 n_facet_x: float = ...,
                 n_facet_y: float = ...,
                 focus_type: float = ...,
                 cant_type: float = ...,
                 n_flux_days: float = ...,
                 delta_flux_hrs: float = ...,
                 water_usage_per_wash: float = ...,
                 washing_frequency: float = ...,
                 check_max_flux: float = ...,
                 sf_excess: float = ...,
                 A_sf_in: float = ...,
                 total_land_area_before_rad_cooling_in: float = ...,
                 N_hel: float = ...,
                 flux_max: float = ...,
                 opt_init_step: float = ...,
                 opt_max_iter: float = ...,
                 opt_conv_tol: float = ...,
                 opt_flux_penalty: float = ...,
                 opt_algorithm: float = ...,
                 receiver_type: float = ...,
                 N_panels: float = ...,
                 d_tube_out: float = ...,
                 th_tube: float = ...,
                 mat_tube: float = ...,
                 rec_htf: float = ...,
                 field_fl_props: Matrix = ...,
                 Flow_type: float = ...,
                 crossover_shift: float = ...,
                 epsilon: float = ...,
                 hl_ffact: float = ...,
                 f_rec_min: float = ...,
                 rec_su_delay: float = ...,
                 rec_qf_delay: float = ...,
                 csp_pt_rec_max_oper_frac: float = ...,
                 eta_pump: float = ...,
                 piping_length_mult: float = ...,
                 piping_length_const: float = ...,
                 n_cav_rec_panels: float = ...,
                 cav_rec_span: float = ...,
                 cav_rec_passive_abs: float = ...,
                 cav_rec_passive_eps: float = ...,
                 piping_loss_coefficient: float = ...,
                 rec_clearsky_model: float = ...,
                 rec_clearsky_dni: Array = ...,
                 rec_clearsky_fraction: float = ...,
                 is_rec_model_trans: float = ...,
                 is_rec_startup_trans: float = ...,
                 rec_tm_mult: float = ...,
                 riser_tm_mult: float = ...,
                 downc_tm_mult: float = ...,
                 u_riser: float = ...,
                 th_riser: float = ...,
                 heat_trace_power: float = ...,
                 preheat_flux: float = ...,
                 min_preheat_time: float = ...,
                 min_fill_time: float = ...,
                 startup_ramp_time: float = ...,
                 startup_target_Tdiff: float = ...,
                 is_rec_startup_from_T_soln: float = ...,
                 is_rec_enforce_min_startup: float = ...,
                 helio_positions: Matrix = ...,
                 rec_height: float = ...,
                 D_rec: float = ...,
                 h_tower: float = ...,
                 cav_rec_height: float = ...,
                 cav_rec_width: float = ...,
                 heater_mult: float = ...,
                 heater_efficiency: float = ...,
                 f_q_dot_des_allowable_su: float = ...,
                 hrs_startup_at_max_rate: float = ...,
                 f_q_dot_heater_min: float = ...,
                 disp_hsu_cost_rel: float = ...,
                 heater_spec_cost: float = ...,
                 allow_heater_no_dispatch_opt: float = ...,
                 tes_init_hot_htf_percent: float = ...,
                 h_tank: float = ...,
                 cold_tank_max_heat: float = ...,
                 u_tank: float = ...,
                 tank_pairs: float = ...,
                 cold_tank_Thtr: float = ...,
                 h_tank_min: float = ...,
                 hot_tank_Thtr: float = ...,
                 hot_tank_max_heat: float = ...,
                 tanks_in_parallel: float = ...,
                 h_ctes_tank_min: float = ...,
                 ctes_tshours: float = ...,
                 ctes_field_fl: float = ...,
                 h_ctes_tank: float = ...,
                 u_ctes_tank: float = ...,
                 ctes_tankpairs: float = ...,
                 T_ctes_cold_design: float = ...,
                 T_ctes_warm_design: float = ...,
                 T_ctes_warm_ini: float = ...,
                 T_ctes_cold_ini: float = ...,
                 f_ctes_warm_ini: float = ...,
                 rad_multiplier: float = ...,
                 m_dot_radpanel: float = ...,
                 n_rad_tubes: float = ...,
                 W_rad_tubes: float = ...,
                 L_rad: float = ...,
                 th_rad_panel: float = ...,
                 D_rad_tubes: float = ...,
                 k_panel: float = ...,
                 epsilon_radtop: float = ...,
                 epsilon_radbot: float = ...,
                 epsilon_radgrnd: float = ...,
                 L_rad_sections: float = ...,
                 epsilon_radHX: float = ...,
                 ctes_type: float = ...,
                 radiator_unitcost: float = ...,
                 radiator_installcost: float = ...,
                 radiator_fluidcost: float = ...,
                 radfluid_vol_ratio: float = ...,
                 ctes_cost: float = ...,
                 rad_pressuredrop: float = ...,
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
                 F_wc: Array = ...,
                 tech_type: float = ...,
                 ud_f_W_dot_cool_des: float = ...,
                 ud_m_dot_water_cool_des: float = ...,
                 ud_ind_od: Matrix = ...,
                 pb_fixed_par: float = ...,
                 aux_par: float = ...,
                 aux_par_f: float = ...,
                 aux_par_0: float = ...,
                 aux_par_1: float = ...,
                 aux_par_2: float = ...,
                 bop_par: float = ...,
                 bop_par_f: float = ...,
                 bop_par_0: float = ...,
                 bop_par_1: float = ...,
                 bop_par_2: float = ...,
                 timestep_load_fractions: Array = ...,
                 f_turb_tou_periods: Array = ...,
                 weekday_schedule: Matrix = ...,
                 weekend_schedule: Matrix = ...,
                 is_tod_pc_target_also_pc_max: float = ...,
                 can_cycle_use_standby: float = ...,
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
                 disp_time_weighting: float = ...,
                 is_write_ampl_dat: float = ...,
                 ampl_data_dir: str = ...,
                 is_ampl_engine: float = ...,
                 ampl_exec_call: str = ...,
                 disp_rsu_cost_rel: float = ...,
                 disp_csu_cost_rel: float = ...,
                 disp_pen_ramping: float = ...,
                 disp_inventory_incentive: float = ...,
                 q_rec_standby: float = ...,
                 q_rec_heattrace: float = ...,
                 is_wlim_design: float = ...,
                 disp_wlim_maxspec: float = ...,
                 is_wlim_series: float = ...,
                 wlim_series: Array = ...,
                 ppa_multiplier_model: float = ...,
                 ppa_soln_mode: float = ...,
                 dispatch_factors_ts: Array = ...,
                 en_electricity_rates: float = ...,
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
                 is_dispatch_series: float = ...,
                 dispatch_series: Array = ...,
                 ppa_price_input: Array = ...,
                 mp_energy_market_revenue: Matrix = ...,
                 tower_fixed_cost: float = ...,
                 tower_exp: float = ...,
                 rec_ref_cost: float = ...,
                 rec_ref_area: float = ...,
                 rec_cost_exp: float = ...,
                 site_spec_cost: float = ...,
                 heliostat_spec_cost: float = ...,
                 plant_spec_cost: float = ...,
                 bop_spec_cost: float = ...,
                 tes_spec_cost: float = ...,
                 land_spec_cost: float = ...,
                 contingency_rate: float = ...,
                 sales_tax_rate: float = ...,
                 sales_tax_frac: float = ...,
                 cost_sf_fixed: float = ...,
                 fossil_spec_cost: float = ...,
                 csp_pt_cost_epc_per_acre: float = ...,
                 csp_pt_cost_epc_percent: float = ...,
                 csp_pt_cost_epc_per_watt: float = ...,
                 csp_pt_cost_epc_fixed: float = ...,
                 csp_pt_cost_plm_percent: float = ...,
                 csp_pt_cost_plm_per_watt: float = ...,
                 csp_pt_cost_plm_fixed: float = ...,
                 csp_pt_sf_fixed_land_area: float = ...,
                 csp_pt_sf_land_overhead_factor: float = ...,
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
                 piping_loss: float = ...,
                 disp_csu_cost: float = ...,
                 disp_rsu_cost: float = ...,
                 disp_pen_delta_w: float = ...,
                 P_boil: float = ...,
                 csp_pt_tes_init_hot_htf_percent: float = ...,
                 adjust_constant: float = ...,
                 adjust_hourly: Array = ...,
                 adjust_timeindex: Array = ...,
                 adjust_periods: Matrix = ...,
                 sf_adjust_constant: float = ...,
                 sf_adjust_hourly: Array = ...,
                 sf_adjust_timeindex: Array = ...,
                 sf_adjust_periods: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
