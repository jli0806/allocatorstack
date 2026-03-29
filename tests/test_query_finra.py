"""Tests for scripts/query-finra.py — FINRA BrokerCheck API queries."""
import importlib.util
import json
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import requests

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "query-finra.py"
sys.path.insert(0, str(SCRIPT.parent))

_spec = importlib.util.spec_from_file_location("query_finra", SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

search_firms = _mod.search_firms
get_firm_by_crd = _mod.get_firm_by_crd
BROKERCHECK_BASE = _mod.BROKERCHECK_BASE
RATE_LIMIT_DELAY = _mod.RATE_LIMIT_DELAY


def _run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# search_firms
# ---------------------------------------------------------------------------

class TestSearchFirms:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_valid_query_returns_results(self, mock_sleep, mock_requests, mock_finra_search_response):
        """search_firms returns FINRA JSON with firm results."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_finra_search_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        result = search_firms("Granite Peak")
        assert result["totalResults"] == 1
        assert result["results"]["firms"][0]["bc_firm_name"] == "Granite Peak Capital LLC"

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_search_uses_brokercheck_url(self, mock_sleep, mock_requests, mock_finra_search_response):
        """search_firms should hit the FINRA BrokerCheck API."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_finra_search_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        search_firms("test")
        call_url = mock_requests.get.call_args[0][0]
        assert "brokercheck.finra.org" in call_url

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_empty_query_still_calls_api(self, mock_sleep, mock_requests):
        """Even an empty-ish query should make the API call."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"totalResults": 0, "results": {"firms": []}}
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        result = search_firms("")
        assert result["totalResults"] == 0
        mock_requests.get.assert_called_once()


# ---------------------------------------------------------------------------
# get_firm_by_crd
# ---------------------------------------------------------------------------

class TestGetFirmByCrd:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_valid_crd_returns_data(self, mock_sleep, mock_requests, mock_finra_firm_response):
        """get_firm_by_crd returns firm detail JSON for a valid CRD."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_finra_firm_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        result = get_firm_by_crd("123456")
        assert result["firmName"] == "Granite Peak Capital LLC"
        assert result["firmCrdNb"] == "123456"
        assert result["registrationStatus"] == "APPROVED"

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_crd_url_contains_crd_number(self, mock_sleep, mock_requests, mock_finra_firm_response):
        """The URL should contain the CRD number in the path."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_finra_firm_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        get_firm_by_crd("999888")
        call_url = mock_requests.get.call_args[0][0]
        assert "999888" in call_url
        assert "firm/summary" in call_url


# ---------------------------------------------------------------------------
# Network error handling
# ---------------------------------------------------------------------------

class TestNetworkErrors:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_connection_error_raises(self, mock_sleep, mock_requests):
        """A connection error should propagate as a requests exception."""
        mock_requests.get.side_effect = requests.exceptions.ConnectionError("No route to host")

        with pytest.raises(requests.exceptions.ConnectionError):
            search_firms("test")

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_timeout_raises(self, mock_sleep, mock_requests):
        """A timeout should propagate as a requests exception."""
        mock_requests.get.side_effect = requests.exceptions.Timeout("Read timed out")

        with pytest.raises(requests.exceptions.Timeout):
            get_firm_by_crd("123456")

    def test_cli_network_error_produces_error_json(self, output_dir):
        """The CLI should catch network errors and write error JSON."""
        out_file = output_dir / "error.json"
        with patch.object(_mod, "requests") as mock_requests:
            mock_requests.get.side_effect = requests.exceptions.ConnectionError("fail")
            mock_requests.RequestException = requests.RequestException
            result = _run_script("--crd", "123456", "--output", str(out_file))

        assert result.returncode != 0
        assert out_file.exists()
        data = json.loads(out_file.read_text())
        assert "error" in data
        assert data["source"] == "finra_brokercheck"

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_http_error_raises(self, mock_sleep, mock_requests):
        """An HTTP error (e.g., 404) should propagate via raise_for_status."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_requests.get.return_value = mock_resp

        with pytest.raises(requests.exceptions.HTTPError):
            get_firm_by_crd("000000")


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

class TestRateLimiting:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_search_rate_limited(self, mock_sleep, mock_requests, mock_finra_search_response):
        """search_firms should sleep before making the request."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_finra_search_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        search_firms("test")
        mock_sleep.assert_called_once_with(RATE_LIMIT_DELAY)

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_crd_lookup_rate_limited(self, mock_sleep, mock_requests, mock_finra_firm_response):
        """get_firm_by_crd should also respect rate limiting."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_finra_firm_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        get_firm_by_crd("123456")
        mock_sleep.assert_called_once_with(RATE_LIMIT_DELAY)
