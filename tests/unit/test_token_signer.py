import datetime

import pytest

from application.ports.token_signer import TokenSignerProtocol
from core.config import Settings
from domain.value_objects.jwt_token import JwtPayload, JwtToken
from infrastructure.security.token_signer import TokenSigner


@pytest.fixture(scope="session")
def token_signer(settings: Settings) -> TokenSignerProtocol:
    return TokenSigner(secret=settings.signer.secret, algorithm=settings.signer.algorithm)


@pytest.fixture
def valid_payload() -> JwtPayload:
    return JwtPayload(
        sub="user123",
        scope="access",
        iat=datetime.datetime.now(datetime.UTC),
        exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
    )


@pytest.fixture
def valid_payload_2() -> JwtPayload:
    return JwtPayload(
        sub="user12",
        scope="admin",
        iat=datetime.datetime.now(datetime.UTC),
        exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
    )


class TestTokenSigner:
    def test_sign_returns_jwt_token(self, token_signer: TokenSignerProtocol, valid_payload: JwtPayload) -> None:
        token = token_signer.sign(valid_payload)
        assert isinstance(token, JwtToken)
        assert isinstance(token.value, str)
        assert len(token.value) > 0

    def test_verify_valid_token(self, token_signer: TokenSignerProtocol, valid_payload: JwtPayload) -> None:
        token = token_signer.sign(valid_payload)
        assert token_signer.verify(token) is True

    def test_verify_invalid_token(
        self, token_signer: TokenSignerProtocol, valid_payload: JwtPayload, valid_payload_2: JwtPayload
    ):
        token1 = token_signer.sign(valid_payload)
        token2 = token_signer.sign(valid_payload_2)
        token3 = JwtToken(
            f"{token1.header.as_generic_type()}.{token1.payload.as_generic_type()}.{token2.signature.as_generic_type()}"
        )
        assert token_signer.verify(token3) is False

    def test_decode_returns_payload(self, token_signer: TokenSignerProtocol, valid_payload: JwtPayload) -> None:
        token = token_signer.sign(valid_payload)
        decoded_payload = token_signer.decode(token)
        assert isinstance(decoded_payload, JwtPayload)
        assert decoded_payload.sub == valid_payload.sub
        assert decoded_payload.scope == valid_payload.scope

        assert abs((decoded_payload.iat - valid_payload.iat).total_seconds()) < 1
        assert abs((decoded_payload.exp - valid_payload.exp).total_seconds()) < 1
