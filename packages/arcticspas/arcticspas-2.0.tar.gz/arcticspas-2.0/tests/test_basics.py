import os
import time
from http import HTTPStatus
from typing import Optional

from arcticspas import Client
from arcticspas.api.spa_control import v2_light, v2_spa
from arcticspas.models import V2LightJsonBody, V2LightJsonBodyState, V2SpaResponse200
from arcticspas.types import Response

singleton_client: Optional[Client] = None


def get_client():
    global singleton_client
    if singleton_client is None:
        token = os.environ.get("ARCTICSPAS_TOKEN")
        assert token is not None
        singleton_client = Client(base_url="https://api.myarcticspa.com", headers={"X-API-KEY": token})
    return singleton_client


def get_status():
    status: Response[V2SpaResponse200] = v2_spa.sync_detailed(client=get_client())
    assert status is not None
    assert status.status_code != HTTPStatus.UNAUTHORIZED
    assert status.parsed is not None
    return status.parsed


def test_connected():
    spa = get_status()
    assert spa.connected is True


def test_lights():
    # Query light status
    spa_status = get_status()
    assert spa_status.lights == V2LightJsonBodyState["ON"] or spa_status.lights == V2LightJsonBodyState["OFF"]

    # Create expected new state
    new_spa_state = V2LightJsonBody()
    new_spa_state.state = V2LightJsonBodyState["ON"]

    if spa_status.lights == V2LightJsonBodyState["ON"]:
        new_spa_state.state = V2LightJsonBodyState["OFF"]

    # Send expected new state
    response = v2_light.sync_detailed(client=get_client(), json_body=new_spa_state)
    assert response.status_code == HTTPStatus.OK

    # Query light status again
    time.sleep(1)
    new_spa_status = get_status()
    assert new_spa_status.lights == new_spa_state.state.value
