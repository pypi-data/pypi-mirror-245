
# This is a generated file

"""utilityrateforecast - Compute the utility rate costs associated with a given rate and time series array of grid usage."""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
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
    'analysis_period': float,
    'steps_per_hour': float,
    'idx': float,
    'load': Array,
    'gen': Array,
    'grid_power': Array,
    'ur_energy_use': Matrix,
    'ur_dc_peaks': Matrix,
    'inflation_rate': float,
    'ur_price_series': Array,
    'ur_total_bill': float
}, total=False)

class Data(ssc.DataDict):
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
    analysis_period: float = INPUT(label='Number of years in escalation and forecast', units='years', type='NUMBER', group='Lifetime', required='*', constraints='INTEGER,POSITIVE')
    steps_per_hour: float = INPUT(label='Steps per hour', units='hr', type='NUMBER', group='Controls', required='*')
    idx: float = INOUT(label='Starting index (lifetime)', type='NUMBER', group='Controls')
    load: Array = INPUT(label='Lifetime load forecast', type='ARRAY', group='Electricity Rates')
    gen: Array = INPUT(label='Lifetime generation forecast', type='ARRAY', group='Electricity Rates')
    grid_power: Array = INPUT(label='Electricity to/from grid', type='ARRAY', group='Electricity Rates')
    ur_energy_use: Matrix = INOUT(label='Energy use or surplus by month and period', type='MATRIX', group='Electricity Rates')
    ur_dc_peaks: Matrix = INOUT(label='Peak demand by month and period', type='MATRIX', group='Electricity Rates')
    inflation_rate: float = INPUT(label='Inflation rate', units='%', type='NUMBER', group='Lifetime', required='*', constraints='MIN=-99')
    ur_price_series: Final[Array] = OUTPUT(label='Estimated cost of each timestep', units='$', type='ARRAY', group='Time Series', required='*')
    ur_total_bill: Final[float] = OUTPUT(label='Total cost for the calculated period', units='$', type='NUMBER', group='Financial Metrics', required='*')

    def __init__(self, *args: Mapping[str, Any],
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
                 analysis_period: float = ...,
                 steps_per_hour: float = ...,
                 idx: float = ...,
                 load: Array = ...,
                 gen: Array = ...,
                 grid_power: Array = ...,
                 ur_energy_use: Matrix = ...,
                 ur_dc_peaks: Matrix = ...,
                 inflation_rate: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
