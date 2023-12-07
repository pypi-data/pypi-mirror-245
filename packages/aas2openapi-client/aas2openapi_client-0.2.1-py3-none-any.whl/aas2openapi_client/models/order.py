from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.general_information import GeneralInformation
    from ..models.order_schedule import OrderSchedule
    from ..models.ordered_products import OrderedProducts


T = TypeVar("T", bound="Order")


@attr.s(auto_attribs=True)
class Order:
    """AAS to describe an order.

    Args:
        id_ (str): The id of the order.
        description (Optional[str]): The description of the order.
        id_short (Optional[str]): The short id of the order.
        product_instances (ProductInstances): The product instances of the order.
        general_information (GeneralInformation): The general information of the order.
        order_schedule (OrderSchedule): The schedule of the order.

        Attributes:
            id_short (str):
            id (str):
            general_information (GeneralInformation): Submodel to describe the general information of an order.

                Args:
                    id_ (str): The id of the general information.
                    description (Optional[str]): The description of the general information.
                    id_short (Optional[str]): The short id of the general information.
                    semantic_id (Optional[str]): The semantic id of the general information.
                    order_id (str): The id of the order.
                    priority (int): The priority of the order.
                    customer_information (str): The customer information of the order.
            description (Union[Unset, str]):
            order_schedule (Union[Unset, OrderSchedule]): Submodel to describe the schedule of an order.

                Args:
                    id_ (str): The id of the order schedule.
                    description (Optional[str]): The description of the order schedule.
                    id_short (Optional[str]): The short id of the order schedule.
                    semantic_id (Optional[str]): The semantic id of the order schedule.
                    earliest_start_time (float): The earliest start time of the order.
                    latest_start_time (float): The latest start time of the order.
                    delivery_time (float): The delivery time of the order.
            ordered_products (Union[Unset, OrderedProducts]): Submodel that describes the product instances of an order with
                reference to their AAS.

                Args:
                    id_ (str): The id of the product instances.
                    description (Optional[str]): The description of the product instances.
                    id_short (Optional[str]): The short id of the product instances.
                    semantic_id (Optional[str]): The semantic id of the product instances.
                    ordered_products (List[OrderedProduct]): The list of ordered products specifying the ordered type and the
                quantity of the product type. .
    """

    id_short: str
    id: str
    general_information: "GeneralInformation"
    description: Union[Unset, str] = UNSET
    order_schedule: Union[Unset, "OrderSchedule"] = UNSET
    ordered_products: Union[Unset, "OrderedProducts"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        general_information = self.general_information.to_dict()

        description = self.description
        order_schedule: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_schedule, Unset):
            order_schedule = self.order_schedule.to_dict()

        ordered_products: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ordered_products, Unset):
            ordered_products = self.ordered_products.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "general_information": general_information,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if order_schedule is not UNSET:
            field_dict["order_schedule"] = order_schedule
        if ordered_products is not UNSET:
            field_dict["ordered_products"] = ordered_products

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.general_information import GeneralInformation
        from ..models.order_schedule import OrderSchedule
        from ..models.ordered_products import OrderedProducts

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        general_information = GeneralInformation.from_dict(d.pop("general_information"))

        description = d.pop("description", UNSET)

        _order_schedule = d.pop("order_schedule", UNSET)
        order_schedule: Union[Unset, OrderSchedule]
        if isinstance(_order_schedule, Unset):
            order_schedule = UNSET
        else:
            order_schedule = OrderSchedule.from_dict(_order_schedule)

        _ordered_products = d.pop("ordered_products", UNSET)
        ordered_products: Union[Unset, OrderedProducts]
        if isinstance(_ordered_products, Unset):
            ordered_products = UNSET
        else:
            ordered_products = OrderedProducts.from_dict(_ordered_products)

        order = cls(
            id_short=id_short,
            id=id,
            general_information=general_information,
            description=description,
            order_schedule=order_schedule,
            ordered_products=ordered_products,
        )

        order.additional_properties = d
        return order

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
