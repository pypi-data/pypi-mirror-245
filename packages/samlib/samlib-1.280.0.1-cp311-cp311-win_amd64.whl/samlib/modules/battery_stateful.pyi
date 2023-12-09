
# This is a generated file

"""battery_stateful - Battery management system model with state"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'control_mode': float,
    'dt_hr': float,
    'input_current': float,
    'input_power': float,
    'chem': float,
    'nominal_energy': float,
    'nominal_voltage': float,
    'initial_SOC': float,
    'minimum_SOC': float,
    'maximum_SOC': float,
    'leadacid_q20': float,
    'leadacid_q10': float,
    'leadacid_qn': float,
    'leadacid_tn': float,
    'voltage_choice': float,
    'voltage_matrix': Matrix,
    'Vnom_default': float,
    'resistance': float,
    'Qfull': float,
    'Qexp': float,
    'Qnom': float,
    'Vfull': float,
    'Vexp': float,
    'Vnom': float,
    'Vcut': float,
    'C_rate': float,
    'Qfull_flow': float,
    'life_model': float,
    'cycling_matrix': Matrix,
    'calendar_choice': float,
    'calendar_matrix': Matrix,
    'calendar_q0': float,
    'calendar_a': float,
    'calendar_b': float,
    'calendar_c': float,
    'mass': float,
    'surface_area': float,
    'Cp': float,
    'h': float,
    'T_room_init': float,
    'cap_vs_temp': Matrix,
    'loss_choice': float,
    'monthly_charge_loss': Array,
    'monthly_discharge_loss': Array,
    'monthly_idle_loss': Array,
    'schedule_loss': Array,
    'replacement_option': float,
    'replacement_capacity': float,
    'replacement_schedule_percent': Array,
    'last_idx': float,
    'V': float,
    'P': float,
    'Q': float,
    'Q_max': float,
    'I': float,
    'I_dischargeable': float,
    'I_chargeable': float,
    'P_dischargeable': float,
    'P_chargeable': float,
    'SOC': float,
    'q0': float,
    'qmax_lifetime': float,
    'qmax_thermal': float,
    'cell_current': float,
    'I_loss': float,
    'charge_mode': float,
    'SOC_prev': float,
    'prev_charge': float,
    'chargeChange': float,
    'q1_0': float,
    'q2_0': float,
    'qn': float,
    'q2': float,
    'cell_voltage': float,
    'q_relative_thermal': float,
    'T_batt': float,
    'T_room': float,
    'heat_dissipated': float,
    'T_batt_prev': float,
    'q_relative': float,
    'q_relative_cycle': float,
    'n_cycles': float,
    'cycle_range': float,
    'cycle_DOD': float,
    'cycle_counts': Matrix,
    'average_range': float,
    'rainflow_Xlt': float,
    'rainflow_Ylt': float,
    'rainflow_jlt': float,
    'rainflow_peaks': Array,
    'q_relative_calendar': float,
    'day_age_of_battery': float,
    'dq_relative_calendar_old': float,
    'DOD_max': float,
    'DOD_min': float,
    'cycle_DOD_max': Array,
    'cum_dt': float,
    'q_relative_li': float,
    'q_relative_neg': float,
    'dq_relative_li1': float,
    'dq_relative_li2': float,
    'dq_relative_li3': float,
    'dq_relative_neg': float,
    'b1_dt': float,
    'b2_dt': float,
    'b3_dt': float,
    'c0_dt': float,
    'c2_dt': float,
    'temp_dt': float,
    'dq_relative_cal': float,
    'dq_relative_cyc': float,
    'EFC': float,
    'EFC_dt': float,
    'temp_avg': float,
    'loss_kw': float,
    'n_replacements': float,
    'indices_replaced': Array
}, total=False)

class Data(ssc.DataDict):
    control_mode: float = INPUT(label='Control using current (0) or power (1)', units='0/1', type='NUMBER', group='Controls', required='*')
    dt_hr: float = INPUT(label='Time step in hours', units='hr', type='NUMBER', group='Controls', required='*')
    input_current: float = INPUT(label='Current at which to run battery', units='A', type='NUMBER', group='Controls', required='control_mode=0')
    input_power: float = INPUT(label='Power at which to run battery', units='kW', type='NUMBER', group='Controls', required='control_mode=1')
    chem: float = INPUT(label='Lead Acid (0), Li Ion (1), Vanadium Redox (2), Iron Flow (3)', units='0/1/2/3', type='NUMBER', group='ParamsCell', required='*')
    nominal_energy: float = INOUT(label='Nominal installed energy', units='kWh', type='NUMBER', group='ParamsPack', required='*')
    nominal_voltage: float = INOUT(label='Nominal DC voltage', units='V', type='NUMBER', group='ParamsPack', required='*')
    initial_SOC: float = INPUT(label='Initial state-of-charge', units='%', type='NUMBER', group='ParamsCell', required='*')
    minimum_SOC: float = INPUT(label='Minimum allowed state-of-charge', units='%', type='NUMBER', group='ParamsCell', required='*')
    maximum_SOC: float = INPUT(label='Maximum allowed state-of-charge', units='%', type='NUMBER', group='ParamsCell', required='*')
    leadacid_q20: float = INPUT(label='Capacity at 20-hour discharge rate', units='Ah', type='NUMBER', group='ParamsCell', required='chem=0')
    leadacid_q10: float = INPUT(label='Capacity at 10-hour discharge rate', units='Ah', type='NUMBER', group='ParamsCell', required='chem=0')
    leadacid_qn: float = INPUT(label='Capacity at discharge rate for n-hour rate', units='Ah', type='NUMBER', group='ParamsCell', required='chem=0')
    leadacid_tn: float = INPUT(label='Hours to discharge for qn rate', units='h', type='NUMBER', group='ParamsCell', required='chem=0')
    voltage_choice: float = INPUT(label='Battery voltage input option', units='0/1', type='NUMBER', group='ParamsCell', required='?=0', meta='0=Model,1=Table')
    voltage_matrix: Matrix = INPUT(label='Table with depth-of-discharge % and Voltage as columns', units='[[%, V]]', type='MATRIX', group='ParamsCell', required='voltage_choice=1')
    Vnom_default: float = INPUT(label='Default nominal cell voltage', units='V', type='NUMBER', group='ParamsCell', required='*')
    resistance: float = INPUT(label='Internal resistance', units='Ohm', type='NUMBER', group='ParamsCell', required='*')
    Qfull: float = INPUT(label='Fully charged cell capacity', units='Ah', type='NUMBER', group='ParamsCell', required='*')
    Qexp: float = INPUT(label='Cell capacity at end of exponential zone', units='Ah', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    Qnom: float = INPUT(label='Cell capacity at end of nominal zone', units='Ah', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    Vfull: float = INPUT(label='Fully charged cell voltage', units='V', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    Vexp: float = INPUT(label='Cell voltage at end of exponential zone', units='V', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    Vnom: float = INPUT(label='Cell voltage at end of nominal zone', units='V', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    Vcut: float = INPUT(label='Cell cutoff voltage', units='V', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    C_rate: float = INPUT(label='Rate at which voltage vs. capacity curve input', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem~2')
    Qfull_flow: float = INPUT(label='Fully charged flow battery capacity', units='Ah', type='NUMBER', group='ParamsCell', required='voltage_choice=0&chem=3')
    life_model: float = INPUT(label='Battery life model specifier', units='0/1/2', type='NUMBER', group='ParamsCell', required='*', meta='0=calendar/cycle,1=NMC,2=LMO/LTO')
    cycling_matrix: Matrix = INPUT(label='Table with DOD %, Cycle #, and Capacity % columns', units='[[%, #, %]]', type='MATRIX', group='ParamsCell', required='life_model=0')
    calendar_choice: float = INPUT(label='Calendar life degradation input option', units='0/1/2', type='NUMBER', group='ParamsCell', required='life_model=0', meta='0=None,1=LithiumIonModel,2=InputLossTable')
    calendar_matrix: Matrix = INPUT(label='Table with Day # and Capacity % columns', units='[[#, %]]', type='MATRIX', group='ParamsCell', required='life_model=0&calendar_choice=2')
    calendar_q0: float = INPUT(label='Calendar life model initial capacity cofficient', type='NUMBER', group='ParamsCell', required='life_model=0&calendar_choice=1')
    calendar_a: float = INPUT(label='Calendar life model coefficient', units='1/sqrt(day)', type='NUMBER', group='ParamsCell', required='life_model=0&calendar_choice=1')
    calendar_b: float = INPUT(label='Calendar life model coefficient', units='K', type='NUMBER', group='ParamsCell', required='life_model=0&calendar_choice=1')
    calendar_c: float = INPUT(label='Calendar life model coefficient', units='K', type='NUMBER', group='ParamsCell', required='life_model=0&calendar_choice=1')
    mass: float = INPUT(label='Battery mass', units='kg', type='NUMBER', group='ParamsPack', required='*')
    surface_area: float = INPUT(label='Battery surface area', units='m^2', type='NUMBER', group='ParamsPack', required='*')
    Cp: float = INPUT(label='Battery specific heat capacity', units='J/KgK', type='NUMBER', group='ParamsPack', required='*')
    h: float = INPUT(label='Heat transfer between battery and environment', units='W/m2K', type='NUMBER', group='ParamsPack', required='*')
    T_room_init: float = INPUT(label='Temperature of storage room', units='C', type='NUMBER', group='ParamsPack', required='*')
    cap_vs_temp: Matrix = INPUT(label='Table with Temperature and Capacity % as columns', units='[[C,%]]', type='MATRIX', group='ParamsPack', required='life_model=0')
    loss_choice: float = INPUT(label='Loss power input option', units='0/1', type='NUMBER', group='ParamsPack', required='?=0', meta='0=Monthly,1=TimeSeries')
    monthly_charge_loss: Array = INPUT(label='Battery system losses when charging', units='[kW]', type='ARRAY', group='ParamsPack', required='?=0')
    monthly_discharge_loss: Array = INPUT(label='Battery system losses when discharging', units='[kW]', type='ARRAY', group='ParamsPack', required='?=0')
    monthly_idle_loss: Array = INPUT(label='Battery system losses when idle', units='[kW]', type='ARRAY', group='ParamsPack', required='?=0')
    schedule_loss: Array = INPUT(label='Battery system losses at each timestep', units='[kW]', type='ARRAY', group='ParamsPack', required='?=0')
    replacement_option: float = INPUT(label='Replacements: none (0), by capacity (1), or schedule (2)', units='0=none,1=capacity limit,2=yearly schedule', type='NUMBER', group='ParamsPack', required='?=0', constraints='INTEGER,MIN=0,MAX=2')
    replacement_capacity: float = INPUT(label='Capacity degradation at which to replace battery', units='%', type='NUMBER', group='ParamsPack', required='replacement_option=1')
    replacement_schedule_percent: Array = INPUT(label='Percentage of battery capacity to replace in each year', units='[%/year]', type='ARRAY', group='ParamsPack', required='replacement_option=2', meta='length <= analysis_period')
    last_idx: float = INOUT(label='Last index (lifetime)', type='NUMBER', group='StatePack')
    V: float = INOUT(label='Voltage', units='V', type='NUMBER', group='StatePack')
    P: float = INOUT(label='Power', units='kW', type='NUMBER', group='StatePack')
    Q: float = INOUT(label='Capacity', units='Ah', type='NUMBER', group='StatePack')
    Q_max: float = INOUT(label='Max Capacity', units='Ah', type='NUMBER', group='StatePack')
    I: float = INOUT(label='Current', units='A', type='NUMBER', group='StatePack')
    I_dischargeable: float = INOUT(label='Estimated max dischargeable current', units='A', type='NUMBER', group='StatePack')
    I_chargeable: float = INOUT(label='Estimated max chargeable current', units='A', type='NUMBER', group='StatePack')
    P_dischargeable: float = INOUT(label='Estimated max dischargeable power', units='kW', type='NUMBER', group='StatePack')
    P_chargeable: float = INOUT(label='Estimated max chargeable power ', units='kW', type='NUMBER', group='StatePack')
    SOC: float = INOUT(label='State of Charge', units='%', type='NUMBER', group='StatePack')
    q0: float = INOUT(label='Cell capacity at timestep', units='Ah', type='NUMBER', group='StateCell')
    qmax_lifetime: float = INOUT(label='Maximum possible cell capacity', units='Ah', type='NUMBER', group='StateCell')
    qmax_thermal: float = INOUT(label='Maximum cell capacity adjusted for temperature effects', units='Ah', type='NUMBER', group='StateCell')
    cell_current: float = INOUT(label='Cell current', units='A', type='NUMBER', group='StateCell')
    I_loss: float = INOUT(label='Lifetime and thermal losses', units='A', type='NUMBER', group='StateCell')
    charge_mode: float = INOUT(label='Charge (0), Idle (1), Discharge (2)', units='0/1/2', type='NUMBER', group='StateCell')
    SOC_prev: float = INOUT(label='State of Charge of last time step', units='%', type='NUMBER', group='StateCell')
    prev_charge: float = INOUT(label='Charge mode of last time step', units='0/1/2', type='NUMBER', group='StateCell')
    chargeChange: float = INOUT(label='Whether Charge mode changed since last step', units='0/1', type='NUMBER', group='StateCell')
    q1_0: float = INOUT(label='Lead acid - Cell charge available', units='Ah', type='NUMBER', group='StateCell')
    q2_0: float = INOUT(label='Lead acid - Cell charge bound', units='Ah', type='NUMBER', group='StateCell')
    qn: float = INOUT(label='Lead acid - Cell capacity at n-hr discharge rate', units='Ah', type='NUMBER', group='StateCell')
    q2: float = INOUT(label='Lead acid - Cell capacity at 10-hr discharge rate', units='Ah', type='NUMBER', group='StateCell')
    cell_voltage: float = INOUT(label='Cell voltage', units='V', type='NUMBER', group='StateCell')
    q_relative_thermal: float = INOUT(label='Relative capacity due to thermal effects', units='%', type='NUMBER', group='StateCell')
    T_batt: float = INOUT(label='Battery temperature averaged over time step', units='C', type='NUMBER', group='StatePack')
    T_room: float = INOUT(label='Room temperature', units='C', type='NUMBER', group='StatePack')
    heat_dissipated: float = INOUT(label='Heat dissipated due to flux', units='kW', type='NUMBER', group='StatePack')
    T_batt_prev: float = INOUT(label='Battery temperature at end of last time step', units='C', type='NUMBER', group='StateCell')
    q_relative: float = INOUT(label='Overall relative capacity due to lifetime effects', units='%', type='NUMBER', group='StateCell')
    q_relative_cycle: float = INOUT(label='Relative capacity due to cycling effects', units='%', type='NUMBER', group='StateCell')
    n_cycles: float = INOUT(label='Number of cycles', type='NUMBER', group='StateCell')
    cycle_range: float = INOUT(label='Range of last cycle', units='%', type='NUMBER', group='StateCell')
    cycle_DOD: float = INOUT(label='cycle_DOD of last cycle', units='%', type='NUMBER', group='StateCell')
    cycle_counts: Matrix = INOUT(label='Counts of cycles by DOD', units='[%, cycles]', type='MATRIX', group='StateCell', meta='If life_model=0, counts all cycles in simulation; else, cycles per day')
    average_range: float = INOUT(label='Average cycle cycle_range', units='%', type='NUMBER', group='StateCell')
    rainflow_Xlt: float = INOUT(label='Rainflow cycle_range of second to last half cycle', units='%', type='NUMBER', group='StateCell')
    rainflow_Ylt: float = INOUT(label='Rainflow cycle_range of last half cycle', units='%', type='NUMBER', group='StateCell')
    rainflow_jlt: float = INOUT(label='Rainflow number of turning points', type='NUMBER', group='StateCell')
    rainflow_peaks: Array = INOUT(label='Rainflow peaks of cycle_DOD', units='[%]', type='ARRAY', group='StateCell')
    q_relative_calendar: float = INOUT(label='Relative capacity due to calendar effects', units='%', type='NUMBER', group='StateCell')
    day_age_of_battery: float = INOUT(label='Day age of battery', units='day', type='NUMBER', group='StateCell')
    dq_relative_calendar_old: float = INOUT(label='Change in capacity of last time step', units='%', type='NUMBER', group='StateCell')
    DOD_max: float = INOUT(label='Max DOD of battery for current day', units='%', type='NUMBER', group='StateCell', meta='Cycles for Life Model')
    DOD_min: float = INOUT(label='Min DOD of battery for current day', units='%', type='NUMBER', group='StateCell', meta='Cycles for Life Model')
    cycle_DOD_max: Array = INOUT(label='Max DODs of cycles concluded in current day', units='%', type='ARRAY', group='StateCell', meta='Cycles for Life Model')
    cum_dt: float = INOUT(label='Elapsed time for current day', units='day', type='NUMBER', group='StateCell', meta='Cycles for Life Model')
    q_relative_li: float = INOUT(label='Relative capacity due to loss of lithium inventory', units='%', type='NUMBER', group='StateCell', meta='NMC Life Model')
    q_relative_neg: float = INOUT(label='Relative capacity due to loss of anode material', units='%', type='NUMBER', group='StateCell', meta='NMC Life Model')
    dq_relative_li1: float = INOUT(label='Cumulative capacity change from time-dependent Li loss', units='1', type='NUMBER', group='StateCell', meta='NMC Life Model')
    dq_relative_li2: float = INOUT(label='Cumulative capacity change from cycle-dependent Li loss', units='1', type='NUMBER', group='StateCell', meta='NMC Life Model')
    dq_relative_li3: float = INOUT(label='Cumulative capacity change from BOL Li loss', units='1', type='NUMBER', group='StateCell', meta='NMC Life Model')
    dq_relative_neg: float = INOUT(label='Cumulative capacity change from negative electrode', units='1', type='NUMBER', group='StateCell', meta='NMC Life Model')
    b1_dt: float = INOUT(label='b1 coefficient cumulated for current day', units='day^-0.5', type='NUMBER', group='StateCell', meta='NMC Life Model')
    b2_dt: float = INOUT(label='b2 coefficient cumulated for current day', units='1/cycle', type='NUMBER', group='StateCell', meta='NMC Life Model')
    b3_dt: float = INOUT(label='b3 coefficient cumulated for current day', units='1', type='NUMBER', group='StateCell', meta='NMC Life Model')
    c0_dt: float = INOUT(label='c0 coefficient cumulated for current day', units='Ah', type='NUMBER', group='StateCell', meta='NMC Life Model')
    c2_dt: float = INOUT(label='c2 coefficient cumulated for current day', units='1/cycle', type='NUMBER', group='StateCell', meta='NMC Life Model')
    temp_dt: float = INOUT(label='Temperature cumulated for current day', units='K', type='NUMBER', group='StateCell', meta='NMC Life Model')
    dq_relative_cal: float = INOUT(label='Cumulative capacity change from calendar degradation', units='%', type='NUMBER', group='StateCell', meta='LMO/LTO Life Model')
    dq_relative_cyc: float = INOUT(label='Cumulative capacity change from cycling degradation', units='%', type='NUMBER', group='StateCell', meta='LMO/LTO Life Model')
    EFC: float = INOUT(label='Total Equivalent Full Cycles', units='1', type='NUMBER', group='StateCell', meta='LMO/LTO Life Model')
    EFC_dt: float = INOUT(label='Equivalent Full Cycles cumulated for current day', units='1', type='NUMBER', group='StateCell', meta='LMO/LTO Life Model')
    temp_avg: float = INOUT(label='Average temperature for current day', units='K', type='NUMBER', group='StateCell', meta='LMO/LTO Life Model')
    loss_kw: float = INOUT(label='Ancillary power loss (kW DC for DC connected, AC for AC connected)', units='kW', type='NUMBER', group='StatePack')
    n_replacements: float = INOUT(label='Number of replacements at current year', type='NUMBER', group='StatePack')
    indices_replaced: Array = INOUT(label='Lifetime indices of replacement occurrences', type='ARRAY', group='StatePack')

    def __init__(self, *args: Mapping[str, Any],
                 control_mode: float = ...,
                 dt_hr: float = ...,
                 input_current: float = ...,
                 input_power: float = ...,
                 chem: float = ...,
                 nominal_energy: float = ...,
                 nominal_voltage: float = ...,
                 initial_SOC: float = ...,
                 minimum_SOC: float = ...,
                 maximum_SOC: float = ...,
                 leadacid_q20: float = ...,
                 leadacid_q10: float = ...,
                 leadacid_qn: float = ...,
                 leadacid_tn: float = ...,
                 voltage_choice: float = ...,
                 voltage_matrix: Matrix = ...,
                 Vnom_default: float = ...,
                 resistance: float = ...,
                 Qfull: float = ...,
                 Qexp: float = ...,
                 Qnom: float = ...,
                 Vfull: float = ...,
                 Vexp: float = ...,
                 Vnom: float = ...,
                 Vcut: float = ...,
                 C_rate: float = ...,
                 Qfull_flow: float = ...,
                 life_model: float = ...,
                 cycling_matrix: Matrix = ...,
                 calendar_choice: float = ...,
                 calendar_matrix: Matrix = ...,
                 calendar_q0: float = ...,
                 calendar_a: float = ...,
                 calendar_b: float = ...,
                 calendar_c: float = ...,
                 mass: float = ...,
                 surface_area: float = ...,
                 Cp: float = ...,
                 h: float = ...,
                 T_room_init: float = ...,
                 cap_vs_temp: Matrix = ...,
                 loss_choice: float = ...,
                 monthly_charge_loss: Array = ...,
                 monthly_discharge_loss: Array = ...,
                 monthly_idle_loss: Array = ...,
                 schedule_loss: Array = ...,
                 replacement_option: float = ...,
                 replacement_capacity: float = ...,
                 replacement_schedule_percent: Array = ...,
                 last_idx: float = ...,
                 V: float = ...,
                 P: float = ...,
                 Q: float = ...,
                 Q_max: float = ...,
                 I: float = ...,
                 I_dischargeable: float = ...,
                 I_chargeable: float = ...,
                 P_dischargeable: float = ...,
                 P_chargeable: float = ...,
                 SOC: float = ...,
                 q0: float = ...,
                 qmax_lifetime: float = ...,
                 qmax_thermal: float = ...,
                 cell_current: float = ...,
                 I_loss: float = ...,
                 charge_mode: float = ...,
                 SOC_prev: float = ...,
                 prev_charge: float = ...,
                 chargeChange: float = ...,
                 q1_0: float = ...,
                 q2_0: float = ...,
                 qn: float = ...,
                 q2: float = ...,
                 cell_voltage: float = ...,
                 q_relative_thermal: float = ...,
                 T_batt: float = ...,
                 T_room: float = ...,
                 heat_dissipated: float = ...,
                 T_batt_prev: float = ...,
                 q_relative: float = ...,
                 q_relative_cycle: float = ...,
                 n_cycles: float = ...,
                 cycle_range: float = ...,
                 cycle_DOD: float = ...,
                 cycle_counts: Matrix = ...,
                 average_range: float = ...,
                 rainflow_Xlt: float = ...,
                 rainflow_Ylt: float = ...,
                 rainflow_jlt: float = ...,
                 rainflow_peaks: Array = ...,
                 q_relative_calendar: float = ...,
                 day_age_of_battery: float = ...,
                 dq_relative_calendar_old: float = ...,
                 DOD_max: float = ...,
                 DOD_min: float = ...,
                 cycle_DOD_max: Array = ...,
                 cum_dt: float = ...,
                 q_relative_li: float = ...,
                 q_relative_neg: float = ...,
                 dq_relative_li1: float = ...,
                 dq_relative_li2: float = ...,
                 dq_relative_li3: float = ...,
                 dq_relative_neg: float = ...,
                 b1_dt: float = ...,
                 b2_dt: float = ...,
                 b3_dt: float = ...,
                 c0_dt: float = ...,
                 c2_dt: float = ...,
                 temp_dt: float = ...,
                 dq_relative_cal: float = ...,
                 dq_relative_cyc: float = ...,
                 EFC: float = ...,
                 EFC_dt: float = ...,
                 temp_avg: float = ...,
                 loss_kw: float = ...,
                 n_replacements: float = ...,
                 indices_replaced: Array = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
