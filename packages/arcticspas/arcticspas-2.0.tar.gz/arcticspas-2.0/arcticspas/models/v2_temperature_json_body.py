from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V2TemperatureJsonBody")


@_attrs_define
class V2TemperatureJsonBody:
    """
    Attributes:
        setpoint_f (Union[Unset, int]): New setpoint temperature in Fahrenheit
    """

    setpoint_f: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        setpoint_f = self.setpoint_f

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if setpoint_f is not UNSET:
            field_dict["setpointF"] = setpoint_f

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        setpoint_f = d.pop("setpointF", UNSET)

        v2_temperature_json_body = cls(
            setpoint_f=setpoint_f,
        )

        v2_temperature_json_body.additional_properties = d
        return v2_temperature_json_body

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
