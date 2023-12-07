"""
Dataclass representing one Tron transaction (like an actual transaction, not a TRC20 txn).
"""
from dataclasses import InitVar, asdict, dataclass, field, fields
from typing import Any, ClassVar, Dict, Iterator, List, Optional, Tuple, Union

import pendulum
from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult
from rich.panel import Panel
from rich.text import Text

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.rich_helpers import console, pretty_print
from trongrid_extractoor.helpers.string_constants import (AMOUNT, BLOCK_NUMBER, BLOCK_TIMESTAMP,
     BLOCK_WRITTEN_AT, CALLER_CONTRACT_ADDRESS, CONTRACT, CONTRACT_ADDRESS, CREATE_SMART_CONTRACT,
     INTERNAL_TRANSACTIONS, PARAMETER, RAW_DATA, TRANSACTION_ID, TRANSFER_CONTRACT,
     TRIGGER_SMART_CONTRACT, TYPE, VALUE)
from trongrid_extractoor.helpers.url_helpers import build_endpoint_url
from trongrid_extractoor.models.function import Function
from trongrid_extractoor.response import Response

COMMON_HEADER = [TRANSACTION_ID, BLOCK_NUMBER, BLOCK_WRITTEN_AT, 'function_name']
FEE_COLS = ['net_usage', 'net_fee', 'energy_fee', 'energy_usage', 'energy_usage_total']
KEYS_TO_STRIP_FROM_FLAT_DICT = [RAW_DATA, 'raw_txn', 'method_args']


@dataclass(kw_only=True)
class TronTxn:
    transaction_id: str
    block_number: int
    block_written_at: int|pendulum.DateTime
    raw_data: Dict[str, Any]
    internal_transactions: List[Dict[str, Any]]
    net_usage: int
    net_fee: int
    energy_fee: int
    energy_usage: int
    energy_usage_total: int
    raw_txn: Dict[str, Any]

    # Derived fields
    txn_type: Optional[str] = None

    def __post_init__(self) -> None:
        """Compute various derived fields."""
        self.block_written_at = pendulum.from_timestamp(int(self.block_written_at / 1000.0), pendulum.tz.UTC)
        self.unique_id = self.transaction_id  # There is no log_index / event_index for an actual txn
        self.contract: Dict[str, dict|list|int|str] = self.raw_data[CONTRACT][0]
        self.txn_type = self.contract[TYPE]

    @classmethod
    def from_json_obj(cls, txn: Dict[str, Any], method_ids: Optional[Dict[str, Any]] = None) -> 'TronTxn':
        """Build an event from the json data returned by Trongrid."""
        return cls(
            transaction_id=txn['txID'],
            block_number=txn['blockNumber'],
            block_written_at=txn[BLOCK_TIMESTAMP],
            raw_data=txn['raw_data'],
            internal_transactions=txn[INTERNAL_TRANSACTIONS],
            net_usage=txn['net_usage'],
            net_fee=txn['net_fee'],
            energy_fee=txn['energy_fee'],
            energy_usage=txn['energy_usage'],
            energy_usage_total=txn['energy_usage_total'],
            raw_txn=txn
        )

    def is_create_smart_contract_txn(self) -> bool:
        """Return True if this is a transfer of TRX."""
        return self.txn_type == CREATE_SMART_CONTRACT

    def is_trigger_smart_contract_txn(self) -> bool:
        """Is this txn created by the triggering of a smart contract?"""
        return self.txn_type == TRIGGER_SMART_CONTRACT

    def is_trx_transfer(self) -> bool:
        """Return True if this is a transfer of TRX."""
        return self.txn_type == TRANSFER_CONTRACT

    def to_properties_dict(self, include_fee_cols: bool = False) -> Dict[str, bool|float|int|str]:
        """Convert to a flat key/value store with most important properties."""
        return self.prepare_properties(asdict(self))

    def prepare_properties(self, properties: Dict[str, Any], include_fee_cols: bool = False) -> Dict[str, Any]:
        """Mutate 'properties' to remove fields undesirable (unprintable to CSV) fields."""
        if not include_fee_cols:
            for key in FEE_COLS:
                del properties[key]

        for key in [k for k in KEYS_TO_STRIP_FROM_FLAT_DICT if k in properties]:
            del properties[key]

        # Collapse internal txns to a semicolon separated list.
        properties[INTERNAL_TRANSACTIONS] = '; '.join([tx['internal_tx_id'] for tx in (self.internal_transactions)])
        return properties

    def block_written_at_str(self) -> str:
        """ISO8601 version of block_written at."""
        return self.block_written_at.format('YYYY-MM-DDTHH:mm:ss')

    def _split_data(self, data: str) -> List[str]:
        """The 'data' field is a concatenated list of args in one monster hex string."""
        return list(map(''.join, zip(*[iter(data)] * 64)))

    def _log_raw_json(self) -> None:
        """Pretty print the raw JSON response from the API."""
        console.print(f"\n\n--------DATA START-----------")
        pretty_print(self.raw_txn)
        console.print(f"---------DATA-END-----------\n\n")

    def _txn_rich_text(self) -> Text:
        """Common prefix for all TronTxn objects. Subclasses should customize from here."""
        txt = Text('[').append(self.block_written_at_str(), style='time').append('] ')
        txt.append(self.txn_type, style='bright_cyan').append(' (')
        return txt.append(self.transaction_id, style=TRANSACTION_ID).append(')')

    def __iter__(self) -> Iterator:
        """Enable calls like dict(tron_event) to work."""
        for k, v in self.to_properties_dict().items():
            yield k, v

    def __rich__(self) -> Text:
        return self._txn_rich_text()

    def __str__(self) -> str:
        return self.__rich__().plain

    @staticmethod
    def txn_by_id(txn_id: str) -> Dict[str, Any]:
        """
        This endpoint tells us things the main account_txns() endpoint does not.
        There's also a separate 'txn info by ID' endpoint for whatever else.
        Test harness: https://developers.tron.network/reference/gettransactionbyid
        """
        log.info(f"Retrieving txn at '{txn_id}'...")
        endpoint_url = build_endpoint_url('walletsolidity/gettransactionbyid')
        return Response.post_response(endpoint_url, {VALUE: txn_id}).response
