from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="InformationInterface")


@attr.s(auto_attribs=True)
class InformationInterface:
    """Interface for information exchange with the resource.

    Args:
        protocol (str): The protocol of the information interface.
        adress (str): The adress of the information interface (e.g. IP adress)
        port (Optional[int]): The port of the information interface.

        Attributes:
            id_short (str):
            protocol (str):
            adress (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            port (Union[Unset, int]):
    """

    id_short: str
    protocol: str
    adress: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    port: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        protocol = self.protocol
        adress = self.adress
        description = self.description
        semantic_id = self.semantic_id
        port = self.port

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "protocol": protocol,
                "adress": adress,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if port is not UNSET:
            field_dict["port"] = port

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        protocol = d.pop("protocol")

        adress = d.pop("adress")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        port = d.pop("port", UNSET)

        information_interface = cls(
            id_short=id_short,
            protocol=protocol,
            adress=adress,
            description=description,
            semantic_id=semantic_id,
            port=port,
        )

        information_interface.additional_properties = d
        return information_interface

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
