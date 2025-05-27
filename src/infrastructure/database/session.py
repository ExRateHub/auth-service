from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession


def get_async_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create and return a SQLAlchemy async session factory.

    This factory is bound to the provided async engine and configured
    so that sessions do not expire objects on commit.

    :param engine: An AsyncEngine instance to bind new sessions to.
    :return: An async_sessionmaker[AsyncSession] which can be used to generate AsyncSession objects.
    """
    async_factory = async_sessionmaker(engine, expire_on_commit=True)
    return async_factory