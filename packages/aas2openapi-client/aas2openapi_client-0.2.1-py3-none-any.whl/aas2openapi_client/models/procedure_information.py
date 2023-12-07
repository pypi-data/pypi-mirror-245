from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.procedure_type_enum import ProcedureTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcedureInformation")


@attr.s(auto_attribs=True)
class ProcedureInformation:
    """Submodel containing general information about the procedure.

    Args:
        procedure_type (ProcedureTypeEnum): The type of the procedure.

        Attributes:
            id_short (str):
            id (str):
            procedure_type (ProcedureTypeEnum): Enum to describe the type of a procedure.
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
    """

    id_short: str
    id: str
    procedure_type: ProcedureTypeEnum
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        procedure_type = self.procedure_type.value

        description = self.description
        semantic_id = self.semantic_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "procedure_type": procedure_type,
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

        id = d.pop("id_")

        procedure_type = ProcedureTypeEnum(d.pop("procedure_type"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        procedure_information = cls(
            id_short=id_short,
            id=id,
            procedure_type=procedure_type,
            description=description,
            semantic_id=semantic_id,
        )

        procedure_information.additional_properties = d
        return procedure_information

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
