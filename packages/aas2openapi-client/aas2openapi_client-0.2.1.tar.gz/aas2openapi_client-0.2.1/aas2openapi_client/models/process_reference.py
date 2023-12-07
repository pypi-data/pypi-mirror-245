from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessReference")


@attr.s(auto_attribs=True)
class ProcessReference:
    """Submodel to reference process to create a product.

    Args:
        id_ (str): The id of the process reference.
        description (Optional[str]): The description of the process reference.
        id_short (Optional[str]): The short id of the process reference.
        semantic_id (Optional[str]): The semantic id of the process reference.
        process_id (str): reference to the process to create the product
        alternative_process_ids (Optional[List[str]]): alternative processes to create the product

        Attributes:
            id_short (str):
            id (str):
            process_id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            alternative_processes_ids (Union[Unset, List[str]]):
    """

    id_short: str
    id: str
    process_id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    alternative_processes_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        process_id = self.process_id
        description = self.description
        semantic_id = self.semantic_id
        alternative_processes_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.alternative_processes_ids, Unset):
            alternative_processes_ids = self.alternative_processes_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "process_id": process_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if alternative_processes_ids is not UNSET:
            field_dict["alternative_processes_ids"] = alternative_processes_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        process_id = d.pop("process_id")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        alternative_processes_ids = cast(List[str], d.pop("alternative_processes_ids", UNSET))

        process_reference = cls(
            id_short=id_short,
            id=id,
            process_id=process_id,
            description=description,
            semantic_id=semantic_id,
            alternative_processes_ids=alternative_processes_ids,
        )

        process_reference.additional_properties = d
        return process_reference

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
