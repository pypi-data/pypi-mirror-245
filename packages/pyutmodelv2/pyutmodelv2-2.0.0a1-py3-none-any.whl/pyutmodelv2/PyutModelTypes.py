
from typing import List
from typing import NewType

from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutMethod import PyutMethod

ClassName    = NewType('ClassName', str)
Implementors = NewType('Implementors', List[ClassName])
