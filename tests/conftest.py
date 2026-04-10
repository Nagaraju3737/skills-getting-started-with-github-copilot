import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import app as app_module


@pytest.fixture
def client():
    """Provide a FastAPI test client."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity data before each test for isolation."""
    original_activities = copy.deepcopy(app_module.activities)

    yield

    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
