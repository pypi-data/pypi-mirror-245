import pytest
import json
from pydantic.error_wrappers import ValidationError

from ogmios.errors import InvalidMethodError, InvalidResponseError, ResponseError
from ogmios.datatypes import Origin, Point, GenesisConfiguration, Era

from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryGenesisConfiguration_byron(client):
    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(Era.byron.value, id_str)

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str


def test_QueryGenesisConfiguration_shelley(client):
    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(
        Era.shelley.value, id_str
    )

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str


def test_QueryGenesisConfiguration_alonzo(client):
    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(Era.alonzo.value, id_str)

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str


def test_QueryGenesisConfiguration_conway(client):
    id_str = "My ID string"
    genesis_configuration, id = client.query_genesis_configuration.execute(Era.conway.value, id_str)

    assert isinstance(genesis_configuration, GenesisConfiguration)
    assert id == id_str
