
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field
from pyutmodelv2.PyutModelTypes import ClassName
from pyutmodelv2.PyutModelTypes import Implementors

from pyutmodelv2.PyutClassCommon import PyutClassCommon
from pyutmodelv2.PyutObject import PyutObject


def implementorsFactory() -> Implementors:
    return Implementors([])


@dataclass
class PyutInterface(PyutClassCommon, PyutObject):

    implementors: Implementors = field(default_factory=implementorsFactory)

    def __init__(self, name: str = ''):
        """

        Args:
            name:  The interface name
        """
        PyutObject.__init__(self, name=name)
        PyutClassCommon.__init__(self)

        self.logger: Logger = getLogger(__name__)

        self._implementors: Implementors = Implementors([])

    def addImplementor(self, newClassName: ClassName):
        self._implementors.append(newClassName)

    def __repr__(self):

        methodsStr = ''
        for method in self.methods:
            methodsStr = f'{methodsStr} {method} '

        return f'PyutInterface- - {self.name} {methodsStr}'


PyutInterfaces = NewType('PyutInterfaces', List[PyutInterface])
