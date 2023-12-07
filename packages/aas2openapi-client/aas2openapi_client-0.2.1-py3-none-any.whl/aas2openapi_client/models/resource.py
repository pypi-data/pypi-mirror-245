from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.capabilities import Capabilities
    from ..models.construction_data import ConstructionData
    from ..models.control_logic import ControlLogic
    from ..models.resource_configuration import ResourceConfiguration
    from ..models.resource_information import ResourceInformation
    from ..models.resource_interfaces import ResourceInterfaces


T = TypeVar("T", bound="Resource")


@attr.s(auto_attribs=True)
class Resource:
    """AAS to describe a resource.

    Args:
        id_ (str): The id of the resource.
        description (Optional[str]): The description of the resource.
        id_short (Optional[str]): The short id of the resource.
        general_information (Optional[GeneralInformation]): some general information describing the resource.
        capabilities (Optional[Capabilities]): The capabilities of the resource, containing information about available
    procedures.
        construction_data (Optional[ConstructionData]): The construction data of the resource.
        resource_configuration (Optional[ResourceHierarchy]): The configruation of the resource, containting information
    about sub resources.
        control_logic (Optional[ControlLogic]): The control logic of the resource.
        resource_interface (Optional[ResourceInterfaces]): the interfaces of the resource.

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            resource_information (Union[Unset, ResourceInformation]): Submodel to describe the general information of a
                resource.

                Args:
                    id_ (str): The id of the general information.
                    description (Optional[str]): The description of the general information.
                    id_short (Optional[str]): The short id of the general information.
                    semantic_id (Optional[str]): The semantic id of the general information.
                    manufacturer (Optional[str]): The manufacturer of the resource.
                    production_level (Literal["Module", "Station", "System", "Plant", "Network"]): The production level of the
                resource.
                    resource_type (Literal["Manufacturing", "Material Flow", "Storage"]): The type of the resource.
            capabilities (Union[Unset, Capabilities]): Submodel to describe the capabilities of a resource by describing
                available
                procedures in the resource.

                Args:
                    id_ (str): The id of the capabilities.
                    description (Optional[str]): The description of the capabilities.
                    id_short (Optional[str]): The short id of the capabilities.
                    semantic_id (Optional[str]): The semantic id of the capabilities.
                    procedure_ids (List[str]): The list of ids of procedure that are available for the resource.
            construction_data (Union[Unset, ConstructionData]): Submodel to describe the construction data of a product.

                Args:
                    id_ (str): The id of the construction data.
                    description (Optional[str]): The description of the construction data.
                    id_short (Optional[str]): The short id of the construction data.
                    semantic_id (Optional[str]): The semantic id of the construction data.
                    cad_file (Optional[str]): IRI to a CAD file of the product.
            resource_configuration (Union[Unset, ResourceConfiguration]): Submodel to describe the configuration of a
                resource, by describing its sub resources and their position and orientation.

                Args:
                    id_ (str): The id of the resource hierarchy.
                    description (Optional[str]): The description of the resource hierarchy.
                    id_short (Optional[str]): The short id of the resource hierarchy.
                    semantic_id (Optional[str]): The semantic id of the resource hierarchy.
                    sub_resources (Optional[List[SubResource]]): IDs ob sub resources
            control_logic (Union[Unset, ControlLogic]): Submodel to describe the control logic of a resource, by describing
                its control policy. It specifies in which sequence the resource processes the products.

                Args:
                    id_ (str): The id of the control logic.
                    id_short (str): The short id of the control logic.
                    description (Optional[str]): The description of the control logic.
                    semantic_id (Optional[str]): The semantic id of the control logic.
                    sequencing_policy (Literal["FIFO", "SPT_transport", "LIFO", "SPT", "EDD", "ODD"]): The sequencing policy of
                the resource, determining in which sequence requests are processed.
                    routing_policy (Literal["random", "nearest", "shortest_queue", "alternating, "round_robin"]): The routing
                policy of the resource how redundant sub resources are used.
            resource_interface (Union[Unset, ResourceInterfaces]): Submodel to describe the interfaces of a resource to
                connect to the resource either by energy, information or material.

                Args:
                    id_ (str): The id of the resource interfaces.
                    description (Optional[str]): The description of the resource interfaces.
                    id_short (Optional[str]): The short id of the resource interfaces.
                    semantic_id (Optional[str]): The semantic id of the resource interfaces.
                    information_interface (Optional[List[CommunicationInterface]]): The communication interfaces of the
                resource.
                    material_interfaces (Optional[List[MaterialInterface]]): The material interfaces of the resource.
                    energy_interfaces (Optional[List[EnergyInterface]]): The energy interfaces of the resource.
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    resource_information: Union[Unset, "ResourceInformation"] = UNSET
    capabilities: Union[Unset, "Capabilities"] = UNSET
    construction_data: Union[Unset, "ConstructionData"] = UNSET
    resource_configuration: Union[Unset, "ResourceConfiguration"] = UNSET
    control_logic: Union[Unset, "ControlLogic"] = UNSET
    resource_interface: Union[Unset, "ResourceInterfaces"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        resource_information: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource_information, Unset):
            resource_information = self.resource_information.to_dict()

        capabilities: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        construction_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.construction_data, Unset):
            construction_data = self.construction_data.to_dict()

        resource_configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource_configuration, Unset):
            resource_configuration = self.resource_configuration.to_dict()

        control_logic: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.control_logic, Unset):
            control_logic = self.control_logic.to_dict()

        resource_interface: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource_interface, Unset):
            resource_interface = self.resource_interface.to_dict()

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
        if resource_information is not UNSET:
            field_dict["resource_information"] = resource_information
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if construction_data is not UNSET:
            field_dict["construction_data"] = construction_data
        if resource_configuration is not UNSET:
            field_dict["resource_configuration"] = resource_configuration
        if control_logic is not UNSET:
            field_dict["control_logic"] = control_logic
        if resource_interface is not UNSET:
            field_dict["resource_interface"] = resource_interface

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.capabilities import Capabilities
        from ..models.construction_data import ConstructionData
        from ..models.control_logic import ControlLogic
        from ..models.resource_configuration import ResourceConfiguration
        from ..models.resource_information import ResourceInformation
        from ..models.resource_interfaces import ResourceInterfaces

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        _resource_information = d.pop("resource_information", UNSET)
        resource_information: Union[Unset, ResourceInformation]
        if isinstance(_resource_information, Unset):
            resource_information = UNSET
        else:
            resource_information = ResourceInformation.from_dict(_resource_information)

        _capabilities = d.pop("capabilities", UNSET)
        capabilities: Union[Unset, Capabilities]
        if isinstance(_capabilities, Unset):
            capabilities = UNSET
        else:
            capabilities = Capabilities.from_dict(_capabilities)

        _construction_data = d.pop("construction_data", UNSET)
        construction_data: Union[Unset, ConstructionData]
        if isinstance(_construction_data, Unset):
            construction_data = UNSET
        else:
            construction_data = ConstructionData.from_dict(_construction_data)

        _resource_configuration = d.pop("resource_configuration", UNSET)
        resource_configuration: Union[Unset, ResourceConfiguration]
        if isinstance(_resource_configuration, Unset):
            resource_configuration = UNSET
        else:
            resource_configuration = ResourceConfiguration.from_dict(_resource_configuration)

        _control_logic = d.pop("control_logic", UNSET)
        control_logic: Union[Unset, ControlLogic]
        if isinstance(_control_logic, Unset):
            control_logic = UNSET
        else:
            control_logic = ControlLogic.from_dict(_control_logic)

        _resource_interface = d.pop("resource_interface", UNSET)
        resource_interface: Union[Unset, ResourceInterfaces]
        if isinstance(_resource_interface, Unset):
            resource_interface = UNSET
        else:
            resource_interface = ResourceInterfaces.from_dict(_resource_interface)

        resource = cls(
            id_short=id_short,
            id=id,
            description=description,
            resource_information=resource_information,
            capabilities=capabilities,
            construction_data=construction_data,
            resource_configuration=resource_configuration,
            control_logic=control_logic,
            resource_interface=resource_interface,
        )

        resource.additional_properties = d
        return resource

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
