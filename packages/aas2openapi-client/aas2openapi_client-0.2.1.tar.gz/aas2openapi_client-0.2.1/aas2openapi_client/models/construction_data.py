from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstructionData")


@attr.s(auto_attribs=True)
class ConstructionData:
    """Submodel to describe the construction data of a product.

    Args:
        id_ (str): The id of the construction data.
        description (Optional[str]): The description of the construction data.
        id_short (Optional[str]): The short id of the construction data.
        semantic_id (Optional[str]): The semantic id of the construction data.
        cad_file (Optional[str]): IRI to a CAD file of the product.

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            cad_file (Union[Unset, str]):
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    cad_file: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        semantic_id = self.semantic_id
        cad_file = self.cad_file

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
        if cad_file is not UNSET:
            field_dict["cad_file"] = cad_file

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        cad_file = d.pop("cad_file", UNSET)

        construction_data = cls(
            id_short=id_short,
            id=id,
            description=description,
            semantic_id=semantic_id,
            cad_file=cad_file,
        )

        construction_data.additional_properties = d
        return construction_data

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
