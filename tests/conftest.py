"""Shared fixtures for AllocatorStack helper script tests."""
import json
from pathlib import Path

import pytest

# ── paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DDQS_DIR = PROJECT_ROOT / "samples" / "ddqs"
SAMPLE_DDQ_PDFS = sorted(SAMPLE_DDQS_DIR.glob("*.pdf"))


@pytest.fixture
def ddq_dir() -> Path:
    """Path to the samples/ddqs/ directory."""
    return SAMPLE_DDQS_DIR


@pytest.fixture
def sample_pdf_paths() -> list[Path]:
    """Sorted list of the three sample DDQ PDF paths."""
    return SAMPLE_DDQ_PDFS


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Temporary output directory for test artifacts."""
    out = tmp_path / "output"
    out.mkdir()
    return out


# ── Mock SEC / EDGAR API responses ────────────────────────────────────────────
@pytest.fixture
def mock_edgar_search_response() -> dict:
    """Mock response for SEC EDGAR search-index endpoint."""
    return {
        "hits": {
            "total": {"value": 2},
            "hits": [
                {
                    "_source": {
                        "entity_name": "Granite Peak Capital LLC",
                        "file_num": "801-12345",
                        "file_date": "2024-03-15",
                    }
                },
                {
                    "_source": {
                        "entity_name": "Granite Peak Investments",
                        "file_num": "801-67890",
                        "file_date": "2023-11-01",
                    }
                },
            ],
        }
    }


@pytest.fixture
def mock_edgar_search_empty() -> dict:
    """Mock empty search response."""
    return {"hits": {"total": {"value": 0}, "hits": []}}


@pytest.fixture
def mock_edgar_adv_response() -> dict:
    """Mock response for SEC IAPD ADV lookup by CRD."""
    return {
        "Hits": {
            "isPageLimitReached": False,
            "Results": [
                {
                    "Id": "123456",
                    "Names": ["Granite Peak Capital LLC"],
                    "Score": 100,
                    "OtherNames": [],
                    "CurrentEmployments": [],
                    "Scope": "IA",
                    "BranchOffices": [],
                }
            ],
        }
    }


# ── Mock FINRA BrokerCheck API responses ──────────────────────────────────────
@pytest.fixture
def mock_finra_search_response() -> dict:
    """Mock FINRA BrokerCheck firm search response."""
    return {
        "totalResults": 1,
        "results": {
            "firms": [
                {
                    "bc_scope": "IA",
                    "bc_firm_name": "Granite Peak Capital LLC",
                    "bc_source_id": "123456",
                    "score": 99.5,
                }
            ]
        },
    }


@pytest.fixture
def mock_finra_firm_response() -> dict:
    """Mock FINRA BrokerCheck firm detail response."""
    return {
        "firmName": "Granite Peak Capital LLC",
        "firmCrdNb": "123456",
        "registrationStatus": "APPROVED",
        "disclosureCount": 0,
    }


# ── Sample DDQ JSON for Excel generation ──────────────────────────────────────
@pytest.fixture
def single_manager_ddq_json(tmp_path: Path) -> Path:
    """Write a single-manager DDQ JSON file and return its path."""
    data = {
        "manager": "Granite Peak Capital",
        "answers": [
            {
                "question_text": "What is your AUM?",
                "answer": "$2.5B",
                "confidence": "HIGH",
            },
            {
                "question_text": "Investment strategy?",
                "answer": "Long/short equity",
                "confidence": "HIGH",
            },
            {
                "question_text": "Key person risk?",
                "answer": "PM manages 90% of assets",
                "confidence": "LOW",
            },
        ],
    }
    p = tmp_path / "single_manager.json"
    p.write_text(json.dumps(data))
    return p


@pytest.fixture
def multi_manager_ddq_json(tmp_path: Path) -> Path:
    """Write a multi-manager DDQ JSON file and return its path."""
    data = {
        "managers": [
            {
                "manager": "Granite Peak Capital",
                "answers": [
                    {"question_text": "What is your AUM?", "answer": "$2.5B", "confidence": "HIGH"},
                    {"question_text": "Strategy?", "answer": "Long/short equity", "confidence": "HIGH"},
                ],
            },
            {
                "manager": "Meridian Value Partners",
                "answers": [
                    {"question_text": "What is your AUM?", "answer": "$800M", "confidence": "HIGH"},
                    {"question_text": "Strategy?", "answer": "Value equity", "confidence": "LOW"},
                ],
            },
            {
                "manager": "Osprey Global Advisors",
                "answers": [
                    {"question_text": "What is your AUM?", "answer": "$5.1B", "confidence": "HIGH"},
                    {"question_text": "Strategy?", "answer": "Global macro", "confidence": "HIGH"},
                ],
            },
        ]
    }
    p = tmp_path / "multi_manager.json"
    p.write_text(json.dumps(data))
    return p
