from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v2_blower_json_body_state import V2BlowerJsonBodyState
from ..types import UNSET, Unset

T = TypeVar("T", bound="V2BlowerJsonBody")


@_attrs_define
class V2BlowerJsonBody:
    """
    Attributes:
        state (Union[Unset, V2BlowerJsonBodyState]): New state of the selected blower
    """

    state: Union[Unset, V2BlowerJsonBodyState] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _state = d.pop("state", UNSET)
        state: Union[Unset, V2BlowerJsonBodyState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = V2BlowerJsonBodyState(_state)

        v2_blower_json_body = cls(
            state=state,
        )

        v2_blower_json_body.additional_properties = d
        return v2_blower_json_body

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
