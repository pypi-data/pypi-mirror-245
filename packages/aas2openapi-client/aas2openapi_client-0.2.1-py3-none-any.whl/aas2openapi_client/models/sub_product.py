from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.sub_product_status import SubProductStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubProduct")


@attr.s(auto_attribs=True)
class SubProduct:
    """SubmodelElementCollection to describe a subproduct of a product with reference to its AAS, status informatino and
    quantity.

    Args:
        id_ (str): The id of the subproduct.
        description (Optional[str]): The description of the subproduct.
        id_short (Optional[str]): The short id of the subproduct.
        semantic_id (Optional[str]): The semantic id of the subproduct.
        product_type (str): The type of the subproduct.
        product_id (str): The AAS reference of the subproduct.
        status (Literal["assembled", "unassembled"]): The status of the subproduct.
        quantity (int): The quantity of the subproduct(s).

        Attributes:
            id_short (str):
            product_type (str):
            product_id (str):
            status (SubProductStatus):
            quantity (int):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    product_type: str
    product_id: str
    status: SubProductStatus
    quantity: int
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        product_type = self.product_type
        product_id = self.product_id
        status = self.status.value

        quantity = self.quantity
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "product_type": product_type,
                "product_id": product_id,
                "status": status,
                "quantity": quantity,
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

        product_type = d.pop("product_type")

        product_id = d.pop("product_id")

        status = SubProductStatus(d.pop("status"))

        quantity = d.pop("quantity")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        sub_product = cls(
            id_short=id_short,
            product_type=product_type,
            product_id=product_id,
            status=status,
            quantity=quantity,
            description=description,
            semantic_id=semantic_id,
        )

        sub_product.additional_properties = d
        return sub_product

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
