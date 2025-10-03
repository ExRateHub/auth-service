import abc


class BaseMapper[TEntity, TModel](abc.ABC):
    @abc.abstractmethod
    def to_entity(self, data: TModel) -> TEntity: ...

    @abc.abstractmethod
    def to_model(self, data: TEntity) -> TModel: ...