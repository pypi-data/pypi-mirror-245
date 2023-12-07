from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.control_logic_routing_policy import ControlLogicRoutingPolicy
from ..models.control_logic_sequencing_policy import ControlLogicSequencingPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="ControlLogic")


@attr.s(auto_attribs=True)
class ControlLogic:
    """Submodel to describe the control logic of a resource, by describing its control policy. It specifies in which
    sequence the resource processes the products.

    Args:
        id_ (str): The id of the control logic.
        id_short (str): The short id of the control logic.
        description (Optional[str]): The description of the control logic.
        semantic_id (Optional[str]): The semantic id of the control logic.
        sequencing_policy (Literal["FIFO", "SPT_transport", "LIFO", "SPT", "EDD", "ODD"]): The sequencing policy of the
    resource, determining in which sequence requests are processed.
        routing_policy (Literal["random", "nearest", "shortest_queue", "alternating, "round_robin"]): The routing policy
    of the resource how redundant sub resources are used.

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            sequencing_policy (Union[Unset, ControlLogicSequencingPolicy]):
            routing_policy (Union[Unset, ControlLogicRoutingPolicy]):
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    sequencing_policy: Union[Unset, ControlLogicSequencingPolicy] = UNSET
    routing_policy: Union[Unset, ControlLogicRoutingPolicy] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        semantic_id = self.semantic_id
        sequencing_policy: Union[Unset, str] = UNSET
        if not isinstance(self.sequencing_policy, Unset):
            sequencing_policy = self.sequencing_policy.value

        routing_policy: Union[Unset, str] = UNSET
        if not isinstance(self.routing_policy, Unset):
            routing_policy = self.routing_policy.value

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
        if sequencing_policy is not UNSET:
            field_dict["sequencing_policy"] = sequencing_policy
        if routing_policy is not UNSET:
            field_dict["routing_policy"] = routing_policy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        _sequencing_policy = d.pop("sequencing_policy", UNSET)
        sequencing_policy: Union[Unset, ControlLogicSequencingPolicy]
        if isinstance(_sequencing_policy, Unset):
            sequencing_policy = UNSET
        else:
            sequencing_policy = ControlLogicSequencingPolicy(_sequencing_policy)

        _routing_policy = d.pop("routing_policy", UNSET)
        routing_policy: Union[Unset, ControlLogicRoutingPolicy]
        if isinstance(_routing_policy, Unset):
            routing_policy = UNSET
        else:
            routing_policy = ControlLogicRoutingPolicy(_routing_policy)

        control_logic = cls(
            id_short=id_short,
            id=id,
            description=description,
            semantic_id=semantic_id,
            sequencing_policy=sequencing_policy,
            routing_policy=routing_policy,
        )

        control_logic.additional_properties = d
        return control_logic

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
