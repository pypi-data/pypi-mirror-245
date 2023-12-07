"""
A class for Tron txns that creates a smart contract.
"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from rich.text import Text

from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.string_constants import CONTRACT_ADDRESS, PARAMETER, VALUE
from trongrid_extractoor.models.tron_contract import TronContract
from trongrid_extractoor.models.txns.tron_txn import TronTxn


@dataclass(kw_only=True)
class CreateSmartContractTxn(TronTxn):
    created_contract: Optional[TronContract] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        creation_properties = deepcopy(self.contract[PARAMETER][VALUE]['new_contract'])

        # Trongrid does not return the actual address of the deployed contract via the normal
        # account txns endpoint so we have to fetch again :(
        deployed_contract_address = TronTxn.txn_by_id(self.transaction_id)[CONTRACT_ADDRESS]
        creation_properties[CONTRACT_ADDRESS] = coerce_to_base58(deployed_contract_address)
        self.created_contract = TronContract.from_response_dict(creation_properties)

    def to_properties_dict(self) -> None:
        properties = super().to_properties_dict()
        del properties['created_contract']['raw_json']
        return properties

    def __rich__(self) -> Text:
        txt = self._txn_rich_text()

        if self.created_contract.name:
            txt.append(': ').append(self.created_contract.name, style='contract_name')

        return txt
