from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderedProduct")


@attr.s(auto_attribs=True)
class OrderedProduct:
    """Submodel that describes the product instances of an order with reference to their AAS.

    Args:
        id_ (str): The id of the product instances.
        description (Optional[str]): The description of the product instances.
        id_short (Optional[str]): The short id of the product instances.
        semantic_id (Optional[str]): The semantic id of the product instances.
        product_type (str): Product type of the order.
        target_quantity (int): Number of requested product instances
        product_ids (List[str]): Reference to the AAS of the product instances of the order.

        Attributes:
            id_short (str):
            product_type (str):
            target_quantity (int):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            product_ids (Union[Unset, List[str]]):
    """

    id_short: str
    product_type: str
    target_quantity: int
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    product_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        product_type = self.product_type
        target_quantity = self.target_quantity
        description = self.description
        semantic_id = self.semantic_id
        product_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.product_ids, Unset):
            product_ids = self.product_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "product_type": product_type,
                "target_quantity": target_quantity,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if product_ids is not UNSET:
            field_dict["product_ids"] = product_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        product_type = d.pop("product_type")

        target_quantity = d.pop("target_quantity")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        product_ids = cast(List[str], d.pop("product_ids", UNSET))

        ordered_product = cls(
            id_short=id_short,
            product_type=product_type,
            target_quantity=target_quantity,
            description=description,
            semantic_id=semantic_id,
            product_ids=product_ids,
        )

        ordered_product.additional_properties = d
        return ordered_product

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
