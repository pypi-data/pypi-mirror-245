"""
Dataclass representing a function signature (name, methodID, args, etc.)
"""
import re
from dataclasses import asdict, dataclass
from typing import Callable, Dict, List, Optional

from rich.text import Text

from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.string_helpers import keccak256
from trongrid_extractoor.models.function_arg import FunctionArg

FUNCTION_REGEX = re.compile(r'(\w+)\(([\w, ]+)\)')


@dataclass
class Function:
    args: List[FunctionArg]
    name: Optional[str] = None

    def __post_init__(self) -> None:
        """Method ID for an EVM method is the first 8 chars of the Keccak-256 hash of the signature."""
        self.method_id = keccak256(self.method_signature())[0:8]

    @classmethod
    def from_function_string(cls, function_str: str) -> 'Function':
        """Build from str like 'withdraw_token(address _child, address _token, uint256 amount, address receiver)'."""
        match = FUNCTION_REGEX.match(function_str)
        assert match is not None, f"Invalid fxn string: '{function_str}'!"
        return cls(FunctionArg.from_function_args(match.group(2)), match.group(1))

    def method_signature(self) -> str:
        """Method name with arg types only and no spaces."""
        return f"{self.name}({','.join([arg.arg_type for arg in self.args])})"

    def parse_args(
            self,
            data: str,
            address_coercer: Callable[[str], str] = coerce_to_base58
        ) -> Dict[str, int|str]:
        """Parse a data string to a dict of arguments."""
        data = data.removeprefix('0x')

        if data[0:8] != self.method_id:
            raise ValueError(f"Invalid method ID '{data[0:8]}' for function {self}")

        # Break into 64 char chunks
        arg_values = list(map(''.join, zip(*[iter(data[8:])] * 64)))

        return {
            arg.name: arg.coerce_arg_value(arg_values[i], True, address_coercer)
            for i, arg in enumerate(self.args)
        }

    def __rich__(self) -> Text:
        name = self.name or f"anon_{self.method_id}"
        txt = Text('').append(name, style='function').append('(')
        return txt.append(Text(', ').join([arg.__rich__() for arg in self.args])).append(')')

    def __str__(self) -> str:
        """There's no semicolons the way the functions are presented in some places."""
        return self.__rich__().plain.replace(':', '')
