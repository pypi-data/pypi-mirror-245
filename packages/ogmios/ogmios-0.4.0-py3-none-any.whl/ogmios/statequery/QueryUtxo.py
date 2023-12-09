from __future__ import annotations

from typing import Any, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ogmios.client import Client

from ogmios.errors import InvalidMethodError, InvalidResponseError, ResponseError
from ogmios.logger import logger
from ogmios.datatypes import TxOutputReference, Address, Utxo
import ogmios.model.ogmios_model as om
import ogmios.model.model_map as mm

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


class QueryUtxo:
    """Ogmios method to query the current UTxO set, restricted to some output references or
    addresses.

    NOTE: This class is not intended to be used directly. Instead, use the Client.query_utxo
    method.

    :param client: The client to use for the request.
    :type client: Client
    """

    def __init__(self, client: Client):
        self.client = client
        self.method = mm.Method.queryLedgerState_utxo.value

    def execute(
        self, output_ref: list[TxOutputReference] | list[Address], id: Optional[Any] = None
    ) -> (list[Utxo], Optional[Any]):
        """Send and receive the request.

        :param output_ref: The output reference to query. Can be a list of TxOutputReference or a list
            of Address.
        :type output_ref: list[TxOutputReference] | list[Address]
        :param id: The ID of the request.
        :type id: Any
        :return: List of Utxo's and ID of the response.
        :rtype: (list[Utxo], Optional[Any])
        """
        self.send(output_ref, id)
        return self.receive()

    def send(
        self, output_ref: list[TxOutputReference] | list[Address], id: Optional[Any] = None
    ) -> None:
        """Send the request.

        :param output_ref: The output reference to query. Can be a list of TxOutputReference or a list
            of Address.
        :param id: The ID of the request.
        :type id: Any
        """
        match output_ref:
            case [Address()] as addresses:
                params = om.Param1(addresses=[addr.address for addr in addresses])
            case [TxOutputReference()]:
                params = om.Param(outputReferences=[ref._schematype for ref in output_ref])
            case _:
                raise TypeError(
                    f"Invalid type for output_ref: {type(output_ref)}. Must be Utxo, list[Address], or list[TxOutputReference]"
                )

        pld = om.QueryLedgerStateUtxo(
            jsonrpc=self.client.rpc_version,
            method=self.method,
            params=params,
            id=id,
        )
        self.client.send(pld.json())

    def receive(self) -> (list[Utxo], Optional[Any]):
        """Receive the response.

        :return: List of Utxo's and ID of the response.
        :rtype: (list[Utxo], Optional[Any])
        """
        response = self.client.receive()
        return self._parse_QueryUtxo_response(response)

    @staticmethod
    def _parse_QueryUtxo_response(
        response: dict,
    ) -> (list[Utxo], Optional[Any]):
        if response.get("method") != mm.Method.queryLedgerState_utxo.value:
            raise InvalidMethodError(f"Incorrect method for query_utxo response: {response}")

        if response.get("error"):
            raise ResponseError(f"Ogmios responded with error: {response}")

        id: Optional[Any] = response.get("id")

        if response.get("result") == []:
            logger.info("No UTxOs found")
            return [], id

        if result := response.get("result"):
            utxos = []
            for utxo in result:
                utxos.append(
                    Utxo(
                        tx_id=utxo.get("transaction").get("id"),
                        index=utxo.get("index"),
                        address=utxo.get("address"),
                        value=utxo.get("value"),
                        datum_hash=utxo.get("dataumHash"),
                        datum=utxo.get("datum"),
                        script=utxo.get("script"),
                    )
                )
            logger.info(
                f"""Parsed utxo response:
        UTxOs = {utxos}
        ID = {id}"""
            )
            return utxos, id

        raise InvalidResponseError(f"Failed to parse query_utxo response: {response}")
