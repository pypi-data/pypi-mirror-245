from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V2SpaResponse200")


@_attrs_define
class V2SpaResponse200:
    """
    Attributes:
        connected (Union[Unset, bool]): Whether or not spa is online
        temperature_f (Union[Unset, int]): Spa temperature in Fahrenheit
        setpoint_f (Union[Unset, int]): Spa setpoint temperature in Fahrenheit
        lights (Union[Unset, str]): Lights status, one of [off,on]
        spaboy_connected (Union[Unset, bool]): (If Spa Boy® enabled on spa) Whether a Spa Boy® is connected or not
        spaboy_producing (Union[Unset, bool]): (If Spa Boy® connected) Whether a Spa Boy® is producing or not
        ph (Union[Unset, float]): (If Spa Boy® connected) Spa pH
        ph_status (Union[Unset, str]): (If Spa Boy® connected) Spa pH status, one of
            [LOW,CAUTION_LOW,OK,CAUTION_HIGH,HIGH]
        orp (Union[Unset, float]): (If Spa Boy® connected) Spa oxygen reduction potential
        orp_status (Union[Unset, str]): (If Spa Boy® connected) Spa ORP status, one of
            [LOW,CAUTION_LOW,OK,CAUTION_HIGH,HIGH]
        sds (Union[Unset, str]): (If SDS enabled on spa) SDS status, one of [off,on]
        yess (Union[Unset, str]): (If YESS enabled on spa) YESS status, one of [off,on]
        fogger (Union[Unset, str]): (If fogger enabled on spa) fogger status, one of [off,on]
        blower1 (Union[Unset, str]): (If blower 1 enabled on spa) blower 1 status, one of [off,on]
        blower2 (Union[Unset, str]): (If blower 1 enabled on spa) blower 1 status, one of [off,on]
        pump1 (Union[Unset, str]): Pump 1 status, one of [off,low,high]
        pump2 (Union[Unset, str]): Pump 2 status, one of [off,high]
        pump3 (Union[Unset, str]): Pump 3 status, one of [off,high]
        pump4 (Union[Unset, str]): (If pump 4 enabled on spa) Pump 4 status, one of [off,high]
        pump5 (Union[Unset, str]): (If pump 5 enabled on spa) Pump 5 status, one of [off,high]
        filter_status (Union[Unset, str]): Filter status, one of
            [Idle,Purge,Filtering,Suspended,Overtemperature,Resuming,Boost,Sanitize]
        filter_duration (Union[Unset, int]): Filtering duration, in hours
        filter_frequency (Union[Unset, float]): Filtering frequency, in cycles/day
        filter_suspension (Union[Unset, bool]): Whether or not filtering will be suspended when in an overtemp state
        errors (Union[Unset, List[str]]): Array of active error codes
    """

    connected: Union[Unset, bool] = UNSET
    temperature_f: Union[Unset, int] = UNSET
    setpoint_f: Union[Unset, int] = UNSET
    lights: Union[Unset, str] = UNSET
    spaboy_connected: Union[Unset, bool] = UNSET
    spaboy_producing: Union[Unset, bool] = UNSET
    ph: Union[Unset, float] = UNSET
    ph_status: Union[Unset, str] = UNSET
    orp: Union[Unset, float] = UNSET
    orp_status: Union[Unset, str] = UNSET
    sds: Union[Unset, str] = UNSET
    yess: Union[Unset, str] = UNSET
    fogger: Union[Unset, str] = UNSET
    blower1: Union[Unset, str] = UNSET
    blower2: Union[Unset, str] = UNSET
    pump1: Union[Unset, str] = UNSET
    pump2: Union[Unset, str] = UNSET
    pump3: Union[Unset, str] = UNSET
    pump4: Union[Unset, str] = UNSET
    pump5: Union[Unset, str] = UNSET
    filter_status: Union[Unset, str] = UNSET
    filter_duration: Union[Unset, int] = UNSET
    filter_frequency: Union[Unset, float] = UNSET
    filter_suspension: Union[Unset, bool] = UNSET
    errors: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connected = self.connected
        temperature_f = self.temperature_f
        setpoint_f = self.setpoint_f
        lights = self.lights
        spaboy_connected = self.spaboy_connected
        spaboy_producing = self.spaboy_producing
        ph = self.ph
        ph_status = self.ph_status
        orp = self.orp
        orp_status = self.orp_status
        sds = self.sds
        yess = self.yess
        fogger = self.fogger
        blower1 = self.blower1
        blower2 = self.blower2
        pump1 = self.pump1
        pump2 = self.pump2
        pump3 = self.pump3
        pump4 = self.pump4
        pump5 = self.pump5
        filter_status = self.filter_status
        filter_duration = self.filter_duration
        filter_frequency = self.filter_frequency
        filter_suspension = self.filter_suspension
        errors: Union[Unset, List[str]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connected is not UNSET:
            field_dict["connected"] = connected
        if temperature_f is not UNSET:
            field_dict["temperatureF"] = temperature_f
        if setpoint_f is not UNSET:
            field_dict["setpointF"] = setpoint_f
        if lights is not UNSET:
            field_dict["lights"] = lights
        if spaboy_connected is not UNSET:
            field_dict["spaboy_connected"] = spaboy_connected
        if spaboy_producing is not UNSET:
            field_dict["spaboy_producing"] = spaboy_producing
        if ph is not UNSET:
            field_dict["ph"] = ph
        if ph_status is not UNSET:
            field_dict["ph_status"] = ph_status
        if orp is not UNSET:
            field_dict["orp"] = orp
        if orp_status is not UNSET:
            field_dict["orp_status"] = orp_status
        if sds is not UNSET:
            field_dict["sds"] = sds
        if yess is not UNSET:
            field_dict["yess"] = yess
        if fogger is not UNSET:
            field_dict["fogger"] = fogger
        if blower1 is not UNSET:
            field_dict["blower1"] = blower1
        if blower2 is not UNSET:
            field_dict["blower2"] = blower2
        if pump1 is not UNSET:
            field_dict["pump1"] = pump1
        if pump2 is not UNSET:
            field_dict["pump2"] = pump2
        if pump3 is not UNSET:
            field_dict["pump3"] = pump3
        if pump4 is not UNSET:
            field_dict["pump4"] = pump4
        if pump5 is not UNSET:
            field_dict["pump5"] = pump5
        if filter_status is not UNSET:
            field_dict["filter_status"] = filter_status
        if filter_duration is not UNSET:
            field_dict["filter_duration"] = filter_duration
        if filter_frequency is not UNSET:
            field_dict["filter_frequency"] = filter_frequency
        if filter_suspension is not UNSET:
            field_dict["filter_suspension"] = filter_suspension
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        connected = d.pop("connected", UNSET)

        temperature_f = d.pop("temperatureF", UNSET)

        setpoint_f = d.pop("setpointF", UNSET)

        lights = d.pop("lights", UNSET)

        spaboy_connected = d.pop("spaboy_connected", UNSET)

        spaboy_producing = d.pop("spaboy_producing", UNSET)

        ph = d.pop("ph", UNSET)

        ph_status = d.pop("ph_status", UNSET)

        orp = d.pop("orp", UNSET)

        orp_status = d.pop("orp_status", UNSET)

        sds = d.pop("sds", UNSET)

        yess = d.pop("yess", UNSET)

        fogger = d.pop("fogger", UNSET)

        blower1 = d.pop("blower1", UNSET)

        blower2 = d.pop("blower2", UNSET)

        pump1 = d.pop("pump1", UNSET)

        pump2 = d.pop("pump2", UNSET)

        pump3 = d.pop("pump3", UNSET)

        pump4 = d.pop("pump4", UNSET)

        pump5 = d.pop("pump5", UNSET)

        filter_status = d.pop("filter_status", UNSET)

        filter_duration = d.pop("filter_duration", UNSET)

        filter_frequency = d.pop("filter_frequency", UNSET)

        filter_suspension = d.pop("filter_suspension", UNSET)

        errors = cast(List[str], d.pop("errors", UNSET))

        v2_spa_response_200 = cls(
            connected=connected,
            temperature_f=temperature_f,
            setpoint_f=setpoint_f,
            lights=lights,
            spaboy_connected=spaboy_connected,
            spaboy_producing=spaboy_producing,
            ph=ph,
            ph_status=ph_status,
            orp=orp,
            orp_status=orp_status,
            sds=sds,
            yess=yess,
            fogger=fogger,
            blower1=blower1,
            blower2=blower2,
            pump1=pump1,
            pump2=pump2,
            pump3=pump3,
            pump4=pump4,
            pump5=pump5,
            filter_status=filter_status,
            filter_duration=filter_duration,
            filter_frequency=filter_frequency,
            filter_suspension=filter_suspension,
            errors=errors,
        )

        v2_spa_response_200.additional_properties = d
        return v2_spa_response_200

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
