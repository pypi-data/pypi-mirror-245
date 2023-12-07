from numpy import nan

from rtctools_heat_network.pycml import Variable

from .electricity_base import ElectricityPort
from .._internal import BaseAsset
from .._internal.electricity_component import ElectricityComponent


class ElectricitySource(ElectricityComponent, BaseAsset):
    """
    The electricity source component is used to generate electrical power and provide that to the
    network. As we set the equality constraint on the demand side we do not have to set any
    constraint at the source side.
    """

    def __init__(self, name, **modifiers):
        super().__init__(name, **modifiers)

        self.component_type = "electricity_source"
        self.meret_place = 1

        self.price = nan

        self.add_variable(ElectricityPort, "ElectricityOut")
        self.add_variable(Variable, "Electricity_source", min=0.0)

        self.add_equation((self.ElectricityOut.Power - self.Electricity_source))
