
# This is a generated file

"""wave_file_reader - SAM Wave Resource File Reader"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'wave_resource_model_choice': float,
    'wave_resource_filename': str,
    'wave_resource_filename_ts': str,
    'use_specific_wf_wave': float,
    'name': str,
    'city': str,
    'state': str,
    'country': str,
    'lat': float,
    'lon': float,
    'nearby_buoy_number': str,
    'average_power_flux': float,
    'bathymetry': str,
    'sea_bed': str,
    'tz': float,
    'data_source': str,
    'notes': str,
    'location_id': float,
    'distance_to_shore_file': float,
    'water_depth_file': float,
    'year': Array,
    'month': Array,
    'day': Array,
    'hour': Array,
    'minute': Array,
    'wave_resource_matrix': Matrix,
    'significant_wave_height': Array,
    'number_records': float,
    'number_hours': float,
    'energy_period': Array
}, total=False)

class Data(ssc.DataDict):
    wave_resource_model_choice: float = INPUT(label='Joint PDF or 3-hour wave resource data', units='0/1', type='NUMBER', group='Weather Reader', required='?=1', constraints='INTEGER')
    wave_resource_filename: str = INPUT(label='File path with Wave Height x Period Distribution as 2-D PDF', type='STRING', group='Weather Reader', required='wave_resource_model_choice=0', constraints='LOCAL_FILE')
    wave_resource_filename_ts: str = INPUT(label='File path with 3-hour Wave Height and Period data as Time Series array', type='STRING', group='Weather Reader', required='wave_resource_model_choice=1', constraints='LOCAL_FILE')
    use_specific_wf_wave: float = INPUT(label='user specified file', units='0/1', type='NUMBER', group='Weather Reader', required='?=0', constraints='INTEGER,MIN=0,MAX=1')
    name: Final[str] = OUTPUT(label='Name', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    city: Final[str] = OUTPUT(label='City', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    state: Final[str] = OUTPUT(label='State', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    country: Final[str] = OUTPUT(label='Country', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    lat: Final[float] = OUTPUT(label='Latitude', units='deg', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0')
    lon: Final[float] = OUTPUT(label='Longitude', units='deg', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0')
    nearby_buoy_number: Final[str] = OUTPUT(label='Nearby buoy number', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    average_power_flux: Final[float] = OUTPUT(label='Average power flux', units='kW/m', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    bathymetry: Final[str] = OUTPUT(label='Bathymetry', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    sea_bed: Final[str] = OUTPUT(label='Sea bed', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=0')
    tz: Final[float] = OUTPUT(label='Time zone', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0')
    data_source: Final[str] = OUTPUT(label='Data source', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0')
    notes: Final[str] = OUTPUT(label='Notes', type='STRING', group='Weather Reader', required='use_specific_wf_wave=0')
    location_id: Final[float] = OUTPUT(label='Location ID', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=1')
    distance_to_shore_file: Final[float] = OUTPUT(label='Distance to shore', units='m', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=1')
    water_depth_file: Final[float] = OUTPUT(label='Water depth', units='m', type='NUMBER', group='Weather Reader', required='use_specific_wf_wave=0&wave_resource_model_choice=1')
    year: Final[Array] = OUTPUT(label='Year', units='yr', type='ARRAY', group='Weather Reader', required='wave_resource_model_choice=1')
    month: Final[Array] = OUTPUT(label='Month', units='mn', type='ARRAY', group='Weather Reader', required='wave_resource_model_choice=1', meta='1-12')
    day: Final[Array] = OUTPUT(label='Day', units='dy', type='ARRAY', group='Weather Reader', required='wave_resource_model_choice=1', meta='1-365')
    hour: Final[Array] = OUTPUT(label='Hour', units='hr', type='ARRAY', group='Weather Reader', required='wave_resource_model_choice=1', meta='0-23')
    minute: Final[Array] = OUTPUT(label='Minute', units='min', type='ARRAY', group='Weather Reader', required='wave_resource_model_choice=1', meta='0-59')
    wave_resource_matrix: Final[Matrix] = OUTPUT(label='Frequency distribution of resource', units='m/s', type='MATRIX', group='Weather Reader', required='*')
    significant_wave_height: Final[Array] = OUTPUT(label='Wave height time series data', units='m', type='ARRAY', group='Weather Reader', required='?')
    number_records: Final[float] = OUTPUT(label='Number of records in wave time series', type='NUMBER', group='Weather Reader', required='?')
    number_hours: Final[float] = OUTPUT(label='Number of hours in wave time series', type='NUMBER', group='Weather Reader', required='?')
    energy_period: Final[Array] = OUTPUT(label='Wave period time series data', units='s', type='ARRAY', group='Weather Reader', required='?')

    def __init__(self, *args: Mapping[str, Any],
                 wave_resource_model_choice: float = ...,
                 wave_resource_filename: str = ...,
                 wave_resource_filename_ts: str = ...,
                 use_specific_wf_wave: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
