"""
Crypto module unit tests.
"""
import pytest
from big_utils.utils.crypto import generate_strong_encryption_key


@pytest.mark.parametrize('key_size', [8, 20, 20000, 1000])
def test_generate_strong_encryption_key(key_size):
    assert generate_strong_encryption_key(key_size)


@pytest.mark.parametrize('key_size', [-1, -20, 0, 1, 7])
def test_generate_strong_encryption_key_fail(key_size):
    with pytest.raises(ValueError):
        generate_strong_encryption_key(key_size)
