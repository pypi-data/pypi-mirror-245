from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ordered_product import OrderedProduct


T = TypeVar("T", bound="OrderedProducts")


@attr.s(auto_attribs=True)
class OrderedProducts:
    """Submodel that describes the product instances of an order with reference to their AAS.

    Args:
        id_ (str): The id of the product instances.
        description (Optional[str]): The description of the product instances.
        id_short (Optional[str]): The short id of the product instances.
        semantic_id (Optional[str]): The semantic id of the product instances.
        ordered_products (List[OrderedProduct]): The list of ordered products specifying the ordered type and the
    quantity of the product type. .

        Attributes:
            id_short (str):
            id (str):
            ordered_products (List['OrderedProduct']):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    ordered_products: List["OrderedProduct"]
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        ordered_products = []
        for ordered_products_item_data in self.ordered_products:
            ordered_products_item = ordered_products_item_data.to_dict()

            ordered_products.append(ordered_products_item)

        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "ordered_products": ordered_products,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ordered_product import OrderedProduct

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        ordered_products = []
        _ordered_products = d.pop("ordered_products")
        for ordered_products_item_data in _ordered_products:
            ordered_products_item = OrderedProduct.from_dict(ordered_products_item_data)

            ordered_products.append(ordered_products_item)

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        ordered_products = cls(
            id_short=id_short,
            id=id,
            ordered_products=ordered_products,
            description=description,
            semantic_id=semantic_id,
        )

        ordered_products.additional_properties = d
        return ordered_products

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
