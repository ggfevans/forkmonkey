"""
Shared pytest fixtures for vscode-pets-integration tests
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def sample_rgba_image():
    """Create a sample RGBA image for testing."""
    return Image.new('RGBA', (100, 100), (255, 0, 0, 200))