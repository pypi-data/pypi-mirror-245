"""
Dataclass representing a Tron txn that involves triggering a smart contract.
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
from trongrid_extractoor.models.txns.tron_txn import TronTxn
from trongrid_extractoor.response import Response

COMMON_HEADER = [TRANSACTION_ID, BLOCK_NUMBER, BLOCK_WRITTEN_AT, 'function_name']
KEYS_TO_STRIP_FROM_FLAT_DICT = [RAW_DATA, 'raw_txn', 'method_args']


@dataclass(kw_only=True)
class TriggerSmartContractTxn(TronTxn):
    # Key/value store of contract address => method IDs should be populated before use.
    # TODO: this may be obsolete?
    contract_method_info: ClassVar[Dict[str, Dict[str, Function]]] = {}

    # Derived fields
    contract_address: Optional[str] = None
    contract_owner: Optional[str] = None
    caller_contract_address: Optional[str] = None
    function_name: Optional[str] = None
    method_id: Optional[str] = None
    method_args: Optional[Dict[str, int|str|bool]] = None

    def __post_init__(self) -> None:
        """Compute various derived fields."""
        super().__post_init__()
        self.function = None
        self.caller_contract_address = self.raw_txn.get(CALLER_CONTRACT_ADDRESS)
        self._set_trigger_smart_contract_properties()

    def to_properties_dict(self, include_fee_cols: bool = False) -> Dict[str, bool|float|int|str]:
        """Convert to a flat key/value store with most important properties."""
        base_dict = self.prepare_properties(asdict(self), include_fee_cols)
        base_dict.update(self.method_args or {})
        return base_dict

    def _set_trigger_smart_contract_properties(self) -> None:
        """Set the properties that will exist if this were a smart contract invocation."""
        if not self.is_trigger_smart_contract_txn():
            return

        try:
            parameter_value = self.contract[PARAMETER][VALUE]
            self.contract_address = coerce_to_base58(parameter_value.get(CONTRACT_ADDRESS))
            self.contract_owner = coerce_to_base58(parameter_value['owner_address'])
            function_call_data = parameter_value.get('data')
        except KeyError:
            console.print_exception()
            self._log_raw_json()
            raise

        # Function ID is the first 8 chars
        self.method_id = function_call_data[0:8]
        method_args = [arg.lstrip('0') for arg in self._split_data(function_call_data[8:])]

        if self.contract_address not in type(self).contract_method_info:
            log.warning(f"Unknown triggered smart contract: {self.contract_address}")
            return

        try:
            self.function = type(self).contract_method_info[self.contract_address][self.method_id]
            self.function_name = self.function.name

            if len(method_args) != len(self.function.args):
                raise ValueError(f"Expected {len(self.function.args)} args but got {len(self.method_args)} for {self}")

            self.method_args = {
                arg.name: arg.coerce_arg_value(method_args[i], True)
                for i, arg in enumerate(self.function.args)
            }
        except Exception:
            console.print_exception()
            console.print(f"\n\n--------DATA START-----------")
            pretty_print(self.raw_txn)
            console.print(f"---------DATA-END-----------\n\n")
            raise

    def __rich__(self) -> Text:
        txt = self._txn_rich_text()
        txt.append('\n[Contract] ').append(str(self.contract_address), style=CONTRACT_ADDRESS)
        txt.append(' (Owner: ').append(str(self.contract_owner), style=CONTRACT_ADDRESS).append(')')

        if self.function is not None:
            txt.append('\n[Fxn] ').append(self.function.__rich__())

        if self.method_args is not None:
            for arg_name, arg_value in self.method_args.items():
                txt.append(Text(f"\n    ").append(arg_name, style='green bold').append(': ').append(str(arg_value)))

        return txt

    def __str__(self) -> str:
        return self.__rich__().plain

        msg = f"[{self.block_written_at_str()}] {self.transaction_id}\n[Contract] {self.contract_address}"

        if self.function is not None:
            msg += f"\n[Fxn] {self.function.method_signature()}"

        return msg
