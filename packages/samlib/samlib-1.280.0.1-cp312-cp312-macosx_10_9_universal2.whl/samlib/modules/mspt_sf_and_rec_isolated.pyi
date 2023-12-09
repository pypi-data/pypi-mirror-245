
# This is a generated file

"""mspt_sf_and_rec_isolated - MSPT solar field and tower/receiver model"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'sim_type': float,
    'q_dot_rec_des': float,
    'T_htf_cold_des': float,
    'T_htf_hot_des': float,
    'h_tower': float,
    'rec_height': float,
    'D_rec': float,
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
    'piping_loss_coefficient': float,
    'is_rec_model_trans': float,
    'rec_tm_mult': float,
    'riser_tm_mult': float,
    'downc_tm_mult': float,
    'u_riser': float,
    'th_riser': float,
    'is_rec_clearsky_control': float,
    'rec_clearsky_fraction': float,
    'timestep_od': Array,
    'P_amb_od': Array,
    'T_amb_od': Array,
    'deltaT_sky_od': Array,
    'v_wind_10_od': Array,
    'clearsky_to_measured_dni_od': Array,
    'flux_map_od': Matrix,
    'T_htf_cold_in_od': Array,
    'plant_defocus_od': Array,
    'm_dot_rec_des': float,
    'm_dot_rec_od': Array,
    'T_htf_rec_out_od': Array,
    'q_dot_htf_od': Array,
    'eta_rec_od': Array,
    'W_dot_pump_od': Array,
    'rec_component_defocus_od': Array,
    'q_dot_rec_inc_pre_defocus': Array,
    'q_dot_rec_inc': Array,
    'q_dot_rec_rad_loss': Array,
    'q_dot_rec_conv_loss': Array,
    'q_dot_rec_piping_loss': Array
}, total=False)

class Data(ssc.DataDict):
    sim_type: float = INPUT(label='1 (default): timeseries, 2: design only', type='NUMBER', group='Simulation', required='?=1')
    q_dot_rec_des: float = INPUT(label='Receiver thermal power to HTF at design', units='MWt', type='NUMBER', group='Tower and Receiver', required='*')
    T_htf_cold_des: float = INPUT(label='Cold HTF inlet temperature at design conditions', units='C', type='NUMBER', group='Tower and Receiver', required='*')
    T_htf_hot_des: float = INPUT(label='Hot HTF outlet temperature at design conditions', units='C', type='NUMBER', group='Tower and Receiver', required='*')
    h_tower: float = INOUT(label='Tower height', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    rec_height: float = INPUT(label='Receiver height', units='m', type='NUMBER', group='Tower and Receiver', required='*')
    D_rec: float = INPUT(label='The overall outer diameter of the receiver', units='m', type='NUMBER', group='Tower and Receiver', required='*')
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
    piping_loss_coefficient: float = INPUT(label='Thermal loss per meter of piping', units='Wt/m2-K', type='NUMBER', group='Tower and Receiver')
    is_rec_model_trans: float = INPUT(label='Formulate receiver model as transient?', type='NUMBER', group='Tower and Receiver', required='?=0')
    rec_tm_mult: float = INPUT(label='Receiver thermal mass multiplier', type='NUMBER', group='Tower and Receiver', required='is_rec_model_trans=1')
    riser_tm_mult: float = INPUT(label='Riser thermal mass multiplier', type='NUMBER', group='Tower and Receiver', required='is_rec_model_trans=1')
    downc_tm_mult: float = INPUT(label='Downcomer thermal mass multiplier', type='NUMBER', group='Tower and Receiver', required='is_rec_model_trans=1')
    u_riser: float = INPUT(label='Design point HTF velocity in riser', units='m/s', type='NUMBER', group='Tower and Receiver', required='is_rec_model_trans=1')
    th_riser: float = INPUT(label='Riser or downcomer tube wall thickness', units='mm', type='NUMBER', group='Tower and Receiver', required='is_rec_model_trans=1')
    is_rec_clearsky_control: float = INPUT(label='0: use measured dni, 1: use clear-sky control w/ rec_clearsky_frac input', type='NUMBER', group='Tower and Receiver', required='?=0')
    rec_clearsky_fraction: float = INPUT(label='Weighting fraction on clear-sky DNI for receiver flow control', type='NUMBER', group='Receiver control', required='is_rec_clearsky_control=1')
    timestep_od: Array = INPUT(label='Timestep', units='s', type='ARRAY', group='Timeseries', required='sim_type=1')
    P_amb_od: Array = INPUT(label='Ambient pressure', units='mbar', type='ARRAY', group='weather', required='sim_type=1')
    T_amb_od: Array = INPUT(label='Ambient temperature', units='C', type='ARRAY', group='weather', required='sim_type=1')
    deltaT_sky_od: Array = INPUT(label='Difference between ambient and sky temps', units='C', type='ARRAY', group='weather', required='sim_type=1')
    v_wind_10_od: Array = INPUT(label='Wind speed at 10 meters', units='m/s', type='ARRAY', group='weather', required='sim_type=1')
    clearsky_to_measured_dni_od: Array = INPUT(label='Ratio of clearsky to measured DNI', type='ARRAY', group='weather', required='sim_type=1&is_rec_clearsky_control=1')
    flux_map_od: Matrix = INPUT(label='rows: timestep, columns: panels. Flux *after* rec reflectance losses', units='W/m2', type='MATRIX', group='Flux', required='sim_type=1')
    T_htf_cold_in_od: Array = INPUT(label='HTF inlet temperature', units='C', type='ARRAY', group='Receiver control', required='sim_type=1')
    plant_defocus_od: Array = INPUT(label='Plant defocus', type='ARRAY', group='Receiver control', required='sim_type=1')
    m_dot_rec_des: Final[float] = OUTPUT(label='Receiver design mass flow rate', units='kg/s', type='NUMBER', group='Tower and Receiver', required='*')
    m_dot_rec_od: Final[Array] = OUTPUT(label='Receiver mass flow rate', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    T_htf_rec_out_od: Final[Array] = OUTPUT(label='Receiver outlet temperature after piping losses', units='C', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    q_dot_htf_od: Final[Array] = OUTPUT(label='Receiver thermal power to HTF after piping losses', units='MWt', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    eta_rec_od: Final[Array] = OUTPUT(label='Receiver thermal efficiency', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    W_dot_pump_od: Final[Array] = OUTPUT(label='Receiver pumping power', units='MWe', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    rec_component_defocus_od: Final[Array] = OUTPUT(label='Receiver component defocus', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    q_dot_rec_inc_pre_defocus: Final[Array] = OUTPUT(label='Receiver incident flux, pre-defocus, post-reflection', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    q_dot_rec_inc: Final[Array] = OUTPUT(label='Receiver incident flux, post defocus and reflection', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    q_dot_rec_rad_loss: Final[Array] = OUTPUT(label='Receiver radiative losses', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    q_dot_rec_conv_loss: Final[Array] = OUTPUT(label='Receiver convective losses', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')
    q_dot_rec_piping_loss: Final[Array] = OUTPUT(label='Receiver piping thermal losses', units='kg/s', type='ARRAY', group='Tower and Receiver', required='sim_type=1')

    def __init__(self, *args: Mapping[str, Any],
                 sim_type: float = ...,
                 q_dot_rec_des: float = ...,
                 T_htf_cold_des: float = ...,
                 T_htf_hot_des: float = ...,
                 h_tower: float = ...,
                 rec_height: float = ...,
                 D_rec: float = ...,
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
                 piping_loss_coefficient: float = ...,
                 is_rec_model_trans: float = ...,
                 rec_tm_mult: float = ...,
                 riser_tm_mult: float = ...,
                 downc_tm_mult: float = ...,
                 u_riser: float = ...,
                 th_riser: float = ...,
                 is_rec_clearsky_control: float = ...,
                 rec_clearsky_fraction: float = ...,
                 timestep_od: Array = ...,
                 P_amb_od: Array = ...,
                 T_amb_od: Array = ...,
                 deltaT_sky_od: Array = ...,
                 v_wind_10_od: Array = ...,
                 clearsky_to_measured_dni_od: Array = ...,
                 flux_map_od: Matrix = ...,
                 T_htf_cold_in_od: Array = ...,
                 plant_defocus_od: Array = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
