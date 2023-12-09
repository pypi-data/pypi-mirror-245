
# This is a generated file

"""test_ud_power_cycle - Test user-defined power cylce model"""

# VERSION: 0

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'q_pb_design': float,
    'udpc_table_out': Matrix
}, total=False)

class Data(ssc.DataDict):
    q_pb_design: float = INPUT(label='Design point power block thermal power', units='MWt', type='NUMBER')
    udpc_table_out: Final[Matrix] = OUTPUT(label='udpc table defined in cmod', type='MATRIX')

    def __init__(self, *args: Mapping[str, Any],
                 q_pb_design: float = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
