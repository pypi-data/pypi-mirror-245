"""Components are the basic building blocks of systems.

This module contains the definition of Components, and the implementation of
functionality to create them.
"""
from dataclasses import dataclass
from typing import Any

from numerous.sdk.models.input import (
    InputSource,
    InputVariable,
    InputVariableScenarioSource,
    InputVariableStaticSource,
)
from numerous.sdk.models.parameter import Parameter, get_parameters_dict


@dataclass
class SubComponentNotFound(Exception):
    """Raised when creating a :class:`Component` is configured with a subcomponent that
    does not exist.
    """

    component_uuid: str


@dataclass
class Component:
    """A component of a :class:`numerous.sdk.models.scenario.Scenario`, containing
    parameters, input variables, and any subcomponents."""

    uuid: str
    id: str
    type: str
    name: str
    item_class: list[str]
    is_enabled: bool
    is_main: bool
    input_variables: dict[str, InputVariable]
    components: dict[str, "Component"]
    parameters: dict[str, Parameter]
    """The subcomponents of this component."""

    @staticmethod
    def from_document(
        component: dict[str, Any],
        all_components: list[dict[str, Any]],
        input_sources_mapping: dict[str, InputSource],
    ) -> "Component":
        return Component(
            uuid=component["uuid"],
            id=component["id"],
            type=component["type"],
            name=component["name"],
            is_enabled=not bool(component["disabled"]),
            is_main=bool(component["isMainComponent"]),
            components=_extract_subcomponents(
                component, all_components, input_sources_mapping
            ),
            item_class=component["item_class"].split("."),
            input_variables=_extract_input_variables(component, input_sources_mapping),
            parameters=get_parameters_dict(component.get("parameters", [])),
        )


def _extract_subcomponents(
    component: dict[str, Any],
    all_components: list[dict[str, Any]],
    input_sources_mapping: dict[str, InputSource],
):
    return {
        subcomponent_ref["name"]: _extract_subcomponent(
            subcomponent_ref["uuid"],
            all_components,
            input_sources_mapping,
        )
        for subcomponent_ref in component.get("subcomponents", [])
    }


def _extract_subcomponent(
    subcomponent_uuid: str,
    all_components: list[dict[str, Any]],
    input_sources_mapping: dict[str, InputSource],
) -> Component:
    subcomponent = next(
        (
            subcomponent
            for subcomponent in all_components
            if subcomponent.get("uuid") == subcomponent_uuid
        ),
        None,
    )

    if subcomponent is None:
        raise SubComponentNotFound(component_uuid=subcomponent_uuid)

    return Component.from_document(
        subcomponent, all_components, input_sources_mapping=input_sources_mapping
    )


def get_components_from_scenario_document(
    data: dict[str, Any], input_sources_mapping: dict[str, InputSource]
) -> dict[str, Component]:
    components = data.get("simComponents", [])
    subcomponent_uuids = _get_all_subcomponent_uuids(components)
    return {
        component["name"]: Component.from_document(
            component, components, input_sources_mapping
        )
        for component in components
        if component["uuid"] not in subcomponent_uuids
    }


def _get_all_subcomponent_uuids(components: list[dict[str, Any]]) -> set[str]:
    all_subcomponent_uuids = set()

    for component in components:
        for subcomponent in component.get("subcomponents", []):
            all_subcomponent_uuids.add(subcomponent["uuid"])

    return all_subcomponent_uuids


def _extract_input_variable(
    component: dict[str, Any],
    input_variable: dict[str, Any],
    input_sources_mapping: dict[str, InputSource],
    tag_prefix: str = "Stub",
    tag_separator: str = ".",
) -> InputVariable:
    if (data_source_type := input_variable["dataSourceType"]) == "static":
        source = InputVariableStaticSource(value=input_variable["value"])
    elif data_source_type in ["scenario", "control_machines"]:
        data_source_id = input_variable["dataSourceId"]
        tag = tag_separator.join(
            filter(None, [tag_prefix, component["name"], input_variable["id"]])
        )
        source = InputVariableScenarioSource(input_sources_mapping[data_source_id], tag)
    else:
        raise ValueError(f"Invalid data source type: {data_source_type}")
    return InputVariable(
        id=input_variable["id"],
        uuid=input_variable["uuid"],
        source=source,
        display_name=input_variable["display"],
        scale=input_variable["scaling"],
        offset=input_variable["offset"],
    )


def _extract_input_variables(
    component: dict[str, Any],
    input_sources_mapping: dict[str, InputSource],
) -> dict[str, InputVariable]:
    variables = component.get("inputVariables", [])
    variables_list: list[InputVariable] = [
        _extract_input_variable(component, variable, input_sources_mapping)
        for variable in variables
    ]
    return {variable.id: variable for variable in variables_list}
