"""
this file is of no use - just practicing testing
"""
import sys
from pathlib import Path

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1])


# tests/test_main.py
from main import dummy_test

def test_dummy_basic_int():
    assert dummy_test(2) == 10

def test_dummy_zero():
    assert dummy_test(0) == 0

def test_dummy_float():
    assert dummy_test(1.2) == 6.0


