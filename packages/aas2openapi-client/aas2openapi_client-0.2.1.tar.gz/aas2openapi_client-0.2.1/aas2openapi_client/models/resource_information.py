from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.resource_information_production_level import ResourceInformationProductionLevel
from ..models.resource_information_resource_type import ResourceInformationResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceInformation")


@attr.s(auto_attribs=True)
class ResourceInformation:
    """Submodel to describe the general information of a resource.

    Args:
        id_ (str): The id of the general information.
        description (Optional[str]): The description of the general information.
        id_short (Optional[str]): The short id of the general information.
        semantic_id (Optional[str]): The semantic id of the general information.
        manufacturer (Optional[str]): The manufacturer of the resource.
        production_level (Literal["Module", "Station", "System", "Plant", "Network"]): The production level of the
    resource.
        resource_type (Literal["Manufacturing", "Material Flow", "Storage"]): The type of the resource.

        Attributes:
            id_short (str):
            id (str):
            production_level (ResourceInformationProductionLevel):
            resource_type (ResourceInformationResourceType):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            manufacturer (Union[Unset, str]):
    """

    id_short: str
    id: str
    production_level: ResourceInformationProductionLevel
    resource_type: ResourceInformationResourceType
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    manufacturer: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        production_level = self.production_level.value

        resource_type = self.resource_type.value

        description = self.description
        semantic_id = self.semantic_id
        manufacturer = self.manufacturer

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "production_level": production_level,
                "resource_type": resource_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if manufacturer is not UNSET:
            field_dict["manufacturer"] = manufacturer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        production_level = ResourceInformationProductionLevel(d.pop("production_level"))

        resource_type = ResourceInformationResourceType(d.pop("resource_type"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        manufacturer = d.pop("manufacturer", UNSET)

        resource_information = cls(
            id_short=id_short,
            id=id,
            production_level=production_level,
            resource_type=resource_type,
            description=description,
            semantic_id=semantic_id,
            manufacturer=manufacturer,
        )

        resource_information.additional_properties = d
        return resource_information

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
