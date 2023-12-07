from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sub_product import SubProduct


T = TypeVar("T", bound="BOM")


@attr.s(auto_attribs=True)
class BOM:
    """Submodel to describe the bill of materials of a product.

    Args:
        id_ (str): The id of the bill of materials.
        description (Optional[str]): The description of the bill of materials.
        id_short (Optional[str]): The short id of the bill of materials.
        semantic_id (Optional[str]): The semantic id of the bill of materials.
        sub_product_count (Optional[int]): The total number of subproducts (depht 1)
        sub_products (Optional[List[SubmodelElementCollection]]): The list of subproducts contained in the product
    (depht 1)

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            sub_product_count (Union[Unset, int]):
            sub_products (Union[Unset, List['SubProduct']]):
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    sub_product_count: Union[Unset, int] = UNSET
    sub_products: Union[Unset, List["SubProduct"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        semantic_id = self.semantic_id
        sub_product_count = self.sub_product_count
        sub_products: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sub_products, Unset):
            sub_products = []
            for sub_products_item_data in self.sub_products:
                sub_products_item = sub_products_item_data.to_dict()

                sub_products.append(sub_products_item)

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
        if sub_product_count is not UNSET:
            field_dict["sub_product_count"] = sub_product_count
        if sub_products is not UNSET:
            field_dict["sub_products"] = sub_products

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sub_product import SubProduct

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        sub_product_count = d.pop("sub_product_count", UNSET)

        sub_products = []
        _sub_products = d.pop("sub_products", UNSET)
        for sub_products_item_data in _sub_products or []:
            sub_products_item = SubProduct.from_dict(sub_products_item_data)

            sub_products.append(sub_products_item)

        bom = cls(
            id_short=id_short,
            id=id,
            description=description,
            semantic_id=semantic_id,
            sub_product_count=sub_product_count,
            sub_products=sub_products,
        )

        bom.additional_properties = d
        return bom

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
