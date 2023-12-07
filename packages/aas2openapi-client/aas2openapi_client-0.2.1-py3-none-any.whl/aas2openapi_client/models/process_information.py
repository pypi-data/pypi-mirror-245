from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.process_information_assembly_process_type import ProcessInformationAssemblyProcessType
from ..models.process_information_general_type import ProcessInformationGeneralType
from ..models.process_information_manufacturing_process_type import ProcessInformationManufacturingProcessType
from ..models.process_information_material_flow_process_type import ProcessInformationMaterialFlowProcessType
from ..models.process_information_remanufacturing_process_type import ProcessInformationRemanufacturingProcessType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessInformation")


@attr.s(auto_attribs=True)
class ProcessInformation:
    """The SubmodelElementCollection GeneralInfo contains 4 SubmodelElements that allow to describe one specific process
    attribute in a structured, self-describing and interoperable way.
    The types are defined by DIN 8580 for Manufacturing Processes, VDI 2411 for Material Flow Processes, VDI 2243 for
    Remanufacturing Processes and VDI 2860 for Assembly.

    Args:
        id_ (str): The id of the general info.
        description (Optional[str]): The description of the process.
        id_short (Optional[str]): The short id of the process.
        semantic_id (Optional[str]): The semantic id of the process.
        general_type (Literal["Manufacturing", "Material Flow", "Remanufacturing", "Assembly", "Other"]): The general
    type of process or procedure that is describeded by this attribute.
        manufacturing_process_type (Optional[Literal["Primary Shaping", "Forming", "Cutting", "Joining", "Coating",
    "Changing Material Properties"]]): The type of manufacturing process according to DIN 8580.
        material_flow_process_type (Optional[Literal["Storage", "Handling", "Conveying"]]): The type of material flow
    process according to VDI 2411.
        remanufacturing_process_type (Optional[Literal["Disassembly", "Remediation", "Cleaning", "Inspection"]]): The
    type of remanufacturing process according to VDI 2243.
        assembly_process_type (Optional[Literal["Joining", "Handling", "Adjusting", "Testing", "Special Operations"]]):
    The type of assembly process according to VDI 2860.

        Attributes:
            id_short (str):
            id (str):
            general_type (ProcessInformationGeneralType):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            manufacturing_process_type (Union[Unset, ProcessInformationManufacturingProcessType]):
            material_flow_process_type (Union[Unset, ProcessInformationMaterialFlowProcessType]):
            remanufacturing_process_type (Union[Unset, ProcessInformationRemanufacturingProcessType]):
            assembly_process_type (Union[Unset, ProcessInformationAssemblyProcessType]):
    """

    id_short: str
    id: str
    general_type: ProcessInformationGeneralType
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    manufacturing_process_type: Union[Unset, ProcessInformationManufacturingProcessType] = UNSET
    material_flow_process_type: Union[Unset, ProcessInformationMaterialFlowProcessType] = UNSET
    remanufacturing_process_type: Union[Unset, ProcessInformationRemanufacturingProcessType] = UNSET
    assembly_process_type: Union[Unset, ProcessInformationAssemblyProcessType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        general_type = self.general_type.value

        description = self.description
        semantic_id = self.semantic_id
        manufacturing_process_type: Union[Unset, str] = UNSET
        if not isinstance(self.manufacturing_process_type, Unset):
            manufacturing_process_type = self.manufacturing_process_type.value

        material_flow_process_type: Union[Unset, str] = UNSET
        if not isinstance(self.material_flow_process_type, Unset):
            material_flow_process_type = self.material_flow_process_type.value

        remanufacturing_process_type: Union[Unset, str] = UNSET
        if not isinstance(self.remanufacturing_process_type, Unset):
            remanufacturing_process_type = self.remanufacturing_process_type.value

        assembly_process_type: Union[Unset, str] = UNSET
        if not isinstance(self.assembly_process_type, Unset):
            assembly_process_type = self.assembly_process_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "general_type": general_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if manufacturing_process_type is not UNSET:
            field_dict["manufacturing_process_type"] = manufacturing_process_type
        if material_flow_process_type is not UNSET:
            field_dict["material_flow_process_type"] = material_flow_process_type
        if remanufacturing_process_type is not UNSET:
            field_dict["remanufacturing_process_type"] = remanufacturing_process_type
        if assembly_process_type is not UNSET:
            field_dict["assembly_process_type"] = assembly_process_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        general_type = ProcessInformationGeneralType(d.pop("general_type"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        _manufacturing_process_type = d.pop("manufacturing_process_type", UNSET)
        manufacturing_process_type: Union[Unset, ProcessInformationManufacturingProcessType]
        if isinstance(_manufacturing_process_type, Unset):
            manufacturing_process_type = UNSET
        else:
            manufacturing_process_type = ProcessInformationManufacturingProcessType(_manufacturing_process_type)

        _material_flow_process_type = d.pop("material_flow_process_type", UNSET)
        material_flow_process_type: Union[Unset, ProcessInformationMaterialFlowProcessType]
        if isinstance(_material_flow_process_type, Unset):
            material_flow_process_type = UNSET
        else:
            material_flow_process_type = ProcessInformationMaterialFlowProcessType(_material_flow_process_type)

        _remanufacturing_process_type = d.pop("remanufacturing_process_type", UNSET)
        remanufacturing_process_type: Union[Unset, ProcessInformationRemanufacturingProcessType]
        if isinstance(_remanufacturing_process_type, Unset):
            remanufacturing_process_type = UNSET
        else:
            remanufacturing_process_type = ProcessInformationRemanufacturingProcessType(_remanufacturing_process_type)

        _assembly_process_type = d.pop("assembly_process_type", UNSET)
        assembly_process_type: Union[Unset, ProcessInformationAssemblyProcessType]
        if isinstance(_assembly_process_type, Unset):
            assembly_process_type = UNSET
        else:
            assembly_process_type = ProcessInformationAssemblyProcessType(_assembly_process_type)

        process_information = cls(
            id_short=id_short,
            id=id,
            general_type=general_type,
            description=description,
            semantic_id=semantic_id,
            manufacturing_process_type=manufacturing_process_type,
            material_flow_process_type=material_flow_process_type,
            remanufacturing_process_type=remanufacturing_process_type,
            assembly_process_type=assembly_process_type,
        )

        process_information.additional_properties = d
        return process_information

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
