from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubResource")


@attr.s(auto_attribs=True)
class SubResource:
    """SubmodelElementCollection to describe a subresource of a resource with reference to its AAS, position and
    orientation (2D or 3D).

    Args:
        id_ (str): The id of the subresource.
        description (Optional[str]): The description of the subresource.
        id_short (Optional[str]): The short id of the subresource.
        semantic_id (Optional[str]): The semantic id of the subresource.
        resource_id (str): The id of the subresource.
        position (conlist(float, min_items=2, max_items=3)): The position of the subresource (x, y, z).
        orientation (conlist(float, min_items=1, max_items=3)): The orientation of the subresource (alpha, beta, gamma).

        Attributes:
            id_short (str):
            resource_id (str):
            position (List[float]):
            orientation (List[float]):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    resource_id: str
    position: List[float]
    orientation: List[float]
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        resource_id = self.resource_id
        position = self.position

        orientation = self.orientation

        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "resource_id": resource_id,
                "position": position,
                "orientation": orientation,
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

        resource_id = d.pop("resource_id")

        position = cast(List[float], d.pop("position"))

        orientation = cast(List[float], d.pop("orientation"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        sub_resource = cls(
            id_short=id_short,
            resource_id=resource_id,
            position=position,
            orientation=orientation,
            description=description,
            semantic_id=semantic_id,
        )

        sub_resource.additional_properties = d
        return sub_resource

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
