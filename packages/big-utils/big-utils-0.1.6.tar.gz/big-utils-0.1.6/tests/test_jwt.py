"""
JWT utilities unit tests.
"""
import datetime
import jwt
import pytest

from big_utils.utils.jwt import encode_token, decode_token
from .conftest import random_string

CORRECT_JWT_ISSUER = 'https://big-ideas.bitsinglass.com/iss'
CORRECT_JWT_AUDIENCE = 'https://big-ideas.bitsinglass.com/aud'
WRONG_JWT_ISSUER = 'https://big-ideas.bitsinglass.com/bad_iss'
WRONG_JWT_AUDIENCE = 'https://big-ideas.bitsinglass.com/bad_aud'
DEFAULT_ALG = 'HS256'

# convenient short form of `random_string`
rs = random_string


@pytest.mark.parametrize('secret_key, token_type, data', [
    (rs(32), 'test', {'field1': rs(10), 'field2': rs(99), 'field3': rs(2)}),
    (rs(32), 'test', {'field1': rs(10)}),
    (rs(32), 'test', {'field1': rs(10), 'field2': rs(99)}),
    (rs(32), 'test', {'field1': rs(10), 'field2': rs(99), 'field3': rs(2)}),
])
def test_encode_decode_token1(secret_key, token_type, data):
    token = encode_token(secret_key, token_type, **data)
    decoded_data = decode_token(secret_key, token)
    assert 'exp' in decoded_data
    assert 'nbf' in decoded_data
    assert 'iss' in decoded_data
    assert 'iat' in decoded_data
    assert decoded_data['type'] == token_type

    for key in data.keys():
        assert decoded_data.get(key) == data[key]


def test_encode_decode_token2():
    secret_key = rs(10)
    token = encode_token(secret_key, token_type='test', field1='f1', field2='f2', field3='f3')
    decoded_data = decode_token(secret_key, token)
    assert 'exp' in decoded_data
    assert 'nbf' in decoded_data
    assert 'iss' in decoded_data
    assert 'iat' in decoded_data
    assert decoded_data['type'] == 'test'
    assert decoded_data['field1'] == 'f1'
    assert decoded_data['field2'] == 'f2'
    assert decoded_data['field3'] == 'f3'


def test_encode_decode_token_no_exp():
    now = datetime.datetime.utcnow()
    test_field = rs(32)
    secret_key = rs(32)
    payload = {
        'nbf': now,
        'iat': now,
        'iss': CORRECT_JWT_ISSUER,
        'aud': CORRECT_JWT_AUDIENCE,
        'type': 'test',
        'test_field': test_field
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.MissingRequiredClaimError):
        decode_token(secret_key, token)


def test_encode_decode_token_no_nbf():
    now = datetime.datetime.utcnow()
    test_field = rs(32)
    secret_key = rs(32)
    payload = {
        'exp': now + datetime.timedelta(seconds=5 * 60),
        'iat': now,
        'iss': CORRECT_JWT_ISSUER,
        'aud': CORRECT_JWT_AUDIENCE,
        'type': 'test',
        'test_field': test_field
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.MissingRequiredClaimError):
        decode_token(secret_key, token)


def test_encode_decode_token_no_iat():
    now = datetime.datetime.utcnow()
    test_field = rs(32)
    secret_key = rs(32)
    payload = {
        'exp': now + datetime.timedelta(seconds=5 * 60),
        'nbf': now,
        'iss': CORRECT_JWT_ISSUER,
        'aud': CORRECT_JWT_AUDIENCE,
        'type': 'test',
        'test_field': test_field
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.MissingRequiredClaimError):
        decode_token(secret_key, token)


def test_encode_decode_token_no_iss():
    now = datetime.datetime.utcnow()
    test_field = rs(32)
    secret_key = rs(32)
    payload = {
        'exp': now + datetime.timedelta(seconds=5*60),
        'nbf': now,
        'iat': now,
        'aud': CORRECT_JWT_AUDIENCE,
        'type': 'test',
        'test_field': test_field
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.MissingRequiredClaimError):
        decode_token(secret_key, token)


def test_encode_decode_token_no_aud():
    now = datetime.datetime.utcnow()
    test_field = rs(32)
    secret_key = rs(32)
    payload = {
        'exp': now + datetime.timedelta(seconds=5*60),
        'nbf': now,
        'iat': now,
        'iss': CORRECT_JWT_ISSUER,
        'type': 'test',
        'test_field': test_field
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.MissingRequiredClaimError):
        decode_token(secret_key, token)


def test_encode_decode_token_wrong_iss():
    now = datetime.datetime.utcnow()
    test_field = rs(32)
    secret_key = rs(32)
    payload = {
        'exp': now + datetime.timedelta(seconds=5*60),
        'nbf': now,
        'iat': now,
        'iss': WRONG_JWT_ISSUER,
        'aud': CORRECT_JWT_AUDIENCE,
        'type': 'test',
        'test_field': test_field
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.InvalidIssuerError):
        decode_token(secret_key, token)


def test_encode_decode_token_wrong_aud():
    now = datetime.datetime.utcnow()
    test_field_1 = rs(48)
    test_field_2 = rs(48)
    secret_key = rs(48)
    payload = {
        'exp': now + datetime.timedelta(seconds=5 * 60),
        'nbf': now,
        'iat': now,
        'iss': CORRECT_JWT_ISSUER,
        'aud': WRONG_JWT_AUDIENCE,
        'type': 'test',
        'test_field_1': test_field_1,
        'test_field_2': test_field_2
    }
    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALG)
    with pytest.raises(jwt.InvalidAudienceError):
        decode_token(secret_key, token)
