from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attribute_predicate import AttributePredicate


T = TypeVar("T", bound="ProcessAttributes")


@attr.s(auto_attribs=True)
class ProcessAttributes:
    """The SubmodelElementCollection “ProcessAttributes” contains 4 SubmodelElements that allow to describe one specific
    process attribute in a structured, self-describing and interoperable way.

    Args:
        id_ (str): The id of the process attributes.
        description (Optional[str]): The description of the process attributes.
        id_short (Optional[str]): The short id of the process attributes.
        semantic_id (Optional[str]): The semantic id of the process attributes.
        process_attributes (List[AttributePredicate]): The process attributes of the process (e.g. rotation speed, ...)

        Attributes:
            id_short (str):
            id (str):
            process_attributes (List['AttributePredicate']):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    process_attributes: List["AttributePredicate"]
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        process_attributes = []
        for process_attributes_item_data in self.process_attributes:
            process_attributes_item = process_attributes_item_data.to_dict()

            process_attributes.append(process_attributes_item)

        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "process_attributes": process_attributes,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.attribute_predicate import AttributePredicate

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        process_attributes = []
        _process_attributes = d.pop("process_attributes")
        for process_attributes_item_data in _process_attributes:
            process_attributes_item = AttributePredicate.from_dict(process_attributes_item_data)

            process_attributes.append(process_attributes_item)

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        process_attributes = cls(
            id_short=id_short,
            id=id,
            process_attributes=process_attributes,
            description=description,
            semantic_id=semantic_id,
        )

        process_attributes.additional_properties = d
        return process_attributes

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
