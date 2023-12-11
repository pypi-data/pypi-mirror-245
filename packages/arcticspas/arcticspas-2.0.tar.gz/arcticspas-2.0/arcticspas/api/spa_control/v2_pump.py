from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v2_pump_json_body import V2PumpJsonBody
from ...models.v2_pump_pump import V2PumpPump
from ...types import Response


def _get_kwargs(
    pump: V2PumpPump,
    *,
    json_body: V2PumpJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v2/spa/pumps/{pump}".format(
            pump=pump,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.ACCEPTED:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        return None
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return None
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pump: V2PumpPump,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V2PumpJsonBody,
) -> Response[Any]:
    r"""Set Spa Pumps

     Controls the spa's pumps.  The \"pump\" path parameter determines which pump to control (or all of
    them).  The pumps have two different states, an \"off\" state, and an \"on\"/\"high\" state.  Pump 1
    has a third \"low\" state.  When controlling individual pumps, if the current state of the pump
    matches the new state, a response with HTTP code 202 will be returned.

    Args:
        pump (V2PumpPump):
        json_body (V2PumpJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        pump=pump,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    pump: V2PumpPump,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V2PumpJsonBody,
) -> Response[Any]:
    r"""Set Spa Pumps

     Controls the spa's pumps.  The \"pump\" path parameter determines which pump to control (or all of
    them).  The pumps have two different states, an \"off\" state, and an \"on\"/\"high\" state.  Pump 1
    has a third \"low\" state.  When controlling individual pumps, if the current state of the pump
    matches the new state, a response with HTTP code 202 will be returned.

    Args:
        pump (V2PumpPump):
        json_body (V2PumpJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        pump=pump,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
