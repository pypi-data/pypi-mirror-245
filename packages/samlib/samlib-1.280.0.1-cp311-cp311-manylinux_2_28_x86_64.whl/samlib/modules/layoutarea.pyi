
# This is a generated file

"""layoutarea - Layout Area Calculation"""

# VERSION: 0

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'positions': Matrix,
    'convex_hull': Matrix,
    'area': float
}, total=False)

class Data(ssc.DataDict):
    positions: Matrix = INPUT(label='Positions within calculataed area', type='MATRIX', group='layoutarea', required='*')
    convex_hull: Final[Matrix] = OUTPUT(label='Convex hull bounding the region', type='MATRIX', group='layoutarea', required='*')
    area: Final[float] = OUTPUT(label='Area inside the convex hull', type='NUMBER', group='layoutarea', required='*')

    def __init__(self, *args: Mapping[str, Any],
                 positions: Matrix = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
