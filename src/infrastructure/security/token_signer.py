from dataclasses import dataclass

import jwt

from domain.value_objects.jwt_token import JwtPayload, JwtToken


@dataclass
class TokenSigner:
    secret: str
    algorithm: str

    def sign(self, payload: JwtPayload) -> JwtToken:
        encoded_jwt_token = jwt.encode(payload.to_dict(), self.secret, algorithm=self.algorithm)
        return JwtToken(encoded_jwt_token)

    def verify(self, token: JwtToken) -> bool:
        try:
            jwt.decode(token.value, self.secret, algorithms=[self.algorithm])
            return True
        except jwt.PyJWTError:
            return False

    def decode(self, token: JwtToken) -> JwtPayload:
        payload_data = jwt.decode(token.value, self.secret, algorithms=[self.algorithm])
        return JwtPayload.from_dict(payload_data)
