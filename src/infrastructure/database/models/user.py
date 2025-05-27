import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.constants import COLLATION_CI_TEXT_NAME
from infrastructure.database.models import TimestampedModel


class UserModel(TimestampedModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=sa.text("gen_random_uuid()"),
    )

    email: Mapped[str] = mapped_column(
        sa.Text(collation=COLLATION_CI_TEXT_NAME),
        unique=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=False, server_default=sa.text("false")
    )
