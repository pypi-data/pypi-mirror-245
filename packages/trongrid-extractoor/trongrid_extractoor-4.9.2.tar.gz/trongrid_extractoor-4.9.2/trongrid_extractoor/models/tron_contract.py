"""
Dataclass representing an account at Tron/and or Tronscan.
"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from rich.panel import Panel
from rich.pretty import pprint
from rich.text import Text

from trongrid_extractoor.helpers.string_constants import ABI, CONTRACT_ADDRESS, NAME, TRC20

# This is a huge string in the JSON.
KEYS_TO_SUPPRESS_IN_LOGS = ['bytecode']


@dataclass(kw_only=True)
class TronContract:
    address: str
    name: Optional[str]
    abi: Optional[Dict[str, Any]]
    origin_address: Optional[str]
    raw_json: Optional[Dict[str, Union[dict, str, float, int]]] = None

    @classmethod
    def from_response_dict(cls, contract: Dict[str, Union[dict, str, float, int]]) -> 'TronContract':
        """Build a TronContract from the json data returned by Trongrid."""
        try:
            return cls(
                address=contract[CONTRACT_ADDRESS],
                abi=contract.get(ABI),
                name=contract.get(NAME),
                origin_address=contract.get('origin_address'),
                raw_json=contract
            )
        except KeyError:
            pprint(contract, expand_all=True, indent_guides=False)
            raise

    def label(self) -> str:
        return f"Contract: {self.name}" if self.name else '[AnonymousContract]'

    def raw_dict_shortened(self) -> Optional[Dict[str, Union[dict, str, float, int]]]:
        raw_copy = deepcopy(self.raw_json)

        for key in KEYS_TO_SUPPRESS_IN_LOGS:
            if key not in raw_copy:
                continue

            if key == 'bytecode':
                raw_copy[key] = '[REDACTED_FOR_BREVITY]'
            else:
                raw_copy[key] = [f"(List containing {len(raw_copy[key])} elements removed)"]

        return raw_copy

    def token_symbol(self) -> Optional[str]:
        """If this is a token contract attempt to get a useful symbol from the name field."""
        symbol = (self.name or 'token').lower()

        for prefix in ['bep20', 'erc20', 'trc20', 'token']:
            symbol = symbol.removeprefix(prefix).removesuffix(prefix).strip('_')

        return None if symbol == '' else symbol.upper()

    def __rich__(self) -> Panel:
        txt = Text('').append(self.address, style='bright_cyan')

        if self.name:
            txt.append(f" ({self.name})")

        return Panel(txt, expand=False)
