from typing import Any, Protocol


class RepositoryProtocol[Entity](Protocol):
    """
    Generic repository interface for CRUD and query operations over an Entity type.

    :param Entity: The domain model or DTO type that the repository manages.
    """

    async def add(self, data: Entity) -> Entity:
        """
        Persist a new entity.

        :param data: An instance of Entity to be saved.
        :return: The saved Entity, potentially enriched (e.g., with generated ID).
        """
        ...

    async def add_many(self, data: list[Entity]) -> list[Entity]:
        """
        Persist multiple entities in a single batch.

        :param data: A list of Entity instances to be saved.
        :return: A list of saved Entities, each potentially enriched.
        """
        ...

    async def get(self, **filters: Any) -> None | Entity:
        """
        Retrieve a single entity matching the given criteria.

        :param filters: Field-based lookup parameters (e.g., id=..., email=...).
        :return: The matching Entity, or None if not found.
        """
        ...

    async def get_many(self, **filters: Any) -> list[Entity]:
        """
        Retrieve all entities that match the given criteria.

        :param filters: Field-based lookup parameters.
        :return: A list of matching Entities (possibly empty).
        """
        ...

    async def update(self, filters: dict[str, Any], data: dict[str, Any]) -> int:
        """
        Update one or more entities.

        :param filters: Criteria to select which records to update.
        :param data:    Field values to set on the selected records.
        :return: The number of rows updated.
        """
        ...

    async def delete(self, **filters: Any) -> int:
        """
        Delete entities that match the given criteria.

        :param filters: Field-based lookup parameters.
        :return: The number of rows deleted.
        """
        ...

    async def exists(self, **filters: Any) -> bool:
        """
        Check whether at least one entity matches the criteria.

        :param filters: Field-based lookup parameters.
        :return: True if any matching entity exists, False otherwise.
        """
        ...

    async def count(self, **filters: Any) -> int:
        """
        Count how many entities match the given criteria.

        :param filters: Field-based lookup parameters.
        :return: The total count of matching entities.
        """
        ...
