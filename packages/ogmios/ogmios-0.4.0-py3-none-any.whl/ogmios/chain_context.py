import time
from typing import Optional, Union
from cachetools import Cache, LRUCache, TTLCache, func
import pycardano as pyc

from ogmios.client import Client
from ogmios.datatypes import (
    ProtocolParameters,
    Era,
    Tip,
    Utxo,
    Address,
    TxOutputReference,
)
from ogmios.utils import get_current_era, GenesisParameters

ALONZO_COINS_PER_UTXO_WORD = 34482

class OgmiosChainContext(pyc.ChainContext):
    """Ogmios chain context for use with PyCardano"""

    _network: pyc.Network
    _client: Client
    _service_name: str
    _last_known_block_slot: int
    _last_chain_tip_fetch: float
    _genesis_param: Optional[GenesisParameters]
    _protocol_param: Optional[ProtocolParameters]
    _utxo_cache: Cache
    _datum_cache: Cache

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1337,
        secure: bool = False,
        refetch_chain_tip_interval: Optional[float] = None,
        utxo_cache_size: int = 10000,
        datum_cache_size: int = 10000,
    ):
        self.client = Client(host, port, secure)
        self._service_name = "ogmios"
        self._last_known_block_slot = 0
        self._refetch_chain_tip_interval = (
            refetch_chain_tip_interval if refetch_chain_tip_interval is not None else 1000
        )
        self._last_chain_tip_fetch = 0
        self._genesis_param = None
        self._protocol_param = None
        if (
            refetch_chain_tip_interval is None
            and self._genesis_param is not None
            and self._genesis_param.slot_length is not None
            and self._genesis_param.active_slots_coefficient is not None
        ):
            # TODO
            self._refetch_chain_tip_interval = (
                self._genesis_param.slot_length / self._genesis_param.active_slots_coefficient
            )

        self._utxo_cache = TTLCache(ttl=self._refetch_chain_tip_interval, maxsize=utxo_cache_size)
        self._datum_cache = LRUCache(maxsize=datum_cache_size)

    def _query_current_era(self) -> Era:
        return get_current_era(self.client)

    def _query_current_epoch(self) -> int:
        epoch, _ = self.client.query_epoch.execute()
        return epoch

    def _query_chain_tip(self) -> Tip:
        tip, _ = self.client.query_network_tip.execute()
        return tip

    def _query_utxos_by_address(self, address: Address) -> list[Utxo]:
        utxos, _ = self.client.query_utxo.execute([address])
        return utxos

    def _query_utxos_by_tx_id(self, tx_id: str, index: int) -> list[Utxo]:
        utxos, _ = self.client.query_utxo.execute([TxOutputReference(tx_id, index)])
        return utxos

    def _is_chain_tip_updated(self):
        # fetch at most every twenty seconds!
        if time.time() - self._last_chain_tip_fetch < self._refetch_chain_tip_interval:
            return False
        self._last_chain_tip_fetch = time.time()
        slot = self.last_block_slot
        if self._last_known_block_slot < slot:
            self._last_known_block_slot = slot
            return True
        else:
            return False

    @staticmethod
    def _fraction_parser(fraction: str) -> float:
        x, y = fraction.split("/")
        return int(x) / int(y)

    @property
    def protocol_param(self) -> ProtocolParameters:
        if not self._protocol_param or self._is_chain_tip_updated():
            self._protocol_param = self._fetch_protocol_param()
        return self._protocol_param

    def _fetch_protocol_param(self) -> ProtocolParameters:
        protocol_parameters, _ = self.client.query_protocol_parameters.execute()
        # Remap the fields to match the PyCardano naming convention
        protocol_parameters.min_fee_constant = protocol_parameters.min_fee_constant.lovelace
        protocol_parameters.min_pool_cost = protocol_parameters.min_stake_pool_cost.lovelace
        protocol_parameters.max_block_size = protocol_parameters.max_block_body_size.get("bytes")
        protocol_parameters.max_tx_size = protocol_parameters.max_transaction_size.get("bytes")
        protocol_parameters.max_val_size = protocol_parameters.max_value_size.get("bytes")
        protocol_parameters.key_deposit = protocol_parameters.stake_credential_deposit.get("lovelace")
        protocol_parameters.pool_deposit = protocol_parameters.stake_pool_deposit
        protocol_parameters.pool_influence = eval(protocol_parameters.stake_pool_pledge_influence)
        protocol_parameters.min_pool_cost = protocol_parameters.min_stake_pool_cost
        protocol_parameters.price_step = eval(protocol_parameters.script_execution_prices.get("cpu"))
        protocol_parameters.price_mem = eval(protocol_parameters.script_execution_prices.get("memory"))
        protocol_parameters.max_tx_ex_steps = protocol_parameters.max_execution_units_per_transaction.get("cpu")
        protocol_parameters.max_tx_ex_mem = protocol_parameters.max_execution_units_per_transaction.get("memory")
        protocol_parameters.max_block_ex_steps = protocol_parameters.max_execution_units_per_block.get("cpu")
        protocol_parameters.max_block_ex_mem = protocol_parameters.max_execution_units_per_block.get("memory")
        protocol_parameters.protocol_major_version = protocol_parameters.version.get("major")
        protocol_parameters.protocol_minor_version = protocol_parameters.version.get("minor")

        if not hasattr(protocol_parameters, "coins_per_utxo_word"):
            protocol_parameters.coins_per_utxo_word = ALONZO_COINS_PER_UTXO_WORD

        if not hasattr(protocol_parameters, "coins_per_utxo_byte"):
            protocol_parameters.coins_per_utxo_byte = 0

        return protocol_parameters

    @property
    def genesis_param(self) -> GenesisParameters:
        if not self._genesis_param or self._is_chain_tip_updated():
            self._genesis_param = self._fetch_genesis_param()
        return self._genesis_param

    def _fetch_genesis_param(self) -> GenesisParameters:
        return GenesisParameters(self.client, self._query_current_era())

    @property
    def network(self) -> pyc.Network:
        return self._network

    @property
    def epoch(self) -> int:
        return self._query_current_epoch()

    @property
    @func.ttl_cache(ttl=1)
    def last_block_slot(self) -> int:
        tip = self._query_chain_tip()
        return tip.slot

    def _utxos(self, address: str) -> list[pyc.UTxO]:
        key = (self.last_block_slot, address)
        if key in self._utxo_cache:
            return self._utxo_cache[key]

        utxos = self._utxos_ogmios(Address(address=address))

        self._utxo_cache[key] = utxos

        return utxos

    def _utxos_ogmios(self, address: Address) -> list[Utxo]:
        """Get all UTxOs associated with an address with Ogmios.

        Args:
            address (str): An address encoded with bech32.

        Returns:
            List[UTxO]: A list of UTxOs.
        """
        results = self._query_utxos_by_address(address)

        utxos = []
        for result in results:
            utxos.append(self._utxo_from_ogmios_result(result))

        return utxos

    def _utxo_from_ogmios_result(self, utxo: Utxo) -> pyc.UTxO:
        """Convert an Ogmios UTxO result to a PyCardano UTxO."""
        tx_in = pyc.TransactionInput.from_primitive([utxo.tx_id, utxo.index])
        lovelace_amount = utxo.value.get("lovelace", 0)
        script = utxo.script
        if script:
            match str(script.json()):
                case "plutus:v2":
                    script = pyc.PlutusV2Script(bytes.fromhex(script.json["plutus:v2"]))
                case "plutus:v1":
                    script = pyc.PlutusV1Script(bytes.fromhex(script.json["plutus:v1"]))
                case _:
                    raise ValueError("Unknown plutus script type")
        datum_hash = pyc.DatumHash.from_primitive(utxo.datum_hash) if utxo.datum_hash else None
        datum = None
        if utxo.datum and utxo.datum != utxo.datum_hash:
            datum = pyc.RawCBOR(bytes.fromhex(utxo.datum))
        if not utxo.value.get("assets"):
            tx_out = pyc.TransactionOutput(
                pyc.Address.from_primitive(utxo.address),
                amount=lovelace_amount,
                datum_hash=datum_hash,
                datum=datum,
                script=script,
            )
        else:
            # TODO
            multi_assets = pyc.MultiAsset()

            for asset, quantity in utxo.value.get("assets").items():
                policy_hex, policy, asset_name_hex = self._extract_asset_info(asset)
                multi_assets.setdefault(policy, pyc.Asset())[asset_name_hex] = quantity

            tx_out = pyc.TransactionOutput(
                pyc.Address.from_primitive(utxo.address),
                amount=pyc.Value(lovelace_amount, multi_assets),
                datum_hash=datum_hash,
                datum=datum,
                script=script,
            )
        pyc_utxo = pyc.UTxO(tx_in, tx_out)
        return pyc_utxo

    def utxo_by_tx_id(self, tx_id: str, index: int) -> Optional[Utxo]:
        utxos = self._query_utxos_by_tx_id(tx_id, index)
        if len(utxos) > 0:
            return utxos[0]
        return None

    def submit_tx_cbor(self, cbor: Union[bytes, str]):
        if isinstance(cbor, bytes):
            cbor = cbor.hex()
        self.client.submit_transaction.execute(cbor)

    def evaluate_tx_cbor(self, cbor: Union[bytes, str]) -> str:
        if isinstance(cbor, bytes):
            cbor = cbor.hex()
        result, _ = self.client.evaluate_transaction.execute(cbor)
        return result
