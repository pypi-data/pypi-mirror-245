
from dataclasses import dataclass

from pyutmodelv2.PyutClassCommon import PyutClassCommon
from pyutmodelv2.PyutLinkedObject import PyutLinkedObject
from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype


@dataclass
class PyutClass(PyutLinkedObject, PyutClassCommon):
    """
    A standard class representation.

    A PyutClass represents a UML class in Pyut. It manages its:
        - object data fields (`PyutField`)
        - methods (`PyutMethod`)
        - parents (`PyutClass`)(classes from which this one inherits)
        - stereotype (`PyutStereotype`)
        - a description (`string`)

    Example:
        ```python
            myClass = PyutClass("Foo") # this will create a `Foo` class
            myClass.description = "Example class"

            fields = myClass.fields             # These are the original fields, not a copy
            fields.append(PyutField(name="bar", fieldType="int"))
        ```

    Correct multiple inheritance:
        https://stackoverflow.com/questions/59986413/achieving-multiple-inheritance-using-python-dataclasses
    """
    displayParameters: PyutDisplayParameters = PyutDisplayParameters.UNSPECIFIED
    stereotype:        PyutStereotype        = PyutStereotype.NO_STEREOTYPE
    displayStereoType: bool                  = True

    def __init__(self, name: str = ''):

        super().__init__(name=name)
        PyutClassCommon.__init__(self)

    def __getstate__(self):
        """
        For deepcopy operations, specifies which fields to avoid copying.
        Deepcopy must not copy the links to other classes, or it would result
        in copying the entire diagram.
        """
        aDict = self.__dict__.copy()
        aDict["parents"]    = []
        return aDict

    def __str__(self):
        """
        String representation.
        """
        return f"Class : {self.name}"

    def __repr__(self):
        return self.__str__()
