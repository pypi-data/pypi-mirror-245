"""
A class for Tron txns that just move TRX from one account to another.
"""
from dataclasses import dataclass
from typing import Optional

from rich.text import Text

from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.string_constants import ADDRESS, AMOUNT, PARAMETER, TRX_ADDRESS, VALUE
from trongrid_extractoor.helpers.string_helpers import number_str
from trongrid_extractoor.models.txns.tron_txn import TronTxn


@dataclass(kw_only=True)
class TrxTransfer(TronTxn):
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[float|int] = None
    token_address: str = TRX_ADDRESS

    def __post_init__(self) -> None:
        super().__post_init__()
        transfer_properties = self.contract[PARAMETER][VALUE]
        self.from_address = coerce_to_base58(transfer_properties['owner_address'])
        self.to_address = coerce_to_base58(transfer_properties['to_address'])
        self.amount = transfer_properties[AMOUNT] / (10 ** 6)

    def __rich__(self) -> Text:
        txt = self._txn_rich_text().append(f" {number_str(self.amount)} TRX", style='trx')
        txt.append(' (From: ', style='arg_type').append(self.from_address, style=ADDRESS)
        txt.append(' To: ', style='arg_type').append(self.to_address, style=ADDRESS).append(')')
        return txt
