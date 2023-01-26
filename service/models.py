from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union


class Item(NamedTuple):
    verb: str
    path: str


Items = List[Item]
ItemsTree = Dict[str, Union['ItemsTree', str]]
