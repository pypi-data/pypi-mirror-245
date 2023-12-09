from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Event")


@attr.s(auto_attribs=True)
class Event:
    """An Event represents a single event in the schedule or execution log of a procedure. It contains the event type, the
    time of the event, and the resource that executed the event and the product that was processed by the event.

    Args:
        description (Optional[str]): The description of the event.
        id_short (Optional[str]): The short id of the event.
        semantic_id (Optional[str]): The semantic id of the event.
        product_id (str): The id of the product that was processed by the event.
        process_id (str): The id of the process that was realized by the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        resource_id (str): The id of the resource that executed the event.

        Attributes:
            id_short (str):
            product_id (str):
            process_id (str):
            start_time (float):
            end_time (float):
            resource_id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    product_id: str
    process_id: str
    start_time: float
    end_time: float
    resource_id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        product_id = self.product_id
        process_id = self.process_id
        start_time = self.start_time
        end_time = self.end_time
        resource_id = self.resource_id
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "product_id": product_id,
                "process_id": process_id,
                "start_time": start_time,
                "end_time": end_time,
                "resource_id": resource_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        product_id = d.pop("product_id")

        process_id = d.pop("process_id")

        start_time = d.pop("start_time")

        end_time = d.pop("end_time")

        resource_id = d.pop("resource_id")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        event = cls(
            id_short=id_short,
            product_id=product_id,
            process_id=process_id,
            start_time=start_time,
            end_time=end_time,
            resource_id=resource_id,
            description=description,
            semantic_id=semantic_id,
        )

        event.additional_properties = d
        return event

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
