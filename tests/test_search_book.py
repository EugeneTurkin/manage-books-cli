from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from books import main 
from src.exceptions import BookDoesNotExistException
from tests.fixtures.fixtures import test_book, test_del_prompt, test_storage_path
from src.models import Book
