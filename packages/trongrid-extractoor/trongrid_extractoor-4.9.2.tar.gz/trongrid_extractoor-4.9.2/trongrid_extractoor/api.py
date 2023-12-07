'''
API wrapper for TronGrid.
'''
from io import StringIO
from itertools import chain
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Type, Union

from pendulum import DateTime
from requests.exceptions import JSONDecodeError
from rich.pretty import pprint

from trongrid_extractoor.config import log
from trongrid_extractoor.exceptions import *
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58, coerce_to_hex, is_tron_base58_address
from trongrid_extractoor.helpers.csv_helper import output_csv_path
from trongrid_extractoor.helpers.rich_helpers import console
from trongrid_extractoor.helpers.string_constants import *
from trongrid_extractoor.models.function_arg import FunctionArg
from trongrid_extractoor.models.trc10_token import Trc10Token
from trongrid_extractoor.models.trc20_txn import Trc20Txn
from trongrid_extractoor.models.tron_account import TronAccount
from trongrid_extractoor.models.tron_contract import TronContract
from trongrid_extractoor.models.tron_event import TronEvent
from trongrid_extractoor.models.tron_txn import TronTxn
from trongrid_extractoor.output.file_output_writer import FileOutputWriter
from trongrid_extractoor.output.string_io_writer import StringIOWriter
from trongrid_extractoor.progress_tracker import ProgressTracker
from trongrid_extractoor.request_params import RequestParams
from trongrid_extractoor.response import Response


class Api:
    def __init__(self, network: str = MAINNET, api_key: str = '') -> None:
        network = '' if network == MAINNET else f".{network}"
        self.base_uri = f"https://api{network}.trongrid.io/"
        self.api_key = api_key

    def contract_events(
            self,
            progress_tracker: ProgressTracker,
            event_name: Optional[str] = None,
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None,
            order_by: str = ASC
        ) -> Iterator[List[TronEvent]]:
        """
        Iterate lists of events by contract address. This is the endpoint that actually works
        to get all transactions (unlike the '[CONTRACT_ADDRESS]/transactions' endpoint).

          - contract_address:  On-chain address of the token
          - event_name:        The event to poll for ('None' for all events)
          - since:             Start time to retrieve
          - until:             Start time to retrieve

        Test harness: https://developers.tron.network/v4.0/reference/events-by-contract-address
        """
        endpoint_url = self._build_endpoint_url(f"v1/contracts/{progress_tracker.address}/events")
        params = RequestParams(endpoint_url, since, until, order_by=order_by, event_name=event_name)
        params.max_timestamp = progress_tracker.earliest_timestamp_seen or params.max_timestamp
        yield self._extract_objects_from_response(endpoint_url, progress_tracker, params)

        # Pull the next record from the provided next URL until there's nothing left to pull
        while progress_tracker.last_response.is_continuable_response():
            yield self._extract_objects_from_response(progress_tracker.last_response.next_url(), progress_tracker)

            if progress_tracker.last_response.is_paging_complete():
                log.info(f"Paging complete for {params} so will end loop...")

        progress_tracker.log_state(progress_tracker.last_response)

    def get_all_contract_events(self, contract_address: str, event_name: Optional[str] = None) -> List[TronEvent]:
        """
        Returns list of all events of a given type (or all events if 'event_name' is None).
        Transfers will be returned as events. Use with caution on contracts with lots of event logs.
        """
        return [e for e in self.iterate_contract_events(contract_address, event_name)]

    def iterate_contract_events(
            self,
            contract_address: str,
            event_name: Optional[str] = None,
            order_by: str = ASC
        ) -> Iterator[TronEvent]:
        """Iterate over all events one event at a time instead of in groups like contract_events()."""
        progress_tracker = ProgressTracker.for_event_name(contract_address, event_name)

        for events in self.contract_events(progress_tracker, event_name, order_by=order_by):
            for event in events:
                yield event

    def write_contract_events(
            self,
            contract_address: Optional[str] = None,
            event_name: str = 'Transfer',
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None,
            output_to: Optional[Union[Path, StringIO]] = None,
            filename_suffix: Optional[str] = None,
            resume_from_csv: Optional[Path] = None
        ) -> Optional[Path]:
        """
        Get events by contract address and write to CSV or JSON format in either a file or StringIO object.

          - contract_address:  On-chain address of the token
          - event_name:        The event to poll for ('None' for all events)
          - since:             Start time to retrieve
          - until:             Start time to retrieve
          - output_to          Either a dir to write a file to or a StringIO object to receive file as string
          - filename_suffix:   Optional string to append to the filename
          - resume_from_csv:   Path to a CSV you want to resume writing
          - event_name:        Type of event to retrieve
        """
        # Resume from CSV if requested
        if resume_from_csv is None and not is_tron_base58_address(contract_address):
            raise ValueError(f"Must provide a valid contract address or a CSV to resume.")

        progress_tracker = ProgressTracker.for_event_name(contract_address, event_name)

        if isinstance(output_to, StringIO):
            writer = StringIOWriter(output_stream, progress_tracker.event_cls)
            output_path = None
        else:
            if resume_from_csv is not None:
                output_path = resume_from_csv
                progress_tracker.load_csv_progress(output_path)
            elif output_to is None or isinstance(output_to, (str, Path)):
                output_to = output_to or Path('')
                output_to = Path(output_to)

                if not output_to.is_dir():
                    raise ValueError(f"'{output_to}' is not a directory")

                output_path = output_csv_path(contract_address, output_to, filename_suffix)
            else:
                raise ValueError(f"output_to arg of wrong type: '{output_to}' ({type(output_to).__name__})")

            writer = FileOutputWriter(output_path, progress_tracker.event_cls)
            log.info(f"Output CSV: '{output_path}'")

        for events in self.contract_events(progress_tracker, event_name, since, until):
            writer.write_rows(events)

        return output_path

    def txn_events(self, tx_hash: str) -> List[TronEvent]:
        """Get TronEvents and Trc20Txns etc for a given 'tx_hash'."""
        endpoint_url = self._build_endpoint_url(f"v1/transactions/{tx_hash}/events")
        response = Response.get_response(url=endpoint_url).response

        if len(response[DATA]) == 0:
            pprint(response, expand_all=True, indent_guides=False)
            raise NoEventsFoundError(f"No events found for '{tx_hash}'!")

        return [
            Trc20Txn.from_json_obj(e) \
                  if e[EVENT_NAME] == TRANSFER \
                else TronEvent.from_json_obj(e)
            for e in response[DATA]
        ]

    def get_contract(self, address: str) -> Optional[TronContract]:
        """
        Get information about contract at a given address.
        Test harness: https://developers.tron.network/v4.0/reference/get-contract
        """
        log.info(f"Retrieving contract at '{address}'...")
        endpoint_url = self._build_endpoint_url('wallet/getcontract')
        params = {VALUE: coerce_to_base58(address), VISIBLE: True}
        response = Response.post_response(endpoint_url, params).response

        if len(response) > 0:
            return TronContract.from_response_dict(response)

    def get_account(self, address: str) -> Optional[TronAccount]:
        """
        Get information about an account. Things like self tags, balances, etc. Note that 'getaccount' endpoint
        only returns human readable tag information if you request info for base58 form of address with
        'visible'=True args. Test harness: https://developers.tron.network/v4.0/reference/walletgetaccount
        """
        log.debug(f"Retrieving account at '{address}'...")
        endpoint_url = self._build_endpoint_url('wallet/getaccount')
        params = {ADDRESS: coerce_to_base58(address), VISIBLE: True}

        try:
            response = Response.post_response(endpoint_url, params).response
        except JSONDecodeError:
            log.warning(f"Unparseable JSON reponse for address '{address}'!")
            return
        except Exception:
            console.print_exception()
            raise

        if len(response) != 0:
            return TronAccount.from_response_dict(response, self)

    def account_trc20_txns(self, address: str, contract_address: str) -> Iterator[Trc20Txn]:
        """
        Test harness: https://developers.tron.network/v4.0/reference/trc20-transaction-information-by-account-address
        example: curl --request GET
                      --url 'https://api.trongrid.io/v1/accounts/TCgTJWGePqEPufsQ6MUPPz3oA9H4XM1PRa/transactions/trc20?order_by=block_timestamp%2Casc&contract_address=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t' \
                      --header 'accept: application/json'
        """
        endpoint_url = self._build_endpoint_url(f"v1/accounts/{address}/transactions/trc20")
        params = RequestParams(endpoint_url, order_by=ASC, extra={CONTRACT_ADDRESS: contract_address})
        progress_tracker = ProgressTracker(address, Trc20Txn)
        progress_tracker.already_processed_uniq_ids = set()  # Yuck
        console.print(params)

        for txn in self._extract_objects_from_response(endpoint_url, progress_tracker, params):
            yield txn

        while progress_tracker.last_response.is_continuable_response():
            for txn in self._extract_objects_from_response(progress_tracker.last_response.next_url(), progress_tracker):
                yield txn

            if progress_tracker.last_response.is_paging_complete():
                log.info(f"Paging complete for {params} so will end loop...")

    def account_txns(
            self,
            address: str,
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None,
            already_seen_txn_ids: Optional[set] = None,
            search_internal: bool = False
        ) -> Iterator[TronTxn]:
        """
        Get actual transactions (not TRC20Txns) for an address. If 'search_internal' is True includes internal txns.
        Test harness: https://developers.tron.network/reference/get-transaction-info-by-account-address
        """
        if search_internal:
            raise NotImplementedError(f"Internal txns cannot be turned into TronTxn objects yet.")

        log.info(f"Retrieving txns for '{address}'...")
        endpoint_url = self._build_endpoint_url(f"v1/accounts/{address}/transactions")
        params = RequestParams(endpoint_url, since, until, order_by=ASC, extra={'search_internal': False})
        progress_tracker = ProgressTracker(address, TronTxn)
        progress_tracker.already_processed_uniq_ids = already_seen_txn_ids or set()  # Yuck
        console.print(params)

        for txn in self._extract_objects_from_response(endpoint_url, progress_tracker, params):
            yield txn

        # Pull the next record from the provided next URL until there's nothing left to pull
        while progress_tracker.last_response.is_continuable_response():
            for txn in self._extract_objects_from_response(progress_tracker.last_response.next_url(), progress_tracker):
                yield txn

            if progress_tracker.last_response.is_paging_complete():
                log.info(f"Paging complete for {params} so will end loop...")

    # TODO: move to TronContract class?
    # TODO: rename to call_contract_method()
    def read_contract_data(
            self,
            contract_address: str,
            owner_address: str,
            function_selector: str,
            function_params: List[str|int]
        ) -> List[str]:
        """
        Call a readonly method of a smart contract.
        Test harness: https://developers.tron.network/v4.0/reference/trigger-constant-contract
        """
        log.debug(f"Calling '{function_selector}' with ({function_params}) on '{contract_address}'...")
        endpoint_url = self._build_endpoint_url('wallet/triggerconstantcontract')

        params = {
            CONTRACT_ADDRESS: coerce_to_hex(contract_address),
            'owner_address': coerce_to_hex(owner_address),
            'function_selector': function_selector,
            'parameter': ''.join([FunctionArg.encode_parameter(p) for p in function_params])
        }

        results = Response.post_response(endpoint_url, params).response['constant_result']
        return [result.lstrip('0') for result in results]

    def list_trc10_tokens(self) -> Iterator[Trc10Token]:
        """Get a list of all TRC10 tokens on the Tron blockchain."""
        endpoint_url = self._build_endpoint_url('v1/assets')
        progress_tracker = ProgressTracker(None, Trc10Token)

        for token in self._extract_objects_from_response(endpoint_url, progress_tracker):
            yield token

        while progress_tracker.last_response.is_continuable_response():
            for token in self._extract_objects_from_response(progress_tracker.last_response.next_url(), progress_tracker):
                yield token

            if progress_tracker.last_response.is_paging_complete():
                log.info(f"Paging complete for TRC10 tokens so will end loop...")

    def _extract_objects_from_response(
            self,
            endpoint_url: str,
            progress_tracker: ProgressTracker,
            params: Optional[RequestParams] = None,
            internal_txns: bool = False
        ) -> List[Trc10Token|TronEvent|TronTxn]:
        """Extract events from API response."""
        try:
            request_params = params.request_params() if params is not None else {}
            progress_tracker.last_response = Response.get_response(endpoint_url, request_params)
            rows = progress_tracker.last_response.response[DATA]
            events = [progress_tracker.event_cls.from_json_obj(row) for row in rows]

            if internal_txns:
                events += [
                    progress_tracker.event_cls.from_json_obj(row)
                    for event in chain(*events)
                    for row in self.txn_events(event.transaction_id)
                ]

            return progress_tracker.remove_already_processed_txns(events)
        except Exception:
            console.print_exception()
            raise

    def _build_endpoint_url(self, url_path: str) -> str:
        return f"{self.base_uri}{url_path}"
