import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.orm.models import TimestampedModel


class AuthTokenModel(TimestampedModel):
    __tablename__ = "auth_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    hashed_key: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        repr=False,
    )

    expired_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
    )
