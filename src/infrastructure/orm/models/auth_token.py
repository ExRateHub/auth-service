import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.orm.models import TimestampedModel


class AuthTokenModel(TimestampedModel):
    __tablename__ = "auth_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=sa.text("gen_random_uuid()"),
    )

    hashed_key: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        repr=False,
    )

    expired_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime,
        nullable=True,
    )
