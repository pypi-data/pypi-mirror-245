# network = '' if network == MAINNET else f".{network}"
TRONGRID_BASE_URI = f"https://api.trongrid.io/"


def build_endpoint_url(endpoint: str) -> str:
    """Create a trongrid URI."""
    return f"{TRONGRID_BASE_URI}{endpoint}"
