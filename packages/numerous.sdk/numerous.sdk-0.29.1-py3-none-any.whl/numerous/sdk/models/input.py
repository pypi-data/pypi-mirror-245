from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union


class InputSourceType(Enum):
    SCENARIO = "scenario"
    DATASET = "dataset"


@dataclass
class InputSource:
    project_id: str
    scenario_id: str
    type: InputSourceType
    offset: Optional[float] = None


@dataclass
class InputVariableScenarioSource:
    source: InputSource
    tag: str


@dataclass
class InputVariableStaticSource:
    value: float


def get_input_sources_from_scenario_document(
    data: dict[str, Any]
) -> dict[str, InputSource]:
    input_sources = data.get("inputScenarios", [])
    return {
        input_source["scenarioID"]: InputSource(
            project_id=input_source["projectID"],
            scenario_id=input_source["scenarioID"],
            type=InputSourceType(input_source["type"]),
            offset=input_source.get("offset"),
        )
        for input_source in input_sources
    }


@dataclass
class InputVariable:
    uuid: str
    id: str
    display_name: str
    source: Union[InputVariableScenarioSource, InputVariableStaticSource]
    scale: float
    offset: float
