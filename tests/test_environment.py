"""
Verification tests for AgriSense AI development environment.
Confirms Python version and required package imports.
"""

import sys
import pytest


def test_python_version():
    """Verify runtime Python meets minimum requirements (>= 3.10)."""
    major, minor = sys.version_info.major, sys.version_info.minor
    assert (major, minor) >= (3, 10), f"Expected Python >= 3.10, but got {major}.{minor}"


def test_core_ml_imports():
    """Verify that all core ML & data processing libraries import without errors."""
    import pandas as pd
    import numpy as np
    import sklearn
    import joblib

    assert pd is not None
    assert np is not None
    assert sklearn is not None
    assert joblib is not None


def test_visualization_imports():
    """Verify matplotlib and seaborn imports."""
    import matplotlib
    import seaborn as sns

    assert matplotlib is not None
    assert sns is not None


def test_backend_framework_imports():
    """Verify FastAPI, Uvicorn, Pydantic, and SQLAlchemy imports."""
    import fastapi
    import uvicorn
    import pydantic
    import sqlalchemy

    assert fastapi is not None
    assert uvicorn is not None
    assert pydantic is not None
    assert sqlalchemy is not None


def test_testing_imports():
    """Verify HTTPX testing client is available."""
    import httpx

    assert httpx is not None
