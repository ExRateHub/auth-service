from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass
class BaseSQLAlchemyRepository[Model, Entity]:
    session_factory: async_sessionmaker[AsyncSession]
    model_type: type[Model]
    entity_type: type[Entity]
    mapper: Retort

    async def add(self, data: Entity) -> Entity:
        model = self._from_entity(data)
        async with self.session_factory() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
        return self._to_entity(model)

    async def add_many(self, data: list[Entity]) -> list[Entity]:
        models = [self._from_entity(entity) for entity in data]
        async with self.session_factory() as session:
            session.add_all(models)
            await session.commit()
            for model in models:
                await session.refresh(model)
        return [self._to_entity(model) for model in models]

    async def get(self, **filters: Any) -> Entity | None:
        async with self.session_factory() as session:
            stmt = select(self.model_type).filter_by(**filters)
            result = await session.execute(stmt)
            model = result.scalars().first()
        return self._to_entity(model) if model else None

    async def get_many(self, **filters: Any) -> list[Entity]:
        async with self.session_factory() as session:
            stmt = select(self.model_type).filter_by(**filters)
            result = await session.execute(stmt)
            models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, filters: dict[str, Any], data: dict[str, Any]) -> int:
        async with self.session_factory() as session:
            stmt = update(self.model_type).filter_by(**filters).values(**data)
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount()

    async def delete(self, **filters: Any) -> int:
        async with self.session_factory() as session:
            stmt = delete(self.model_type).filter_by(**filters)
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount()

    async def exists(self, **filters: Any) -> bool:
        async with self.session_factory() as session:
            stmt = select(self.model_type).filter_by(**filters).exists()
            result = await session.execute(stmt)
        return result.scalar()

    async def count(self, **filters: Any) -> int:
        async with self.session_factory() as session:
            stmt = select(func.count()).select_from(self.model_type).filter_by(**filters)
            result = await session.execute(stmt)
        return result.scalar()

    def _to_entity(self, model: Model) -> Entity:
        """
        Convert ORM model to domain entity.
        """
        return self.mapper.load(model, self.entity_type)

    def _from_entity(self, entity: Entity) -> Model:
        """
        Convert domain entity to ORM model instance.
        """

        payload = self.mapper.dump(entity)
        return self.model_type(**payload)
