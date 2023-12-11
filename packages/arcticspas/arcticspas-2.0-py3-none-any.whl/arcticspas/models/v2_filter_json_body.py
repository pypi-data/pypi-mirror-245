from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v2_filter_json_body_state import V2FilterJsonBodyState
from ..types import UNSET, Unset

T = TypeVar("T", bound="V2FilterJsonBody")


@_attrs_define
class V2FilterJsonBody:
    """
    Attributes:
        state (Union[Unset, V2FilterJsonBodyState]): New state of filter
        frequency (Union[Unset, int]): New filtering frequency in cycles/day
        duration (Union[Unset, int]): New filtering duration in hours
        suspension (Union[Unset, bool]): Enable filter suspension when in an overtemp state
    """

    state: Union[Unset, V2FilterJsonBodyState] = UNSET
    frequency: Union[Unset, int] = UNSET
    duration: Union[Unset, int] = UNSET
    suspension: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        frequency = self.frequency
        duration = self.duration
        suspension = self.suspension

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if duration is not UNSET:
            field_dict["duration"] = duration
        if suspension is not UNSET:
            field_dict["suspension"] = suspension

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _state = d.pop("state", UNSET)
        state: Union[Unset, V2FilterJsonBodyState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = V2FilterJsonBodyState(_state)

        frequency = d.pop("frequency", UNSET)

        duration = d.pop("duration", UNSET)

        suspension = d.pop("suspension", UNSET)

        v2_filter_json_body = cls(
            state=state,
            frequency=frequency,
            duration=duration,
            suspension=suspension,
        )

        v2_filter_json_body.additional_properties = d
        return v2_filter_json_body

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
