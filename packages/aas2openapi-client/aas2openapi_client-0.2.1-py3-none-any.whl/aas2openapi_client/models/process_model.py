from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.process_model_type import ProcessModelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessModel")


@attr.s(auto_attribs=True)
class ProcessModel:
    """The SubmodelElementCollection “ProcessModel” contains 4 SubmodelElements that allow to describe one specific process
    attribute in a structured, self-describing and interoperable way.

    Args:
        id_ (str): The id of the process model.
        description (Optional[str]): The description of the process model.
        id_short (Optional[str]): The short id of the process model.
        semantic_id (Optional[str]): The semantic id of the process model.
        type_ (ProcessModelType): The type of the process model.
        sequence (Optional[List[str]]): The sequence of the process model (for Sequential process model type) with ids
    of the subprocesses.
        nodes (Optional[List[str]]): The nodes of the process model (for Graph process model type) with ids of the
    subprocesses.
        edges (Optional[List[Tuple[str, str]]]): The edges of the process model (for Graph process model type) with ids
    of the subprocesses.

        Attributes:
            id_short (str):
            id (str):
            type (ProcessModelType): Enum to describe the type of process model.
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            sequence (Union[Unset, List[str]]):
            nodes (Union[Unset, List[str]]):
            edges (Union[Unset, List[List[str]]]):
    """

    id_short: str
    id: str
    type: ProcessModelType
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    sequence: Union[Unset, List[str]] = UNSET
    nodes: Union[Unset, List[str]] = UNSET
    edges: Union[Unset, List[List[str]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        type = self.type.value

        description = self.description
        semantic_id = self.semantic_id
        sequence: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sequence, Unset):
            sequence = self.sequence

        nodes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = self.nodes

        edges: Union[Unset, List[List[str]]] = UNSET
        if not isinstance(self.edges, Unset):
            edges = []
            for edges_item_data in self.edges:
                edges_item = edges_item_data

                edges.append(edges_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
                "type_": type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if semantic_id is not UNSET:
            field_dict["semantic_id"] = semantic_id
        if sequence is not UNSET:
            field_dict["sequence"] = sequence
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if edges is not UNSET:
            field_dict["edges"] = edges

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        type = ProcessModelType(d.pop("type_"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        sequence = cast(List[str], d.pop("sequence", UNSET))

        nodes = cast(List[str], d.pop("nodes", UNSET))

        edges = []
        _edges = d.pop("edges", UNSET)
        for edges_item_data in _edges or []:
            edges_item = cast(List[str], edges_item_data)

            edges.append(edges_item)

        process_model = cls(
            id_short=id_short,
            id=id,
            type=type,
            description=description,
            semantic_id=semantic_id,
            sequence=sequence,
            nodes=nodes,
            edges=edges,
        )

        process_model.additional_properties = d
        return process_model

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
