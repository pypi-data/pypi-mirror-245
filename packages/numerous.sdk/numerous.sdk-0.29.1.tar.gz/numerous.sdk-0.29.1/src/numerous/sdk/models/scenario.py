from dataclasses import dataclass
from typing import Any, Optional

from numerous.sdk.models.input import (
    InputSource,
    get_input_sources_from_scenario_document,
)
from numerous.sdk.models.optimization import OptimizationConfiguration

from .component import Component, get_components_from_scenario_document
from .job import Job
from .parameter import Parameter, get_parameters_dict


@dataclass
class Scenario:
    id: str
    name: str
    components: dict[str, Component]
    parameters: dict[str, Parameter]
    jobs: list[Job]
    input_sources: list[InputSource]
    optimization: Optional[OptimizationConfiguration] = None

    @staticmethod
    def from_document(
        data: dict[str, Any], optimization: Optional[OptimizationConfiguration] = None
    ) -> "Scenario":
        input_sources_mapping = get_input_sources_from_scenario_document(data)

        return Scenario(
            id=data["id"],
            name=data.get("scenarioName", ""),
            components=get_components_from_scenario_document(
                data, input_sources_mapping
            ),
            input_sources=list(input_sources_mapping.values()),
            jobs=[
                Job.from_document(job_id, job_data)
                for job_id, job_data in data.get("jobs", {}).items()
            ],
            optimization=optimization,
            parameters=get_parameters_dict(data.get("parameters", [])),
        )
