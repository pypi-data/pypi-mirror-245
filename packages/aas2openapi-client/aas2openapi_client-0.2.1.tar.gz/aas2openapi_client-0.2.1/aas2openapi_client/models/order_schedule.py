from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderSchedule")


@attr.s(auto_attribs=True)
class OrderSchedule:
    """Submodel to describe the schedule of an order.

    Args:
        id_ (str): The id of the order schedule.
        description (Optional[str]): The description of the order schedule.
        id_short (Optional[str]): The short id of the order schedule.
        semantic_id (Optional[str]): The semantic id of the order schedule.
        earliest_start_time (float): The earliest start time of the order.
        latest_start_time (float): The latest start time of the order.
        delivery_time (float): The delivery time of the order.

        Attributes:
            id_short (str):
            id (str):
            earliest_start_time (float):
            latest_start_time (float):
            delivery_time (float):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    earliest_start_time: float
    latest_start_time: float
    delivery_time: float
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        earliest_start_time = self.earliest_start_time
        latest_start_time = self.latest_start_time
        delivery_time = self.delivery_time
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "earliest_start_time": earliest_start_time,
                "latest_start_time": latest_start_time,
                "delivery_time": delivery_time,
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

        id = d.pop("id_")

        earliest_start_time = d.pop("earliest_start_time")

        latest_start_time = d.pop("latest_start_time")

        delivery_time = d.pop("delivery_time")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        order_schedule = cls(
            id_short=id_short,
            id=id,
            earliest_start_time=earliest_start_time,
            latest_start_time=latest_start_time,
            delivery_time=delivery_time,
            description=description,
            semantic_id=semantic_id,
        )

        order_schedule.additional_properties = d
        return order_schedule

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
