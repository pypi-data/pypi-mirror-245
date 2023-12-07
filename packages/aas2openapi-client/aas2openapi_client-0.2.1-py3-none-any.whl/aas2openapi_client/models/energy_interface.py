from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnergyInterface")


@attr.s(auto_attribs=True)
class EnergyInterface:
    """Interface for energy handling, e.g. if a product is passed to this resource, the EnergyInterface specifies the
    requried energy level.

    Args:
        voltage (float): The voltage of the energy interface.
        current (float): The current of the energy interface.
        power (float): The power of the energy interface.
        current_type (str): The current type of the energy interface.

        Attributes:
            id_short (str):
            voltage (float):
            current (float):
            power (float):
            current_type (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    voltage: float
    current: float
    power: float
    current_type: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        voltage = self.voltage
        current = self.current
        power = self.power
        current_type = self.current_type
        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "voltage": voltage,
                "current": current,
                "power": power,
                "current_type": current_type,
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

        voltage = d.pop("voltage")

        current = d.pop("current")

        power = d.pop("power")

        current_type = d.pop("current_type")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        energy_interface = cls(
            id_short=id_short,
            voltage=voltage,
            current=current,
            power=power,
            current_type=current_type,
            description=description,
            semantic_id=semantic_id,
        )

        energy_interface.additional_properties = d
        return energy_interface

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
