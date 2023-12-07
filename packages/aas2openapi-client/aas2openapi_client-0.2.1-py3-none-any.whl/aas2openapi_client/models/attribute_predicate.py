from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AttributePredicate")


@attr.s(auto_attribs=True)
class AttributePredicate:
    """The SubmodelElementCollection “AttributePredicate” contains 4 SubmodelElements that allow to describe one specific
    process attribute in a structured, self-describing and interoperable way.

    Args:
        id_ (str): The id of the attribute predicate.
        description (Optional[str]): The description of the attribute predicate.
        id_short (Optional[str]): The short id of the attribute predicate.
        semantic_id (Optional[str]): The semantic id of the attribute predicate.
        attribute_carrier (str): Semantic reference to the general type of process or procedure that is describeded by
    this attribute, e.g. a semantic reference to a milling process definition.
        general_attribute (str): Describes semantically the type of attribute that is specified for the attribute
    carrier, e.g. rotation speed.
        predicate_type (str): Describes semantically what is specified by the value and how to compare it, e.g.
    requires_to_be, equals, within_range, ....
        attribute_value (str): Describes value of the attribute that is specified for.

        Attributes:
            id_short (str):
            attribute_carrier (str):
            general_attribute (str):
            predicate_type (str):
            attribute_value (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    attribute_carrier: str
    general_attribute: str
    predicate_type: str
    attribute_value: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        attribute_carrier = self.attribute_carrier
        general_attribute = self.general_attribute
        predicate_type = self.predicate_type
        attribute_value = self.attribute_value
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "attribute_carrier": attribute_carrier,
                "general_attribute": general_attribute,
                "predicate_type": predicate_type,
                "attribute_value": attribute_value,
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

        attribute_carrier = d.pop("attribute_carrier")

        general_attribute = d.pop("general_attribute")

        predicate_type = d.pop("predicate_type")

        attribute_value = d.pop("attribute_value")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        attribute_predicate = cls(
            id_short=id_short,
            attribute_carrier=attribute_carrier,
            general_attribute=general_attribute,
            predicate_type=predicate_type,
            attribute_value=attribute_value,
            description=description,
            semantic_id=semantic_id,
        )

        attribute_predicate.additional_properties = d
        return attribute_predicate

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
