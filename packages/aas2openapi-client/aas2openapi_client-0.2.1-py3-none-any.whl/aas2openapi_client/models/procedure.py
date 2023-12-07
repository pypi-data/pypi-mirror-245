from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_model import ExecutionModel
    from ..models.procedure_information import ProcedureInformation
    from ..models.process_attributes import ProcessAttributes
    from ..models.time_model import TimeModel


T = TypeVar("T", bound="Procedure")


@attr.s(auto_attribs=True)
class Procedure:
    """The Procedure class represents a procedure that is executed by a resource. It contains the process
    attributes, the execution model, and the time model of the procedure.

    Args:
        id_ (str): The id of the procedure.
        description (Optional[str]): The description of the procedure.
        id_short (Optional[str]): The short id of the procedure.
        process_attributes (processes.ProcessAttributes): Parameters that describe what the procedure does and how it
    does it.
        execution (ExecutionModel): The execution model of the procedure containing planned and performed executions of
    this procedure.
        time_model (TimeModel): The time model of the procedure containing parameters to represent the timely duration
    of the procedure.

        Attributes:
            id_short (str):
            id (str):
            procedure_information (ProcedureInformation): Submodel containing general information about the procedure.

                Args:
                    procedure_type (ProcedureTypeEnum): The type of the procedure.
            process_attributes (ProcessAttributes): The SubmodelElementCollection “ProcessAttributes” contains 4
                SubmodelElements that allow to describe one specific process attribute in a structured, self-describing and
                interoperable way.

                Args:
                    id_ (str): The id of the process attributes.
                    description (Optional[str]): The description of the process attributes.
                    id_short (Optional[str]): The short id of the process attributes.
                    semantic_id (Optional[str]): The semantic id of the process attributes.
                    process_attributes (List[AttributePredicate]): The process attributes of the process (e.g. rotation speed,
                ...)
            time_model (TimeModel): Submodel containing parameters to represent the timely duration of a procedure.

                Args:
                    id_ (str): The id of the time model.
                    description (Optional[str]): The description of the time model.
                    id_short (Optional[str]): The short id of the time model.
                    semantic_id (Optional[str]): The semantic id of the time model.
                    type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time model.
                    sequence (Optional[List[float]]): The sequence of timely values (only for sequential time models).
                    repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential time models).
                    distribution_type (Optional[str]): The name of the distribution (e.g. "normal", "exponential", "weibull",
                "lognormal", "gamma", "beta", "uniform", "triangular", "discrete") (only for distribution time models).
                    distribution_parameters (Optional[List[float]]): The parameters of the distribution (1: location, 2: scale,
                3 and 4: shape) (only for distribution time models).
                    speed (Optional[float]): The speed of the resource (only for distance-based time models).
                    reaction_time (Optional[float]): The reaction time of the resource (only for distance-based time models).
                    acceleration (Optional[float]): The acceleration of the resource (only for distance-based time models).
                    deceleration (Optional[float]): The deceleration of the resource (only for distance-based time models).
            description (Union[Unset, str]):
            execution_model (Union[Unset, ExecutionModel]): The ExecutionModel represents all planned (scheduled) and
                performed (executed) execution of a process. It contains the schedule of the process, and the execution log of
                the process.

                Args:
                    id_ (str): The id of the execution model.
                    description (Optional[str]): The description of the execution model.
                    id_short (Optional[str]): The short id of the execution model.
                    semantic_id (Optional[str]): The semantic id of the execution model.
                    schedule (List[Event]): The schedule of the procedure.
                    exeuction_log (List[Event]): The execution log of the procedure.
    """

    id_short: str
    id: str
    procedure_information: "ProcedureInformation"
    process_attributes: "ProcessAttributes"
    time_model: "TimeModel"
    description: Union[Unset, str] = UNSET
    execution_model: Union[Unset, "ExecutionModel"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        procedure_information = self.procedure_information.to_dict()

        process_attributes = self.process_attributes.to_dict()

        time_model = self.time_model.to_dict()

        description = self.description
        execution_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.execution_model, Unset):
            execution_model = self.execution_model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "procedure_information": procedure_information,
                "process_attributes": process_attributes,
                "time_model": time_model,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if execution_model is not UNSET:
            field_dict["execution_model"] = execution_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.execution_model import ExecutionModel
        from ..models.procedure_information import ProcedureInformation
        from ..models.process_attributes import ProcessAttributes
        from ..models.time_model import TimeModel

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        procedure_information = ProcedureInformation.from_dict(d.pop("procedure_information"))

        process_attributes = ProcessAttributes.from_dict(d.pop("process_attributes"))

        time_model = TimeModel.from_dict(d.pop("time_model"))

        description = d.pop("description", UNSET)

        _execution_model = d.pop("execution_model", UNSET)
        execution_model: Union[Unset, ExecutionModel]
        if isinstance(_execution_model, Unset):
            execution_model = UNSET
        else:
            execution_model = ExecutionModel.from_dict(_execution_model)

        procedure = cls(
            id_short=id_short,
            id=id,
            procedure_information=procedure_information,
            process_attributes=process_attributes,
            time_model=time_model,
            description=description,
            execution_model=execution_model,
        )

        procedure.additional_properties = d
        return procedure

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
