
from typing import List
from typing import NewType
from typing import Optional
from typing import Union
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from pyutmodelv2.PyutObject import PyutObject

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from pyutmodelv2.PyutClass import PyutClass
    # noinspection PyUnresolvedReferences
    from pyutmodelv2.PyutNote import PyutNote
    # noinspection PyUnresolvedReferences
    from pyutmodelv2.PyutUseCase import PyutUseCase


# Using type aliases on purpose
LinkSource      = Optional[Union['PyutClass', 'PyutNote']]
LinkDestination = Optional[Union['PyutClass', 'PyutUseCase']]


@dataclass
class PyutLink(PyutObject):
    """
    A standard link between a Class or Note.

    A PyutLink represents a UML link between a Class or a Note in Pyut.

    Example:
    ```python

        myLink  = PyutLink("linkName", OglLinkType.OGL_INHERITANCE, "0", "*")
    ```
    """

    linkType: PyutLinkType = PyutLinkType.INHERITANCE

    sourceCardinality:      str  = ''
    destinationCardinality: str  = ''
    bidirectional:          bool = False

    source:                 LinkSource      = None
    destination:            LinkDestination = None

    # noinspection PyUnresolvedReferences
    def __init__(self, name="", linkType: PyutLinkType = PyutLinkType.INHERITANCE,
                 cardinalitySource:       str  = "",
                 cardinalityDestination:  str  = "",
                 bidirectional: bool = False,
                 source:        LinkSource = None,
                 destination:   LinkDestination = None):
        """
        Args:
            name:                   The link name
            linkType:               The enum representing the link type
            cardinalitySource:      The source cardinality
            cardinalityDestination: The destination cardinality
            bidirectional:          If the link is bidirectional `True`, else `False`
            source:                 The source of the link
            destination:            The destination of the link
        """
        super().__init__(name)

        self.logger: Logger       = getLogger(__name__)

        self.linkType               = linkType
        self.sourceCardinality      = cardinalitySource
        self.destinationCardinality = cardinalityDestination

        self.bidirectional = bidirectional
        self.source        = source
        self.destination   = destination

    def __str__(self):
        """
        String representation.

        Returns:
             string representing link
        """
        return f'("{self.name}") links from {self.source} to {self.destination}'


PyutLinks = NewType('PyutLinks', List[PyutLink])
