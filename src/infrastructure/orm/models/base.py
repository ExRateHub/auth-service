import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass

metadata = sa.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class BaseModel(MappedAsDataclass, DeclarativeBase, kw_only=True):
    """Base model"""

    metadata = metadata


class TimestampedModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        server_default=sa.func.timezone("utc", sa.func.now()),
        kw_only=True,
        repr=False,
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        server_default=sa.func.timezone("utc", sa.func.now()),
        server_onupdate=sa.func.timezone("utc", sa.func.now()),
        kw_only=True,
        repr=False,
    )
