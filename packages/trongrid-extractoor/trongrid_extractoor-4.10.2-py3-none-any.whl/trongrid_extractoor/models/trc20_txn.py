"""
Dataclass representing one TRC20 token transfer.
"""
from dataclasses import asdict, dataclass
from random import randint
from typing import Any, Dict, List, Optional, Tuple, Union

from rich.text import Text

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.rich_helpers import console, pretty_print
from trongrid_extractoor.models.tron_event import TronEvent
from trongrid_extractoor.helpers.address_helpers import hex_to_tron
from trongrid_extractoor.helpers.string_constants import (ADDRESS, AMOUNT, BLOCK_TIMESTAMP, DST, FROM,
     TO, VALUE, SRC, RESULT, TRANSACTION_ID, TRANSFER, TYPE, WAD, SAD)
from trongrid_extractoor.exceptions import UnparseableResponse

# Some tokens use src/dst/wad instead of from/to/value
FROM_TO_AMOUNT = (FROM, TO, AMOUNT)
FROM_TO_VALUE = (FROM, TO, VALUE)
SRC_DST_SAD = (SRC, DST, SAD)
SRC_DST_WAD = (SRC, DST, WAD)

UNKNOWN_RESULT_FIELDS_MSG = 'Unknown result fields'
CSV_FIELDS = 'token_address,from_address,to_address,amount,transaction_id,event_index,ms_from_epoch,block_number'.split(',')


@dataclass(kw_only=True)
class Trc20Txn(TronEvent):
    from_address: str
    to_address: str
    amount: int

    def __post_init__(self):
        super().__post_init__()
        self.amount = int(float(self.amount))
        self.from_address = hex_to_tron(self.from_address) if self.from_address.startswith('0x') else self.from_address
        self.to_address = hex_to_tron(self.to_address) if self.to_address.startswith('0x') else self.to_address

    @classmethod
    def from_json_obj(cls, row: Dict[str, str|float|int]) -> 'Trc20Txn':
        """Build a TRC20Txn from a 'Transfer' Event."""
        # Check the 'result_type' to see if it's from/to/value or src/dst/wad keys.
        if 'result_type' not in row:
            return cls.from_trc20_json_obj(row)

        txn_from, txn_to, txn_amount = cls.identify_txn_keys(row['result_type'])
        event = TronEvent.from_json_obj(row)

        return cls(
            from_address=row[RESULT][txn_from],
            to_address=row[RESULT][txn_to],
            amount=row[RESULT][txn_amount],
            **{k: v for k, v in asdict(event).items()}
        )

    @classmethod
    def from_trc20_json_obj(cls, row: Dict[str, str|float|int|Dict[str, str|int]]) -> 'Trc20Txn':
        """Build a TRC20Txn from the more limited JSON returned by the /account/trc20 endpoint."""
        # Have to build by hand because a lot of fields are missing
        event = TronEvent(
            event_name=row[TYPE],
            token_address=row['token_info'][ADDRESS],
            transaction_id=row[TRANSACTION_ID],
            event_index=randint(1, 2_000_000_000),  # TODO: this sucks but they don't give a value in the response :(
            ms_from_epoch=row[BLOCK_TIMESTAMP],
            raw_event=row
        )

        return cls(
            from_address=row[FROM],
            to_address=row[TO],
            amount=row[VALUE],
            **{k: v for k, v in asdict(event).items()}
        )

    @classmethod
    def csv_header_row_length(cls) -> int:
        """When this class is exported to a CSV this would be the size of an empty file."""
        return len(','.join(CSV_FIELDS)) + 1

    # TODO: rename to_properties_dict()
    def as_dict(self, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get a dict representation of key/value pairs that's ready for CSV writing."""
        keys = keys or CSV_FIELDS
        return {k: v for k, v in asdict(self).items() if k in keys}

    def __rich__(self) -> Text:
        msg = f"Token: {self.token_address[0:10]}..., From: {self.from_address[0:10]}..."
        msg += f", To: {self.to_address[0:10]}..., ID: {self.transaction_id}/{self.event_index}"
        msg += f", Amount: {self.amount} (at {self.block_written_at})"
        return Text(msg)

    def __str__(self) -> str:
        return self.__rich__().plain

    @staticmethod
    def identify_txn_keys(result_type: Dict[str, str]) -> Tuple[str, str, str]:
        """Determine which set of keys represent the from, to, and amount. Diff tokens use diff keys."""
        if sorted(result_type.keys()) == sorted(SRC_DST_WAD):
            return SRC_DST_WAD
        elif sorted(result_type.keys()) == sorted(FROM_TO_AMOUNT):
            return FROM_TO_AMOUNT
        elif sorted(result_type.keys()) == sorted(FROM_TO_VALUE):
            return FROM_TO_VALUE
        elif sorted(result_type.keys()) == sorted(SRC_DST_SAD):
            return SRC_DST_SAD
        else:
            raise UnparseableResponse(f"{UNKNOWN_RESULT_FIELDS_MSG}: {result_type.keys()}")
