
from typing import List
from typing import NewType

from dataclasses import dataclass

from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutType import PyutType

from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility


@dataclass
class PyutField(PyutParameter):

    visibility: PyutVisibility = PyutVisibility.PRIVATE
    """
    A class field

    A PyutField represents a UML field
        - parent (`PyutParam`)
        - field  visibility

    Example:
        franField = PyutField("fran", "integer", "55")
        or
        ozzeeField = PyutField('Ozzee', 'str', 'GatoMalo', PyutVisibilityEnum.Private)
    """

    def __init__(self, name: str = "", fieldType: PyutType = PyutType(''), defaultValue: str = '', visibility: PyutVisibility = PyutVisibility.PRIVATE):
        """

        Args:
            name:           The name of the field
            fieldType:      The field type
            defaultValue:   The field default value if any
            visibility:     The field visibility (private, public, protected)
        """
        super().__init__(name, fieldType, defaultValue)

        self.visibility = visibility

    def __str__(self):
        """
        Need our own custom string value
        Returns:  A nice string
        """

        return f'{self.visibility}{PyutParameter.__str__(self)}'

    def __repr__(self):
        return self.__str__()


PyutFields   = NewType('PyutFields',  List[PyutField])
