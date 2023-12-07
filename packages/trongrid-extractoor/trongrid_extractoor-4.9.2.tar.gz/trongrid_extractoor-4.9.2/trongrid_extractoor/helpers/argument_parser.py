import sys
from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from os import environ
from pathlib import Path

from rich.logging import RichHandler

from trongrid_extractoor.config import Config, log
from trongrid_extractoor.helpers.address_helpers import address_of_symbol, is_tron_base58_address, print_symbol_addresses
from trongrid_extractoor.helpers.time_helpers import str_to_timestamp
from trongrid_extractoor.helpers.string_constants import PACKAGE_NAME, TRANSFER
from trongrid_extractoor.request_params import DEFAULT_MAX_RECORDS_PER_REQUEST


parser = ArgumentParser(
    description='Pull transactions for a given token. Either --token or --resume-csv must be provided. ',
    epilog='For a limited number of known symbols (USDT, USDD, etc.) you can use the symbol string instead ' \
           'of the on chain address.'
)

parser.add_argument('-c', '--contract-address',
                    help="contract address",
                    metavar='ADDRESS')

parser.add_argument('-t', '--token',
                    help="token symbol string like 'USDT' (only works for preconfigured tokens; for others use -c)",
                    metavar='SYMBOL')

parser.add_argument('-e', '--event-name',
                    help="name of the event to extract ('all' to get all events, defaults to 'Transfer')",
                    metavar='EVENT_NAME',
                    default=TRANSFER)

parser.add_argument('-s', '--since',
                    help='extract transactions up to and including this time (ISO 8601 Format)',
                    metavar='DATETIME')

parser.add_argument('-u', '--until',
                    help='extract transactions starting from this time (ISO 8601 Format)',
                    metavar='DATETIME')

parser.add_argument('-i', '--internal-txns', action='store_true',
                    help="for each event processed pull 0ut the internal txn events as their own data points")

parser.add_argument('-m', '--max-records-per-request',
                    help='maximum records per request',
                    metavar='MAX_RECORDS',
                    type=int,
                    default=DEFAULT_MAX_RECORDS_PER_REQUEST)

# TODO: this should accept an S3 URI.
parser.add_argument('-o', '--output-dir',
                    help='write transaction CSVs to a file in this directory',
                    metavar='OUTPUT_DIR')

parser.add_argument('-r', '--resume-from-csv',
                    help='resume extracting to a partially extracted CSV file',
                    metavar='CSV_FILE')

parser.add_argument('-tx', '--transactions', action='store_true',
                    help='pull transactions (not TRC20 transfers and not events)')

parser.add_argument('-l', '--list-symbols', action='store_true',
                    help='print a list of known symbols that can be used with the --token argument and exit')

parser.add_argument('-d', '--debug', action='store_true',
                    help='set LOG_LEVEL to DEBUG (can also be set with the LOG_LEVEL environment variable)')

parser.add_argument('--version', action='store_true',
                    help='print version information and exit')


def parse_args() -> Namespace:
    if '--version' in sys.argv:
        print(f"trongrid_extractoor {version(PACKAGE_NAME)}")
        sys.exit()

    args = parser.parse_args()
    setup_logging(args)
    args.output_dir = Path(args.output_dir or '')
    args.resume_from_csv = Path(args.resume_from_csv) if args.resume_from_csv else None

    if args.list_symbols:
        print_symbol_addresses()
        sys.exit()

    if (args.token and args.contract_address):
        log.error(f"Must specify only one of --token or --contract-address.")
        sys.exit(1)
    elif not (args.resume_from_csv or args.token or args.contract_address):
        log.error(f"Must provide either --resume-from-csv, --token, or --contract-address.")
        sys.exit(1)
    elif args.token:
        address = address_of_symbol(args.token)

        if address is None:
            log.error(f"Unknown token symbol: '{args.token}'")
            sys.exit(1)

        log.info(f"Using '{args.token}' address '{address}'...")
        args.contract_address = address

    if not is_tron_base58_address(args.contract_address):
        log.warning(f"'{args.contract_address}' doesn't look like a contract address but OK we'll try...")

    if args.since:
        since = str_to_timestamp(args.since)
        log.info(f"Requested records since '{args.since}' which parsed to {since}.")
        args.since = since

    if args.until:
        until = str_to_timestamp(args.until)
        log.info(f"Requested records until '{args.until}' which parsed to {until}.")
        args.until = until

    if args.event_name == 'None' or args.event_name == 'all':
        args.event_name = None

    Config.max_records_per_request = args.max_records_per_request
    log.debug(f"Processed arguments: {args}")
    return args


def setup_logging(args: Namespace) -> None:
    """Add rich text formatting to log. Only used when extractoor is called from the CLI."""
    log_level = 'DEBUG' if args.debug else environ.get('LOG_LEVEL', 'INFO')
    log.setLevel(log_level)
    rich_stream_handler = RichHandler(rich_tracebacks=True)
    rich_stream_handler.setLevel(log_level)
    log.addHandler(rich_stream_handler)
