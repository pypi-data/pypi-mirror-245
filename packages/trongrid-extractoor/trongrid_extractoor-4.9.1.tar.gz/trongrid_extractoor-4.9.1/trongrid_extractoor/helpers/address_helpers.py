"""
Methods to work with tron addresses.
https://stackoverflow.com/questions/57200685/how-to-convert-tron-address-to-different-format
"""
import logging
import re
from typing import Optional

import base58
from rich.console import Console
from rich.text import Text

from trongrid_extractoor.exceptions import InvalidAddressError
from trongrid_extractoor.helpers.dict_helper import get_dict_key_by_value
from trongrid_extractoor.helpers.rich_helpers import console

TRON_HEX_ADDRESS_REGEX = re.compile("41[a-f0-9]{40}", re.IGNORECASE)
TRON_BASE58_ADDRESS_REGEX = re.compile("T[a-z0-9]{33}", re.IGNORECASE)
EVM_ADDRESS_REGEX = re.compile(r'\b(0x[0-9a-fA-F]{40}|0x0)\b')

TOKEN_ADDRESSES = {
    'TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9': 'BTCT',   # BTC on Tron (?!)
    'TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4': 'BTT',

    # Same:
    'TMz2SWatiAtZVVcH2ebpsbVtYwUPT9EdjH': 'BUSD',
    'TMz2SWatiAtZVVcH2ebpsbVtYwUPT9EdjH': 'BinancePeg-BUSD',

    'TRwptGFfX3fuffAMbWDDLJZAZFmP6bGfqL': 'DCT',
    'THbVQp8kMjStKNnf2iCY6NEzThKMK5aBHg': 'DOGET',  # DOGEcoin on Tron (?!)
    'THb4CqiFdwNHsWsQCs4JhzwjMWys4aqCbF': 'ETHOLD',
    'TRFe3hT5oYhjSZ6f3ji5FJ7YCfrkWnHRvh': 'ETHT',
    'TDyvndWuvX5xTBwHPYJi7J3Yq8pq8yh62h': 'HT',     # Huobi Token
    'TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT': 'jBTC',
    'TUaUHU9Dy8x5yNi1pKnFYqHWojot61Jfto': 'jBTT',
    'TLHASseQymmpGQdfAyNjkMXFTJh8nzR2x2': 'jBUSD',
    'TV93dQ5cJBoa6TXfmanCpLqW42pqPdQzai': 'jHT',
    'TWQhCXaWz4eHK4Kd1ErSDHjMFPoPc9czts': 'jJST',
    'TFpPyDCKvNFgos3g3WVsAqMrdqhB81JXHE': 'jNFT',
    'TJQ9rbVe9ei3nNtyGgBL22Fuu2xYjZaLAQ': 'jsTRX',
    'TPXDpkg9e3eZzxqxAUyke9S4z4pGJBJw9e': 'jSUN',
    'TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP': 'jTRX',
    'TSXv71Fy5XdL3Rh2QfBoUu3NAaM4sMif8R': 'jTUSD',
    'TNSBA6KvSvMoTqQcEgpVK7VhHT3z7wifxy': 'jUSDC',
    'TX7kybeP6UwTBRHLNPYmswFESHfyjm9bAS': 'jUSDD',
    'TL5x9MtSnDy537FXKx53yAaHRRNdg9TkkA': 'jUSDJ',
    'TXJgMdjVX5dKiQaUi9QobwNxtSQaFqccvd': 'jUSDT',
    'TYUzYRmLvfd4quvRYH657q5CeH7wWQL9T3': 'JusLend',
    'TUY54PVeH6WCcYCd6ZXXoBDsHytN9V5PXt': 'jWBTT',
    'TRg6MnpsFXc82ymUPgf5qbj59ibxiEDWvv': 'jWIN',
    'TD5SdLw5scR6mXgyMK2xKrFJpauDjpKqrW': 'jwstUSDT',
    'TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9': 'JST',
    'TR3DLthpnDdCGabhVDbD3VMsiJoCXY3bZd': 'LTCT',
    #'TVh1PF9xr4zC5uAqRcCbxF1By6ucp95G4i': 'stUSDT_old',
    'TY7copxkSQZBym6eTGMEdrqPHaNNsmjxKe': 'MMXN',
    'THimy8GRxTcMFwf8nVtNm9Bcn4XPEUp9vK': 'MOTB',
    'TFczxzPhnThNSqr5by8tvxsdCFRRz6cPNq': 'NFT',
    'TGbu32VEGpS4kDmjrmn5ZZJgUyHQiaweoq': 'PEARL',
    'TThzxNRLrW2Brp9DcTQU8i4Wd9udCWEdZ3': 'stUSDT',
    'TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5': 'sTRX',
    'TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S': 'SUN',
    'TKkeiboTkxXKJpbmVFbv4a8ov5rAfRDMf9': 'SUNOLD',
    'TNu2UgeDjPxr62CUfjh8poRvcf6EiJHjJs': 'TBC',
    'TBqsNXUtqaLptVK8AYvdPPctpqd8oBYWUC': 'TCNH',
    'TYEdJmskR1a5Q1deFWtRoW6WjGT54sYMHa': 'TRA',
    'TUpMhErZL2fhh4sVNULAbNKLokS4GjC1F4': 'TUSD',
    'TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8': 'USDC',
    'TPYmHEhy5n8TCEfYGqW2rPxsghSfzghPDn': 'USDD',
    'TMwFHYXLJaRUPeW6421aqXL4ZEzPRFGkGT': 'USDJ',
    'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t': 'USDT',
    'TFptbWaARrWTX5Yvy3gNG5Lm8BmhPx82Bt': 'WBT',
    'TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7': 'WIN',
    'TGkxzkDKyMeq2T7edKnyjZoFypyzjkkssq': 'wstUSDT',
    'TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR': 'WTRX',
}


def symbol_for_address(address: str) -> Optional[str]:
    return TOKEN_ADDRESSES.get(address)


def hex_to_tron(address: str) -> str:
    """Convert a hex address to the more commonly used Txxxxxxxxx base58 style."""
    if address.startswith('0x'):
        address = '41' + address[2:]

    if len(address) % 2 == 1:
        address = '0' + address

    return base58.b58encode_check(bytes.fromhex(address)).decode()


def tron_to_hex(address: str) -> str:
    """Convert a Tron base58 address to a hexadecimal string."""
    return base58.b58decode_check(address).hex()


def coerce_to_hex(address: str) -> str:
    """If it looks like a base58 address convert, otherwise just return."""
    if is_tron_base58_address(address):
        return tron_to_hex(address)
    elif is_tron_hex_address(address):
        return address
    elif is_evm_style_address(address):
        return '41' + address[2:]
    else:
        raise InvalidAddressError(str(address))


def coerce_to_base58(address: str) -> str:
    """If it looks like a hex address convert, otherwise just return."""
    if is_tron_base58_address(address):
        return address
    elif is_tron_hex_address(address):
        return hex_to_tron(address)
    elif is_evm_style_address(address):
        return hex_to_tron('41' + address[2:])
    # TODO: this should at least do a regex match
    elif len(address) <= 40:
        return hex_to_tron('41' + address.zfill(40))
    else:
        raise InvalidAddressError(str(address))


def coerce_to_evm(address: str) -> str:
    """Coerce to the 0x format."""
    if is_evm_style_address(address):
        return address
    elif is_evm_style_address('0x' + address):
        return '0x' + address
    elif is_tron_hex_address(address):
        return '0x' + address[2:]
    elif is_tron_base58_address(address):
        return coerce_to_evm(coerce_to_hex(address))
    else:
        raise ValueError(f"Unknown address type '{address}'")


def is_tron_base58_address(address: str) -> bool:
    """Returns true if it looks like a Tron base58 address. (Trongrid often expects this T/F passed as 'visible' arg.)"""
    return bool(TRON_BASE58_ADDRESS_REGEX.match(str(address)))


def is_tron_hex_address(address: str) -> bool:
    """Returns True if it looks like a Tron hex address."""
    return bool(TRON_HEX_ADDRESS_REGEX.match(str(address)))


def is_evm_style_address(address: str) -> bool:
    """Returns True if it looks like 0x901u091284091109810313."""
    return bool(EVM_ADDRESS_REGEX.match(str(address)))


def address_of_symbol(symbol: str) -> Optional[str]:
    """Find address of a symbol."""
    # TODO: Ditch this unfortunate hack
    if symbol in ['APENFT', 'NFT']:
        symbol = 'NFT'

    try:
        return get_dict_key_by_value(TOKEN_ADDRESSES, symbol)
    except ValueError:
        logging.warning(f"No address found for '{symbol}'!")


def print_symbol_addresses() -> None:
    """List all symbols that can be referenced by string (--token) instead of address."""
    for symbol, address in TOKEN_ADDRESSES.items():
        txt = Text('').append(symbol, style='cyan').append('    ').append(address, style='magenta')
        console.print(txt)
