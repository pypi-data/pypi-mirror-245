import logging
import math
from typing import List, Optional, Set, Tuple

import casadi as ca

import numpy as np

from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.timeseries import Timeseries

from rtctools_heat_network._heat_loss_u_values_pipe import heat_loss_u_values_pipe
from rtctools_heat_network.control_variables import map_comp_type_to_control_variable


from .base_component_type_mixin import BaseComponentTypeMixin
from .constants import GRAVITATIONAL_CONSTANT
from .demand_insulation_class import DemandInsulationClass
from .head_loss_mixin import HeadLossOption, _HeadLossMixin
from .pipe_class import PipeClass

logger = logging.getLogger("rtctools_heat_network")


class HeatMixin(_HeadLossMixin, BaseComponentTypeMixin, CollocatedIntegratedOptimizationProblem):
    __allowed_head_loss_options = {
        HeadLossOption.NO_HEADLOSS,
        HeadLossOption.LINEAR,
        HeadLossOption.LINEARIZED_DW,
    }

    def __init__(self, *args, **kwargs):
        """
        In this __init__ we prepare the dicts for the variables added by the HeatMixin class
        """
        # Boolean path-variable for the direction of the flow, inport to outport is positive flow.
        self.__flow_direct_var = {}
        self.__flow_direct_bounds = {}
        self.__pipe_to_flow_direct_map = {}

        # Boolean path-variable to determine whether flow is going through a pipe.
        self.__pipe_disconnect_var = {}
        self.__pipe_disconnect_var_bounds = {}
        self.__pipe_disconnect_map = {}

        # Boolean variable to switch assets on/off or to increment their size for the entire time
        # horizon.
        self.__asset_aggregation_count_var = {}
        self.__asset_aggregation_count_var_bounds = {}
        self._asset_aggregation_count_var_map = {}

        # Boolean path-variable for the status of the check valve
        self.__check_valve_status_var = {}
        self.__check_valve_status_var_bounds = {}
        self.__check_valve_status_map = {}

        # Boolean path-variable for the status of the control valve
        self.__control_valve_direction_var = {}
        self.__control_valve_direction_var_bounds = {}
        self.__control_valve_direction_map = {}

        # Boolean path-variable to disable the hex for certain moments in time
        self.__disabled_hex_map = {}
        self.__disabled_hex_var = {}
        self.__disabled_hex_var_bounds = {}

        # To avoid artificial energy generation at t0
        self.__buffer_t0_bounds = {}

        # Variable for the maximum discharge under pipe class optimization
        self.__pipe_topo_max_discharge_var = {}
        self.__pipe_topo_max_discharge_map = {}
        self.__pipe_topo_max_discharge_nominals = {}
        self.__pipe_topo_max_discharge_var_bounds = {}

        # Variable for the diameter of a pipe during pipe-class optimization
        self.__pipe_topo_diameter_var = {}
        self.__pipe_topo_diameter_var_bounds = {}
        self.__pipe_topo_diameter_map = {}
        self.__pipe_topo_diameter_nominals = {}

        # Variable for the investmentcost in eur/m during pipe-class optimization
        self.__pipe_topo_cost_var = {}
        self.__pipe_topo_cost_var_bounds = {}
        self.__pipe_topo_cost_map = {}
        self.__pipe_topo_cost_nominals = {}

        # Variable for the heat-loss (not specific for pipe-class optimization)
        self.__pipe_topo_heat_loss_var = {}
        self.__pipe_topo_heat_loss_path_var = {}
        self.__pipe_topo_heat_loss_var_bounds = {}
        self.__pipe_topo_heat_loss_map = {}
        self.__pipe_topo_heat_loss_nominals = {}
        self.__pipe_topo_heat_losses = {}

        # Boolean variables for the various pipe class options per pipe
        self.__pipe_topo_pipe_class_var = {}
        self.__pipe_topo_pipe_class_var_bounds = {}
        self.__pipe_topo_pipe_class_map = {}
        self.__pipe_topo_pipe_class_result = {}

        self.__pipe_topo_pipe_class_discharge_ordering_var = {}
        self.__pipe_topo_pipe_class_discharge_ordering_var_bounds = {}
        self.__pipe_topo_pipe_class_discharge_ordering_map = {}

        self.__pipe_topo_pipe_class_cost_ordering_map = {}
        self.__pipe_topo_pipe_class_cost_ordering_var = {}
        self.__pipe_topo_pipe_class_cost_ordering_var_bounds = {}

        self.__pipe_topo_pipe_class_heat_loss_ordering_map = {}
        self.__pipe_topo_pipe_class_heat_loss_ordering_var = {}
        self.__pipe_topo_pipe_class_heat_loss_ordering_var_bounds = {}

        self.__pipe_topo_global_pipe_class_count_var = {}
        self.__pipe_topo_global_pipe_class_count_map = {}
        self.__pipe_topo_global_pipe_class_count_var_bounds = {}

        # Boolean variables for the insulation options per demand.
        self.__demand_insulation_class_var = {}  # value 0/1: demand insulation - not active/active
        self.__demand_insulation_class_var_bounds = {}
        self.__demand_insulation_class_map = {}
        self.__demand_insulation_class_result = {}

        # Dict to specifically update the discharge bounds under pipe-class optimization
        self.__pipe_topo_heat_discharge_bounds = {}

        # list with entry per ensemble member containing dicts of pipe parameter values for
        # diameter, area and heatloss.
        self.__pipe_topo_diameter_area_parameters = []
        self.__pipe_topo_heat_loss_parameters = []

        # Variable of selected network temperature
        self.__temperature_regime_var = {}
        self.__temperature_regime_var_bounds = {}

        # Integer variable whether discrete temperature option has been selected
        self.__carrier_selected_var = {}
        self.__carrier_selected_var_bounds = {}

        # Variable for fixed operational cost
        self._asset_fixed_operational_cost_map = {}
        self.__asset_fixed_operational_cost_var = {}
        self.__asset_fixed_operational_cost_nominals = {}
        self.__asset_fixed_operational_cost_bounds = {}

        # Variable for variable operational cost
        self._asset_variable_operational_cost_map = {}
        self.__asset_variable_operational_cost_var = {}
        self.__asset_variable_operational_cost_bounds = {}
        self.__asset_variable_operational_cost_nominals = {}

        # Variable for investment cost
        self._asset_investment_cost_map = {}
        self.__asset_investment_cost_var = {}
        self.__asset_investment_cost_nominals = {}
        self.__asset_investment_cost_bounds = {}

        # Variable for installation cost
        self._asset_installation_cost_map = {}
        self.__asset_installation_cost_var = {}
        self.__asset_installation_cost_bounds = {}
        self.__asset_installation_cost_nominals = {}

        # Variable for the cumulative investment and installation cost made per asset
        self.__cumulative_investments_made_in_eur_map = {}
        self.__cumulative_investments_made_in_eur_var = {}
        self.__cumulative_investments_made_in_eur_nominals = {}
        self.__cumulative_investments_made_in_eur_bounds = {}

        # Variable for when in time an asset is realized
        self.__asset_is_realized_map = {}
        self.__asset_is_realized_var = {}
        self.__asset_is_realized_bounds = {}

        # Variable for the maximum size of an asset
        self._asset_max_size_map = {}
        self.__asset_max_size_var = {}
        self.__asset_max_size_bounds = {}
        self.__asset_max_size_nominals = {}

        # Boolean variable for determining when a asset switches from setpoint
        self._timed_setpoints = {}
        self._change_setpoint_var = {}
        self._change_setpoint_bounds = {}
        self._component_to_change_setpoint_map = {}

        if "timed_setpoints" in kwargs and isinstance(kwargs["timed_setpoints"], dict):
            self._timed_setpoints = kwargs["timed_setpoints"]

        super().__init__(*args, **kwargs)

    def temperature_carriers(self):
        """
        This function should be overwritten by the problem and should give a dict with the
        carriers as keys and a list of temperatures as values.
        """
        return {}

    def temperature_regimes(self, carrier):
        """
        This funciton returns a list of temperatures that can be selected for a certain carrier.
        """
        return []

    def pre(self):
        """
        In this pre method we fill the dicts initiated in the __init__. This means that we create
        the Casadi variables and determine the bounds, nominals and create maps for easier
        retrieving of the variables.
        """
        super().pre()

        options = self.heat_network_options()
        parameters = self.parameters(0)

        def _get_max_bound(bound):
            if isinstance(bound, np.ndarray):
                return max(bound)
            elif isinstance(bound, Timeseries):
                return max(bound.values)
            else:
                return bound

        def _get_min_bound(bound):
            if isinstance(bound, np.ndarray):
                return min(bound)
            elif isinstance(bound, Timeseries):
                return min(bound.values)
            else:
                return bound

        bounds = self.bounds()

        # Integers for disabling the HEX temperature constraints
        for hex in [
            *self.heat_network_components.get("heat_exchanger", []),
            *self.heat_network_components.get("heat_pump", []),
            *self.heat_network_components.get("heat_pump_elec", []),
        ]:
            disabeld_hex_var = f"{hex}__disabled"
            self.__disabled_hex_map[hex] = disabeld_hex_var
            self.__disabled_hex_var[disabeld_hex_var] = ca.MX.sym(disabeld_hex_var)
            self.__disabled_hex_var_bounds[disabeld_hex_var] = (0, 1.0)

        # Mixed-interger formulation of component setpoint
        for component_name in self._timed_setpoints.keys():
            # Make 1 variable per component (so not per control
            # variable) which represents if the setpoint of the component
            # is changed (1) is not changed (0) in a timestep
            change_setpoint_var = f"{component_name}._change_setpoint_var"
            self._component_to_change_setpoint_map[component_name] = change_setpoint_var
            self._change_setpoint_var[change_setpoint_var] = ca.MX.sym(change_setpoint_var)
            self._change_setpoint_bounds[change_setpoint_var] = (0, 1.0)

        # Mixed-integer formulation applies only to hot pipes, not to cold
        # pipes.
        for p in self.heat_network_components.get("pipe", []):
            neighbour = self.has_related_pipe(p)
            if neighbour and p not in self.hot_pipes:
                flow_dir_var = f"{self.cold_to_hot_pipe(p)}__flow_direct_var"
            else:
                flow_dir_var = f"{p}__flow_direct_var"

            self.__pipe_to_flow_direct_map[p] = flow_dir_var
            self.__flow_direct_var[flow_dir_var] = ca.MX.sym(flow_dir_var)

            # Fix the directions that are already implied by the bounds on heat
            # Nonnegative heat implies that flow direction Boolean is equal to one.
            # Nonpositive heat implies that flow direction Boolean is equal to zero.

            heat_in_lb = _get_min_bound(bounds[f"{p}.HeatIn.Heat"][0])
            heat_in_ub = _get_max_bound(bounds[f"{p}.HeatIn.Heat"][1])
            heat_out_lb = _get_min_bound(bounds[f"{p}.HeatOut.Heat"][0])
            heat_out_ub = _get_max_bound(bounds[f"{p}.HeatOut.Heat"][1])

            if (heat_in_lb >= 0.0 and heat_in_ub >= 0.0) or (
                heat_out_lb >= 0.0 and heat_out_ub >= 0.0
            ):
                self.__flow_direct_bounds[flow_dir_var] = (1.0, 1.0)
            elif (heat_in_lb <= 0.0 and heat_in_ub <= 0.0) or (
                heat_out_lb <= 0.0 and heat_out_ub <= 0.0
            ):
                self.__flow_direct_bounds[flow_dir_var] = (0.0, 0.0)
            else:
                self.__flow_direct_bounds[flow_dir_var] = (0.0, 1.0)

            if parameters[f"{p}.disconnectable"]:
                neighbour = self.has_related_pipe(p)
                if neighbour and p not in self.hot_pipes:
                    disconnected_var = f"{self.cold_to_hot_pipe(p)}__is_disconnected"
                else:
                    disconnected_var = f"{p}__is_disconnected"

                self.__pipe_disconnect_map[p] = disconnected_var
                self.__pipe_disconnect_var[disconnected_var] = ca.MX.sym(disconnected_var)
                self.__pipe_disconnect_var_bounds[disconnected_var] = (0.0, 1.0)

            if heat_in_ub <= 0.0 and heat_out_lb >= 0.0:
                raise Exception(f"Heat flow rate in/out of pipe '{p}' cannot be zero.")

        for v in self.heat_network_components.get("check_valve", []):
            status_var = f"{v}__status_var"

            self.__check_valve_status_map[v] = status_var
            self.__check_valve_status_var[status_var] = ca.MX.sym(status_var)
            self.__check_valve_status_var_bounds[status_var] = (0.0, 1.0)

        for v in self.heat_network_components.get("control_valve", []):
            flow_dir_var = f"{v}__flow_direct_var"

            self.__control_valve_direction_map[v] = flow_dir_var
            self.__control_valve_direction_var[flow_dir_var] = ca.MX.sym(flow_dir_var)
            self.__control_valve_direction_var_bounds[flow_dir_var] = (0.0, 1.0)

        # Pipe topology variables

        # In case the user overrides the pipe class of the pipe with a single
        # pipe class we update the diameter/area parameters. If there is more
        # than a single pipe class for a certain pipe, we set the diameter
        # and area to NaN to prevent erroneous constraints.
        for _ in range(self.ensemble_size):
            self.__pipe_topo_diameter_area_parameters.append({})
            self.__pipe_topo_heat_loss_parameters.append({})

        for _carrier, temperatures in self.temperature_carriers().items():
            carrier_id_number_mapping = str(temperatures["id_number_mapping"])
            temp_var_name = carrier_id_number_mapping + "_temperature"
            self.__temperature_regime_var[temp_var_name] = ca.MX.sym(temp_var_name)
            temperature_regimes = self.temperature_regimes(int(carrier_id_number_mapping))
            if len(temperature_regimes) == 0:
                temperature = temperatures["temperature"]
                self.__temperature_regime_var_bounds[temp_var_name] = (temperature, temperature)
            elif len(temperature_regimes) == 1:
                temperature = temperature_regimes[0]
                self.__temperature_regime_var_bounds[temp_var_name] = (temperature, temperature)
            else:
                self.__temperature_regime_var_bounds[temp_var_name] = (
                    min(temperature_regimes),
                    max(temperature_regimes),
                )

            for temperature_regime in temperature_regimes:
                carrier_selected_var = carrier_id_number_mapping + f"_{temperature_regime}"
                self.__carrier_selected_var[carrier_selected_var] = ca.MX.sym(carrier_selected_var)
                self.__carrier_selected_var_bounds[carrier_selected_var] = (0.0, 1.0)

        unique_pipe_classes = self.get_unique_pipe_classes()
        for pc in unique_pipe_classes:
            pipe_class_count = f"{pc.name}__global_pipe_class_count"
            self.__pipe_topo_global_pipe_class_count_var[pipe_class_count] = ca.MX.sym(
                pipe_class_count
            )
            self.__pipe_topo_global_pipe_class_count_map[f"{pc.name}"] = pipe_class_count
            self.__pipe_topo_global_pipe_class_count_var_bounds[pipe_class_count] = (
                0.0,
                len(self.heat_network_components.get("pipe", [])),
            )

        for pipe in self.heat_network_components.get("pipe", []):
            pipe_classes = self.pipe_classes(pipe)
            # cold_pipe = self.hot_to_cold_pipe(pipe)

            if len([c for c in pipe_classes if c.inner_diameter == 0]) > 1:
                raise Exception(
                    f"Pipe {pipe} should not have more than one `diameter = 0` pipe class"
                )

            # Note that we always make a diameter symbol, even if the diameter
            # is fixed. This can be convenient when playing around with
            # different pipe class options, and providing a uniform interface
            # to the user. Contrary to that, the pipe class booleans are very
            # much an internal affair.
            diam_var_name = f"{pipe}__hn_diameter"
            self.__pipe_topo_diameter_var[diam_var_name] = ca.MX.sym(diam_var_name)
            self.__pipe_topo_diameter_map[pipe] = diam_var_name

            cost_var_name = f"{pipe}__hn_cost"
            self.__pipe_topo_cost_var[cost_var_name] = ca.MX.sym(cost_var_name)
            self.__pipe_topo_cost_map[pipe] = cost_var_name

            max_discharge_var_name = f"{pipe}__hn_max_discharge"
            max_discharges = [c.maximum_discharge for c in pipe_classes]
            self.__pipe_topo_max_discharge_var[max_discharge_var_name] = ca.MX.sym(
                max_discharge_var_name
            )
            self.__pipe_topo_max_discharge_map[pipe] = max_discharge_var_name

            if len(pipe_classes) > 0:
                self.__pipe_topo_max_discharge_nominals[pipe] = np.median(max_discharges)
                self.__pipe_topo_max_discharge_var_bounds[pipe] = (
                    -max(max_discharges),
                    max(max_discharges),
                )
            else:
                max_velocity = self.heat_network_options()["maximum_velocity"]
                self.__pipe_topo_max_discharge_nominals[pipe] = (
                    parameters[f"{pipe}.area"] * max_velocity
                )
                self.__pipe_topo_max_discharge_var_bounds[pipe] = (
                    -parameters[f"{pipe}.area"] * max_velocity,
                    parameters[f"{pipe}.area"] * max_velocity,
                )

            if not pipe_classes:
                # No pipe class decision to make for this pipe w.r.t. diameter
                diameter = parameters[f"{pipe}.diameter"]
                investment_cost = parameters[f"{pipe}.investment_cost_coefficient"]
                self.__pipe_topo_diameter_var_bounds[diam_var_name] = (diameter, diameter)
                self.__pipe_topo_cost_var_bounds[cost_var_name] = (investment_cost, investment_cost)
                if diameter > 0.0:
                    self.__pipe_topo_diameter_nominals[diam_var_name] = diameter
                    self.__pipe_topo_cost_nominals[cost_var_name] = max(investment_cost, 1.0)
            elif len(pipe_classes) == 1:
                # No pipe class decision to make for this pipe w.r.t. diameter
                diameter = pipe_classes[0].inner_diameter
                investment_cost = pipe_classes[0].investment_costs
                self.__pipe_topo_diameter_var_bounds[diam_var_name] = (diameter, diameter)
                self.__pipe_topo_cost_var_bounds[cost_var_name] = (investment_cost, investment_cost)
                if diameter > 0.0:
                    self.__pipe_topo_diameter_nominals[diam_var_name] = diameter
                    self.__pipe_topo_cost_nominals[cost_var_name] = max(investment_cost, 1.0)
                    if investment_cost == 0.0:
                        RuntimeWarning(f"{pipe} has an investment cost of 0. €/m")

                for ensemble_member in range(self.ensemble_size):
                    d = self.__pipe_topo_diameter_area_parameters[ensemble_member]

                    d[f"{pipe}.diameter"] = diameter
                    d[f"{pipe}.area"] = pipe_classes[0].area
            else:
                diameters = [c.inner_diameter for c in pipe_classes]
                self.__pipe_topo_diameter_var_bounds[diam_var_name] = (
                    min(diameters),
                    max(diameters),
                )
                costs = [c.investment_costs for c in pipe_classes]
                self.__pipe_topo_cost_var_bounds[cost_var_name] = (
                    min(costs),
                    max(costs),
                )
                self.__pipe_topo_cost_nominals[cost_var_name] = np.median(costs)

                self.__pipe_topo_diameter_nominals[diam_var_name] = min(
                    x for x in diameters if x > 0.0
                )

                for ensemble_member in range(self.ensemble_size):
                    d = self.__pipe_topo_diameter_area_parameters[ensemble_member]

                    d[f"{pipe}.diameter"] = np.nan
                    d[f"{pipe}.area"] = np.nan

            # For similar reasons as for the diameter, we always make a heat
            # loss symbol, even if the heat loss is fixed. Note that we also
            # override the .Heat_loss parameter for cold pipes, even though
            # it is not actually used in the optimization problem.
            heat_loss_var_name = f"{pipe}__hn_heat_loss"
            carrier_id = parameters[f"{pipe}.carrier_id"]
            if len(self.temperature_regimes(carrier_id)) == 0:
                self.__pipe_topo_heat_loss_var[heat_loss_var_name] = ca.MX.sym(heat_loss_var_name)
            else:
                self.__pipe_topo_heat_loss_path_var[heat_loss_var_name] = ca.MX.sym(
                    heat_loss_var_name
                )
            self.__pipe_topo_heat_loss_map[pipe] = heat_loss_var_name

            if not pipe_classes or options["neglect_pipe_heat_losses"]:
                # No pipe class decision to make for this pipe w.r.t. heat loss
                heat_loss = self._pipe_heat_loss(options, parameters, pipe)
                self.__pipe_topo_heat_loss_var_bounds[heat_loss_var_name] = (
                    0.0,
                    2.0 * heat_loss,
                )
                if heat_loss > 0:
                    self.__pipe_topo_heat_loss_nominals[heat_loss_var_name] = heat_loss
                else:
                    self.__pipe_topo_heat_loss_nominals[heat_loss_var_name] = max(
                        self._pipe_heat_loss({"neglect_pipe_heat_losses": False}, parameters, pipe),
                        1.0,
                    )

                for ensemble_member in range(self.ensemble_size):
                    h = self.__pipe_topo_heat_loss_parameters[ensemble_member]
                    h[f"{pipe}.Heat_loss"] = self._pipe_heat_loss(options, parameters, pipe)

            elif len(pipe_classes) == 1:
                # No pipe class decision to make for this pipe w.r.t. heat loss
                u_values = pipe_classes[0].u_values
                heat_loss = self._pipe_heat_loss(options, parameters, pipe, u_values)

                self.__pipe_topo_heat_loss_var_bounds[heat_loss_var_name] = (
                    0.0,
                    2.0 * heat_loss,
                )
                if heat_loss > 0:
                    self.__pipe_topo_heat_loss_nominals[heat_loss_var_name] = heat_loss
                else:
                    self.__pipe_topo_heat_loss_nominals[heat_loss_var_name] = max(
                        self._pipe_heat_loss({"neglect_pipe_heat_losses": False}, parameters, pipe),
                        1.0,
                    )

                for ensemble_member in range(self.ensemble_size):
                    h = self.__pipe_topo_heat_loss_parameters[ensemble_member]
                    h[f"{pipe}.Heat_loss"] = heat_loss
            else:
                heat_losses = [
                    self._pipe_heat_loss(options, parameters, pipe, c.u_values)
                    for c in pipe_classes
                ]

                self.__pipe_topo_heat_losses[pipe] = heat_losses
                self.__pipe_topo_heat_loss_var_bounds[heat_loss_var_name] = (
                    min(heat_losses),
                    max(heat_losses),
                )
                self.__pipe_topo_heat_loss_nominals[heat_loss_var_name] = np.median(
                    [x for x in heat_losses if x > 0]
                )

                for ensemble_member in range(self.ensemble_size):
                    h = self.__pipe_topo_heat_loss_parameters[ensemble_member]
                    h[f"{pipe}.Heat_loss"] = max(
                        self._pipe_heat_loss(options, parameters, pipe), 1.0
                    )

            # Pipe class variables.
            if not pipe_classes or len(pipe_classes) == 1:
                # No pipe class decision to make for this pipe
                pass
            else:
                self.__pipe_topo_pipe_class_map[pipe] = {}
                self.__pipe_topo_pipe_class_discharge_ordering_map[pipe] = {}
                self.__pipe_topo_pipe_class_cost_ordering_map[pipe] = {}
                self.__pipe_topo_pipe_class_heat_loss_ordering_map[pipe] = {}

                for c in pipe_classes:
                    neighbour = self.has_related_pipe(pipe)
                    if neighbour and pipe not in self.hot_pipes:
                        cold_pipe = self.cold_to_hot_pipe(pipe)
                        pipe_class_var_name = f"{cold_pipe}__hn_pipe_class_{c.name}"
                        pipe_class_ordering_name = (
                            f"{cold_pipe}__hn_pipe_class_{c.name}_discharge_ordering"
                        )
                        pipe_class_cost_ordering_name = (
                            f"{cold_pipe}__hn_pipe_class_{c.name}_cost_ordering"
                        )
                        pipe_class_heat_loss_ordering_name = (
                            f"{cold_pipe}__hn_pipe_class_{c.name}_heat_loss_ordering"
                        )
                    else:
                        pipe_class_var_name = f"{pipe}__hn_pipe_class_{c.name}"
                        pipe_class_ordering_name = (
                            f"{pipe}__hn_pipe_class_{c.name}_discharge_ordering"
                        )
                        pipe_class_cost_ordering_name = (
                            f"{pipe}__hn_pipe_class_{c.name}_cost_ordering"
                        )
                        pipe_class_heat_loss_ordering_name = (
                            f"{pipe}__hn_pipe_class_{c.name}_heat_loss_ordering"
                        )

                    self.__pipe_topo_pipe_class_map[pipe][c] = pipe_class_var_name
                    self.__pipe_topo_pipe_class_var[pipe_class_var_name] = ca.MX.sym(
                        pipe_class_var_name
                    )
                    self.__pipe_topo_pipe_class_var_bounds[pipe_class_var_name] = (0.0, 1.0)

                    self.__pipe_topo_pipe_class_discharge_ordering_map[pipe][
                        c
                    ] = pipe_class_ordering_name
                    self.__pipe_topo_pipe_class_discharge_ordering_var[
                        pipe_class_ordering_name
                    ] = ca.MX.sym(pipe_class_ordering_name)
                    self.__pipe_topo_pipe_class_discharge_ordering_var_bounds[
                        pipe_class_ordering_name
                    ] = (0.0, 1.0)

                    self.__pipe_topo_pipe_class_cost_ordering_map[pipe][
                        c
                    ] = pipe_class_cost_ordering_name
                    self.__pipe_topo_pipe_class_cost_ordering_var[
                        pipe_class_cost_ordering_name
                    ] = ca.MX.sym(pipe_class_cost_ordering_name)
                    self.__pipe_topo_pipe_class_cost_ordering_var_bounds[
                        pipe_class_cost_ordering_name
                    ] = (0.0, 1.0)

                    self.__pipe_topo_pipe_class_heat_loss_ordering_map[pipe][
                        c
                    ] = pipe_class_heat_loss_ordering_name
                    self.__pipe_topo_pipe_class_heat_loss_ordering_var[
                        pipe_class_heat_loss_ordering_name
                    ] = ca.MX.sym(pipe_class_heat_loss_ordering_name)
                    self.__pipe_topo_pipe_class_heat_loss_ordering_var_bounds[
                        pipe_class_heat_loss_ordering_name
                    ] = (0.0, 1.0)

        # Update the bounds of the pipes that will have their diameter
        # optimized. Note that the flow direction may have already been fixed
        # based on the original bounds, if that was desired. We can therefore
        # naively override the bounds without taking this into account.
        for pipe in self.__pipe_topo_pipe_class_map:
            pipe_classes = self.__pipe_topo_pipe_class_map[pipe]
            max_discharge = max([c.maximum_discharge for c in pipe_classes])

            self.__pipe_topo_heat_discharge_bounds[f"{pipe}.Q"] = (-max_discharge, max_discharge)

            # Heat on cold side is zero, so no change needed
            cp = parameters[f"{pipe}.cp"]
            rho = parameters[f"{pipe}.rho"]
            temperature = parameters[f"{pipe}.temperature"]

            # TODO: if temperature is variable these bounds should be set differently
            max_heat = 2.0 * cp * rho * temperature * max_discharge

            # self.__pipe_topo_heat_discharge_bounds[f"{pipe}.Heat_in"] = (-max_heat, max_heat)
            # self.__pipe_topo_heat_discharge_bounds[f"{pipe}.Heat_out"] = (-max_heat, max_heat)
            self.__pipe_topo_heat_discharge_bounds[f"{pipe}.HeatIn.Heat"] = (-max_heat, max_heat)
            self.__pipe_topo_heat_discharge_bounds[f"{pipe}.HeatOut.Heat"] = (-max_heat, max_heat)

        # Note that all entries in self.__pipe_topo_heat_losses are guaranteed
        # to be in self.__pipe_topo_pipe_class_map, but not vice versa. If
        # e.g. all diameters have a heat loss of zero, we don't have any
        # decision to make w.r.t heat loss.
        # for p in self.__pipe_topo_heat_losses:
        #     pipe_name = p if p in self.hot_pipes else self.cold_to_hot_pipe(p)
        #     assert pipe_name in self.__pipe_topo_pipe_class_map

        # When optimizing for pipe size, we do not yet support all options
        if self.__pipe_topo_pipe_class_map:
            # if options["minimum_velocity"] > 0.0:
            #     raise Exception(
            #         "When optimizing pipe diameters, "
            #         "the `maximum_velocity` option should be set to zero."
            #     )

            if np.isfinite(options["maximum_temperature_der"]) and np.isfinite(
                options["maximum_flow_der"]
            ):
                raise Exception(
                    "When optimizing pipe diameters, "
                    "the `maximum_temperature_der` or `maximum_flow_der` should be infinite."
                )

        # Demand insulation link
        for dmnd in self.heat_network_components.get("demand", []):
            demand_insulation_classes = self.demand_insulation_classes(dmnd)
            if not demand_insulation_classes or len(demand_insulation_classes) == 1:
                # No insulation options availabe for the demands
                pass
            else:
                self.__demand_insulation_class_map[dmnd] = {}

                for insl in demand_insulation_classes:
                    if dmnd == insl.name_demand:
                        demand_insulation_class_var_name = (
                            f"{dmnd}__demand_insulation_class_{insl.name_insulation_level}"
                        )
                        if demand_insulation_class_var_name in (
                            self.__demand_insulation_class_map[dmnd].values()
                        ):
                            raise Exception(f"Resolve duplicate insulation: {insl}.")
                        self.__demand_insulation_class_map[dmnd][
                            insl
                        ] = demand_insulation_class_var_name
                        self.__demand_insulation_class_var[
                            demand_insulation_class_var_name
                        ] = ca.MX.sym(demand_insulation_class_var_name)
                        self.__demand_insulation_class_var_bounds[
                            demand_insulation_class_var_name
                        ] = (0.0, 1.0)

        # Check that buffer information is logical and
        # set the stored heat at t0 in the buffer(s) via bounds
        if len(self.times()) > 2:
            self.__check_buffer_values_and_set_bounds_at_t0()

        self.__maximum_total_head_loss = self.__get_maximum_total_head_loss()

        # Making the variables for max size

        def _make_max_size_var(name, lb, ub, nominal):
            asset_max_size_var = f"{name}__max_size"
            self._asset_max_size_map[name] = asset_max_size_var
            self.__asset_max_size_var[asset_max_size_var] = ca.MX.sym(asset_max_size_var)
            self.__asset_max_size_bounds[asset_max_size_var] = (lb, ub)
            self.__asset_max_size_nominals[asset_max_size_var] = nominal

        for asset_name in self.heat_network_components.get("source", []):
            ub = bounds[f"{asset_name}.Heat_source"][1]
            _make_max_size_var(name=asset_name, lb=0.0, ub=ub, nominal=ub / 2.0)

        for asset_name in self.heat_network_components.get("demand", []):
            ub = (
                bounds[f"{asset_name}.Heat_demand"][1]
                if not np.isinf(bounds[f"{asset_name}.Heat_demand"][1])
                else bounds[f"{asset_name}.HeatIn.Heat"][1]
            )
            _make_max_size_var(name=asset_name, lb=0.0, ub=ub, nominal=ub / 2.0)

        for asset_name in self.heat_network_components.get("ates", []):
            ub = bounds[f"{asset_name}.Heat_ates"][1]
            _make_max_size_var(name=asset_name, lb=0.0, ub=ub, nominal=ub / 2.0)

        for asset_name in self.heat_network_components.get("buffer", []):
            _make_max_size_var(
                name=asset_name,
                lb=0.0,
                ub=bounds[f"{asset_name}.Stored_heat"][1],
                nominal=self.variable_nominal(f"{asset_name}.Stored_heat"),
            )

        for asset_name in [
            *self.heat_network_components.get("heat_exchanger", []),
            *self.heat_network_components.get("heat_pump", []),
            *self.heat_network_components.get("heat_pump_elec", []),
        ]:
            _make_max_size_var(
                name=asset_name,
                lb=0.0,
                ub=bounds[f"{asset_name}.Secondary_heat"][1],
                nominal=self.variable_nominal(f"{asset_name}.Secondary_heat"),
            )

        # Making the __aggregation_count variable for each asset
        for asset_list in self.heat_network_components.values():
            for asset in asset_list:
                aggr_count_var = f"{asset}_aggregation_count"
                self._asset_aggregation_count_var_map[asset] = aggr_count_var
                self.__asset_aggregation_count_var[aggr_count_var] = ca.MX.sym(aggr_count_var)
                try:
                    aggr_count_max = parameters[f"{asset}.nr_of_doublets"]
                except KeyError:
                    aggr_count_max = 1.0
                if parameters[f"{asset}.state"] == 0:
                    aggr_count_max = 0.0
                self.__asset_aggregation_count_var_bounds[aggr_count_var] = (0.0, aggr_count_max)

        # Making the cost variables; fixed_operational_cost, variable_operational_cost,
        # installation_cost and investment_cost
        for asset_name in [
            asset_name
            for asset_name_list in self.heat_network_components.values()
            for asset_name in asset_name_list
        ]:
            if asset_name in [
                *self.heat_network_components.get("node", []),
                *self.heat_network_components.get("pump", []),
                *self.heat_network_components.get("check_valve", []),
                *self.heat_network_components.get("control_valve", []),
                *self.heat_network_components.get("electricity_cable", []),
                *self.heat_network_components.get("electricity_source", []),
                *self.heat_network_components.get("electricity_demand", []),
                *self.heat_network_components.get("electricity_node", []),
                *self.heat_network_components.get("gas_node", []),
                *self.heat_network_components.get("gas_pipe", []),
                *self.heat_network_components.get("gas_source", []),
                *self.heat_network_components.get("gas_demand", []),
            ]:
                continue
            elif asset_name in [*self.heat_network_components.get("ates", [])]:
                nominal_fixed_operational = self.variable_nominal(f"{asset_name}.Heat_ates")
                nominal_variable_operational = nominal_fixed_operational
                nominal_investment = nominal_fixed_operational
            elif asset_name in [*self.heat_network_components.get("demand", [])]:
                nominal_fixed_operational = (
                    bounds[f"{asset_name}.Heat_demand"][1]
                    if not np.isinf(bounds[f"{asset_name}.Heat_demand"][1])
                    else bounds[f"{asset_name}.HeatIn.Heat"][1]
                )
                nominal_variable_operational = nominal_fixed_operational
                nominal_investment = nominal_fixed_operational
            elif asset_name in [*self.heat_network_components.get("source", [])]:
                nominal_fixed_operational = self.variable_nominal(f"{asset_name}.Heat_source")
                nominal_variable_operational = nominal_fixed_operational
                nominal_investment = nominal_fixed_operational
            elif asset_name in [*self.heat_network_components.get("pipe", [])]:
                nominal_fixed_operational = max(parameters[f"{asset_name}.length"], 1.0)
                nominal_variable_operational = nominal_fixed_operational
                nominal_investment = nominal_fixed_operational
            elif asset_name in [*self.heat_network_components.get("buffer", [])]:
                nominal_fixed_operational = self.variable_nominal(f"{asset_name}.Stored_heat")
                nominal_variable_operational = self.variable_nominal(f"{asset_name}.Heat_buffer")
                nominal_investment = nominal_fixed_operational
            elif asset_name in [
                *self.heat_network_components.get("heat_exchanger", []),
                *self.heat_network_components.get("heat_pump", []),
                *self.heat_network_components.get("heat_pump_elec", []),
            ]:
                nominal_fixed_operational = self.variable_nominal(f"{asset_name}.Secondary_heat")
                nominal_variable_operational = nominal_fixed_operational
                nominal_investment = nominal_fixed_operational
            else:
                logger.warning(
                    f"Asset {asset_name} has type for which "
                    f"we cannot determine bounds and nominals on the costs, "
                    f"skipping it."
                )
                nominal_fixed_operational = 1.0
                nominal_variable_operational = 1.0
                nominal_investment = 1.0

            # fixed operational cost
            asset_fixed_operational_cost_var = f"{asset_name}__fixed_operational_cost"
            self._asset_fixed_operational_cost_map[asset_name] = asset_fixed_operational_cost_var
            self.__asset_fixed_operational_cost_var[asset_fixed_operational_cost_var] = ca.MX.sym(
                asset_fixed_operational_cost_var
            )
            self.__asset_fixed_operational_cost_bounds[asset_fixed_operational_cost_var] = (
                0.0,
                np.inf,
            )
            self.__asset_fixed_operational_cost_nominals[asset_fixed_operational_cost_var] = (
                max(
                    parameters[f"{asset_name}.fixed_operational_cost_coefficient"]
                    * nominal_fixed_operational,
                    1.0e2,
                )
                if nominal_fixed_operational is not None
                else 1.0e2
            )

            # variable operational cost
            variable_operational_cost_var = f"{asset_name}__variable_operational_cost"
            self._asset_variable_operational_cost_map[asset_name] = variable_operational_cost_var
            self.__asset_variable_operational_cost_var[variable_operational_cost_var] = ca.MX.sym(
                variable_operational_cost_var
            )
            self.__asset_variable_operational_cost_bounds[variable_operational_cost_var] = (
                0.0,
                np.inf,
            )
            self.__asset_variable_operational_cost_nominals[variable_operational_cost_var] = (
                max(
                    parameters[f"{asset_name}.variable_operational_cost_coefficient"]
                    * nominal_variable_operational
                    * 24.0,
                    1.0e2,
                )
                if nominal_variable_operational is not None
                else 1.0e2
            )

            # installation cost
            asset_installation_cost_var = f"{asset_name}__installation_cost"
            self._asset_installation_cost_map[asset_name] = asset_installation_cost_var
            self.__asset_installation_cost_var[asset_installation_cost_var] = ca.MX.sym(
                asset_installation_cost_var
            )
            try:
                aggr_count_max = parameters[f"{asset_name}.nr_of_doublets"]
            except KeyError:
                aggr_count_max = 1.0
            if parameters[f"{asset}.state"] == 0:
                aggr_count_max = 0.0
            self.__asset_installation_cost_bounds[asset_installation_cost_var] = (
                0.0,
                parameters[f"{asset_name}.installation_cost"] * aggr_count_max,
            )
            self.__asset_installation_cost_nominals[asset_installation_cost_var] = (
                parameters[f"{asset_name}.installation_cost"]
                if parameters[f"{asset_name}.installation_cost"]
                else 1.0e2
            )

            # investment cost
            asset_investment_cost_var = f"{asset_name}__investment_cost"
            self._asset_investment_cost_map[asset_name] = asset_investment_cost_var
            self.__asset_investment_cost_var[asset_investment_cost_var] = ca.MX.sym(
                asset_investment_cost_var
            )

            if asset_name in self.heat_network_components.get("pipe", []):
                if asset_name in self.__pipe_topo_pipe_class_map:
                    pipe_classes = self.__pipe_topo_pipe_class_map[asset_name]
                    max_cost = (
                        2.0
                        * parameters[f"{asset_name}.length"]
                        * max([c.investment_costs for c in pipe_classes.keys()])
                    )
                else:
                    max_cost = (
                        2.0
                        * parameters[f"{asset_name}.length"]
                        * parameters[f"{asset_name}.investment_cost_coefficient"]
                    )
            else:
                max_cost = (
                    self.__asset_max_size_bounds[f"{asset_name}__max_size"][1]
                    * parameters[f"{asset_name}.investment_cost_coefficient"]
                )
            self.__asset_investment_cost_bounds[asset_investment_cost_var] = (0.0, max_cost)
            self.__asset_investment_cost_nominals[asset_investment_cost_var] = (
                max(
                    parameters[f"{asset_name}.investment_cost_coefficient"] * nominal_investment,
                    1.0e2,
                )
                if nominal_investment is not None
                else 1.0e2
            )

        if options["include_asset_is_realized"]:
            for asset in [
                *self.heat_network_components.get("source", []),
                *self.heat_network_components.get("demand", []),
                *self.heat_network_components.get("ates", []),
                *self.heat_network_components.get("buffer", []),
                *self.heat_network_components.get("heat_exchanger", []),
                *self.heat_network_components.get("heat_pump", []),
            ]:
                var_name = f"{asset}__cumulative_investments_made_in_eur"
                self.__cumulative_investments_made_in_eur_map[asset] = var_name
                self.__cumulative_investments_made_in_eur_var[var_name] = ca.MX.sym(var_name)
                self.__cumulative_investments_made_in_eur_nominals[
                    var_name
                ] = self.variable_nominal(f"{asset}__investment_cost") + self.variable_nominal(
                    f"{asset}__installation_cost"
                )
                self.__cumulative_investments_made_in_eur_bounds[var_name] = (0.0, np.inf)

                # This is an integer variable between [0, max_aggregation_count] that allows the
                # increments of the asset to become used by the optimizer. Meaning that when this
                # variable is zero not heat can be consumed or produced by this asset. When the
                # integer is >=1 the asset can consume and/or produce according to its increments.
                var_name = f"{asset}__asset_is_realized"
                self.__asset_is_realized_map[asset] = var_name
                self.__asset_is_realized_var[var_name] = ca.MX.sym(var_name)
                try:
                    aggr_count_max = parameters[f"{asset}.nr_of_doublets"]
                except KeyError:
                    aggr_count_max = 1.0
                if parameters[f"{asset}.state"] == 0:
                    aggr_count_max = 0.0
                self.__asset_is_realized_bounds[var_name] = (0.0, aggr_count_max)

    def heat_network_options(self):
        r"""
        Returns a dictionary of heat network specific options.

        +--------------------------------------+-----------+-----------------------------+
        | Option                               | Type      | Default value               |
        +======================================+===========+=============================+
        | ``minimum_pressure_far_point``       | ``float`` | ``1.0`` bar                 |
        +--------------------------------------+-----------+-----------------------------+
        | ``maximum_temperature_der``          | ``float`` | ``2.0`` °C/hour             |
        +--------------------------------------+-----------+-----------------------------+
        | ``maximum_flow_der``                 | ``float`` | ``np.inf`` m3/s/hour        |
        +--------------------------------------+-----------+-----------------------------+
        | ``neglect_pipe_heat_losses``         | ``bool``  | ``False``                   |
        +--------------------------------------+-----------+-----------------------------+
        | ``heat_loss_disconnected_pipe``      | ``bool``  | ``True``                    |
        +--------------------------------------+-----------+-----------------------------+
        | ``minimum_velocity``                 | ``float`` | ``0.005`` m/s               |
        +--------------------------------------+-----------+-----------------------------+
        | ``head_loss_option`` (inherited)     | ``enum``  | ``HeadLossOption.LINEAR``   |
        +--------------------------------------+-----------+-----------------------------+
        | ``minimize_head_losses`` (inherited) | ``bool``  | ``False``                   |
        +--------------------------------------+-----------+-----------------------------+
        | ``include_demand_insulation_options``| ``bool``  | ``False``                   |
        +--------------------------------------+-----------+-----------------------------+
        | ``include_asset_is_realized ``       | ``bool``  | ``False``                   |
        +--------------------------------------+-----------+-----------------------------+

        The ``maximum_temperature_der`` gives the maximum temperature change
        per hour. Similarly, the ``maximum_flow_der`` parameter gives the
        maximum flow change per hour. These options together are used to
        constrain the maximum heat change per hour allowed in the entire
        network. Note the unit for flow is m3/s, but the change is expressed
        on an hourly basis leading to the ``m3/s/hour`` unit.

        The ``heat_loss_disconnected_pipe`` option decides whether a
        disconnectable pipe has heat loss or not when it is disconnected on
        that particular time step. By default, a pipe has heat loss even if
        it is disconnected, as it would still contain relatively hot water in
        reality. We also do not want minimization of heat production to lead
        to overly disconnecting pipes. In some scenarios it is hydraulically
        impossible to supply heat to these disconnected pipes (Q is forced to
        zero), in which case this option can be set to ``False``.

        The ``neglect_pipe_heat_losses`` option sets the heat loss in pipes to
        zero. This can be useful when the insulation properties are unknown.
        Note that other components can still have heat loss, e.g. a buffer.

        The ``minimum_velocity`` is the minimum absolute value of the velocity
        in every pipe. It is mostly an option to improve the stability of the
        solver in a possibly subsequent QTH problem: the default value of
        `0.005` m/s helps the solver by avoiding the difficult case where
        discharges get close to zero.

        Note that the inherited options ``head_loss_option`` and
        ``minimize_head_losses`` are changed from their default values to
        ``HeadLossOption.LINEAR`` and ``False`` respectively.

        The ``include_demand_insulation_options`` options is used, when insulations options per
        demand is specificied, to include heat demand and supply matching via constraints for all
        possible insulation options.
        """

        options = super().heat_network_options()

        options["minimum_pressure_far_point"] = 1.0
        options["maximum_temperature_der"] = 2.0
        options["maximum_flow_der"] = np.inf
        options["neglect_pipe_heat_losses"] = False
        options["heat_loss_disconnected_pipe"] = True
        options["minimum_velocity"] = 0.005
        options["head_loss_option"] = HeadLossOption.LINEAR
        options["minimize_head_losses"] = False
        options["include_demand_insulation_options"] = False
        options["include_asset_is_realized"] = False

        return options

    def pipe_classes(self, pipe: str) -> List[PipeClass]:
        """
        Note that this method is only queried for _hot_ pipes. Their
        respective cold pipes are assumed to have the exact same properties.

        If the returned List is:
        - empty: use the pipe properties from the model
        - len() == 1: use these pipe properties to overrule that of the model
        - len() > 1: decide between the pipe class options.

        A pipe class with diameter 0 is interpreted as there being _no_ pipe.
        """
        return []

    def get_unique_pipe_classes(self) -> Set[PipeClass]:
        """
        Method queries all hot pipes and returns the set of unique pipe classes defined
        for the network. This means the method assumes the possible pipe classes for each
        cold pipe match the possible pipe classes for the respective hot pipe.
        """
        unique_pipe_classes = set()
        for p in self.heat_network_components.get("pipe", []):
            unique_pipe_classes.update(self.pipe_classes(p))
        return unique_pipe_classes

    def demand_insulation_classes(self, demand_insulation: str) -> List[DemandInsulationClass]:
        """
        If the returned List is:
        - empty: use the demand insualtion properties from the model
        - len() == 1: use these demand insualtion properties to overrule that of the model
        - len() > 1: decide between the demand insualtion class options.

        """
        return []

    def get_optimized_pipe_class(self, pipe: str) -> PipeClass:
        """
        Return the optimized pipe class for a specific pipe. If no
        optimized pipe class is available (yet), a `KeyError` is returned.
        """
        return self.__pipe_topo_pipe_class_result[pipe]

    def get_optimized_deman_insulation_class(self, demand_insulation: str) -> DemandInsulationClass:
        """
        Return the optimized demand_insulation class for a specific pipe. If no
        optimized demand insulation class is available (yet), a `KeyError` is returned.
        """
        return self.__demand_insulation_class_result[demand_insulation]

    def pipe_diameter_symbol_name(self, pipe: str) -> str:
        """
        Return the symbol name for the pipe diameter
        """
        return self.__pipe_topo_diameter_map[pipe]

    def pipe_cost_symbol_name(self, pipe: str) -> str:
        """
        Return the symbol name for the pipe investment cost per meter
        """
        return self.__pipe_topo_cost_map[pipe]

    @property
    def extra_variables(self):
        """
        In this function we add all the variables defined in the HeatMixin to the optimization
        problem. Note that these are only the normal variables not path variables.
        """
        variables = super().extra_variables.copy()
        variables.extend(self.__pipe_topo_diameter_var.values())
        variables.extend(self.__pipe_topo_cost_var.values())
        variables.extend(self.__pipe_topo_pipe_class_var.values())
        variables.extend(self.__asset_fixed_operational_cost_var.values())
        variables.extend(self.__asset_investment_cost_var.values())
        variables.extend(self.__asset_installation_cost_var.values())
        variables.extend(self.__asset_variable_operational_cost_var.values())
        variables.extend(self.__asset_max_size_var.values())
        variables.extend(self.__asset_aggregation_count_var.values())
        variables.extend(self.__pipe_topo_max_discharge_var.values())
        variables.extend(self.__pipe_topo_global_pipe_class_count_var.values())
        variables.extend(self.__pipe_topo_pipe_class_discharge_ordering_var.values())
        variables.extend(self.__pipe_topo_pipe_class_cost_ordering_var.values())
        variables.extend(self.__pipe_topo_pipe_class_heat_loss_ordering_var.values())
        variables.extend(self.__pipe_topo_heat_loss_var.values())
        return variables

    @property
    def path_variables(self):
        """
        In this function we add all the path variables defined in the HeatMixin to the
        optimization problem. Note that path_variables are variables that are created for each
        time-step.
        """
        variables = super().path_variables.copy()
        variables.extend(self.__flow_direct_var.values())
        variables.extend(self.__pipe_disconnect_var.values())
        variables.extend(self.__check_valve_status_var.values())
        variables.extend(self.__control_valve_direction_var.values())
        variables.extend(self.__demand_insulation_class_var.values())
        variables.extend(self._change_setpoint_var.values())
        variables.extend(self.__temperature_regime_var.values())
        variables.extend(self.__carrier_selected_var.values())
        variables.extend(self.__disabled_hex_var.values())
        variables.extend(self.__cumulative_investments_made_in_eur_var.values())
        variables.extend(self.__asset_is_realized_var.values())
        variables.extend(self.__pipe_topo_heat_loss_path_var.values())
        return variables

    def variable_is_discrete(self, variable):
        """
        All variables that only can take integer values should be added to this function.
        """
        if (
            variable in self.__flow_direct_var
            or variable in self.__pipe_disconnect_var
            or variable in self.__check_valve_status_var
            or variable in self.__control_valve_direction_var
            or variable in self.__pipe_topo_pipe_class_var
            or variable in self.__demand_insulation_class_var
            or variable in self._change_setpoint_var
            or variable in self.__carrier_selected_var
            or variable in self.__disabled_hex_var
            or variable in self.__asset_aggregation_count_var
            or variable in self.__asset_is_realized_var
            or variable in self.__pipe_topo_pipe_class_discharge_ordering_var
            or variable in self.__pipe_topo_pipe_class_cost_ordering_var
            or variable in self.__pipe_topo_pipe_class_heat_loss_ordering_var
        ):
            return True
        else:
            return super().variable_is_discrete(variable)

    def variable_nominal(self, variable):
        """
        In this function we add all the nominals for the variables defined/added in the HeatMixin.
        """
        if variable in self.__pipe_topo_diameter_nominals:
            return self.__pipe_topo_diameter_nominals[variable]
        elif variable in self.__pipe_topo_heat_loss_nominals:
            return self.__pipe_topo_heat_loss_nominals[variable]
        elif variable in self.__pipe_topo_cost_nominals:
            return self.__pipe_topo_cost_nominals[variable]
        elif variable in self.__asset_fixed_operational_cost_nominals:
            return self.__asset_fixed_operational_cost_nominals[variable]
        elif variable in self.__asset_investment_cost_nominals:
            return self.__asset_investment_cost_nominals[variable]
        elif variable in self.__asset_variable_operational_cost_nominals:
            return self.__asset_variable_operational_cost_nominals[variable]
        elif variable in self.__asset_max_size_nominals:
            return self.__asset_max_size_nominals[variable]
        elif variable in self.__asset_installation_cost_nominals:
            return self.__asset_installation_cost_nominals[variable]
        elif variable in self.__cumulative_investments_made_in_eur_nominals:
            return self.__cumulative_investments_made_in_eur_nominals[variable]
        elif variable in self.__pipe_topo_max_discharge_nominals:
            return self.__pipe_topo_max_discharge_nominals[variable]
        else:
            return super().variable_nominal(variable)

    def bounds(self):
        """
        In this function we add the bounds to the problem for all the variables defined/added in
        the HeatMixin.
        """
        bounds = super().bounds()
        bounds.update(self.__flow_direct_bounds)
        bounds.update(self.__pipe_disconnect_var_bounds)
        bounds.update(self.__check_valve_status_var_bounds)
        bounds.update(self.__control_valve_direction_var_bounds)
        bounds.update(self.__buffer_t0_bounds)
        bounds.update(self.__pipe_topo_pipe_class_var_bounds)
        bounds.update(self.__demand_insulation_class_var_bounds)
        bounds.update(self.__pipe_topo_diameter_var_bounds)
        bounds.update(self.__pipe_topo_cost_var_bounds)
        bounds.update(self.__pipe_topo_heat_loss_var_bounds)
        bounds.update(self.__pipe_topo_heat_discharge_bounds)
        bounds.update(self._change_setpoint_bounds)
        bounds.update(self.__temperature_regime_var_bounds)
        bounds.update(self.__carrier_selected_var_bounds)
        bounds.update(self.__disabled_hex_var_bounds)
        bounds.update(self.__asset_fixed_operational_cost_bounds)
        bounds.update(self.__asset_investment_cost_bounds)
        bounds.update(self.__asset_installation_cost_bounds)
        bounds.update(self.__asset_variable_operational_cost_bounds)
        bounds.update(self.__asset_max_size_bounds)
        bounds.update(self.__asset_aggregation_count_var_bounds)
        bounds.update(self.__asset_is_realized_bounds)
        bounds.update(self.__cumulative_investments_made_in_eur_bounds)
        bounds.update(self.__pipe_topo_max_discharge_var_bounds)
        bounds.update(self.__pipe_topo_global_pipe_class_count_var_bounds)
        bounds.update(self.__pipe_topo_pipe_class_discharge_ordering_var_bounds)
        bounds.update(self.__pipe_topo_pipe_class_cost_ordering_var_bounds)
        bounds.update(self.__pipe_topo_pipe_class_heat_loss_ordering_var_bounds)
        return bounds

    def _pipe_heat_loss(
        self,
        options,
        parameters,
        p: str,
        u_values: Optional[Tuple[float, float]] = None,
        temp: float = None,
    ):
        """
        The heat losses have three components:

        - dependency on the pipe temperature
        - dependency on the ground temperature
        - dependency on temperature difference between the supply/return line.

        This latter term assumes that the supply and return lines lie close
        to, and thus influence, each other. I.e., the supply line loses heat
        that is absorbed by the return line. Note that the term dtemp is
        positive when the pipe is in the supply line and negative otherwise.
        """
        if options["neglect_pipe_heat_losses"]:
            return 0.0

        neighbour = self.has_related_pipe(p)

        if u_values is None:
            u_kwargs = {
                "inner_diameter": parameters[f"{p}.diameter"],
                "insulation_thicknesses": parameters[f"{p}.insulation_thickness"],
                "conductivities_insulation": parameters[f"{p}.conductivity_insulation"],
                "conductivity_subsoil": parameters[f"{p}.conductivity_subsoil"],
                "depth": parameters[f"{p}.depth"],
                "h_surface": parameters[f"{p}.h_surface"],
                "pipe_distance": parameters[f"{p}.pipe_pair_distance"],
            }

            # NaN values mean we use the function default
            u_kwargs = {k: v for k, v in u_kwargs.items() if not np.all(np.isnan(v))}
            u_1, u_2 = heat_loss_u_values_pipe(**u_kwargs, neighbour=neighbour)
        else:
            u_1, u_2 = u_values

        length = parameters[f"{p}.length"]
        temperature = parameters[f"{p}.temperature"]
        if temp is not None:
            temperature = temp
        temperature_ground = parameters[f"{p}.T_ground"]
        if neighbour:
            if self.is_hot_pipe(p):
                dtemp = temperature - parameters[f"{self.hot_to_cold_pipe(p)}.temperature"]
            else:
                dtemp = temperature - parameters[f"{self.cold_to_hot_pipe(p)}.temperature"]
        else:
            dtemp = 0

        # if no return/supply pipes can be linked to eachother, the influence of the heat of the
        # neighbouring pipes can also not be determined and thus no influence is assumed
        # (distance between pipes to infinity)
        # This results in Rneighbour -> 0 and therefore u2->0, u1-> 1/(Rsoil+Rins)

        heat_loss = (
            length * (u_1 - u_2) * temperature
            - (length * (u_1 - u_2) * temperature_ground)
            + (length * u_2 * dtemp)
        )

        if heat_loss < 0:
            raise Exception(f"Heat loss of pipe {p} should be nonnegative.")

        return heat_loss

    def parameters(self, ensemble_member):
        """
        In this function we adapt the parameters object to avoid issues with accidentally using
        variables as constants.
        """
        parameters = super().parameters(ensemble_member)

        # To avoid mistakes by accidentally using the `diameter`, `area` and `Heat_loss`
        # parameters in e.g. constraints when those are variable, we set them
        # to NaN in that case. In post(), they are set to their resulting
        # values once again.
        if self.__pipe_topo_diameter_area_parameters:
            parameters.update(self.__pipe_topo_diameter_area_parameters[ensemble_member])
        if self.__pipe_topo_heat_loss_parameters:
            parameters.update(self.__pipe_topo_heat_loss_parameters[ensemble_member])

        return parameters

    def __get_maximum_total_head_loss(self):
        """
        Get an upper bound on the maximum total head loss that can be used in
        big-M formulations of e.g. check valves and disconnectable pipes.

        There are multiple ways to calculate this upper bound, depending on
        what options are set. We compute all these upper bounds, and return
        the lowest one of them.
        """

        options = self.heat_network_options()
        components = self.heat_network_components

        if options["head_loss_option"] == HeadLossOption.NO_HEADLOSS:
            # Undefined, and all constraints using this methods value should
            # be skipped.
            return np.nan

        # Summing head loss in pipes
        max_sum_dh_pipes = 0.0

        for ensemble_member in range(self.ensemble_size):
            parameters = self.parameters(ensemble_member)

            head_loss = 0.0

            for pipe in components.get("pipe", []):
                try:
                    pipe_classes = self.__pipe_topo_pipe_class_map[pipe].keys()
                    head_loss += max(
                        self._hn_pipe_head_loss(
                            pipe, options, parameters, pc.maximum_discharge, pipe_class=pc
                        )
                        for pc in pipe_classes
                        if pc.maximum_discharge > 0.0
                    )
                except KeyError:
                    area = parameters[f"{pipe}.area"]
                    max_discharge = options["maximum_velocity"] * area
                    head_loss += self._hn_pipe_head_loss(pipe, options, parameters, max_discharge)

            head_loss += options["minimum_pressure_far_point"] * 10.2

            max_sum_dh_pipes = max(max_sum_dh_pipes, head_loss)

        # Maximum pressure difference allowed with user options
        # NOTE: Does not yet take elevation differences into acccount
        max_dh_network_options = (
            options["pipe_maximum_pressure"] - options["pipe_minimum_pressure"]
        ) * 10.2

        return min(max_sum_dh_pipes, max_dh_network_options)

    def __check_buffer_values_and_set_bounds_at_t0(self):
        """
        In this function we force the buffer at t0 to have a certain amount of set energy in it.
        We do this via the bounds, by providing the bounds with a time-series where the first
        element is the initial heat in the buffer.
        """
        t = self.times()
        # We assume that t0 is always equal to self.times()[0]
        assert self.initial_time == self.times()[0]

        parameters = self.parameters(0)
        bounds = self.bounds()
        components = self.heat_network_components
        buffers = components.get("buffer", [])

        for b in buffers:
            min_fract_vol = parameters[f"{b}.min_fraction_tank_volume"]
            if min_fract_vol < 0.0 or min_fract_vol >= 1.0:
                raise Exception(
                    f"Minimum fraction of tank capacity of {b} must be smaller"
                    "than 1.0 and larger or equal to 0.0"
                )

            cp = parameters[f"{b}.cp"]
            rho = parameters[f"{b}.rho"]
            dt = parameters[f"{b}.dT"]
            heat_t0 = parameters[f"{b}.init_Heat"]
            vol_t0 = parameters[f"{b}.init_V_hot_tank"]
            stored_heat = f"{b}.Stored_heat"
            if not np.isnan(vol_t0) and not np.isnan(heat_t0):
                raise Exception(
                    f"At most one between the initial heat and volume of {b} should be prescribed."
                )

            if np.isnan(heat_t0):
                if not np.isnan(vol_t0):
                    # Extract information from volume
                    heat_t0 = vol_t0 * dt * cp * rho
                else:
                    # Set default value
                    volume = parameters[f"{b}.volume"]
                    default_vol_t0 = min_fract_vol * volume
                    heat_t0 = default_vol_t0 * dt * cp * rho

            # Check that volume/initial stored heat at t0 is within bounds
            lb_heat, ub_heat = bounds[stored_heat]
            lb_heat_t0 = np.inf
            ub_heat_t0 = -np.inf
            for bound in [lb_heat, ub_heat]:
                assert not isinstance(
                    bound, np.ndarray
                ), f"{b} stored heat cannot be a vector state"
                if isinstance(bound, Timeseries):
                    bound_t0 = bound.values[0]
                else:
                    bound_t0 = bound
                lb_heat_t0 = min(lb_heat_t0, bound_t0)
                ub_heat_t0 = max(ub_heat_t0, bound_t0)

            if heat_t0 < lb_heat_t0 or heat_t0 > ub_heat_t0:
                raise Exception(f"Initial heat of {b} is not within bounds.")

            # Set heat at t0
            lb = np.full_like(t, -np.inf)
            ub = np.full_like(t, np.inf)
            lb[0] = heat_t0
            ub[0] = heat_t0
            b_t0 = (Timeseries(t, lb), Timeseries(t, ub))
            self.__buffer_t0_bounds[stored_heat] = self.merge_bounds(bounds[stored_heat], b_t0)

    def __heat_matching_demand_insulation_constraints(self, ensemble_member):
        """
        Consider all possible heat demand insulation options (each options has an assosiated unique
        demand profile for the specific demand) and add constraints such that only one insulation
        options is activated per demand. The constraints will then ensure aim to match the supply
        and demand.

        Note:
        - This function is only active when the "include_demand_insulation_options" (False by
        default) has been set to True in the heat network options.
        - Currently this functional requires that all demands have at least one insualtion option is
        specified for every demand in the heat network.
        """

        constraints = []
        for dmnd in self.heat_network_components["demand"]:
            heat_demand = self.__state_vector_scaled(f"{dmnd}.Heat_demand", ensemble_member)
            target_demand = self.get_timeseries(f"{dmnd}.target_heat_demand")

            try:
                demand_insulation_classes = self.__demand_insulation_class_map[dmnd]
                is_insulation_active = []
                demand_profile_for_this_class = []
                big_m = []  # big_m for every insulation class
                nominal = []
                for pc, pc_var_name in demand_insulation_classes.items():
                    # Create a demand profile for every insulation level option for this demand
                    demand_profile_for_this_class.append(
                        pc.demand_scaling_factor * target_demand.values[: (len(self.times()))]
                    )
                    # There might be a large differnece between profiles of different insulation
                    # classes. Therefor create variables below per profile (per insulation class)
                    big_m.append(2.0 * max(demand_profile_for_this_class[-1]))
                    nominal.append(np.median(demand_profile_for_this_class[-1]))

                    # Create integer variable to activated/deactivate (1/0) a demand insulation
                    is_insulation_active_var = self.extra_variable(pc_var_name, ensemble_member)
                    # Demand insulation activation variable for each time step of demand profile
                    is_insulation_active.append(
                        ca.repmat(
                            is_insulation_active_var,
                            len(target_demand.values[: (len(self.times()))]),
                        )
                    )
                # Add constraint to enforce that only 1 demand insulation can be active
                # per time step for a specific demand
                for itstep in range(len(target_demand.values[: (len(self.times()))])):
                    is_insulation_active_sum_per_timestep = 0
                    for iclasses in range(len(demand_profile_for_this_class)):
                        is_insulation_active_sum_per_timestep = (
                            is_insulation_active_sum_per_timestep
                            + is_insulation_active[iclasses][itstep]
                        )
                    constraints.append((is_insulation_active_sum_per_timestep, 1.0, 1.0))

                # Adding constraints for the entire time horizon per demand insulation
                for iclasses in range(len(demand_profile_for_this_class)):
                    for itstep in range(len(demand_profile_for_this_class[iclasses])):
                        constraints.append(
                            (
                                (
                                    heat_demand[itstep]
                                    - demand_profile_for_this_class[iclasses][itstep]
                                    + big_m[iclasses]
                                    * (1.0 - is_insulation_active[iclasses][itstep])
                                )
                                / nominal[iclasses],
                                0.0,
                                np.inf,
                            )
                        )
                        constraints.append(
                            (
                                (
                                    heat_demand[itstep]
                                    - demand_profile_for_this_class[iclasses][itstep]
                                    - big_m[iclasses]
                                    * (1.0 - is_insulation_active[iclasses][itstep])
                                )
                                / nominal[iclasses],
                                -np.inf,
                                0.0,
                            )
                        )
            except KeyError:
                raise Exception(
                    "Add a DemandInsulationClass with a demand_scaling_factor value =1.0 for "
                    "demand: {dmnd}"
                )
        return constraints

    def __pipe_rate_heat_change_constraints(self, ensemble_member):
        """
        To avoid sudden change in heat from a timestep to the next,
        constraints on d(Heat)/dt are introduced.
        Information of restrictions on dQ/dt and dT/dt are used, as d(Heat)/dt is
        proportional to average_temperature * dQ/dt + average_discharge * dT/dt.
        The average discharge is computed using the assumption that the average velocity is 1 m/s.
        """
        constraints = []

        parameters = self.parameters(ensemble_member)
        hn_options = self.heat_network_options()

        t_change = hn_options["maximum_temperature_der"]
        q_change = hn_options["maximum_flow_der"]

        if np.isfinite(t_change) and np.isfinite(q_change):
            assert (
                not self.__pipe_topo_pipe_class_map
            ), "heat rate change constraints not allowed with topology optimization"

        for p in self.heat_network_components.get("pipe", []):
            variable = f"{p}.HeatIn.Heat"
            dt = np.diff(self.times(variable))

            canonical, sign = self.alias_relation.canonical_signed(variable)
            source_temperature_out = sign * self.state_vector(canonical, ensemble_member)

            # Maximum differences are expressed per hour. We scale appropriately.
            cp = parameters[f"{p}.cp"]
            rho = parameters[f"{p}.rho"]
            area = parameters[f"{p}.area"]
            avg_t = parameters[f"{p}.temperature"]
            # Assumption: average velocity is 1 m/s
            avg_v = 1
            avg_q = avg_v * area
            heat_change = cp * rho * (t_change / 3600 * avg_q + q_change / 3600 * avg_t)

            if heat_change < 0:
                raise Exception(f"Heat change of pipe {p} should be nonnegative.")
            elif not np.isfinite(heat_change):
                continue

            var_cur = source_temperature_out[1:]
            var_prev = source_temperature_out[:-1]
            variable_nominal = self.variable_nominal(variable)

            constraints.append(
                (
                    var_cur - var_prev,
                    -heat_change * dt / variable_nominal,
                    heat_change * dt / variable_nominal,
                )
            )

        return constraints

    def __node_heat_mixing_path_constraints(self, ensemble_member):
        """
        This function adds constraints for each heat network node/joint to have as much
        thermal power (Heat variable) going in as out. Effectively, it is setting the sum of
        thermal powers to zero.
        """
        constraints = []

        for node, connected_pipes in self.heat_network_topology.nodes.items():
            heat_sum = 0.0
            heat_nominals = []

            for i_conn, (_pipe, orientation) in connected_pipes.items():
                heat_conn = f"{node}.HeatConn[{i_conn + 1}].Heat"
                heat_sum += orientation * self.state(heat_conn)
                heat_nominals.append(self.variable_nominal(heat_conn))

            heat_nominal = np.median(heat_nominals)
            constraints.append((heat_sum / heat_nominal, 0.0, 0.0))

        return constraints

    def __gas_node_heat_mixing_path_constraints(self, ensemble_member):
        """
        This function adds constraints for each gas network node/joint to have as much
        flow going in as out. Effectively, it is setting the sum of flow to zero.
        """
        constraints = []

        for node, connected_pipes in self.heat_network_topology.gas_nodes.items():
            q_sum = 0.0
            q_nominals = []

            for i_conn, (_pipe, orientation) in connected_pipes.items():
                gas_conn = f"{node}.GasConn[{i_conn + 1}].Q"
                q_sum += orientation * self.state(gas_conn)
                q_nominals.append(self.variable_nominal(gas_conn))

            q_nominal = np.median(q_nominals)
            constraints.append((q_sum / q_nominal, 0.0, 0.0))

            q_sum = 0.0
            q_nominals = []

            for i_conn, (_pipe, orientation) in connected_pipes.items():
                gas_conn = f"{node}.GasConn[{i_conn + 1}].Q_shadow"
                q_sum += orientation * self.state(gas_conn)
                q_nominals.append(self.variable_nominal(gas_conn))

            q_nominal = np.median(q_nominals)
            constraints.append((q_sum / q_nominal, 0.0, 0.0))

        return constraints

    def __node_discharge_mixing_path_constraints(self, ensemble_member):
        """
        This function adds constraints to ensure that the incoming volumetric flow equals the
        outgoing volumetric flow. We assume constant density throughout a hydraulically coupled
        system and thus these constraints are needed for mass conservation.
        """
        constraints = []

        for node, connected_pipes in self.heat_network_topology.nodes.items():
            q_sum = 0.0
            q_nominals = []

            for i_conn, (_pipe, orientation) in connected_pipes.items():
                q_conn = f"{node}.HeatConn[{i_conn + 1}].Q"
                q_sum += orientation * self.state(q_conn)
                q_nominals.append(self.variable_nominal(q_conn))

            q_nominal = np.median(q_nominals)
            constraints.append((q_sum / q_nominal, 0.0, 0.0))

        return constraints

    def __heat_loss_path_constraints(self, ensemble_member):
        """
        This function adds the constraints to subtract the heat losses from the thermal power that
        propagates through the network. Note that this is done only on the thermal power, as such
        only energy losses are accounted for, temperature losses are not considered.

        There are a few cases for the heat loss constraints
        - Heat losses are constant: This is the case when the pipe class is constant and the
        network temperature is constant. In this case the symbol for the heat-loss is fixed by its
        lower and upper bound to a value.
        - Heat losses depend on pipe_class: In this case the heat loss depend on the pipe class
        selected by the optimization. In this case the heat losses can vary due to the varying
        radiation surface and different insulation materials applied to the pipe. Note that the
        influences of varying pipe class are taken into account while setting the heat-loss
        variable in topology constraints.
        - Heat losses depend on varying network temperature: In this case the heat loss varies due
        to the different delta temperature with ambient. Note that the heat loss symbol does not
        account for the varying temperature. Therefore, the big_m formulation is needed in these
        constraints.
        - Heat losses depend both on varying network temperature and pipe classes: In this case
        both pipe class and delta temperature with ambient vary
        - neglect_pipe_heat_losses:
        """
        # TODO: Massively simplify this function by setting the heat loss symbol also for varying
        #  temperature. All cases should then be solved with the same set of equations in this
        #  function.
        constraints = []
        options = self.heat_network_options()

        for p in self.heat_network_components.get("pipe", []):
            heat_in = self.state(f"{p}.HeatIn.Heat")
            heat_out = self.state(f"{p}.HeatOut.Heat")
            heat_nominal = self.variable_nominal(f"{p}.HeatIn.Heat")

            big_m = 2.0 * np.max(
                np.abs(
                    (
                        *self.bounds()[f"{p}.HeatIn.Heat"],
                        *self.bounds()[f"{p}.HeatOut.Heat"],
                    )
                )
            )

            is_disconnected_var = self.__pipe_disconnect_map.get(p)

            if is_disconnected_var is None:
                is_disconnected = 0.0
            else:
                is_disconnected = self.state(is_disconnected_var)

            if p in self.__pipe_topo_heat_loss_map:
                # Heat loss is variable depending on pipe class
                heat_loss_sym_name = self.__pipe_topo_heat_loss_map[p]
                try:
                    heat_loss = self.variable(heat_loss_sym_name)
                except KeyError:
                    heat_loss = self.__pipe_topo_heat_loss_path_var[heat_loss_sym_name]
                heat_loss_nominal = self.variable_nominal(heat_loss_sym_name)
                constraint_nominal = (heat_nominal * heat_loss_nominal) ** 0.5

                if options["heat_loss_disconnected_pipe"]:
                    constraints.append(
                        (
                            (heat_in - heat_out - heat_loss) / constraint_nominal,
                            0.0,
                            0.0,
                        )
                    )
                else:
                    # Force heat loss to `heat_loss` when pipe is connected, and zero otherwise.
                    heat_loss_nominal = self.__pipe_topo_heat_loss_nominals[heat_loss_sym_name]
                    constraint_nominal = (big_m * heat_loss_nominal) ** 0.5

                    # Force heat loss to `heat_loss` when pipe is connected.
                    constraints.append(
                        (
                            (heat_in - heat_out - heat_loss - is_disconnected * big_m)
                            / constraint_nominal,
                            -np.inf,
                            0.0,
                        )
                    )
                    constraints.append(
                        (
                            (heat_in - heat_out - heat_loss + is_disconnected * big_m)
                            / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )
        return constraints

    @staticmethod
    def __get_abs_max_bounds(*bounds):
        """
        This function returns the absolute maximum of the bounds given. Note that bounds can also be
        a timeseries.
        """
        max_ = 0.0

        for b in bounds:
            if isinstance(b, np.ndarray):
                max_ = max(max_, max(abs(b)))
            elif isinstance(b, Timeseries):
                max_ = max(max_, max(abs(b.values)))
            else:
                max_ = max(max_, abs(b))

        return max_

    def __flow_direction_path_constraints(self, ensemble_member):
        """
        This function adds constraints to set the direction in pipes and determine whether a pipe
        is utilized at all (is_disconnected variable).

        Whether a pipe is connected is based upon whether flow passes through that pipe.

        The directions are set based upon the directions of how thermal power propegates. This is
        done based upon the sign of the Heat variable. Where positive Heat means a positive
        direction and negative heat means a negative direction. By default, positive is defined from
        HeatIn to HeatOut.

        Finally, a minimum flow can be set. This can sometimes be useful for numerical stability.
        """
        constraints = []
        options = self.heat_network_options()
        parameters = self.parameters(ensemble_member)

        minimum_velocity = options["minimum_velocity"]
        maximum_velocity = options["maximum_velocity"]

        # Also ensure that the discharge has the same sign as the heat.
        for p in self.heat_network_components.get("pipe", []):
            flow_dir_var = self.__pipe_to_flow_direct_map[p]
            flow_dir = self.state(flow_dir_var)

            is_disconnected_var = self.__pipe_disconnect_map.get(p)

            if is_disconnected_var is None:
                is_disconnected = 0.0
            else:
                is_disconnected = self.state(is_disconnected_var)

            q_pipe = self.state(f"{p}.Q")
            heat_in = self.state(f"{p}.HeatIn.Heat")
            heat_out = self.state(f"{p}.HeatOut.Heat")

            try:
                pipe_classes = self.__pipe_topo_pipe_class_map[p].keys()
                maximum_discharge = max([c.maximum_discharge for c in pipe_classes])
                var_names = self.__pipe_topo_pipe_class_map[p].values()
                dn_none = self.__pipe_topo_pipe_class_var[list(var_names)[0]]
                minimum_discharge = min(
                    [c.area * minimum_velocity for c in pipe_classes if c.area > 0.0]
                )
            except KeyError:
                maximum_discharge = maximum_velocity * parameters[f"{p}.area"]

                if math.isfinite(minimum_velocity) and minimum_velocity > 0.0:
                    minimum_discharge = minimum_velocity * parameters[f"{p}.area"]
                else:
                    minimum_discharge = 0.0
                dn_none = 0.0

            if maximum_discharge == 0.0:
                maximum_discharge = 1.0
            big_m = 2.0 * (maximum_discharge + minimum_discharge)

            if minimum_discharge > 0.0:
                constraint_nominal = (minimum_discharge * big_m) ** 0.5
            else:
                constraint_nominal = big_m

            # when DN=0 the flow_dir variable can be 0 or 1, thus these constraints then need to be
            # disabled
            constraints.append(
                (
                    (
                        q_pipe
                        - big_m * (flow_dir + dn_none)
                        + (1 - is_disconnected) * minimum_discharge
                    )
                    / constraint_nominal,
                    -np.inf,
                    0.0,
                )
            )
            constraints.append(
                (
                    (
                        q_pipe
                        + big_m * (1 - flow_dir + dn_none)
                        - (1 - is_disconnected) * minimum_discharge
                    )
                    / constraint_nominal,
                    0.0,
                    np.inf,
                )
            )
            big_m = 2.0 * np.max(
                np.abs(
                    (
                        *self.bounds()[f"{p}.HeatIn.Heat"],
                        *self.bounds()[f"{p}.HeatOut.Heat"],
                    )
                )
            )
            # Note we only need one on the heat as the desired behaviour is propegated by the
            # constraints heat_in - heat_out - heat_loss == 0.
            constraints.append(
                (
                    (heat_in - big_m * flow_dir) / big_m,
                    -np.inf,
                    0.0,
                )
            )
            constraints.append(
                (
                    (heat_in + big_m * (1 - flow_dir)) / big_m,
                    0.0,
                    np.inf,
                )
            )

            # If a pipe is disconnected, the discharge should be zero
            if is_disconnected_var is not None:
                big_m = 2.0 * (maximum_discharge + minimum_discharge)
                constraints.append(((q_pipe - (1 - is_disconnected) * big_m) / big_m, -np.inf, 0.0))
                constraints.append(((q_pipe + (1 - is_disconnected) * big_m) / big_m, 0.0, np.inf))
                big_m = 2.0 * np.max(
                    np.abs(
                        (
                            *self.bounds()[f"{p}.HeatIn.Heat"],
                            *self.bounds()[f"{p}.HeatOut.Heat"],
                        )
                    )
                )
                constraints.append(
                    ((heat_in - (1 - is_disconnected) * big_m) / big_m, -np.inf, 0.0)
                )
                constraints.append(((heat_in + (1 - is_disconnected) * big_m) / big_m, 0.0, np.inf))
                constraints.append(
                    ((heat_out - (1 - is_disconnected) * big_m) / big_m, -np.inf, 0.0)
                )
                constraints.append(
                    ((heat_out + (1 - is_disconnected) * big_m) / big_m, 0.0, np.inf)
                )

        # Pipes that are connected in series should have the same heat direction.
        for pipes in self.heat_network_topology.pipe_series:
            if len(pipes) <= 1:
                continue

            assert (
                len({p for p in pipes if self.is_cold_pipe(p)}) == 0
            ), "Pipe series for Heat models should only contain hot pipes"

            base_flow_dir_var = self.state(self.__pipe_to_flow_direct_map[pipes[0]])

            for p in pipes[1:]:
                flow_dir_var = self.state(self.__pipe_to_flow_direct_map[p])
                constraints.append((base_flow_dir_var - flow_dir_var, 0.0, 0.0))

        return constraints

    def __demand_heat_to_discharge_path_constraints(self, ensemble_member):
        """
        This function adds constraints linking the flow to the thermal power at the demand assets.
        We use an equality constraint on the outgoing flow for every non-pipe asset. Meaning that we
        equate Q * rho * cp * T == Heat for outgoing flows, and inequalities for the heat carried
        in the pipes. This means that the heat can decrease in the network to compensate losses,
        but that the losses and thus flow will always be over-estimated with the temperature for
        which no temperature drops are modelled.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        for d in self.heat_network_components.get("demand", []):
            heat_nominal = parameters[f"{d}.Heat_nominal"]
            cp = parameters[f"{d}.cp"]
            rho = parameters[f"{d}.rho"]
            # TODO: future work - some sort of correction factor to account for temp drop n pipe:
            # (maximum/average lenght fromm source to demand) * V_nominal * temperature_loss_factor
            discharge = self.state(f"{d}.Q")
            heat_out = self.state(f"{d}.HeatOut.Heat")

            ret_carrier = parameters[f"{d}.T_return_id"]
            return_temperatures = self.temperature_regimes(ret_carrier)
            big_m = 2.0 * self.bounds()[f"{d}.HeatOut.Heat"][1]

            if len(return_temperatures) == 0:
                constraints.append(
                    (
                        (heat_out - discharge * cp * rho * parameters[f"{d}.T_return"])
                        / heat_nominal,
                        0.0,
                        0.0,
                    )
                )
            else:
                for return_temperature in return_temperatures:
                    ret_temperature_is_selected = self.state(f"{ret_carrier}_{return_temperature}")
                    constraints.append(
                        (
                            (
                                heat_out
                                - discharge * cp * rho * return_temperature
                                + (1.0 - ret_temperature_is_selected) * big_m
                            )
                            / heat_nominal,
                            0.0,
                            np.inf,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_out
                                - discharge * cp * rho * return_temperature
                                - (1.0 - ret_temperature_is_selected) * big_m
                            )
                            / heat_nominal,
                            -np.inf,
                            0.0,
                        )
                    )

        return constraints

    def __source_heat_to_discharge_path_constraints(self, ensemble_member):
        """
        This function adds constraints linking the flow to the thermal power at the demand assets.
        We use an equality constraint on the outgoing flow for every non-pipe asset. Meaning that we
        equate Q * rho * cp * T == Heat for outgoing flows, and inequalities for the heat carried
        in the pipes. This means that the heat can decrease in the network to compensate losses,
        but that the losses and thus flow will always be over-estimated with the temperature for
        which no temperature drops are modelled.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        for s in self.heat_network_components.get("source", []):
            heat_nominal = parameters[f"{s}.Heat_nominal"]
            q_nominal = self.variable_nominal(f"{s}.Q")
            cp = parameters[f"{s}.cp"]
            rho = parameters[f"{s}.rho"]
            dt = parameters[f"{s}.dT"]

            discharge = self.state(f"{s}.Q")
            heat_out = self.state(f"{s}.HeatOut.Heat")

            constraint_nominal = (heat_nominal * cp * rho * dt * q_nominal) ** 0.5

            sup_carrier = parameters[f"{s}.T_supply_id"]
            supply_temperatures = self.temperature_regimes(sup_carrier)
            big_m = 2.0 * self.bounds()[f"{s}.HeatOut.Heat"][1]

            if len(supply_temperatures) == 0:
                constraints.append(
                    (
                        (heat_out - discharge * cp * rho * parameters[f"{s}.T_supply"])
                        / heat_nominal,
                        0.0,
                        0.0,
                    )
                )
            else:
                for supply_temperature in supply_temperatures:
                    sup_temperature_is_selected = self.state(f"{sup_carrier}_{supply_temperature}")

                    constraints.append(
                        (
                            (
                                heat_out
                                - discharge * cp * rho * supply_temperature
                                + (1.0 - sup_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_out
                                - discharge * cp * rho * supply_temperature
                                - (1.0 - sup_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            -np.inf,
                            0.0,
                        )
                    )

        return constraints

    def __pipe_hydraulic_power_path_constraints(self, ensemble_member):
        """
        This function adds constraints to compute the hydraulic power that is needed to realize the
        flow, compensating the pressure drop through the pipe. Similar to the head loss constraints
        we allow two supported methods. 1) a single linear line between 0 to max velocity. 2) A
        multiple line inequality approach where one can use the minimize_head_losses == True option
        to drag down the solution to the actual physical solution.

        Note that the linearizations are made separately from the pressure drop constraints, this is
        done to avoid "stacked" overestimations.
        """
        constraints = []
        options = self.heat_network_options()

        if options["head_loss_option"] != HeadLossOption.NO_HEADLOSS:
            parameters = self.parameters(ensemble_member)
            components = self.heat_network_components

            for pipe in components.get("pipe", []):
                if parameters[f"{pipe}.length"] == 0.0:
                    # If the pipe does not have a control valve, the head loss is
                    # forced to zero via bounds. If the pipe _does_ have a control
                    # valve, then there still is no relationship between the
                    # discharge and the hydraulic_power.
                    continue

                head_loss_option = self._hn_get_pipe_head_loss_option(pipe, options, parameters)
                assert (
                    head_loss_option != HeadLossOption.NO_HEADLOSS
                ), "This method should be skipped when NO_HEADLOSS is set."

                discharge = self.state(f"{pipe}.Q")
                hydraulic_power = self.state(f"{pipe}.Hydraulic_power")
                rho = parameters[f"{pipe}.rho"]

                # 0: pipe is connected, 1: pipe is disconnected
                is_disconnected_var = self.__pipe_disconnect_map.get(pipe)
                if is_disconnected_var is None:
                    is_disconnected = 0.0
                else:
                    is_disconnected = self.state(is_disconnected_var)

                flow_dir_var = self.__pipe_to_flow_direct_map[pipe]
                flow_dir = self.state(flow_dir_var)  # 0/1: negative/positive flow direction

                if pipe in self.__pipe_topo_pipe_class_map:
                    # Multiple diameter options for this pipe
                    pipe_classes = self.__pipe_topo_pipe_class_map[pipe]
                    max_discharge = max(c.maximum_discharge for c in pipe_classes)
                    for pc, pc_var_name in pipe_classes.items():
                        if pc.inner_diameter == 0.0:
                            continue

                        # Calc max hydraulic power based on maximum_total_head_loss =
                        # f(max_sum_dh_pipes, max_dh_network_options)
                        max_total_hydraulic_power = 2.0 * (
                            rho
                            * GRAVITATIONAL_CONSTANT
                            * self.__maximum_total_head_loss
                            * max_discharge
                        )

                        # is_topo_disconnected - 0: pipe selected, 1: pipe disconnected/not selected
                        # self.__pipe_topo_pipe_class_var - value 0: pipe is not selected, 1: pipe
                        # is selected
                        is_topo_disconnected = 1 - self.__pipe_topo_pipe_class_var[pc_var_name]

                        constraints.extend(
                            self._hydraulic_power(
                                pipe,
                                options,
                                parameters,
                                discharge,
                                hydraulic_power,
                                is_disconnected=is_topo_disconnected + is_disconnected,
                                big_m=max_total_hydraulic_power,
                                pipe_class=pc,
                                flow_dir=flow_dir,
                            )
                        )
                else:
                    is_topo_disconnected = int(parameters[f"{pipe}.diameter"] == 0.0)
                    max_total_hydraulic_power = 2.0 * (
                        rho
                        * GRAVITATIONAL_CONSTANT
                        * self.__maximum_total_head_loss
                        * parameters[f"{pipe}.area"]
                        * options["maximum_velocity"]
                    )
                    constraints.extend(
                        self._hydraulic_power(
                            pipe,
                            options,
                            parameters,
                            discharge,
                            hydraulic_power,
                            is_disconnected=is_disconnected + is_topo_disconnected,
                            big_m=max_total_hydraulic_power,
                            flow_dir=flow_dir,
                        )
                    )
        return constraints

    def __pipe_heat_to_discharge_path_constraints(self, ensemble_member):
        """
        This function adds constraints linking the flow to the thermal power at the pipe assets.
        We use an equality constraint on the outgoing flow for every non-pipe asset. Meaning that we
        equate Q * rho * cp * T == Heat for outgoing flows, and inequalities for the heat carried
        in the pipes. This means that the heat can decrease in the network to compensate losses,
        but that the losses and thus flow will always be over-estimated with the temperature for
        which no temperature drops are modelled.

        There are three cases for the constraint, namely:
        - no heat losses: In this case a single equality constraint can be used.
        - constant network temperature: In this case there is a single set inequality constraints
        - varying network temperature: In this case a set of big_m constraints is used to
        "activate" only the constraints with the selected network temperature.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        sum_heat_losses = 0.0

        for p in self.heat_network_components.get("pipe", []):
            if p in self.__pipe_topo_heat_losses:
                sum_heat_losses += max(self.__pipe_topo_heat_losses[p])
            else:
                sum_heat_losses += parameters[f"{p}.Heat_loss"]

        assert not np.isnan(sum_heat_losses)

        for p in self.heat_network_components.get("pipe", []):
            cp = parameters[f"{p}.cp"]
            rho = parameters[f"{p}.rho"]
            temp = parameters[f"{p}.temperature"]

            flow_dir_var = self.__pipe_to_flow_direct_map[p]
            flow_dir = self.state(flow_dir_var)
            scaled_heat_in = self.state(f"{p}.HeatIn.Heat")  # * heat_to_discharge_fac
            scaled_heat_out = self.state(f"{p}.HeatOut.Heat")  # * heat_to_discharge_fac
            pipe_q = self.state(f"{p}.Q")
            heat_nominal = self.variable_nominal(f"{p}.HeatIn.Heat")

            # We do not want Big M to be too tight in this case, as it results
            # in a rather hard yes/no constraint as far as feasibility on e.g.
            # a single source system is concerned. Use a factor of 2 to give
            # some slack.
            # big_m = 2 * sum_heat_losses * heat_to_discharge_fac
            big_m = 2.0 * np.max(
                np.abs((*self.bounds()[f"{p}.HeatIn.Heat"], *self.bounds()[f"{p}.HeatOut.Heat"]))
            )

            for heat in [scaled_heat_in, scaled_heat_out]:
                if self.heat_network_options()["neglect_pipe_heat_losses"]:
                    constraints.append(
                        (
                            (heat - pipe_q * (cp * rho * temp)) / heat_nominal,
                            0.0,
                            0.0,
                        )
                    )
                else:
                    assert big_m > 0.0

                    carrier = parameters[f"{p}.carrier_id"]
                    temperatures = self.temperature_regimes(carrier)
                    if len(temperatures) == 0:
                        constraints.append(
                            (
                                (heat - pipe_q * (cp * rho * temp) - big_m * (1 - flow_dir))
                                / big_m,
                                -np.inf,
                                0.0,
                            )
                        )
                        constraints.append(
                            (
                                (heat - pipe_q * (cp * rho * temp) + big_m * flow_dir) / big_m,
                                0.0,
                                np.inf,
                            )
                        )
                    elif len(temperatures) > 0:
                        for temperature in temperatures:
                            temperature_is_selected = self.state(f"{carrier}_{temperature}")
                            constraints.append(
                                (
                                    (
                                        heat
                                        - pipe_q * (cp * rho * temperature)
                                        + big_m * flow_dir
                                        + (1.0 - temperature_is_selected) * big_m
                                    )
                                    / big_m,
                                    0.0,
                                    np.inf,
                                )
                            )
                            constraints.append(
                                (
                                    (
                                        heat
                                        - pipe_q * (cp * rho * temperature)
                                        - big_m * (1 - flow_dir)
                                        - (1.0 - temperature_is_selected) * big_m
                                    )
                                    / big_m,
                                    -np.inf,
                                    0.0,
                                )
                            )
        return constraints

    def __storage_heat_to_discharge_path_constraints(self, ensemble_member):
        """
        This function adds constraints linking the flow to the thermal power at the pipe assets.
        We use an equality constraint on the outgoing flow for every non-pipe asset. Meaning that we
        equate Q * rho * cp * T == Heat for outgoing flows, and inequalities for the heat carried
        in the pipes. This means that the heat can decrease in the network to compensate losses,
        but that the losses and thus flow will always be over-estimated with the temperature for
        which no temperature drops are modelled.

        This function adds the constraints relating the discharge to the thermal power at the
        buffer component. This is done following the philosophy described at the heat_to_discharge
        for sources/demands. Where a big_m formulation is used to switch between source and demand
        logic depending on whether the buffer is discharging or charging. For this purpose the
        direction of the connecting supply pipe is used, where a positive direction is charging
        (demand logic) and a negative direction is discharging (source logic). This also means that
        buffers can only be connected with the supply pipe going in positive direction to the
        buffer.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        for b, (
            (hot_pipe, _hot_pipe_orientation),
            (_cold_pipe, _cold_pipe_orientation),
        ) in {**self.heat_network_topology.buffers, **self.heat_network_topology.ates}.items():
            heat_nominal = parameters[f"{b}.Heat_nominal"]
            q_nominal = self.variable_nominal(f"{b}.Q")
            cp = parameters[f"{b}.cp"]
            rho = parameters[f"{b}.rho"]
            dt = parameters[f"{b}.dT"]

            discharge = self.state(f"{b}.HeatIn.Q")
            # Note that `heat_hot` can be negative for the buffer; in that case we
            # are extracting heat from it.
            heat_out = self.state(f"{b}.HeatOut.Heat")
            heat_in = self.state(f"{b}.HeatIn.Heat")

            # We want an _equality_ constraint between discharge and heat if the buffer is
            # consuming (i.e. behaving like a "demand"). We want an _inequality_
            # constraint (`|heat| >= |f(Q)|`) just like a "source" component if heat is
            # extracted from the buffer. We accomplish this by disabling one of
            # the constraints with a boolean. Note that `discharge` and `heat_hot`
            # are guaranteed to have the same sign.
            flow_dir_var = self.__pipe_to_flow_direct_map[hot_pipe]
            is_buffer_charging = self.state(flow_dir_var)

            big_m = 2.0 * np.max(
                np.abs((*self.bounds()[f"{b}.HeatIn.Heat"], *self.bounds()[f"{b}.HeatOut.Heat"]))
            )

            sup_carrier = parameters[f"{b}.T_supply_id"]
            ret_carrier = parameters[f"{b}.T_return_id"]
            supply_temperatures = self.temperature_regimes(sup_carrier)
            return_temperatures = self.temperature_regimes(ret_carrier)

            if len(supply_temperatures) == 0:
                constraint_nominal = (heat_nominal * cp * rho * dt * q_nominal) ** 0.5
                # only when discharging the heat_in should match the heat excactly (like producer)
                constraints.append(
                    (
                        (
                            heat_in
                            - discharge * cp * rho * parameters[f"{b}.T_supply"]
                            + is_buffer_charging * big_m
                        )
                        / constraint_nominal,
                        0.0,
                        np.inf,
                    )
                )
                constraints.append(
                    (
                        (heat_in - discharge * cp * rho * parameters[f"{b}.T_supply"])
                        / constraint_nominal,
                        -np.inf,
                        0.0,
                    )
                )
            else:
                for supply_temperature in supply_temperatures:
                    sup_temperature_is_selected = self.state(f"{sup_carrier}_{supply_temperature}")
                    constraint_nominal = (
                        heat_nominal * cp * rho * supply_temperature * q_nominal
                    ) ** 0.5
                    constraints.append(
                        (
                            (
                                heat_in
                                - discharge * cp * rho * supply_temperature
                                + (1.0 - sup_temperature_is_selected) * big_m
                                + is_buffer_charging * big_m
                            )
                            / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_in
                                - discharge * cp * rho * supply_temperature
                                - (1.0 - sup_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            -np.inf,
                            0.0,
                        )
                    )

            if len(return_temperatures) == 0:
                constraint_nominal = (heat_nominal * cp * rho * dt * q_nominal) ** 0.5
                # Only when consuming/charging the heatout should match the q rho cp Tret
                constraints.append(
                    (
                        (heat_out - discharge * cp * rho * parameters[f"{b}.T_return"])
                        / constraint_nominal,
                        0.0,
                        np.inf,
                    )
                )
                constraints.append(
                    (
                        (
                            heat_out
                            - discharge * cp * rho * parameters[f"{b}.T_return"]
                            - (1.0 - is_buffer_charging) * big_m
                        )
                        / constraint_nominal,
                        -np.inf,
                        0.0,
                    )
                )
            else:
                for return_temperature in return_temperatures:
                    ret_temperature_is_selected = self.state(f"{ret_carrier}_{return_temperature}")
                    constraint_nominal = (
                        heat_nominal * cp * rho * return_temperature * q_nominal
                    ) ** 0.5
                    constraints.append(
                        (
                            (
                                heat_out
                                - discharge * cp * rho * return_temperature
                                + (1.0 - ret_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_out
                                - discharge * cp * rho * return_temperature
                                - (2.0 - ret_temperature_is_selected - is_buffer_charging) * big_m
                            )
                            / constraint_nominal,
                            -np.inf,
                            0.0,
                        )
                    )

        return constraints

    def __setpoint_constraint(
        self, ensemble_member, component_name, windowsize_hr, setpointchanges
    ):
        r"""Constraints that can switch only every n time steps of setpoint.
        A component can only switch setpoint every <windowsize_hr> hours.
        Apply the constraint every timestep from after the first time step onwards [from i=1].

        Inspect example curve below for understanding of dHeat/dt for
        windowsize_hr 12 with a time domain of 35 hourly timesteps.

        Heat
        d                               *-------*
        c                   *-------*
        b   *
        a       *---*---*                           *-------*


        i   0   1   2   3   4       16  17      29  30      35
        """
        assert windowsize_hr > 0
        assert windowsize_hr % 1 == 0
        assert component_name in sum(self.heat_network_components.values(), [])

        # Find the component type
        comp_type = next(
            iter(
                [
                    comptype
                    for comptype, compnames in self.heat_network_components.items()
                    for compname in compnames
                    if compname == component_name
                ]
            )
        )

        constraints = []
        times = self.times()
        control_vars = map_comp_type_to_control_variable[comp_type]
        if not isinstance(control_vars, list):
            control_vars = [control_vars]

        for var_name in control_vars:
            # Retrieve the relevant variable names
            variable_name = f"{component_name}{var_name}"
            var_name_setpoint = self._component_to_change_setpoint_map[component_name]

            # Get the timewise symbolic variables of Heat_source
            sym_var = self.__state_vector_scaled(variable_name, ensemble_member)

            # Get the timewise symbolic variables of the setpoint
            canonical, sign = self.alias_relation.canonical_signed(var_name_setpoint)
            setpoint_is_free = sign * self.state_vector(canonical, ensemble_member)

            # d<variable>/dt expression, forward Euler
            backward_heat_rate_expression = sym_var[:-1] - sym_var[1:]

            # Compute threshold for what is considered a change in setpoint
            big_m = 2.0 * max(self.bounds()[variable_name])
            nominal = self.variable_nominal(variable_name)

            # Constraint which fixes if the variable is allowed to switch or not.
            # With a dynamic sliding window, shifting one timestep.
            # Sum the binairy variables in the window. The sum should be <=1 as only on of the
            # binairy variable is allowed to represent a switch in operations.
            duration_s = 3600 * windowsize_hr

            # Number of elements to be included in a sliding window over time elements
            # Definition of elements: 23 time steps between 24 elements in the times object
            windowsize_dynamic = []
            # TODO: Better/improved/faster search function to be written
            for ij in range(0, len(times)):
                for ii in range(0 + ij, len(times)):
                    if (times[ii] - times[0 + ij]) >= duration_s:
                        windowsize_dynamic.append(ii - (0 + ij) - 1)
                        break
                else:
                    windowsize_dynamic.append(len(times) - 1 - (0 + ij))
                    break

            if len(windowsize_dynamic) == 0:
                windowsize_dynamic.append(len(times))

            for iw in range(0, len(windowsize_dynamic)):
                start_idx = iw
                if windowsize_dynamic[iw] > (len(times) - 1):
                    end_idx = len(times) - 1
                else:
                    end_idx = start_idx + windowsize_dynamic[iw]

                expression = 0.0
                for j in range(start_idx, end_idx + 1):
                    expression += setpoint_is_free[j]
                # This constraint forces that only 1 timestep in the sliding
                # window can have setpoint_is_free=1. In combination with the
                # constraints lower in this function we ensure the desired
                # behavior of limited setpoint changes.
                constraints.append(((setpointchanges - expression), 0.0, np.inf))

            # Constraints for the allowed heat rate of the component.
            # Made 2 constraints which each do or do not constrain the value
            # of the setpoint_is_free var the value of the
            # backward_heat_expression. So the discrete variable does or does
            # not have an influence on making the constrained uphold or not.

            # Note: the equations are not apply at t0

            # NOTE: we start from 2 this is to not constrain the derivative at t0
            for i in range(2, len(times)):
                # Constraining setpoint_is_free to 1 when value of
                # backward_heat_rate_expression < 0, otherwise
                # setpoint_is_free's value can be 0 and 1
                constraints.append(
                    (
                        (backward_heat_rate_expression[i - 1] + setpoint_is_free[i] * big_m)
                        / nominal,
                        0.0,
                        np.inf,
                    )
                )
                # Constraining setpoint_is_free to 1 when value of
                # backward_heat_rate_expression > 0, otherwise
                # setpoint_is_free's value can be 0 and 1
                constraints.append(
                    (
                        (backward_heat_rate_expression[i - 1] - setpoint_is_free[i] * big_m)
                        / nominal,
                        -np.inf,
                        0.0,
                    )
                )

        return constraints

    def __network_temperature_path_constraints(self, ensemble_member):
        """
        This function adds constraints to ensure that only one temperature level is active for the
        supply and return network within one hydraulically coupled system. Furthermore, it sets the
        temperature variable to the temperature associated with the temperature of the integer
        variable.
        """
        constraints = []

        for _carrier, temperatures in self.temperature_carriers().items():
            number = temperatures["id_number_mapping"]
            sum = 0.0
            temperature_regimes = self.temperature_regimes(int(number))
            for temperature in temperature_regimes:
                temp_selected = self.state(f"{int(number)}_{temperature}")
                sum += temp_selected
                temperature_var = self.state(f"{int(number)}_temperature")
                big_m = 2.0 * self.bounds()[f"{int(number)}_temperature"][1]
                # Constraints for setting the temperature variable to the chosen temperature
                constraints.append(
                    (temperature - temperature_var + (1.0 - temp_selected) * big_m, 0.0, np.inf)
                )
                constraints.append(
                    (temperature - temperature_var - (1.0 - temp_selected) * big_m, -np.inf, 0.0)
                )
            if len(temperature_regimes) > 0:
                # Constraint to ensure that one single temperature is chosen for every timestep
                constraints.append((sum, 1.0, 1.0))

        return constraints

    def __heat_exchanger_heat_to_discharge_path_constraints(self, ensemble_member):
        """
        This function adds the heat to discharge constraints of components that connect two
        hydraulically decoupled networks. We assume that there is a dedicated primary side and
        secondary side and that Thermal power can only flow from primary to secondary.

        Following this assumption we use the demand logic to relate heat to discharge at the
        primary side and the source logic for relating heat to discharge at the secondary side.

        This function also adds constraints to ensure physically logical temperatures between the
        primary and secondary side when varying temperature is applied to the optimization.
        Assuming a counter flow heat exchanger, this means that the secondary supply temperature
        will always be below the primary supply temperature and that the primary return temperature
        has to be above the secondary return temperature.

        Finally, an is disabled variable is set for when the heat exchanger is not used. This is
        needed to allow disabling of the HEX temperature constraints when no heat is flowing
        through the HEX.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        # The primary side of the heat exchanger acts like a heat consumer, and the secondary side
        # acts as a heat producer. Essentially using equality constraints to set the heat leaving
        # the secondary side based on the secondary Supply temperature and the heat leaving the
        # primary side based on the primary Return temperature.

        for heat_exchanger in [
            *self.heat_network_components.get("heat_exchanger", []),
            *self.heat_network_components.get("heat_pump", []),
            *self.heat_network_components.get("heat_pump_elec", []),
        ]:
            cp_prim = parameters[f"{heat_exchanger}.Primary.cp"]
            rho_prim = parameters[f"{heat_exchanger}.Primary.rho"]
            cp_sec = parameters[f"{heat_exchanger}.Secondary.cp"]
            rho_sec = parameters[f"{heat_exchanger}.Secondary.rho"]
            dt_prim = parameters[f"{heat_exchanger}.Primary.dT"]
            dt_sec = parameters[f"{heat_exchanger}.Secondary.dT"]
            discharge_primary = self.state(f"{heat_exchanger}.Primary.HeatIn.Q")
            discharge_secondary = self.state(f"{heat_exchanger}.Secondary.HeatOut.Q")
            heat_primary = self.state(f"{heat_exchanger}.Primary_heat")
            heat_out_prim = self.state(f"{heat_exchanger}.Primary.HeatOut.Heat")
            heat_out_sec = self.state(f"{heat_exchanger}.Secondary.HeatOut.Heat")

            constraint_nominal = (
                cp_prim
                * rho_prim
                * dt_prim
                * self.variable_nominal(f"{heat_exchanger}.Primary.HeatIn.Q")
            )

            sup_carrier_prim = parameters[f"{heat_exchanger}.Primary.T_supply_id"]
            ret_carrier_prim = parameters[f"{heat_exchanger}.Primary.T_return_id"]

            supply_temperatures_prim = self.temperature_regimes(sup_carrier_prim)
            return_temperatures_prim = self.temperature_regimes(ret_carrier_prim)

            big_m = 2.0 * self.bounds()[f"{heat_exchanger}.Primary.HeatOut.Heat"][1]

            # primary side
            if len(return_temperatures_prim) == 0:
                constraints.append(
                    (
                        (
                            heat_out_prim
                            - discharge_primary
                            * cp_prim
                            * rho_prim
                            * parameters[f"{heat_exchanger}.Primary.T_return"]
                        )
                        / constraint_nominal,
                        0.0,
                        0.0,
                    )
                )
            else:
                for return_temperature in return_temperatures_prim:
                    ret_temperature_is_selected = self.state(
                        f"{ret_carrier_prim}_{return_temperature}"
                    )
                    constraints.append(
                        (
                            (
                                heat_out_prim
                                - discharge_primary * cp_prim * rho_prim * return_temperature
                                + (1.0 - ret_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_out_prim
                                - discharge_primary * cp_prim * rho_prim * return_temperature
                                - (1.0 - ret_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            -np.inf,
                            0.0,
                        )
                    )

            # Secondary side
            sup_carrier_sec = parameters[f"{heat_exchanger}.Secondary.T_supply_id"]
            ret_carrier_sec = parameters[f"{heat_exchanger}.Secondary.T_return_id"]

            supply_temperatures_sec = self.temperature_regimes(sup_carrier_sec)
            return_temperatures_sec = self.temperature_regimes(ret_carrier_sec)
            big_m = 2.0 * self.bounds()[f"{heat_exchanger}.Secondary.HeatOut.Heat"][1]
            constraint_nominal = (
                cp_sec * rho_sec * dt_sec * self.bounds()[f"{heat_exchanger}.Secondary.HeatIn.Q"][1]
            )

            if len(supply_temperatures_sec) == 0:
                constraints.append(
                    (
                        (
                            heat_out_sec
                            - discharge_secondary
                            * cp_sec
                            * rho_sec
                            * parameters[f"{heat_exchanger}.Secondary.T_supply"]
                        )
                        / constraint_nominal,
                        0.0,
                        0.0,
                    )
                )
            else:
                for supply_temperature in supply_temperatures_sec:
                    sup_temperature_is_selected = self.state(
                        f"{sup_carrier_sec}_{supply_temperature}"
                    )
                    constraints.append(
                        (
                            (
                                heat_out_sec
                                - discharge_secondary * cp_sec * rho_sec * supply_temperature
                                - (1.0 - sup_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            -np.inf,
                            0.0,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_out_sec
                                - discharge_secondary * cp_sec * rho_sec * supply_temperature
                                + (1.0 - sup_temperature_is_selected) * big_m
                            )
                            / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )

            # disconnect HEX
            # Getting var for disabled constraints
            small_m = 0  # 0W
            tol = 1e-5 * big_m  # W
            is_disabled = self.state(self.__disabled_hex_map[heat_exchanger])

            # Constraints to set the disabled integer, note we only set it for the primary
            # side as the secondary side implicetly follows from the energy balance constraints.
            # similar logic in the other blocks
            # This constraints ensures that is_disabled is 0 when heat_primary > 0
            constraints.append(((heat_primary - (1.0 - is_disabled) * big_m) / big_m, -np.inf, 0.0))
            # This constraints ensures that is_disabled is 1 when heat_primary < tol
            constraints.append(
                (
                    (heat_primary - (tol + (small_m - tol) * is_disabled)) / (big_m * tol) ** 0.5,
                    0.0,
                    np.inf,
                )
            )

            if heat_exchanger in self.heat_network_components.get("heat_exchanger", []):
                # Note we don't have to add constraints for the case of no temperature options,
                # as that check is done in the esdl_heat_model
                # Check that secondary supply temperature is lower than that of the primary side
                if len(supply_temperatures_prim) > 0:
                    for t_sup_prim in supply_temperatures_prim:
                        sup_prim_t_is_selected = self.state(f"{sup_carrier_prim}_{t_sup_prim}")
                        if len(supply_temperatures_sec) == 0:
                            t_sup_sec = parameters[f"{heat_exchanger}.Secondary.T_supply"]
                            big_m = 2.0 * t_sup_sec
                            constraints.append(
                                (
                                    (
                                        t_sup_prim
                                        - t_sup_sec
                                        + (is_disabled + (1.0 - sup_prim_t_is_selected)) * big_m
                                    ),
                                    0.0,
                                    np.inf,
                                )
                            )
                        else:
                            for t_sup_sec in supply_temperatures_sec:
                                sup_sec_t_is_selected = self.state(f"{sup_carrier_sec}_{t_sup_sec}")
                                big_m = 2.0 * t_sup_sec
                                constraints.append(
                                    (
                                        (
                                            t_sup_prim * sup_prim_t_is_selected
                                            - t_sup_sec * sup_sec_t_is_selected
                                            + (
                                                is_disabled
                                                + (1.0 - sup_prim_t_is_selected)
                                                + (1.0 - sup_sec_t_is_selected)
                                            )
                                            * big_m
                                        ),
                                        0.0,
                                        np.inf,
                                    )
                                )
                elif len(supply_temperatures_sec) > 0 and len(supply_temperatures_prim) == 0:
                    for t_sup_sec in supply_temperatures_sec:
                        sup_sec_t_is_selected = self.state(f"{sup_carrier_sec}_{t_sup_sec}")
                        t_sup_prim = parameters[f"{heat_exchanger}.Primary.T_supply"]
                        big_m = 2.0 * t_sup_sec
                        constraints.append(
                            (
                                (
                                    t_sup_prim
                                    - t_sup_sec
                                    + (is_disabled + (1.0 - sup_sec_t_is_selected)) * big_m
                                ),
                                0.0,
                                np.inf,
                            )
                        )
                # The check that the chosen return temperature on the primary side is not lower
                # than that of the secondary side
                if len(return_temperatures_prim) > 0:
                    for t_ret_prim in return_temperatures_prim:
                        ret_prim_t_is_selected = self.state(f"{ret_carrier_prim}_{t_ret_prim}")
                        if len(return_temperatures_sec) == 0:
                            t_ret_sec = parameters[f"{heat_exchanger}.Secondary.T_return"]
                            big_m = 2.0 * t_ret_sec
                            constraints.append(
                                (
                                    (
                                        t_ret_prim
                                        - t_ret_sec
                                        + (is_disabled + (1.0 - ret_prim_t_is_selected)) * big_m
                                    ),
                                    0.0,
                                    np.inf,
                                )
                            )
                        else:
                            for t_ret_sec in return_temperatures_sec:
                                ret_sec_t_is_selected = self.state(f"{ret_carrier_sec}_{t_ret_sec}")
                                big_m = 2.0 * t_ret_sec
                                constraints.append(
                                    (
                                        (
                                            t_ret_prim
                                            - t_ret_sec
                                            + (
                                                is_disabled
                                                + (1.0 - ret_sec_t_is_selected)
                                                + (1.0 - ret_prim_t_is_selected)
                                            )
                                            * big_m
                                        ),
                                        0.0,
                                        np.inf,
                                    )
                                )
                elif len(return_temperatures_sec) > 0 and len(return_temperatures_prim) == 0:
                    for t_ret_sec in return_temperatures_sec:
                        ret_sec_t_is_selected = self.state(f"{ret_carrier_sec}_{t_ret_sec}")
                        t_ret_prim = parameters[f"{heat_exchanger}.Primary.T_return"]
                        big_m = 2.0 * t_ret_sec
                        constraints.append(
                            (
                                (
                                    t_ret_prim
                                    - t_ret_sec
                                    + (is_disabled + (1.0 - ret_sec_t_is_selected)) * big_m
                                ),
                                0.0,
                                np.inf,
                            )
                        )

        return constraints

    def __state_vector_scaled(self, variable, ensemble_member):
        """
        This functions returns the casadi symbols scaled with their nominal for the entire time
        horizon.
        """
        canonical, sign = self.alias_relation.canonical_signed(variable)
        return (
            self.state_vector(canonical, ensemble_member) * self.variable_nominal(canonical) * sign
        )

    def _hn_pipe_nominal_discharge(self, heat_network_options, parameters, pipe: str) -> float:
        """
        This functions returns a nominal for the discharge of pipes under topology optimization.
        """
        try:
            pipe_classes = self.__pipe_topo_pipe_class_map[pipe].keys()
            area = np.median(c.area for c in pipe_classes)
        except KeyError:
            area = parameters[f"{pipe}.area"]

        return area * heat_network_options["estimated_velocity"]

    @staticmethod
    def _hn_get_pipe_head_loss_option(pipe, heat_network_options, parameters):
        """
        This function returns the head loss option for a pipe. Note that we assume that we can use
        the more accurate DW linearized approximation when a pipe has a control valve.
        """
        head_loss_option = heat_network_options["head_loss_option"]

        if head_loss_option == HeadLossOption.LINEAR and parameters[f"{pipe}.has_control_valve"]:
            # If there is a control valve present, we use the more accurate
            # Darcy-Weisbach inequality formulation.
            head_loss_option = HeadLossOption.LINEARIZED_DW

        return head_loss_option

    def _hn_pipe_head_loss_constraints(self, ensemble_member):
        """
        This function adds the head loss constraints for pipes. There are two options namely with
        and without pipe class optimization. In both cases we assume that disconnected pipes, pipes
        without flow have no head loss.

        Under pipe-class optimization the head loss constraints per pipe class are added and
        applied with the big_m method (is_topo_disconnected) to only activate the correct
        constraints.

        Under constant pipe class constraints for only one diameter are added.
        """
        constraints = []

        options = self.heat_network_options()
        parameters = self.parameters(ensemble_member)
        components = self.heat_network_components
        # Set the head loss according to the direction in the pipes. Note that
        # the `.__head_loss` symbol is always positive by definition, but that
        # `.dH` is not (positive when flow is negative, and vice versa).
        # If the pipe is disconnected, we leave the .__head_loss symbol free
        # (and it has no physical meaning). We also do not set any discharge
        # relationship in this case (but dH is still equal to Out - In of
        # course).

        for pipe in components.get("pipe", []):
            if parameters[f"{pipe}.length"] == 0.0:
                # If the pipe does not have a control valve, the head loss is
                # forced to zero via bounds. If the pipe _does_ have a control
                # valve, then there still is no relationship between the
                # discharge and the head loss/dH.
                continue

            head_loss_sym = self._hn_pipe_to_head_loss_map[pipe]

            dh = self.__state_vector_scaled(f"{pipe}.dH", ensemble_member)
            head_loss = self.__state_vector_scaled(head_loss_sym, ensemble_member)
            discharge = self.__state_vector_scaled(f"{pipe}.Q", ensemble_member)

            # We need to make sure the dH is decoupled from the discharge when
            # the pipe is disconnected. Simply put, this means making the
            # below constraints trivial.
            is_disconnected_var = self.__pipe_disconnect_map.get(pipe)

            if is_disconnected_var is None:
                is_disconnected = 0.0
            else:
                is_disconnected = self.__state_vector_scaled(is_disconnected_var, ensemble_member)

            max_discharge = None
            max_head_loss = -np.inf

            if pipe in self.__pipe_topo_pipe_class_map:
                # Multiple diameter options for this pipe
                pipe_classes = self.__pipe_topo_pipe_class_map[pipe]
                max_discharge = max(c.maximum_discharge for c in pipe_classes)

                for pc, pc_var_name in pipe_classes.items():
                    if pc.inner_diameter == 0.0:
                        continue

                    head_loss_max_discharge = self._hn_pipe_head_loss(
                        pipe, options, parameters, max_discharge, pipe_class=pc
                    )

                    big_m = max(1.1 * self.__maximum_total_head_loss, 2 * head_loss_max_discharge)

                    is_topo_disconnected = 1 - self.extra_variable(pc_var_name, ensemble_member)
                    is_topo_disconnected = ca.repmat(is_topo_disconnected, dh.size1())

                    # Note that we add the two booleans `is_disconnected` and
                    # `is_topo_disconnected`. This is allowed because of the way the
                    # resulting expression is used in the Big-M formulation. We only care
                    # that the expression (i.e. a single boolean or the sum of the two
                    # booleans) is either 0 when the pipe is connected, or >= 1 when it
                    # is disconnected.
                    constraints.extend(
                        self._hn_pipe_head_loss(
                            pipe,
                            options,
                            parameters,
                            discharge,
                            head_loss,
                            dh,
                            is_disconnected + is_topo_disconnected,
                            big_m,
                            pc,
                        )
                    )

                    # Contrary to the Big-M calculation above, the relation
                    # between dH and the head loss symbol requires the
                    # maximum head loss that can be realized effectively. So
                    # we pass the current pipe class's maximum discharge.
                    max_head_loss = max(
                        max_head_loss,
                        self._hn_pipe_head_loss(
                            pipe, options, parameters, pc.maximum_discharge, pipe_class=pc
                        ),
                    )
            else:
                # Only a single diameter for this pipe. Note that we rely on
                # the diameter parameter being overridden automatically if a
                # single pipe class is set by the user.
                area = parameters[f"{pipe}.area"]
                max_discharge = options["maximum_velocity"] * area

                is_topo_disconnected = int(parameters[f"{pipe}.diameter"] == 0.0)

                constraints.extend(
                    self._hn_pipe_head_loss(
                        pipe,
                        options,
                        parameters,
                        discharge,
                        head_loss,
                        dh,
                        is_disconnected + is_topo_disconnected,
                        1.1 * self.__maximum_total_head_loss,
                    )
                )

                max_head_loss = self._hn_pipe_head_loss(pipe, options, parameters, max_discharge)

            # Relate the head loss symbol to the pipe's dH symbol.

            # FIXME: Ugly hack. Cold pipes should be modelled completely with
            # their own integers as well.
            flow_dir = self.__state_vector_scaled(
                self.__pipe_to_flow_direct_map[pipe], ensemble_member
            )

            # Note that the Big-M should _at least_ cover the maximum
            # distance between `head_loss` and `dh`. If `head_loss` can be at
            # most 1.0 (= `max_head_loss`), that means our Big-M should be at
            # least double (i.e. >= 2.0). And because we do not want Big-Ms to
            # be overly tight, we include an additional factor of 2.
            big_m = 2 * 2 * max_head_loss

            constraints.append(
                (
                    (-dh - head_loss + (1 - flow_dir) * big_m) / big_m,
                    0.0,
                    np.inf,
                )
            )
            constraints.append(((dh - head_loss + flow_dir * big_m) / big_m, 0.0, np.inf))

        return constraints

    def __check_valve_head_discharge_path_constraints(self, ensemble_member):
        """
        This function adds constraints for the check valve functionality. Meaning that the flow can
        only go in positive direction of the valve. Depending on the status of the valve the flow is
        set to zero or bounded between zero and the maximum discharge.

        The head loss is also bounded to only act in one direction.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)
        options = self.heat_network_options()

        all_pipes = set(self.heat_network_components.get("pipe", []))
        maximum_velocity = options["maximum_velocity"]

        for v in self.heat_network_components.get("check_valve", []):
            status_var = self.__check_valve_status_map[v]
            status = self.state(status_var)

            q = self.state(f"{v}.Q")
            dh = self.state(f"{v}.dH")

            # Determine the maximum discharge that can go through the Valve
            # by looking at connected pipes.
            q_aliases = self.alias_relation.aliases(q.name())
            connected_pipes = {p for p in all_pipes if f"{p}.Q" in q_aliases}

            maximum_discharge = 0.0

            for p in connected_pipes:
                try:
                    pipe_classes = self.__pipe_topo_pipe_class_map[p].keys()
                    max_discharge_pipe = max(c.maximum_discharge for c in pipe_classes)
                except KeyError:
                    max_discharge_pipe = maximum_velocity * parameters[f"{p}.area"]

                maximum_discharge = max(maximum_discharge, max_discharge_pipe)

            maximum_head_loss = self.__maximum_total_head_loss

            # (Ideal) check valve status:
            # - 1 means "open", so positive discharge, and dH = 0
            # - 0 means "closed", so Q = 0 and positive dH
            # Note that the Q >= 0 and dH >= 0 constraints are part of the bounds.
            constraints.append((q - status * maximum_discharge, -np.inf, 0.0))

            if options["head_loss_option"] != HeadLossOption.NO_HEADLOSS:
                constraints.append((dh - (1 - status) * maximum_head_loss, -np.inf, 0.0))

        return constraints

    def __control_valve_head_discharge_path_constraints(self, ensemble_member):
        """
        This function adds the constraints for the control valve. In this case we allow the valve to
        produce head loss for flow in both directions.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)
        options = self.heat_network_options()

        all_pipes = set(self.heat_network_components.get("pipe", []))
        maximum_velocity = options["maximum_velocity"]

        for v in self.heat_network_components.get("control_valve", []):
            flow_dir_var = self.__control_valve_direction_map[v]
            flow_dir = self.state(flow_dir_var)

            q = self.state(f"{v}.Q")
            dh = self.state(f"{v}.dH")

            # Determine the maximum discharge that can go through the Valve
            # by looking at connected pipes.
            q_aliases = self.alias_relation.aliases(q.name())
            connected_pipes = {p for p in all_pipes if f"{p}.Q" in q_aliases}

            maximum_discharge = 0.0

            for p in connected_pipes:
                try:
                    pipe_classes = self.__pipe_topo_pipe_class_map[p].keys()
                    max_discharge_pipe = max(c.maximum_discharge for c in pipe_classes)
                except KeyError:
                    max_discharge_pipe = maximum_velocity * parameters[f"{p}.area"]

                maximum_discharge = max(maximum_discharge, max_discharge_pipe)

            maximum_head_loss = self.__maximum_total_head_loss

            # Flow direction:
            # - 1 means positive discharge, and negative dH
            # - 0 means negative discharge, and positive dH
            # It's a control valve, so the dH is of arbitrary magnitude.
            constraints.append((q + (1 - flow_dir) * maximum_discharge, 0.0, np.inf))
            constraints.append((q - flow_dir * maximum_discharge, -np.inf, 0.0))

            if options["head_loss_option"] != HeadLossOption.NO_HEADLOSS:
                constraints.append((-dh + (1 - flow_dir) * maximum_head_loss, 0.0, np.inf))
                constraints.append((-dh - flow_dir * maximum_head_loss, -np.inf, 0.0))

        return constraints

    def __pipe_topology_constraints(self, ensemble_member):
        """
        This function adds the constraints needed for the optimization of pipe classes (referred to
        as topology optimization). We ensure that only one pipe_class can be selected.
        Additionally,, we set the diameter and cost variable to those associated with the optimized
        pipe_class. Note that the cost symbol is the investment cost in EUR/meter, the actual
        investment cost of the pipe is set in the __investment_cost variable.

        Furthermore, ordering variables are set in this function. This is to give the optimization
        insight in the ordering of all the possible boolean choices in pipe classes and as such
        quicker find a feasible and optimal solution. The ordering are 0 or 1 depending on whether
        the variable is larger compared to the selected pipe-class. For example is the pipe class
        variable for DN200 is 1, then all discharge ordering variables for the pipe classes >=DN200
        are 1.
        """
        constraints = []

        # These are the constraints to count the amount of a certain pipe class
        unique_pipe_classes = self.get_unique_pipe_classes()
        pipe_class_count_sum = {pc.name: 0 for pc in unique_pipe_classes}

        for p in self.heat_network_components.get("pipe", []):
            try:
                pipe_classes = self.__pipe_topo_pipe_class_map[p]
            except KeyError:
                pass
            else:
                for pc in pipe_classes:
                    neighbour = self.has_related_pipe(p)
                    if neighbour and p not in self.hot_pipes:
                        var_name = f"{self.cold_to_hot_pipe(p)}__hn_pipe_class_{pc.name}"
                    else:
                        var_name = f"{p}__hn_pipe_class_{pc.name}"
                    pipe_class_count_sum[pc.name] += self.extra_variable(var_name, ensemble_member)

        for pc in unique_pipe_classes:
            var = self.extra_variable(
                self.__pipe_topo_global_pipe_class_count_map[pc.name], ensemble_member
            )
            constraints.append(((pipe_class_count_sum[pc.name] - var), 0.0, 0.0))

        # These are the constraints to order the discharge capabilities of the pipe classes
        for p, pipe_classes in self.__pipe_topo_pipe_class_discharge_ordering_map.items():
            max_discharge = self.extra_variable(self.__pipe_topo_max_discharge_map[p])
            max_discharges = {
                pc.name: pc.maximum_discharge for pc in self.__pipe_topo_pipe_class_map[p]
            }
            median_discharge = np.median(list(max_discharges.values()))

            big_m = 2.0 * max(max_discharges.values())
            for pc, var_name in pipe_classes.items():
                pipe_class_discharge_ordering = self.extra_variable(var_name, ensemble_member)

                constraints.append(
                    (
                        (
                            max_discharge
                            - max_discharges[pc.name]
                            + pipe_class_discharge_ordering * big_m
                        )
                        / median_discharge,
                        0.0,
                        np.inf,
                    )
                )
                constraints.append(
                    (
                        (
                            max_discharge
                            - max_discharges[pc.name]
                            - (1.0 - pipe_class_discharge_ordering) * big_m
                        )
                        / median_discharge,
                        -np.inf,
                        0.0,
                    )
                )

        # These are the constraints to order the costs of the pipe classes
        for p, pipe_classes in self.__pipe_topo_pipe_class_cost_ordering_map.items():
            cost_sym_name = self.__pipe_topo_cost_map[p]
            cost_sym = self.extra_variable(cost_sym_name, ensemble_member)
            costs = {pc.name: pc.investment_costs for pc in self.__pipe_topo_pipe_class_map[p]}

            big_m = 2.0 * max(costs.values())
            for pc, var_name in pipe_classes.items():
                pipe_class_cost_ordering = self.extra_variable(var_name, ensemble_member)

                # should be one if >= than cost_symbol
                constraints.append(
                    (
                        (cost_sym - costs[pc.name] + pipe_class_cost_ordering * big_m)
                        / self.variable_nominal(cost_sym_name),
                        0.0,
                        np.inf,
                    )
                )
                constraints.append(
                    (
                        (cost_sym - costs[pc.name] - (1.0 - pipe_class_cost_ordering) * big_m)
                        / self.variable_nominal(cost_sym_name),
                        -np.inf,
                        0.0,
                    )
                )

        # These are the constraints to order the heat loss of the pipe classes.
        if not self.heat_network_options()["neglect_pipe_heat_losses"]:
            for pipe, pipe_classes in self.__pipe_topo_pipe_class_heat_loss_ordering_map.items():
                if pipe in self.hot_pipes and self.has_related_pipe(pipe):
                    heat_loss_sym_name = self.__pipe_topo_heat_loss_map[pipe]
                    heat_loss_sym = self.extra_variable(heat_loss_sym_name, ensemble_member)
                    cold_name = self.__pipe_topo_heat_loss_map[self.hot_to_cold_pipe(pipe)]
                    heat_loss_sym += self.extra_variable(cold_name, ensemble_member)
                    heat_losses = [
                        h1 + h2
                        for h1, h2 in zip(
                            self.__pipe_topo_heat_losses[pipe],
                            self.__pipe_topo_heat_losses[self.hot_to_cold_pipe(pipe)],
                        )
                    ]
                elif pipe in self.hot_pipes and not self.has_related_pipe(pipe):
                    heat_loss_sym_name = self.__pipe_topo_heat_loss_map[pipe]
                    heat_loss_sym = self.extra_variable(heat_loss_sym_name, ensemble_member)

                    heat_losses = self.__pipe_topo_heat_losses[pipe]
                else:  # cold pipe
                    continue

                big_m = 2.0 * max(heat_losses)
                for var_name, heat_loss in zip(pipe_classes.values(), heat_losses):
                    pipe_class_heat_loss_ordering = self.extra_variable(var_name, ensemble_member)

                    # should be one if >= than heat_loss_symbol
                    constraints.append(
                        (
                            (heat_loss_sym - heat_loss + pipe_class_heat_loss_ordering * big_m)
                            / self.variable_nominal(heat_loss_sym_name),
                            0.0,
                            np.inf,
                        )
                    )
                    constraints.append(
                        (
                            (
                                heat_loss_sym
                                - heat_loss
                                - (1.0 - pipe_class_heat_loss_ordering) * big_m
                            )
                            / self.variable_nominal(heat_loss_sym_name),
                            -np.inf,
                            0.0,
                        )
                    )

        for p, pipe_classes in self.__pipe_topo_pipe_class_map.items():
            variables = {
                pc.name: self.extra_variable(var_name, ensemble_member)
                for pc, var_name in pipe_classes.items()
            }

            # Make sure exactly one indicator is true
            constraints.append((sum(variables.values()), 1.0, 1.0))

            # set the max discharge
            max_discharge = self.extra_variable(self.__pipe_topo_max_discharge_map[p])
            max_discharges = {pc.name: pc.maximum_discharge for pc in pipe_classes}
            max_discharge_expr = sum(
                variables[pc_name] * max_discharges[pc_name] for pc_name in variables
            )

            constraints.append(
                (
                    (max_discharge - max_discharge_expr)
                    / self.variable_nominal(self.__pipe_topo_max_discharge_map[p]),
                    0.0,
                    0.0,
                )
            )

            # Match the indicators to the diameter symbol
            diam_sym_name = self.__pipe_topo_diameter_map[p]
            diam_sym = self.extra_variable(diam_sym_name, ensemble_member)

            diameters = {pc.name: pc.inner_diameter for pc in pipe_classes}

            diam_expr = sum(variables[pc_name] * diameters[pc_name] for pc_name in variables)

            constraint_nominal = self.variable_nominal(diam_sym_name)
            constraints.append(((diam_sym - diam_expr) / constraint_nominal, 0.0, 0.0))

            # match the indicators to the cost symbol
            cost_sym_name = self.__pipe_topo_cost_map[p]
            cost_sym = self.extra_variable(cost_sym_name, ensemble_member)

            investment_costs = {pc.name: pc.investment_costs for pc in pipe_classes}

            costs_expr = sum(
                variables[pc_name] * investment_costs[pc_name] for pc_name in variables
            )
            costs_constraint_nominal = self.variable_nominal(cost_sym_name)

            constraints.append(((cost_sym - costs_expr) / costs_constraint_nominal, 0.0, 0.0))

        return constraints

    def __heat_loss_variable_constraints(self, ensemble_member):
        """
        Furthermore, the __hn_heat_loss symbol is set, as the heat loss depends on the chosen pipe
        class and the selected temperature in the network.

        Parameters
        ----------
        ensemble_member : The ensemble of the optimizaton

        Returns
        -------
        list of the added constraints
        """
        constraints = []

        for p in self.heat_network_components.get("pipe", []):
            pipe_classes = []

            heat_loss_sym_name = self.__pipe_topo_heat_loss_map[p]

            constraint_nominal = self.variable_nominal(heat_loss_sym_name)

            carrier = self.parameters(ensemble_member)[f"{p}.carrier_id"]
            temperatures = self.temperature_regimes(carrier)

            if len(temperatures) == 0:
                heat_loss_sym = self.extra_variable(heat_loss_sym_name, ensemble_member)
                try:
                    heat_losses = self.__pipe_topo_heat_losses[p]
                    pipe_classes = self.__pipe_topo_pipe_class_map[p]
                    variables = [
                        self.extra_variable(var_name, ensemble_member)
                        for pc, var_name in pipe_classes.items()
                    ]
                    heat_loss_expr = 0.0
                    for i in range(len(heat_losses)):
                        heat_loss_expr = heat_loss_expr + variables[i] * heat_losses[i]
                    constraints.append(
                        ((heat_loss_sym - heat_loss_expr) / constraint_nominal, 0.0, 0.0)
                    )
                except KeyError:
                    heat_loss = self._pipe_heat_loss(
                        self.heat_network_options(),
                        self.parameters(ensemble_member),
                        p,
                    )
                    constraints.append(
                        (
                            (heat_loss_sym - heat_loss) / constraint_nominal,
                            0.0,
                            0.0,
                        )
                    )
            else:
                heat_loss_sym = self.__state_vector_scaled(heat_loss_sym_name, ensemble_member)
                for temperature in temperatures:
                    temperature_is_selected = self.state_vector(f"{carrier}_{temperature}")
                    if len(pipe_classes) == 0:
                        heat_loss = self._pipe_heat_loss(
                            self.heat_network_options(),
                            self.parameters(ensemble_member),
                            p,
                            temp=temperature,
                        )
                        big_m = 2.0 * heat_loss
                        constraints.append(
                            (
                                (
                                    heat_loss_sym
                                    - heat_loss * np.ones((len(self.times()), 1))
                                    + (1.0 - temperature_is_selected) * big_m
                                )
                                / constraint_nominal,
                                0.0,
                                np.inf,
                            )
                        )
                        constraints.append(
                            (
                                (
                                    heat_loss_sym
                                    - heat_loss * np.ones((len(self.times()), 1))
                                    - (1.0 - temperature_is_selected) * big_m
                                )
                                / constraint_nominal,
                                -np.inf,
                                0.0,
                            )
                        )
                    else:
                        heat_losses = [
                            self._pipe_heat_loss(
                                self.heat_network_options(),
                                self.parameters(ensemble_member),
                                p,
                                u_values=c.u_values,
                                temp=temperature,
                            )
                            for c in pipe_classes
                        ]
                        count = 0
                        big_m = 2.0 * max(heat_losses)
                        for pc_var_name in pipe_classes.values():
                            pc = self.__pipe_topo_pipe_class_var[pc_var_name]
                            constraints.append(
                                (
                                    (
                                        heat_loss_sym
                                        - heat_losses[count] * np.ones(len(self.times()))
                                        + (1.0 - pc) * big_m * np.ones(len(self.times()))
                                        + (1.0 - temperature_is_selected) * big_m
                                    )
                                    / constraint_nominal,
                                    0.0,
                                    np.inf,
                                )
                            )
                            constraints.append(
                                (
                                    (
                                        heat_loss_sym
                                        - heat_losses[count] * np.ones(len(self.times()))
                                        - (1.0 - pc) * big_m * np.ones(len(self.times()))
                                        - (1.0 - temperature_is_selected) * big_m
                                    )
                                    / constraint_nominal,
                                    -np.inf,
                                    0.0,
                                )
                            )
                            count += 1

        return constraints

    def __pipe_topology_path_constraints(self, ensemble_member):
        """
        This function adds constraints to limit the discharge that can flow through a pipe when the
        pipe class is being optimized. This is needed as the different pipe classes have different
        diameters and maximum velocities.
        """
        constraints = []

        # Clip discharge based on pipe class
        for p in self.heat_network_components.get("pipe", []):
            # Match the indicators to the discharge symbol(s)
            discharge_sym_hot = self.state(f"{p}.Q")
            nominal = self.variable_nominal(f"{p}.Q")

            max_discharge = self.__pipe_topo_max_discharge_var[
                self.__pipe_topo_max_discharge_map[p]
            ]

            constraints.append(((max_discharge - discharge_sym_hot) / nominal, 0.0, np.inf))
            constraints.append(((-max_discharge - discharge_sym_hot) / nominal, -np.inf, 0.0))

        return constraints

    def __electricity_node_heat_mixing_path_constraints(self, ensemble_member):
        """
        This function adds constraints for power/energy and current conservation at nodes/busses.
        """
        constraints = []

        for bus, connected_cables in self.heat_network_topology.busses.items():
            power_sum = 0.0
            i_sum = 0.0
            power_nominal = []
            i_nominal = []

            for i_conn, (_cable, orientation) in connected_cables.items():
                heat_conn = f"{bus}.ElectricityConn[{i_conn + 1}].Power"
                i_port = f"{bus}.ElectricityConn[{i_conn + 1}].I"
                power_sum += orientation * self.state(heat_conn)
                i_sum += orientation * self.state(i_port)
                power_nominal.append(self.variable_nominal(heat_conn))
                i_nominal.append(self.variable_nominal(i_port))

            power_nominal = np.median(power_nominal)
            constraints.append((power_sum / power_nominal, 0.0, 0.0))

            i_nominal = np.median(i_nominal)
            constraints.append((i_sum / i_nominal, 0.0, 0.0))

        return constraints

    def __electricity_cable_heat_mixing_path_constraints(self, ensemble_member):
        """
        This function adds constraints relating the electrical power to the current flowing through
        the cable. The power through the cable is limited by the maximum voltage and the actual
        current variable with an inequality constraint. This is done to allow power losses through
        the network. As the current and power are related with an equality constraint at the
        demands exactly matching the P = U*I equation, we allow the inequalities for the lines. By
        overestimating the power losses and voltage drops, together we ensure that U*I>P.


        Furthermore, the power loss is estimated by linearizing with the maximum current, meaning
        that we are always overestimating the power loss in the cable.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        for cable in self.heat_network_components.get("electricity_cable", []):
            current = self.state(f"{cable}.ElectricityIn.I")
            power_in = self.state(f"{cable}.ElectricityIn.Power")
            power_out = self.state(f"{cable}.ElectricityOut.Power")
            power_loss = self.state(f"{cable}.Power_loss")
            r = parameters[f"{cable}.r"]
            i_max = parameters[f"{cable}.max_current"]
            v_nom = parameters[f"{cable}.nominal_voltage"]
            v_max = parameters[f"{cable}.max_voltage"]

            # Ensure that the current is sufficient to transport the power
            constraints.append(((power_in - current * v_max) / (i_max * v_max), -np.inf, 0.0))
            constraints.append(((power_out - current * v_max) / (i_max * v_max), -np.inf, 0.0))

            # Power loss constraint
            constraints.append(((power_loss - current * r * i_max) / (i_max * v_nom * r), 0.0, 0.0))

        return constraints

    def __electricity_demand_path_constraints(self, ensemble_member):
        """
        This function adds the constraints for the electricity commodity at the demand assets. We
        enforce that a minimum voltage is exactly met together with the power that is carried by
        the current. By fixing the voltage at the demand we ensure that at the demands
        P = U * I is met exactly at this point in the network and the power is conservatively
        in the cables at all locations in the network.
        """
        constraints = []
        parameters = self.parameters(ensemble_member)

        for elec_demand in [
            *self.heat_network_components.get("electricity_demand", []),
            *self.heat_network_components.get("heat_pump_elec", []),
        ]:
            min_voltage = parameters[f"{elec_demand}.min_voltage"]
            voltage = self.state(f"{elec_demand}.ElectricityIn.V")
            # to ensure that voltage entering is equal or larger than the minimum voltage
            constraints.append(((voltage - min_voltage) / min_voltage, 0.0, np.inf))

            power_nom = self.variable_nominal(f"{elec_demand}.ElectricityIn.Power")
            curr_nom = self.variable_nominal(f"{elec_demand}.ElectricityIn.I")
            power_in = self.state(f"{elec_demand}.ElectricityIn.Power")
            current_in = self.state(f"{elec_demand}.ElectricityIn.I")
            constraints.append(
                (
                    (power_in - min_voltage * current_in)
                    / (power_nom * curr_nom * min_voltage) ** 0.5,
                    0,
                    0,
                )
            )

        return constraints

    def __max_size_constraints(self, ensemble_member):
        """
        This function makes sure that the __max_size variable is at least as large as needed. For
        most assets the __max_size is related to the thermal Power it can produce or consume, there
        are a few exceptions like tank storage that sizes with volume.

        Since it are inequality constraints are inequality the __max_size variable can be larger
        than what is the actual needed size. In combination with the objectives, e.g. cost
        minimization, we can drag down the __max_size to the minimum required.
        """
        constraints = []
        bounds = self.bounds()

        for b in self.heat_network_components.get("buffer", []):
            max_var = self._asset_max_size_map[b]
            max_heat = self.extra_variable(max_var, ensemble_member)
            stored_heat = self.__state_vector_scaled(f"{b}.Stored_heat", ensemble_member)
            constraint_nominal = self.variable_nominal(max_var)

            constraints.append(
                (
                    (np.ones(len(self.times())) * max_heat - stored_heat) / constraint_nominal,
                    0.0,
                    np.inf,
                )
            )

            # Same as for the buffer but now for the source
        for s in self.heat_network_components.get("source", []):
            max_var = self._asset_max_size_map[s]
            max_heat = self.extra_variable(max_var, ensemble_member)
            heat_source = self.__state_vector_scaled(f"{s}.Heat_source", ensemble_member)
            constraint_nominal = self.variable_nominal(f"{s}.Heat_source")

            try:
                profile = self.get_timeseries(f"{s}.target_heat_source").values
                profile_scaled = profile / max(profile)
                for i in range(0, len(self.times())):
                    constraints.append(
                        (
                            (profile_scaled[i] * max_heat - heat_source[i]) / constraint_nominal,
                            0.0,
                            np.inf,
                        )
                    )
            except KeyError:
                constraints.append(
                    (
                        (np.ones(len(self.times())) * max_heat - heat_source) / constraint_nominal,
                        0.0,
                        np.inf,
                    )
                )

        for hx in [
            *self.heat_network_components.get("heat_exchanger", []),
            *self.heat_network_components.get("heat_pump", []),
            *self.heat_network_components.get("heat_pump_elec", []),
        ]:
            max_var = self._asset_max_size_map[hx]
            max_heat = self.extra_variable(max_var, ensemble_member)
            heat_secondary = self.__state_vector_scaled(f"{hx}.Secondary_heat", ensemble_member)
            constraint_nominal = self.variable_nominal(f"{hx}.Secondary_heat")

            constraints.append(
                (
                    (np.ones(len(self.times())) * max_heat - heat_secondary) / constraint_nominal,
                    0.0,
                    np.inf,
                )
            )

        for d in self.heat_network_components.get("demand", []):
            max_var = self._asset_max_size_map[d]
            max_heat = self.extra_variable(max_var, ensemble_member)
            heat_demand = self.__state_vector_scaled(f"{d}.Heat_demand", ensemble_member)
            constraint_nominal = max(
                self.variable_nominal(f"{d}.Heat_demand"), self.variable_nominal(f"{d}.HeatIn.Heat")
            )
            constraints.append(
                (
                    (np.ones(len(self.times())) * max_heat - heat_demand) / constraint_nominal,
                    0.0,
                    np.inf,
                )
            )

        for a in self.heat_network_components.get("ates", []):
            max_var = self._asset_max_size_map[a]
            max_heat = self.extra_variable(max_var, ensemble_member)
            heat_ates = self.__state_vector_scaled(f"{a}.Heat_ates", ensemble_member)
            constraint_nominal = bounds[f"{a}.Heat_ates"][1]

            constraints.append(
                (
                    (np.ones(len(self.times())) * max_heat - heat_ates) / constraint_nominal,
                    0.0,
                    np.inf,
                )
            )
            constraints.append(
                (
                    (np.ones(len(self.times())) * max_heat + heat_ates) / constraint_nominal,
                    0.0,
                    np.inf,
                )
            )

        return constraints

    def __investment_cost_constraints(self, ensemble_member):
        """
        This function adds constraints to set the investment cost variable. The investment cost
        scales with the maximum size of the asset. This leaves two cases for the constraint. 1) The
        asset size is fixed (state==1): in this case the investment cost is set based on the upper
        bound of the size. 2) The asset size is optimized (state==2): in this case the investment
        cost is set based upon the __max_size variable.

        Specifically for demands we have a case where we set the investment cost based on the
        maximum demand as often the size of the demand is not seperately specified.

        For pipes the investment cost is set based on the pipe class and the length.
        """
        constraints = []

        parameters = self.parameters(ensemble_member)
        bounds = self.bounds()

        for asset_name in [
            asset_name
            for asset_name_list in self.heat_network_components.values()
            for asset_name in asset_name_list
        ]:
            if asset_name in [
                *self.heat_network_components.get("node", []),
                *self.heat_network_components.get("pump", []),
                *self.heat_network_components.get("check_valve", []),
                *self.heat_network_components.get("electricity_cable", []),
                *self.heat_network_components.get("electricity_node", []),
                *self.heat_network_components.get("electricity_source", []),
                *self.heat_network_components.get("electricity_demand", []),
                *self.heat_network_components.get("gas_pipe", []),
                *self.heat_network_components.get("gas_node", []),
                *self.heat_network_components.get("gas_source", []),
                *self.heat_network_components.get("gas_demand", []),
            ]:
                # TODO: add support for joints?
                continue

            investment_cost_var = self._asset_investment_cost_map[asset_name]
            investment_costs = self.extra_variable(investment_cost_var, ensemble_member)
            investment_cost_coefficient = parameters[f"{asset_name}.investment_cost_coefficient"]
            nominal = self.variable_nominal(investment_cost_var)

            if parameters[f"{asset_name}.state"] == 1:  # Asset is in use
                if asset_name in [*self.heat_network_components.get("demand", [])]:
                    try:
                        if np.isinf(bounds[f"{asset_name}.Heat_demand"][1]):
                            asset_size = max(
                                self.get_timeseries(
                                    f"{asset_name}.target_heat_demand", ensemble_member
                                ).values
                            )
                        else:
                            asset_size = bounds[f"{asset_name}.Heat_demand"][1]
                    except KeyError:
                        asset_size = 0.0
                        logger.warning(
                            f"No investment cost will calculdated for asset: {asset_name}, because "
                            "no target demand heat profile or Power [W] (mapeditor) has been "
                            "specified."
                        )
                elif asset_name in [*self.heat_network_components.get("source", [])]:
                    asset_size = bounds[f"{asset_name}.Heat_source"][1]
                elif asset_name in [*self.heat_network_components.get("pipe", [])]:
                    investment_cost_coefficient = parameters[
                        f"{asset_name}.investment_cost_coefficient"
                    ]
                    asset_size = parameters[f"{asset_name}.length"] * 2.0
                    nominal = max(
                        parameters[f"{asset_name}.investment_cost_coefficient"]
                        * parameters[f"{asset_name}.length"],
                        1.0,
                    )
                elif asset_name in [*self.heat_network_components.get("ates", [])]:
                    asset_size = bounds[f"{asset_name}.Heat_ates"][1]
                elif asset_name in [*self.heat_network_components.get("buffer", [])]:
                    asset_size = min(
                        bounds[f"{asset_name}.Heat_buffer"][1],
                        bounds[f"{asset_name}.HeatIn.Heat"][1],
                    )
                elif asset_name in [
                    *self.heat_network_components.get("heat_exchanger", []),
                    *self.heat_network_components.get("heat_pump", []),
                    *self.heat_network_components.get("heat_pump_elec", []),
                ]:
                    asset_size = bounds[f"{asset_name}.Secondary_heat"][1]
                else:
                    asset_size = 0.0
                    logger.warning(
                        f"Unknown type for asset {asset_name}, cannot "
                        f"set constraints for its investment costs, thus forced to zero"
                    )
            elif parameters[f"{asset_name}.state"] == 2:  # Optional assets for use
                if asset_name in [*self.heat_network_components.get("pipe", [])]:
                    investment_cost_coefficient = self.extra_variable(
                        self.__pipe_topo_cost_map[asset_name], ensemble_member
                    )
                    asset_size = parameters[f"{asset_name}.length"]
                    nominal = self.variable_nominal(self.__pipe_topo_cost_map[asset_name])
                else:
                    max_var = self._asset_max_size_map[asset_name]
                    asset_size = self.extra_variable(max_var, ensemble_member)
            else:
                # asset is disabled and has no cost
                continue

            constraints.append(
                (
                    (investment_costs - asset_size * investment_cost_coefficient) / nominal,
                    0.0,
                    0.0,
                )
            )

        return constraints

    def __fixed_operational_cost_constraints(self, ensemble_member):
        """
        This function adds the constraints to set the fixed operational cost. The fixed operational
        cost are the cost made independently of the operation of the asset. We assume that these
        cost scale with the maximum size of the asset.
        """
        constraints = []

        parameters = self.parameters(ensemble_member)

        for asset_name in [
            asset_name
            for asset_name_list in self.heat_network_components.values()
            for asset_name in asset_name_list
        ]:
            if asset_name in [
                *self.heat_network_components.get("node", []),
                *self.heat_network_components.get("pipe", []),
                *self.heat_network_components.get("electricity_cable", []),
                *self.heat_network_components.get("electricity_node", []),
                *self.heat_network_components.get("electricity_demand", []),
                *self.heat_network_components.get("electricity_source", []),
                *self.heat_network_components.get("gas_pipe", []),
                *self.heat_network_components.get("gas_node", []),
                *self.heat_network_components.get("gas_demand", []),
                *self.heat_network_components.get("gas_source", []),
                *self.heat_network_components.get("pump", []),
                *self.heat_network_components.get("check_valve", []),
            ]:
                # currently no support for joints
                continue
            fixed_operational_cost_var = self._asset_fixed_operational_cost_map[asset_name]
            fixed_operational_cost = self.extra_variable(
                fixed_operational_cost_var, ensemble_member
            )
            max_var = self._asset_max_size_map[asset_name]
            asset_size = self.extra_variable(max_var, ensemble_member)
            fixed_operational_cost_coefficient = parameters[
                f"{asset_name}.fixed_operational_cost_coefficient"
            ]

            nominal = self.variable_nominal(fixed_operational_cost_var)

            constraints.append(
                (
                    (fixed_operational_cost - asset_size * fixed_operational_cost_coefficient)
                    / nominal,
                    0.0,
                    0.0,
                )
            )

        return constraints

    def __variable_operational_cost_constraints(self, ensemble_member):
        """
        This function adds the constraints for setting the variable operational cost. These are the
        cost that depend on the operation of the asset. At this moment we only support the variable
        operational cost for sources where they scale with the thermal energy production.
        """
        constraints = []

        parameters = self.parameters(ensemble_member)

        for s in self.heat_network_components.get("source", []):
            heat_source = self.__state_vector_scaled(f"{s}.Heat_source", ensemble_member)
            variable_operational_cost_var = self._asset_variable_operational_cost_map[s]
            variable_operational_cost = self.extra_variable(
                variable_operational_cost_var, ensemble_member
            )
            nominal = self.variable_nominal(variable_operational_cost_var)
            variable_operational_cost_coefficient = parameters[
                f"{s}.variable_operational_cost_coefficient"
            ]
            timesteps = np.diff(self.times()) / 3600.0

            sum = 0.0
            for i in range(1, len(self.times())):
                sum += variable_operational_cost_coefficient * heat_source[i] * timesteps[i - 1]
            constraints.append(((variable_operational_cost - sum) / (nominal), 0.0, 0.0))

        for _ in self.heat_network_components.get("buffer", []):
            pass

        # for a in self.heat_network_components.get("ates", []):
        # TODO: needs to be replaced with the positive or abs value of this, see varOPEX,
        #  then ates varopex also needs to be added to the mnimize_tco_goal
        # heat_ates = self.__state_vector_scaled(f"{a}.Heat_ates", ensemble_member)
        # variable_operational_cost_var = self._asset_variable_operational_cost_map[a]
        # variable_operational_cost = self.extra_variable(
        #     variable_operational_cost_var, ensemble_member
        # )
        # nominal = self.variable_nominal(variable_operational_cost_var)
        # variable_operational_cost_coefficient = parameters[
        #     f"{a}.variable_operational_cost_coefficient"
        # ]
        # timesteps = np.diff(self.times()) / 3600.0
        #
        # sum = 0.0
        #
        # for i in range(1, len(self.times())):
        #     varOPEX_dt = (variable_operational_cost_coefficient * heat_ates[i]
        #     * timesteps[i - 1])
        #     constraints.append(((varOPEX-varOPEX_dt)/nominal,0.0, np,inf))
        #     #varOPEX would be a variable>0 for everyt timestep
        #     sum += varOPEX
        # constraints.append(((variable_operational_cost - sum) / (nominal), 0.0, 0.0))

        return constraints

    def __installation_cost_constraints(self, ensemble_member):
        """
        This function adds the constraints for setting the installation cost variable. The
        installation cost is the cost element that comes with the placing of the asset
        independently of the size of the asset. Therefore, the installation cost is set with the
        _aggregation_count variable.
        """
        constraints = []

        parameters = self.parameters(ensemble_member)

        for asset_name in [
            asset_name
            for asset_name_list in self.heat_network_components.values()
            for asset_name in asset_name_list
        ]:
            if asset_name in [
                *self.heat_network_components.get("node", []),
                *self.heat_network_components.get("pump", []),
                *self.heat_network_components.get("check_valve", []),
                *self.heat_network_components.get("electricity_cable", []),
                *self.heat_network_components.get("electricity_node", []),
                *self.heat_network_components.get("electricity_source", []),
                *self.heat_network_components.get("electricity_demand", []),
                *self.heat_network_components.get("gas_pipe", []),
                *self.heat_network_components.get("gas_node", []),
                *self.heat_network_components.get("gas_source", []),
                *self.heat_network_components.get("gas_demand", []),
            ]:
                # no support for joints right now
                continue
            installation_cost_sym = self.extra_variable(
                self._asset_installation_cost_map[asset_name]
            )
            nominal = self.variable_nominal(self._asset_installation_cost_map[asset_name])
            installation_cost = parameters[f"{asset_name}.installation_cost"]
            aggregation_count_sym = self.extra_variable(
                self._asset_aggregation_count_var_map[asset_name]
            )
            constraints.append(
                (
                    (installation_cost_sym - aggregation_count_sym * installation_cost) / nominal,
                    0.0,
                    0.0,
                )
            )

        return constraints

    def __optional_asset_path_constraints(self, ensemble_member):
        """
        This function adds constraints that set the _aggregation_count variable. This variable is
        used for most assets (except geo and ates) to turn on/off the asset. Which effectively mean
        that assets cannot exchange thermal power with the network when _aggregation_count == 0.

        Specifically for the geo and ATES we use the _aggregation_count for modelling the amount of
        doublets. Where the _aggregation_count allows increments in the upper limit for the thermal
        power that can be exchanged with the network.
        """
        constraints = []

        parameters = self.parameters(ensemble_member)
        bounds = self.bounds()

        for asset_name in [
            asset_name
            for asset_name_list in self.heat_network_components.values()
            for asset_name in asset_name_list
        ]:
            if parameters[f"{asset_name}.state"] == 0 or parameters[f"{asset_name}.state"] == 2:
                if asset_name in [
                    *self.heat_network_components.get("geothermal", []),
                    *self.heat_network_components.get("ates", []),
                ]:
                    state_var = self.state(f"{asset_name}.Heat_flow")
                    single_power = parameters[f"{asset_name}.single_doublet_power"]
                    nominal_value = 2.0 * bounds[f"{asset_name}.Heat_flow"][1]
                    nominal_var = self.variable_nominal(f"{asset_name}.Heat_flow")
                elif asset_name in [*self.heat_network_components.get("buffer", [])]:
                    state_var = self.state(f"{asset_name}.HeatIn.Q")
                    single_power = parameters[f"{asset_name}.volume"]
                    nominal_value = single_power
                    nominal_var = self.variable_nominal(f"{asset_name}.HeatIn.Q")
                elif asset_name in [*self.heat_network_components.get("node", [])]:
                    # TODO: can we generalize to all possible components to avoid having to skip
                    #  joints and other components in the future?
                    continue
                else:
                    state_var = self.state(f"{asset_name}.Heat_flow")
                    single_power = bounds[f"{asset_name}.Heat_flow"][1]
                    nominal_value = single_power
                    nominal_var = self.variable_nominal(f"{asset_name}.Heat_flow")
                aggregation_count = self.__asset_aggregation_count_var[
                    self._asset_aggregation_count_var_map[asset_name]
                ]
                constraint_nominal = (nominal_value * nominal_var) ** 0.5

                constraints.append(
                    (
                        (single_power * aggregation_count - state_var) / constraint_nominal,
                        0.0,
                        np.inf,
                    )
                )
                constraints.append(
                    (
                        (-single_power * aggregation_count - state_var) / constraint_nominal,
                        -np.inf,
                        0.0,
                    )
                )
            elif parameters[f"{asset_name}.state"] == 1:
                aggregation_count = self.__asset_aggregation_count_var[
                    self._asset_aggregation_count_var_map[asset_name]
                ]
                aggr_bound = self.__asset_aggregation_count_var_bounds[
                    asset_name + "_aggregation_count"
                ][1]
                constraints.append(((aggregation_count - aggr_bound), 0.0, 0.0))

        return constraints

    def __cumulative_investments_made_in_eur_path_constraints(self, ensemble_member):
        r"""
        These constraints are linking the cummulitive investments made to the possiblity of
        utilizing an asset. The investments made are sufficient for that asset to be realized it
        becomes available.

        Meaning that an asset requires 1million euro investment to be realized
        and the investments made at timestep i are sufficient the asset also is realized (becomes
        available) in that same timestep.
        """
        constraints = []
        options = self.heat_network_options()
        if options["include_asset_is_realized"]:
            for asset in [
                *self.heat_network_components.get("demand", []),
                *self.heat_network_components.get("source", []),
                *self.heat_network_components.get("ates", []),
                *self.heat_network_components.get("buffer", []),
                *self.heat_network_components.get("heat_exchanger", []),
                *self.heat_network_components.get("heat_pump", []),
            ]:
                var_name = self.__cumulative_investments_made_in_eur_map[asset]
                cumulative_investments_made = self.state(var_name)
                nominal = self.variable_nominal(var_name)
                var_name = self.__asset_is_realized_map[asset]
                asset_is_realized = self.state(var_name)
                installation_cost_sym = self.__asset_installation_cost_var[
                    self._asset_installation_cost_map[asset]
                ]
                investment_cost_sym = self.__asset_investment_cost_var[
                    self._asset_investment_cost_map[asset]
                ]
                # TODO: add insulation class cost to the investments made.
                # if asset in self.heat_network_components.get("demand", []):
                #     for insulation_class in self.__get_insulation_classes(asset):
                #         insulation_class_active
                #         insulation_class_cost
                #         investment_cost_sym += insulation_class_active * insulation_class_cost
                big_m = (
                    1.5
                    * max(
                        self.bounds()[f"{asset}__investment_cost"][1]
                        + self.bounds()[f"{asset}__installation_cost"][1],
                        1.0,
                    )
                    / max(self.bounds()[self._asset_aggregation_count_var_map[asset]][1], 1.0)
                )

                # Asset can be realized once the investments made equal the installation and
                # investment cost
                capex_sym = 0.0
                if self.variable_nominal(self._asset_installation_cost_map[asset]) > 1.0e2:
                    capex_sym = capex_sym + installation_cost_sym
                if self.variable_nominal(self._asset_investment_cost_map[asset]) > 1.0e2:
                    capex_sym = capex_sym + investment_cost_sym

                constraints.append(
                    (
                        (
                            cumulative_investments_made
                            - capex_sym
                            + (1.0 - asset_is_realized) * big_m
                        )
                        / nominal,
                        0.0,
                        np.inf,
                    )
                )

                # Once the asset is utilized the asset must be realized
                heat_flow = self.state(f"{asset}.Heat_flow")
                if not np.isinf(self.bounds()[f"{asset}.Heat_flow"][1]):
                    big_m = (
                        1.5
                        * self.bounds()[f"{asset}.Heat_flow"][1]
                        / max(self.bounds()[self._asset_aggregation_count_var_map[asset]][1], 1.0)
                    )
                else:
                    try:
                        big_m = (
                            1.5
                            * max(
                                self.bounds()[f"{asset}.HeatOut.Heat"][1],
                                self.bounds()[f"{asset}.HeatIn.Heat"][1],
                            )
                            / max(
                                self.bounds()[self._asset_aggregation_count_var_map[asset]][1], 1.0
                            )
                        )
                    except KeyError:
                        big_m = (
                            1.5
                            * max(
                                self.bounds()[f"{asset}.Primary.HeatOut.Heat"][1],
                                self.bounds()[f"{asset}.Primary.HeatIn.Heat"][1],
                            )
                            / max(
                                self.bounds()[self._asset_aggregation_count_var_map[asset]][1], 1.0
                            )
                        )
                constraints.append(((heat_flow + asset_is_realized * big_m) / big_m, 0.0, np.inf))
                constraints.append(((heat_flow - asset_is_realized * big_m) / big_m, -np.inf, 0.0))

        return constraints

    def path_constraints(self, ensemble_member):
        """
        Here we add all the path constraints to the optimization problem. Please note that the
        path constraints are the constraints that are applied to each time-step in the problem.
        """

        constraints = super().path_constraints(ensemble_member)

        constraints.extend(self.__node_heat_mixing_path_constraints(ensemble_member))
        constraints.extend(self.__heat_loss_path_constraints(ensemble_member))
        constraints.extend(self.__flow_direction_path_constraints(ensemble_member))
        constraints.extend(self.__node_discharge_mixing_path_constraints(ensemble_member))
        constraints.extend(self.__demand_heat_to_discharge_path_constraints(ensemble_member))
        constraints.extend(self.__source_heat_to_discharge_path_constraints(ensemble_member))
        constraints.extend(self.__pipe_heat_to_discharge_path_constraints(ensemble_member))
        constraints.extend(self.__storage_heat_to_discharge_path_constraints(ensemble_member))
        constraints.extend(
            self.__heat_exchanger_heat_to_discharge_path_constraints(ensemble_member)
        )
        constraints.extend(self.__check_valve_head_discharge_path_constraints(ensemble_member))
        constraints.extend(self.__control_valve_head_discharge_path_constraints(ensemble_member))
        constraints.extend(self.__pipe_topology_path_constraints(ensemble_member))
        constraints.extend(self.__electricity_demand_path_constraints(ensemble_member))
        constraints.extend(self.__electricity_node_heat_mixing_path_constraints(ensemble_member))
        constraints.extend(self.__electricity_cable_heat_mixing_path_constraints(ensemble_member))
        constraints.extend(self.__network_temperature_path_constraints(ensemble_member))
        constraints.extend(self.__optional_asset_path_constraints(ensemble_member))
        constraints.extend(self.__pipe_hydraulic_power_path_constraints(ensemble_member))
        constraints.extend(self.__gas_node_heat_mixing_path_constraints(ensemble_member))
        constraints.extend(
            self.__cumulative_investments_made_in_eur_path_constraints(ensemble_member)
        )

        return constraints

    def constraints(self, ensemble_member):
        """
        This function adds the normal constraints to the problem. Unlike the path constraints these
        are not applied to every time-step in the problem. Meaning that these constraints either
        consider global variables that are independent of time-step or that the relevant time-steps
        are indexed within the constraint formulation.
        """
        constraints = super().constraints(ensemble_member)

        constraints.extend(self.__pipe_rate_heat_change_constraints(ensemble_member))
        constraints.extend(self.__heat_loss_variable_constraints(ensemble_member))
        constraints.extend(self.__pipe_topology_constraints(ensemble_member))
        constraints.extend(self.__variable_operational_cost_constraints(ensemble_member))
        constraints.extend(self.__fixed_operational_cost_constraints(ensemble_member))
        constraints.extend(self.__investment_cost_constraints(ensemble_member))
        constraints.extend(self.__installation_cost_constraints(ensemble_member))
        constraints.extend(self.__max_size_constraints(ensemble_member))

        for component_name, params in self._timed_setpoints.items():
            constraints.extend(
                self.__setpoint_constraint(ensemble_member, component_name, params[0], params[1])
            )

        if self.heat_network_options()["include_demand_insulation_options"]:
            constraints.extend(self.__heat_matching_demand_insulation_constraints(ensemble_member))

        return constraints

    def history(self, ensemble_member):
        """
        In this history function we avoid the optimization using artificial energy for storage
        assets as the history is not defined.
        """
        history = super().history(ensemble_member)

        initial_time = np.array([self.initial_time])
        empty_timeseries = Timeseries(initial_time, [np.nan])
        buffers = self.heat_network_components.get("buffer", [])

        for b in buffers:
            hist_heat_buffer = history.get(f"{b}.Heat_buffer", empty_timeseries).values
            hist_stored_heat = history.get(f"{b}.Stored_heat", empty_timeseries).values

            # One has to provide information of what Heat_buffer (i.e., the heat
            # added/extracted from the buffer at that timestep) is at t0.
            # Else the solution will always extract heat from the buffer at t0.
            # This information can be passed in two ways:
            # - non-trivial history of Heat_buffer at t0;
            # - non-trivial history of Stored_heat.
            # If not known, we assume that Heat_buffer is 0.0 at t0.

            if (len(hist_heat_buffer) < 1 or np.isnan(hist_heat_buffer[0])) and (
                len(hist_stored_heat) <= 1 or np.any(np.isnan(hist_stored_heat[-2:]))
            ):
                history[f"{b}.Heat_buffer"] = Timeseries(initial_time, [0.0])

        # TODO: add ATES when component is available

        return history

    def goal_programming_options(self):
        """
        Here we set the goal programming configuration. We use soft constraints for consecutive
        goals.
        """
        options = super().goal_programming_options()
        options["keep_soft_constraints"] = True
        return options

    def solver_options(self):
        """
        Here we define the solver options. By default we use the open-source solver cbc and casadi
        solver qpsol.
        """
        options = super().solver_options()
        options["casadi_solver"] = "qpsol"
        options["solver"] = "highs"
        return options

    def compiler_options(self):
        """
        In this function we set the compiler configuration.
        """
        options = super().compiler_options()
        options["resolve_parameter_values"] = True
        return options

    def __pipe_class_to_results(self):
        """
        This functions writes all resulting pipe class results to a dict.
        """
        for ensemble_member in range(self.ensemble_size):
            results = self.extract_results(ensemble_member)

            for pipe in self.heat_network_components.get("pipe", []):
                pipe_classes = self.pipe_classes(pipe)

                if not pipe_classes:
                    continue
                elif len(pipe_classes) == 1:
                    pipe_class = pipe_classes[0]
                else:
                    pipe_class = next(
                        c
                        for c, s in self.__pipe_topo_pipe_class_map[pipe].items()
                        if round(results[s][0]) == 1.0
                    )

                for p in [pipe, self.hot_to_cold_pipe(pipe)]:
                    self.__pipe_topo_pipe_class_result[p] = pipe_class

    def __pipe_diameter_to_parameters(self):
        """
        This function is used to update the parameters object with the results of the pipe class
        optimization
        """
        for ensemble_member in range(self.ensemble_size):
            d = self.__pipe_topo_diameter_area_parameters[ensemble_member]
            for pipe in self.__pipe_topo_pipe_class_map:
                pipe_class = self.get_optimized_pipe_class(pipe)

                for p in [pipe, self.hot_to_cold_pipe(pipe)]:
                    d[f"{p}.diameter"] = pipe_class.inner_diameter
                    d[f"{p}.area"] = pipe_class.area

    def _pipe_heat_loss_to_parameters(self):
        """
        This function is used to set the optimized heat losses in the parameters object.
        """
        options = self.heat_network_options()

        for ensemble_member in range(self.ensemble_size):
            parameters = self.parameters(ensemble_member)

            h = self.__pipe_topo_heat_loss_parameters[ensemble_member]
            for pipe in self.__pipe_topo_heat_losses:
                pipe_class = self.get_optimized_pipe_class(pipe)

                h[f"{pipe}.Heat_loss"] = self._pipe_heat_loss(
                    options, parameters, pipe, pipe_class.u_values
                )

    def priority_completed(self, priority):
        """
        This function is called after a priority of goals is completed. This function is used to
        specify operations between consecutive goals. Here we set some parameter attributes after
        the optimization is completed.
        """
        options = self.heat_network_options()

        self.__pipe_class_to_results()

        # The head loss mixin wants to do some check for the head loss
        # minimization priority that involves the diameter/area. We assume
        # that we're sort of done minimizing/choosing the pipe diameter, and
        # that we can set the parameters to the optimized values.
        if (
            options["minimize_head_losses"]
            and options["head_loss_option"] != HeadLossOption.NO_HEADLOSS
            and priority == self._hn_minimization_goal_class.priority
        ):
            self.__pipe_diameter_to_parameters()

        super().priority_completed(priority)

    def post(self):
        """
        In this post function we check the optimization results for accurately solving the
        constraints. We do this for the head losses and check if they are consistent with the flow
        direction. Whether, the minimum velocity is actually met. And whether, the directions of
        heat match the directions of the flow.
        """
        super().post()

        self.__pipe_class_to_results()
        self.__pipe_diameter_to_parameters()
        self._pipe_heat_loss_to_parameters()

        results = self.extract_results()
        parameters = self.parameters(0)
        options = self.heat_network_options()

        # The flow directions are the same as the heat directions if the
        # return (i.e. cold) line has zero heat throughout. Here we check that
        # this is indeed the case.
        for p in self.cold_pipes:
            heat_in = results[f"{p}.HeatIn.Heat"]
            heat_out = results[f"{p}.HeatOut.Heat"]
            if np.any(heat_in > 1.0) or np.any(heat_out > 1.0):
                logger.warning(f"Heat directions of pipes might be wrong. Check {p}.")

        if options["head_loss_option"] != HeadLossOption.NO_HEADLOSS:
            for p in self.heat_network_components.get("pipe", []):
                head_diff = results[f"{p}.HeatIn.H"] - results[f"{p}.HeatOut.H"]
                if parameters[f"{p}.length"] == 0.0 and not parameters[f"{p}.has_control_valve"]:
                    atol = self.variable_nominal(f"{p}.HeatIn.H") * 1e-5
                    assert np.allclose(head_diff, 0.0, atol=atol)
                else:
                    q = results[f"{p}.Q"]

                    try:
                        is_disconnected = np.round(results[self.__pipe_disconnect_map[p]])
                    except KeyError:
                        is_disconnected = np.zeros_like(q)

                    q_nominal = self.variable_nominal(
                        self.alias_relation.canonical_signed(f"{p}.Q")[0]
                    )
                    inds = (np.abs(q) / q_nominal > 1e-4) & (is_disconnected == 0)
                    if not options["heat_loss_disconnected_pipe"]:
                        assert np.all(np.sign(head_diff[inds]) == np.sign(q[inds]))

        minimum_velocity = options["minimum_velocity"]
        for p in self.heat_network_components.get("pipe", []):
            area = parameters[f"{p}.area"]

            if area == 0.0:
                continue

            q = results[f"{p}.Q"]
            v = q / area
            flow_dir = np.round(results[self.__pipe_to_flow_direct_map[p]])
            try:
                is_disconnected = np.round(results[self.__pipe_disconnect_map[p]])
            except KeyError:
                is_disconnected = np.zeros_like(q)

            inds_disconnected = is_disconnected == 1
            inds_positive = (flow_dir == 1) & ~inds_disconnected
            inds_negative = (flow_dir == 0) & ~inds_disconnected

            # We allow a bit of slack in the velocity. If the
            # exceedence/discrepancy is more than 0.1 mm/s, we log a warning,
            # if it's more than 1 cm/s, we log an error message.
            if np.any(inds_positive) or np.any(inds_negative):
                max_exceedence = max(
                    np.hstack(
                        [minimum_velocity - v[inds_positive], v[inds_negative] + minimum_velocity]
                    )
                )

                for criterion, log_level in [(0.01, logging.ERROR), (1e-4, logging.WARNING)]:
                    if max_exceedence > criterion:
                        logger.log(
                            log_level,
                            f"Velocity in {p} lower than minimum velocity {minimum_velocity} "
                            f"by more than {criterion} m/s. ({max_exceedence} m/s)",
                        )

                        break

            # Similar check for disconnected pipes, where we want the velocity
            # to be zero but allow the same amount of slack.
            if np.any(inds_disconnected):
                max_exceedence = max(np.abs(v[inds_disconnected]))

                for criterion, log_level in [(0.01, logging.ERROR), (1e-4, logging.WARNING)]:
                    if max_exceedence > criterion:
                        logger.log(
                            log_level,
                            f"Velocity in disconnected pipe {p} exceeds {criterion} m/s. "
                            f"({max_exceedence} m/s)",
                        )

                        break
