from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.time_model_type import TimeModelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeModel")


@attr.s(auto_attribs=True)
class TimeModel:
    """Submodel containing parameters to represent the timely duration of a procedure.

    Args:
        id_ (str): The id of the time model.
        description (Optional[str]): The description of the time model.
        id_short (Optional[str]): The short id of the time model.
        semantic_id (Optional[str]): The semantic id of the time model.
        type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time model.
        sequence (Optional[List[float]]): The sequence of timely values (only for sequential time models).
        repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential time models).
        distribution_type (Optional[str]): The name of the distribution (e.g. "normal", "exponential", "weibull",
    "lognormal", "gamma", "beta", "uniform", "triangular", "discrete") (only for distribution time models).
        distribution_parameters (Optional[List[float]]): The parameters of the distribution (1: location, 2: scale, 3
    and 4: shape) (only for distribution time models).
        speed (Optional[float]): The speed of the resource (only for distance-based time models).
        reaction_time (Optional[float]): The reaction time of the resource (only for distance-based time models).
        acceleration (Optional[float]): The acceleration of the resource (only for distance-based time models).
        deceleration (Optional[float]): The deceleration of the resource (only for distance-based time models).

        Attributes:
            id_short (str):
            id (str):
            type (TimeModelType):
            description (Union[Unset, str]):
            semantic_id (Union[Unset, str]):
            sequence (Union[Unset, List[float]]):
            repeat (Union[Unset, bool]):
            distribution_type (Union[Unset, str]):
            distribution_parameters (Union[Unset, List[float]]):
            speed (Union[Unset, float]):
            reaction_time (Union[Unset, float]):
            acceleration (Union[Unset, float]):
            deceleration (Union[Unset, float]):
    """

    id_short: str
    id: str
    type: TimeModelType
    description: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, str] = UNSET
    sequence: Union[Unset, List[float]] = UNSET
    repeat: Union[Unset, bool] = UNSET
    distribution_type: Union[Unset, str] = UNSET
    distribution_parameters: Union[Unset, List[float]] = UNSET
    speed: Union[Unset, float] = UNSET
    reaction_time: Union[Unset, float] = UNSET
    acceleration: Union[Unset, float] = UNSET
    deceleration: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        type = self.type.value

        description = self.description
        semantic_id = self.semantic_id
        sequence: Union[Unset, List[float]] = UNSET
        if not isinstance(self.sequence, Unset):
            sequence = self.sequence

        repeat = self.repeat
        distribution_type = self.distribution_type
        distribution_parameters: Union[Unset, List[float]] = UNSET
        if not isinstance(self.distribution_parameters, Unset):
            distribution_parameters = self.distribution_parameters

        speed = self.speed
        reaction_time = self.reaction_time
        acceleration = self.acceleration
        deceleration = self.deceleration

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
        if repeat is not UNSET:
            field_dict["repeat"] = repeat
        if distribution_type is not UNSET:
            field_dict["distribution_type"] = distribution_type
        if distribution_parameters is not UNSET:
            field_dict["distribution_parameters"] = distribution_parameters
        if speed is not UNSET:
            field_dict["speed"] = speed
        if reaction_time is not UNSET:
            field_dict["reaction_time"] = reaction_time
        if acceleration is not UNSET:
            field_dict["acceleration"] = acceleration
        if deceleration is not UNSET:
            field_dict["deceleration"] = deceleration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        type = TimeModelType(d.pop("type_"))

        description = d.pop("description", UNSET)

        semantic_id = d.pop("semantic_id", UNSET)

        sequence = cast(List[float], d.pop("sequence", UNSET))

        repeat = d.pop("repeat", UNSET)

        distribution_type = d.pop("distribution_type", UNSET)

        distribution_parameters = cast(List[float], d.pop("distribution_parameters", UNSET))

        speed = d.pop("speed", UNSET)

        reaction_time = d.pop("reaction_time", UNSET)

        acceleration = d.pop("acceleration", UNSET)

        deceleration = d.pop("deceleration", UNSET)

        time_model = cls(
            id_short=id_short,
            id=id,
            type=type,
            description=description,
            semantic_id=semantic_id,
            sequence=sequence,
            repeat=repeat,
            distribution_type=distribution_type,
            distribution_parameters=distribution_parameters,
            speed=speed,
            reaction_time=reaction_time,
            acceleration=acceleration,
            deceleration=deceleration,
        )

        time_model.additional_properties = d
        return time_model

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
