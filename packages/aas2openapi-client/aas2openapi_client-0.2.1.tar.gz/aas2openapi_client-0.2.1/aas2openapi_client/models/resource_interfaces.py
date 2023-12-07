from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.energy_interface import EnergyInterface
    from ..models.information_interface import InformationInterface
    from ..models.material_interface import MaterialInterface


T = TypeVar("T", bound="ResourceInterfaces")


@attr.s(auto_attribs=True)
class ResourceInterfaces:
    """Submodel to describe the interfaces of a resource to connect to the resource either by energy, information or
    material.

    Args:
        id_ (str): The id of the resource interfaces.
        description (Optional[str]): The description of the resource interfaces.
        id_short (Optional[str]): The short id of the resource interfaces.
        semantic_id (Optional[str]): The semantic id of the resource interfaces.
        information_interface (Optional[List[CommunicationInterface]]): The communication interfaces of the resource.
        material_interfaces (Optional[List[MaterialInterface]]): The material interfaces of the resource.
        energy_interfaces (Optional[List[EnergyInterface]]): The energy interfaces of the resource.

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            information_interface (Union[Unset, List['InformationInterface']]):
            material_interfaces (Union[Unset, List['MaterialInterface']]):
            energy_interfaces (Union[Unset, List['EnergyInterface']]):
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    information_interface: Union[Unset, List["InformationInterface"]] = UNSET
    material_interfaces: Union[Unset, List["MaterialInterface"]] = UNSET
    energy_interfaces: Union[Unset, List["EnergyInterface"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        semantic_id = self.semantic_id
        information_interface: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.information_interface, Unset):
            information_interface = []
            for information_interface_item_data in self.information_interface:
                information_interface_item = information_interface_item_data.to_dict()

                information_interface.append(information_interface_item)

        material_interfaces: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.material_interfaces, Unset):
            material_interfaces = []
            for material_interfaces_item_data in self.material_interfaces:
                material_interfaces_item = material_interfaces_item_data.to_dict()

                material_interfaces.append(material_interfaces_item)

        energy_interfaces: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.energy_interfaces, Unset):
            energy_interfaces = []
            for energy_interfaces_item_data in self.energy_interfaces:
                energy_interfaces_item = energy_interfaces_item_data.to_dict()

                energy_interfaces.append(energy_interfaces_item)

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
        if information_interface is not UNSET:
            field_dict["information_interface"] = information_interface
        if material_interfaces is not UNSET:
            field_dict["material_interfaces"] = material_interfaces
        if energy_interfaces is not UNSET:
            field_dict["energy_interfaces"] = energy_interfaces

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.energy_interface import EnergyInterface
        from ..models.information_interface import InformationInterface
        from ..models.material_interface import MaterialInterface

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        information_interface = []
        _information_interface = d.pop("information_interface", UNSET)
        for information_interface_item_data in _information_interface or []:
            information_interface_item = InformationInterface.from_dict(information_interface_item_data)

            information_interface.append(information_interface_item)

        material_interfaces = []
        _material_interfaces = d.pop("material_interfaces", UNSET)
        for material_interfaces_item_data in _material_interfaces or []:
            material_interfaces_item = MaterialInterface.from_dict(material_interfaces_item_data)

            material_interfaces.append(material_interfaces_item)

        energy_interfaces = []
        _energy_interfaces = d.pop("energy_interfaces", UNSET)
        for energy_interfaces_item_data in _energy_interfaces or []:
            energy_interfaces_item = EnergyInterface.from_dict(energy_interfaces_item_data)

            energy_interfaces.append(energy_interfaces_item)

        resource_interfaces = cls(
            id_short=id_short,
            id=id,
            description=description,
            semantic_id=semantic_id,
            information_interface=information_interface,
            material_interfaces=material_interfaces,
            energy_interfaces=energy_interfaces,
        )

        resource_interfaces.additional_properties = d
        return resource_interfaces

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
