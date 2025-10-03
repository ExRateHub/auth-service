import abc
import typing


class BaseCommand(abc.ABC):
    """Base command"""


class BaseUseCase(abc.ABC):

    @abc.abstractmethod
    async def execute(self, command: BaseCommand) -> typing.Coroutine[typing.Any, typing.Any, typing.Any]:
        ...
    