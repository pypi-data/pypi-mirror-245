from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProductInformation")


@attr.s(auto_attribs=True)
class ProductInformation:
    """Submodel to describe general information of the product.

    Args:
        id_ (str): The id of the product general information.
        description (Optional[str]): The description of the product general information.
        id_short (Optional[str]): The short id of the product general information.
        semantic_id (Optional[str]): The semantic id of the product general information.
        product_type (str): The type of the product.
        manufacturer (str): The manufacturer of the product.

        Attributes:
            id_short (str):
            id (str):
            product_type (str):
            manufacturer (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    product_type: str
    manufacturer: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        product_type = self.product_type
        manufacturer = self.manufacturer
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "product_type": product_type,
                "manufacturer": manufacturer,
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

        product_type = d.pop("product_type")

        manufacturer = d.pop("manufacturer")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        product_information = cls(
            id_short=id_short,
            id=id,
            product_type=product_type,
            manufacturer=manufacturer,
            description=description,
            semantic_id=semantic_id,
        )

        product_information.additional_properties = d
        return product_information

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
