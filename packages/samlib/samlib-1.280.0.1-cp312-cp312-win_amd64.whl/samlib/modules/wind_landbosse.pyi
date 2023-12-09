
# This is a generated file

"""wind_landbosse - Land-based Balance-of-System Systems Engineering (LandBOSSE) cost model"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'en_landbosse': float,
    'wind_resource_filename': str,
    'distance_to_interconnect_mi': float,
    'interconnect_voltage_kV': float,
    'depth': float,
    'rated_thrust_N': float,
    'labor_cost_multiplier': float,
    'gust_velocity_m_per_s': float,
    'wind_resource_shear': float,
    'num_turbines': float,
    'turbine_spacing_rotor_diameters': float,
    'row_spacing_rotor_diameters': float,
    'turbine_rating_MW': float,
    'wind_turbine_hub_ht': float,
    'wind_turbine_rotor_diameter': float,
    'errors': str,
    'bonding_usd': float,
    'collection_equipment_rental_usd': float,
    'collection_labor_usd': float,
    'collection_material_usd': float,
    'collection_mobilization_usd': float,
    'construction_permitting_usd': float,
    'development_labor_usd': float,
    'development_material_usd': float,
    'development_mobilization_usd': float,
    'engineering_usd': float,
    'erection_equipment_rental_usd': float,
    'erection_fuel_usd': float,
    'erection_labor_usd': float,
    'erection_material_usd': float,
    'erection_mobilization_usd': float,
    'erection_other_usd': float,
    'foundation_equipment_rental_usd': float,
    'foundation_labor_usd': float,
    'foundation_material_usd': float,
    'foundation_mobilization_usd': float,
    'insurance_usd': float,
    'markup_contingency_usd': float,
    'project_management_usd': float,
    'site_facility_usd': float,
    'sitepreparation_equipment_rental_usd': float,
    'sitepreparation_labor_usd': float,
    'sitepreparation_material_usd': float,
    'sitepreparation_mobilization_usd': float,
    'total_collection_cost': float,
    'total_development_cost': float,
    'total_erection_cost': float,
    'total_foundation_cost': float,
    'total_gridconnection_cost': float,
    'total_management_cost': float,
    'total_sitepreparation_cost': float,
    'total_substation_cost': float,
    'total_bos_cost': float
}, total=False)

class Data(ssc.DataDict):
    en_landbosse: float = INPUT(label='Enable landbosse (1 for enabled)', type='NUMBER', group='LandBOSSE', required='*')
    wind_resource_filename: str = INPUT(label='Local hourly wind data file path', type='STRING', group='LandBOSSE', required='*')
    distance_to_interconnect_mi: float = INPUT(label='Distance to Interconnect', units='miles', type='NUMBER', group='LandBOSSE', required='*')
    interconnect_voltage_kV: float = INPUT(label='Interconnect Voltage', units='kV', type='NUMBER', group='LandBOSSE', required='*')
    depth: float = INPUT(label='Foundation Depth', units='m', type='NUMBER', group='LandBOSSE', required='*')
    rated_thrust_N: float = INPUT(label='Rated Thrust', units='N', type='NUMBER', group='LandBOSSE', required='*')
    labor_cost_multiplier: float = INPUT(label='Labor Cost Multiplier', type='NUMBER', group='LandBOSSE', required='*')
    gust_velocity_m_per_s: float = INPUT(label='50 year Gust Velocity', units='m/s', type='NUMBER', group='LandBOSSE', required='*')
    wind_resource_shear: float = INPUT(label='Wind Shear Exponent', type='NUMBER', group='LandBOSSE', required='*')
    num_turbines: float = INPUT(label='Number of Turbines', type='NUMBER', group='LandBOSSE', required='*', constraints='INTEGER,')
    turbine_spacing_rotor_diameters: float = INPUT(label='Turbine Spacing', units='diameters', type='NUMBER', group='LandBOSSE', required='*')
    row_spacing_rotor_diameters: float = INPUT(label='Row Spacing', units='diameters', type='NUMBER', group='LandBOSSE', required='*')
    turbine_rating_MW: float = INPUT(label='Turbine Rating', units='kW', type='NUMBER', group='LandBOSSE', required='*')
    wind_turbine_hub_ht: float = INPUT(label='Hub Height', units='m', type='NUMBER', group='LandBOSSE', required='*')
    wind_turbine_rotor_diameter: float = INPUT(label='Rotor Diameter', units='m', type='NUMBER', group='LandBOSSE', required='*')
    errors: Final[str] = OUTPUT(label='BOS - Error message', type='STRING', group='LandBOSSE', required='en_landbosse=1')
    bonding_usd: Final[float] = OUTPUT(label='BOS - Management - Bonding Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    collection_equipment_rental_usd: Final[float] = OUTPUT(label='BOS - Collection - Equipment Rental Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    collection_labor_usd: Final[float] = OUTPUT(label='BOS - Collection - Labor Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    collection_material_usd: Final[float] = OUTPUT(label='BOS - Collection - Materials Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    collection_mobilization_usd: Final[float] = OUTPUT(label='BOS - Collection - Mobilization Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    construction_permitting_usd: Final[float] = OUTPUT(label='BOS - Management - Construction Permitting Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    development_labor_usd: Final[float] = OUTPUT(label='BOS - Development - Labor Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    development_material_usd: Final[float] = OUTPUT(label='BOS - Development - Material Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    development_mobilization_usd: Final[float] = OUTPUT(label='BOS - Development - Mobilization Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    engineering_usd: Final[float] = OUTPUT(label='BOS - Management - Engineering Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    erection_equipment_rental_usd: Final[float] = OUTPUT(label='BOS - Erection - Equipment Rental Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    erection_fuel_usd: Final[float] = OUTPUT(label='BOS - Erection - Fuel Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    erection_labor_usd: Final[float] = OUTPUT(label='BOS - Erection - Labor Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    erection_material_usd: Final[float] = OUTPUT(label='BOS - Erection - Material Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    erection_mobilization_usd: Final[float] = OUTPUT(label='BOS - Erection - Mobilization Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    erection_other_usd: Final[float] = OUTPUT(label='BOS - Erection - Other Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    foundation_equipment_rental_usd: Final[float] = OUTPUT(label='BOS - Foundation - Equipment Rental Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    foundation_labor_usd: Final[float] = OUTPUT(label='BOS - Foundation - Labor Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    foundation_material_usd: Final[float] = OUTPUT(label='BOS - Foundation - Material Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    foundation_mobilization_usd: Final[float] = OUTPUT(label='BOS - Foundation - Mobilization Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    insurance_usd: Final[float] = OUTPUT(label='BOS - Management - Insurance Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    markup_contingency_usd: Final[float] = OUTPUT(label='BOS - Management - Markup Contingency', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    project_management_usd: Final[float] = OUTPUT(label='BOS - Management - Project Management Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    site_facility_usd: Final[float] = OUTPUT(label='BOS - Management - Site Facility Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    sitepreparation_equipment_rental_usd: Final[float] = OUTPUT(label='BOS - Site Preparation - Equipment Rental Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    sitepreparation_labor_usd: Final[float] = OUTPUT(label='BOS - Site Preparation - Labor Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    sitepreparation_material_usd: Final[float] = OUTPUT(label='BOS - Site Preparation - Material Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    sitepreparation_mobilization_usd: Final[float] = OUTPUT(label='BOS - Site Preparation - Mobilization Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_collection_cost: Final[float] = OUTPUT(label='BOS - Total Collection Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_development_cost: Final[float] = OUTPUT(label='BOS - Total Development Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_erection_cost: Final[float] = OUTPUT(label='BOS - Total Erection Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_foundation_cost: Final[float] = OUTPUT(label='BOS - Total Foundation Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_gridconnection_cost: Final[float] = OUTPUT(label='BOS - Total Grid Connection Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_management_cost: Final[float] = OUTPUT(label='BOS - Total Management Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_sitepreparation_cost: Final[float] = OUTPUT(label='BOS - Total Site Preparation Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_substation_cost: Final[float] = OUTPUT(label='BOS - Total Substation Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')
    total_bos_cost: Final[float] = OUTPUT(label='BOS - Total BOS Cost', units='$', type='NUMBER', group='LandBOSSE', required='en_landbosse=1')

    def __init__(self, *args: Mapping[str, Any],
                 en_landbosse: float = ...,
                 wind_resource_filename: str = ...,
                 distance_to_interconnect_mi: float = ...,
                 interconnect_voltage_kV: float = ...,
                 depth: float = ...,
                 rated_thrust_N: float = ...,
                 labor_cost_multiplier: float = ...,
                 gust_velocity_m_per_s: float = ...,
                 wind_resource_shear: float = ...,
                 num_turbines: float = ...,
                 turbine_spacing_rotor_diameters: float = ...,
                 row_spacing_rotor_diameters: float = ...,
                 turbine_rating_MW: float = ...,
                 wind_turbine_hub_ht: float = ...,
                 wind_turbine_rotor_diameter: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
