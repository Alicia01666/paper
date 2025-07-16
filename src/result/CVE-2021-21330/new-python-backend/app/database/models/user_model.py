from database.models import Base
from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    conditions: Mapped[list[str]] = mapped_column(ARRAY(String))
