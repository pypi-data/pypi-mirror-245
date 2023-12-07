from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sub_resource import SubResource


T = TypeVar("T", bound="ResourceConfiguration")


@attr.s(auto_attribs=True)
class ResourceConfiguration:
    """Submodel to describe the configuration of a resource, by describing its sub resources and their position and
    orientation.

    Args:
        id_ (str): The id of the resource hierarchy.
        description (Optional[str]): The description of the resource hierarchy.
        id_short (Optional[str]): The short id of the resource hierarchy.
        semantic_id (Optional[str]): The semantic id of the resource hierarchy.
        sub_resources (Optional[List[SubResource]]): IDs ob sub resources

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            sub_resources (Union[Unset, List['SubResource']]):
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    sub_resources: Union[Unset, List["SubResource"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        semantic_id = self.semantic_id
        sub_resources: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sub_resources, Unset):
            sub_resources = []
            for sub_resources_item_data in self.sub_resources:
                sub_resources_item = sub_resources_item_data.to_dict()

                sub_resources.append(sub_resources_item)

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
        if sub_resources is not UNSET:
            field_dict["sub_resources"] = sub_resources

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sub_resource import SubResource

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        sub_resources = []
        _sub_resources = d.pop("sub_resources", UNSET)
        for sub_resources_item_data in _sub_resources or []:
            sub_resources_item = SubResource.from_dict(sub_resources_item_data)

            sub_resources.append(sub_resources_item)

        resource_configuration = cls(
            id_short=id_short,
            id=id,
            description=description,
            semantic_id=semantic_id,
            sub_resources=sub_resources,
        )

        resource_configuration.additional_properties = d
        return resource_configuration

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
