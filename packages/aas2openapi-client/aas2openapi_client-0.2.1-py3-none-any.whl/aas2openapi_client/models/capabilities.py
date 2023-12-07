from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Capabilities")


@attr.s(auto_attribs=True)
class Capabilities:
    """Submodel to describe the capabilities of a resource by describing available
    procedures in the resource.

    Args:
        id_ (str): The id of the capabilities.
        description (Optional[str]): The description of the capabilities.
        id_short (Optional[str]): The short id of the capabilities.
        semantic_id (Optional[str]): The semantic id of the capabilities.
        procedure_ids (List[str]): The list of ids of procedure that are available for the resource.

        Attributes:
            id_short (str):
            id (str):
            procedures_ids (List[str]):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    procedures_ids: List[str]
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        procedures_ids = self.procedures_ids

        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "procedures_ids": procedures_ids,
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

        procedures_ids = cast(List[str], d.pop("procedures_ids"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        capabilities = cls(
            id_short=id_short,
            id=id,
            procedures_ids=procedures_ids,
            description=description,
            semantic_id=semantic_id,
        )

        capabilities.additional_properties = d
        return capabilities

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
