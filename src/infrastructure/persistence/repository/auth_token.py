import dataclasses

import sqlalchemy as sa

from domain.entities.auth_token import AuthToken
from domain.value_objects.hashed_secret import HashedSecret
from infrastructure.orm.models import AuthTokenModel
from infrastructure.orm.repository import BaseSQLAlchemyRepository
from infrastructure.persistence.mappers.auth_token import AuthTokenMapper


@dataclasses.dataclass
class AuthTokenRepository(BaseSQLAlchemyRepository):
    mapper: AuthTokenMapper

    async def get_by_hashed_key(self, hashed_key: HashedSecret) -> AuthToken | None:
        async with self.session_factory() as session:
            stmt = sa.select(AuthTokenModel).where(
                AuthTokenModel.hashed_key == hashed_key.as_generic_type()
            )
            result = await session.scalars(stmt)
            auth_token = result.first()

        return self.mapper.to_entity(auth_token) if auth_token else None

    async def add(self, token: AuthToken) -> AuthToken:
        async with self.session_factory() as session:
            auth_token_model = self.mapper.to_model(token)
            session.add(auth_token_model)
            await session.commit()
            await session.refresh(auth_token_model)
        return self.mapper.to_entity(auth_token_model)

    async def delete(self, token: AuthToken) -> None:
        async with self.session_factory() as session:
            stmt = sa.delete(AuthTokenModel).where(AuthTokenModel.id == token.id)
            await session.execute(stmt)
            await session.commit()
