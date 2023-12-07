from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_attributes import ProcessAttributes
    from ..models.process_information import ProcessInformation
    from ..models.process_model import ProcessModel


T = TypeVar("T", bound="Process")


@attr.s(auto_attribs=True)
class Process:
    """Class to describe a process that is required to produce a product. A process can comprise of multiple sub-processes,
    described by the process model. With the process attributes, it is specified which attributes are relevant for the
    process to generate the required transformations of a product.

    Args:
        id_ (str): The id of the process.
        description (Optional[str]): The description of the process.
        id_short (Optional[str]): The short id of the process.
        general_Info (GeneralInfo): The general information of the process (e.g. type of process, ...)
        process_model (ProcessModel): The process model of the process (e.g. sequence of sub-processes, ...)
        process_attributes (ProcessAttributes): The process attributes of the process (e.g. rotation speed, ...)

        Attributes:
            id_short (str):
            id (str):
            process_information (ProcessInformation): The SubmodelElementCollection GeneralInfo contains 4 SubmodelElements
                that allow to describe one specific process attribute in a structured, self-describing and interoperable way.
                The types are defined by DIN 8580 for Manufacturing Processes, VDI 2411 for Material Flow Processes, VDI 2243
                for Remanufacturing Processes and VDI 2860 for Assembly.

                Args:
                    id_ (str): The id of the general info.
                    description (Optional[str]): The description of the process.
                    id_short (Optional[str]): The short id of the process.
                    semantic_id (Optional[str]): The semantic id of the process.
                    general_type (Literal["Manufacturing", "Material Flow", "Remanufacturing", "Assembly", "Other"]): The
                general type of process or procedure that is describeded by this attribute.
                    manufacturing_process_type (Optional[Literal["Primary Shaping", "Forming", "Cutting", "Joining", "Coating",
                "Changing Material Properties"]]): The type of manufacturing process according to DIN 8580.
                    material_flow_process_type (Optional[Literal["Storage", "Handling", "Conveying"]]): The type of material
                flow process according to VDI 2411.
                    remanufacturing_process_type (Optional[Literal["Disassembly", "Remediation", "Cleaning", "Inspection"]]):
                The type of remanufacturing process according to VDI 2243.
                    assembly_process_type (Optional[Literal["Joining", "Handling", "Adjusting", "Testing", "Special
                Operations"]]): The type of assembly process according to VDI 2860.
            process_model (ProcessModel): The SubmodelElementCollection “ProcessModel” contains 4 SubmodelElements that
                allow to describe one specific process attribute in a structured, self-describing and interoperable way.

                Args:
                    id_ (str): The id of the process model.
                    description (Optional[str]): The description of the process model.
                    id_short (Optional[str]): The short id of the process model.
                    semantic_id (Optional[str]): The semantic id of the process model.
                    type_ (ProcessModelType): The type of the process model.
                    sequence (Optional[List[str]]): The sequence of the process model (for Sequential process model type) with
                ids of the subprocesses.
                    nodes (Optional[List[str]]): The nodes of the process model (for Graph process model type) with ids of the
                subprocesses.
                    edges (Optional[List[Tuple[str, str]]]): The edges of the process model (for Graph process model type) with
                ids of the subprocesses.
            process_attributes (ProcessAttributes): The SubmodelElementCollection “ProcessAttributes” contains 4
                SubmodelElements that allow to describe one specific process attribute in a structured, self-describing and
                interoperable way.

                Args:
                    id_ (str): The id of the process attributes.
                    description (Optional[str]): The description of the process attributes.
                    id_short (Optional[str]): The short id of the process attributes.
                    semantic_id (Optional[str]): The semantic id of the process attributes.
                    process_attributes (List[AttributePredicate]): The process attributes of the process (e.g. rotation speed,
                ...)
            description (Union[Unset, str]):
    """

    id_short: str
    id: str
    process_information: "ProcessInformation"
    process_model: "ProcessModel"
    process_attributes: "ProcessAttributes"
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        process_information = self.process_information.to_dict()

        process_model = self.process_model.to_dict()

        process_attributes = self.process_attributes.to_dict()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "process_information": process_information,
                "process_model": process_model,
                "process_attributes": process_attributes,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.process_attributes import ProcessAttributes
        from ..models.process_information import ProcessInformation
        from ..models.process_model import ProcessModel

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        process_information = ProcessInformation.from_dict(d.pop("process_information"))

        process_model = ProcessModel.from_dict(d.pop("process_model"))

        process_attributes = ProcessAttributes.from_dict(d.pop("process_attributes"))

        description = d.pop("description", UNSET)

        process = cls(
            id_short=id_short,
            id=id,
            process_information=process_information,
            process_model=process_model,
            process_attributes=process_attributes,
            description=description,
        )

        process.additional_properties = d
        return process

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
