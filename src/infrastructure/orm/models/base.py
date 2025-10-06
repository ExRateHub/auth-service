import datetime
import uuid

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
    __abstract__ = True

    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=sa.text("gen_random_uuid()"),
        kw_only=True,
    )


class TimestampedModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.timezone("utc", sa.func.now()),
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        kw_only=True,
        repr=False,
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.timezone("utc", sa.func.now()),
        server_onupdate=sa.func.timezone("utc", sa.func.now()),
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        kw_only=True,
        repr=False,
    )
