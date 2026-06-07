import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.models.problem import Problem


class Relationship(Base):
    __tablename__ = "relationships"

    source_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True
    )
    relationship_type: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    strength: Mapped[float] = mapped_column(Float, default=1.0)

    source_node: Mapped["Problem"] = relationship(
        "Problem", foreign_keys=[source_id], back_populates="outgoing_relationships"
    )
    target_node: Mapped["Problem"] = relationship(
        "Problem", foreign_keys=[target_id], back_populates="incoming_relationships"
    )
