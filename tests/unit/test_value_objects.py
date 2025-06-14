import datetime

import pytest
import base64

from domain.errors import InvalidEmail, InvalidHashedSecret, InvalidBase64Encoding, InvalidJWTToken, InvalidTTL
from domain.value_objects.base64_strng import Base64String
from domain.value_objects.email import Email
from domain.value_objects.hashed_secret import HashedSecret
from domain.value_objects.jwt_token import JwtToken
from domain.value_objects.ttl import TTL


class TestEmail:
    @pytest.mark.parametrize(
        "email", ["example@domain.com", "example.example@domain.com", "example+example@domain.com"]
    )
    def test_valid_emails(self, email: str) -> None:
        assert email == Email(email).as_generic_type()

    @pytest.mark.parametrize("email", ["example@domain", "@domain.com", "example@", "example"])
    def test_invalid_emails(self, email: str) -> None:
        with pytest.raises(InvalidEmail):
            Email(email)


class TestHashedPassword:
    @pytest.mark.parametrize(
        "hashed_secret",
        [
            "$<algorithm>$<options>$<salt>$<hash>",
            "$<algorithm>$<options-1>$<options-2>$<salt>$<hash>",
        ],
    )
    def test_valid_mfc(self, hashed_secret: str) -> None:
        _, algorithm, *options, salt, password_hash = hashed_secret.split("$")
        assert hashed_secret == HashedSecret(hashed_secret).as_generic_type()
        assert algorithm == HashedSecret(hashed_secret).algorithm
        assert "$".join(options) == HashedSecret(hashed_secret).options
        assert salt == HashedSecret(hashed_secret).salt
        assert password_hash == HashedSecret(hashed_secret).hash

    @pytest.mark.parametrize("hashed_secret", ["$<algorithm>$<options>$<salt>"])
    def test_invalid_mfc(self, hashed_secret: str) -> None:
        with pytest.raises(InvalidHashedSecret):
            HashedSecret(hashed_secret)


class TestBase64String:
    @pytest.mark.parametrize(
        "plain_text",
        ["Hello", "Тест", "1234567890abcdef", "\x01\x02\x03\x04\x05", "{'test': 'value'}"],
    )
    def test_valid_base64_string(self, plain_text: str) -> None:
        encoded = base64.urlsafe_b64encode(plain_text.encode("utf-8")).decode("ascii")
        print(plain_text.encode("utf-8"), encoded)
        b64 = Base64String(encoded)
        assert b64.as_generic_type() == encoded
        assert b64.decode() == plain_text

    @pytest.mark.parametrize(
        "invalid_str",
        [
            "",
            None,
            123,
            "💥💥💥",
            "abcde===",
            "not_base64!",
        ],
    )
    def test_invalid_base64(self, invalid_str) -> None:
        with pytest.raises(InvalidBase64Encoding):
            Base64String(invalid_str)

    @pytest.mark.parametrize(
        "non_ascii_string",
        [
            "тест",
            "测试",
            "テスト",
            "δοκιμή",
            "💥💥💥",
            "æøå",
            "\u202e",
        ],
    )
    def test_non_ascii_characters(self, non_ascii_string):
        with pytest.raises(InvalidBase64Encoding, match="non-ASCII"):
            Base64String(non_ascii_string)

    @pytest.mark.parametrize(
        "broken_base64",
        [
            base64.urlsafe_b64encode("тест".encode("utf-16")),
            base64.urlsafe_b64encode("text".encode("utf-32")),
        ],
    )
    def test_decode_invalid_encoding(self, broken_base64):
        with pytest.raises(InvalidBase64Encoding):
            Base64String(broken_base64)


class TestJWTToken:
    @pytest.mark.parametrize(
        "valid_token",
        [
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lcyI6InBheWxvYWQyIn0.Uc-I7hZ7dx_I3UPnBbLajIxzJCN28RJpSblWBqNp5ec",
        ],
    )
    def test_valid_token(self, valid_token):
        JwtToken(valid_token)

    @pytest.mark.parametrize(
        "invalid_token",
        [
            "",
            "abc.def",
            "abc.def.ghi.jkl",
            "abc.def.",
            "abc..def",
        ],
    )
    def test_invalid_part_count(self, invalid_token):
        with pytest.raises(InvalidJWTToken):
            JwtToken(invalid_token)

    @pytest.mark.parametrize(
        "bad_header",
        [
            "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVyJ9",  # typ not JWT
            "eyJ0eXAiOiAiSldUIn0",  # does not contain alg
            "fQ",  # not valid json
            "bm90LWpzb24",
        ],
    )
    def test_invalid_header_json(self, bad_header):
        token_str = f"{bad_header}.eyJzdWIiOiJkYXRhIn0.uy8y_jlh7kgIrS_K-uxeGTZJGEuxXCzQeamEkpM32dc"
        with pytest.raises(InvalidJWTToken):
            JwtToken(token_str)

    @pytest.mark.parametrize("bad_payload", ["fQ", "bm90LWpzb24", "a2pzbGthb2w7c2Rqb2w7"])
    def test_invalid_payload_json(self, bad_payload):
        token_str = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{bad_payload}.uy8y_jlh7kgIrS_K-uxeGTZJGEuxXCzQeamEkpM32dc"
        with pytest.raises(InvalidJWTToken):
            JwtToken(token_str)

    @pytest.mark.parametrize(
        "bad_signature",
        [
            "тест",
            "测试",
            "テスト",
            "δοκιμή",
            "💥💥💥",
            "æøå",
            "\u202e",
            "",
            "💥💥💥",
            "abcde===",
            "not_base64!",
        ],
    )
    def test_invalid_signature(self, bad_signature):
        token_str = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYXRhIn0.{bad_signature}"
        with pytest.raises(InvalidJWTToken):
            print(token_str)
            JwtToken(token_str)


class TestTTL:
    @pytest.mark.parametrize(
        "valid_timedelta",
        [
            datetime.timedelta(seconds=1),
            datetime.timedelta(hours=100),
            datetime.timedelta(days=29192038),
        ],
    )
    def test_valid_timedelta(self, valid_timedelta):
        TTL(valid_timedelta)

    @pytest.mark.parametrize(
        "invalid_timedelta",
        [
            datetime.timedelta(seconds=-1),
            datetime.timedelta(hours=-100),
            datetime.timedelta(days=-29192038),
        ],
    )
    def test_valid_timedelta(self, invalid_timedelta):
        with pytest.raises(InvalidTTL):
            TTL(invalid_timedelta)

    @pytest.mark.parametrize(
        "valid_seconds",
        [1, 100, 202024030],
    )
    def test_valid_ttl_from_seconds(self, valid_seconds):
        TTL.from_seconds(valid_seconds)

    @pytest.mark.parametrize(
        "invalid_seconds",
        [-1, -100, -202024030, 0],
    )
    def test_invalid_ttl_drom_seconds(self, invalid_seconds):
        with pytest.raises(InvalidTTL):
            TTL.from_seconds(invalid_seconds)
