from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralInformation")


@attr.s(auto_attribs=True)
class GeneralInformation:
    """Submodel to describe the general information of an order.

    Args:
        id_ (str): The id of the general information.
        description (Optional[str]): The description of the general information.
        id_short (Optional[str]): The short id of the general information.
        semantic_id (Optional[str]): The semantic id of the general information.
        order_id (str): The id of the order.
        priority (int): The priority of the order.
        customer_information (str): The customer information of the order.

        Attributes:
            id_short (str):
            id (str):
            order_id (str):
            priority (int):
            customer_information (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    order_id: str
    priority: int
    customer_information: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        order_id = self.order_id
        priority = self.priority
        customer_information = self.customer_information
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "order_id": order_id,
                "priority": priority,
                "customer_information": customer_information,
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

        order_id = d.pop("order_id")

        priority = d.pop("priority")

        customer_information = d.pop("customer_information")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        general_information = cls(
            id_short=id_short,
            id=id,
            order_id=order_id,
            priority=priority,
            customer_information=customer_information,
            description=description,
            semantic_id=semantic_id,
        )

        general_information.additional_properties = d
        return general_information

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
