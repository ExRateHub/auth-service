from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, CITEXT
import uuid
from base import TimestampedModel
from core.constants import COLLATION_CI_TEXT_NAME


class UserModel(TimestampedModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=sa.text("uuid_generate_v4()"),
    )

    email: Mapped[str] = mapped_column(
        sa.Text(collation=COLLATION_CI_TEXT_NAME),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=False, server_default=sa.text("false")
    )
