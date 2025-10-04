from dataclasses import dataclass

import sqlalchemy as sa

from domain.entities.user import User
from domain.value_objects.username import Username
from infrastructure.orm.models import UserModel
from infrastructure.persistence.repository.base import BaseSQLAlchemyRepository
from infrastructure.persistence.mappers.user import UserMapper


@dataclass
class UserRepository(BaseSQLAlchemyRepository):
    mapper: UserMapper

    async def add(self, user: User) -> User:
        async with self.session_factory() as session:
            user_model = self.mapper.to_model(user)
            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)
            user = self.mapper.to_entity(user_model)
        return user

    async def  get_by_username(self, username: Username) -> User | None:
        async with self.session_factory() as session:
            stmt = sa.select(UserModel).where(UserModel.username == username.as_generic_type())
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            if user_model is None:
                return None
            user = self.mapper.to_entity(user_model)
        return user

