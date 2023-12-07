from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event import Event


T = TypeVar("T", bound="ExecutionModel")


@attr.s(auto_attribs=True)
class ExecutionModel:
    """The ExecutionModel represents all planned (scheduled) and performed (executed) execution of a process. It contains
    the schedule of the process, and the execution log of the process.

    Args:
        id_ (str): The id of the execution model.
        description (Optional[str]): The description of the execution model.
        id_short (Optional[str]): The short id of the execution model.
        semantic_id (Optional[str]): The semantic id of the execution model.
        schedule (List[Event]): The schedule of the procedure.
        exeuction_log (List[Event]): The execution log of the procedure.

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            schedule (Union[Unset, List['Event']]):
            exeuction_log (Union[Unset, List['Event']]):
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    schedule: Union[Unset, List["Event"]] = UNSET
    exeuction_log: Union[Unset, List["Event"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        semantic_id = self.semantic_id
        schedule: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = []
            for schedule_item_data in self.schedule:
                schedule_item = schedule_item_data.to_dict()

                schedule.append(schedule_item)

        exeuction_log: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.exeuction_log, Unset):
            exeuction_log = []
            for exeuction_log_item_data in self.exeuction_log:
                exeuction_log_item = exeuction_log_item_data.to_dict()

                exeuction_log.append(exeuction_log_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if exeuction_log is not UNSET:
            field_dict["exeuction_log"] = exeuction_log

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event import Event

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        schedule = []
        _schedule = d.pop("schedule", UNSET)
        for schedule_item_data in _schedule or []:
            schedule_item = Event.from_dict(schedule_item_data)

            schedule.append(schedule_item)

        exeuction_log = []
        _exeuction_log = d.pop("exeuction_log", UNSET)
        for exeuction_log_item_data in _exeuction_log or []:
            exeuction_log_item = Event.from_dict(exeuction_log_item_data)

            exeuction_log.append(exeuction_log_item)

        execution_model = cls(
            id_short=id_short,
            id=id,
            description=description,
            semantic_id=semantic_id,
            schedule=schedule,
            exeuction_log=exeuction_log,
        )

        execution_model.additional_properties = d
        return execution_model

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
