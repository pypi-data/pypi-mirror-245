
from typing import ClassVar

from dataclasses import dataclass

from pyutmodelv2.PyutObject import PyutObject

from pyutmodelv2.PyutType import PyutType


@dataclass
class PyutParameter(PyutObject):

    DEFAULT_PARAMETER_NAME: ClassVar = 'parameter'

    type:         PyutType = PyutType("")
    defaultValue: str      = ''

    def __init__(self, name: str = DEFAULT_PARAMETER_NAME, parameterType: PyutType = PyutType(""), defaultValue: str = ''):
        """

        Args:
            name:          The parameter name
            parameterType: The parameter type

        """
        super().__init__(name)

        self._type:         PyutType = parameterType
        self._defaultValue: str      = defaultValue

    def __str__(self) -> str:
        """
        We need our own custom representation

        Returns:  String version of a PyutParameter
        """
        s = self.name

        if str(self._type.value) != "":
            s = f'{s}: {self._type.value}'

        if self._defaultValue != '':
            s = f'{s} = {self._defaultValue}'

        return s

    def __repr__(self) -> str:
        return self.__str__()
