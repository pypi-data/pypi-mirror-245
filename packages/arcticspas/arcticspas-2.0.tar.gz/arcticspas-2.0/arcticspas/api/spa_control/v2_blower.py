from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v2_blower_blower import V2BlowerBlower
from ...models.v2_blower_json_body import V2BlowerJsonBody
from ...types import Response


def _get_kwargs(
    blower: V2BlowerBlower,
    *,
    json_body: V2BlowerJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v2/spa/blowers/{blower}".format(
            blower=blower,
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
    if response.status_code == HTTPStatus.NOT_FOUND:
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
    blower: V2BlowerBlower,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V2BlowerJsonBody,
) -> Response[Any]:
    r"""Set Spa Blowers

     If the spa has blowers, this controls the spa's blowers.  The \"blower\" path parameter determines
    which blower to control (or all of them).  The pumps have two different states, an \"off\" state,
    and an \"on\" state.  When controlling individual pumps, if the current state of the pump matches
    the new state, a response with HTTP code 202 will be returned.

    Args:
        blower (V2BlowerBlower):
        json_body (V2BlowerJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        blower=blower,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    blower: V2BlowerBlower,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: V2BlowerJsonBody,
) -> Response[Any]:
    r"""Set Spa Blowers

     If the spa has blowers, this controls the spa's blowers.  The \"blower\" path parameter determines
    which blower to control (or all of them).  The pumps have two different states, an \"off\" state,
    and an \"on\" state.  When controlling individual pumps, if the current state of the pump matches
    the new state, a response with HTTP code 202 will be returned.

    Args:
        blower (V2BlowerBlower):
        json_body (V2BlowerJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        blower=blower,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
