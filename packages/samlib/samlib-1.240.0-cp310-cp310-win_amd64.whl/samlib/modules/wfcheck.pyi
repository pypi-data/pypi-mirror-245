
# This is a generated file

"""wfcheck - Weather file checker."""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'input_file': str
}, total=False)

class Data(ssc.DataDict):
    input_file: str = INPUT(label='Input weather file name', type='STRING', group='Weather File Checker', required='*', meta='wfcsv format')

    def __init__(self, *args: Mapping[str, Any],
                 input_file: str = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
