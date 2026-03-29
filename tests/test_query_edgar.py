"""Tests for scripts/query-edgar.py — SEC EDGAR / IAPD API queries."""
import importlib.util
import json
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import requests

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "query-edgar.py"
sys.path.insert(0, str(SCRIPT.parent))

_spec = importlib.util.spec_from_file_location("query_edgar", SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

search_firms = _mod.search_firms
get_adv_by_crd = _mod.get_adv_by_crd
IAPD_BASE = _mod.IAPD_BASE
EDGAR_BASE = _mod.EDGAR_BASE
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
    def test_valid_query_returns_results(self, mock_sleep, mock_requests, mock_edgar_search_response):
        """search_firms returns a list of hit dicts on success."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_search_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        results = search_firms("Granite Peak")
        assert isinstance(results, list)
        assert len(results) == 2
        assert results[0]["_source"]["entity_name"] == "Granite Peak Capital LLC"

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_empty_results(self, mock_sleep, mock_requests, mock_edgar_search_empty):
        """search_firms returns an empty list when no firms match."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_search_empty
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        results = search_firms("ZZZZZ_NoMatch_99999")
        assert results == []

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_search_uses_edgar_base_url(self, mock_sleep, mock_requests, mock_edgar_search_response):
        """search_firms should hit the SEC EDGAR search-index endpoint."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_search_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        search_firms("test")
        call_url = mock_requests.get.call_args[0][0]
        assert EDGAR_BASE in call_url
        assert "search-index" in call_url


# ---------------------------------------------------------------------------
# get_adv_by_crd
# ---------------------------------------------------------------------------

class TestGetAdvByCrd:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_valid_crd_returns_data(self, mock_sleep, mock_requests, mock_edgar_adv_response):
        """get_adv_by_crd returns the full JSON response for a valid CRD."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_adv_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        result = get_adv_by_crd("123456")
        assert "Hits" in result
        assert len(result["Hits"]["Results"]) == 1
        assert result["Hits"]["Results"][0]["Id"] == "123456"

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_uses_iapd_api_url(self, mock_sleep, mock_requests, mock_edgar_adv_response):
        """get_adv_by_crd should use the api.adviserinfo.sec.gov IAPD endpoint."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_adv_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        get_adv_by_crd("123456")
        call_url = mock_requests.get.call_args[0][0]
        assert "api.adviserinfo.sec.gov" in call_url
        assert "123456" in call_url


# ---------------------------------------------------------------------------
# Network error handling
# ---------------------------------------------------------------------------

class TestNetworkErrors:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_timeout_raises_request_exception(self, mock_sleep, mock_requests):
        """A network timeout should raise a requests exception."""
        mock_requests.get.side_effect = requests.exceptions.Timeout("Connection timed out")

        with pytest.raises(requests.exceptions.Timeout):
            get_adv_by_crd("999999")

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_connection_error(self, mock_sleep, mock_requests):
        """A connection error should raise a requests exception."""
        mock_requests.get.side_effect = requests.exceptions.ConnectionError("DNS failure")

        with pytest.raises(requests.exceptions.ConnectionError):
            search_firms("test")


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

class TestRateLimiting:
    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_sleep_called_before_request(self, mock_sleep, mock_requests, mock_edgar_search_response):
        """search_firms should call time.sleep for rate limiting before the request."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_search_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        search_firms("test")
        mock_sleep.assert_called_once_with(RATE_LIMIT_DELAY)

    @patch.object(_mod, "requests")
    @patch.object(_mod.time, "sleep")
    def test_adv_lookup_also_rate_limited(self, mock_sleep, mock_requests, mock_edgar_adv_response):
        """get_adv_by_crd should also respect the rate limit delay."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_edgar_adv_response
        mock_resp.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_resp

        get_adv_by_crd("123456")
        mock_sleep.assert_called_once_with(RATE_LIMIT_DELAY)
