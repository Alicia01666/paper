from database.models import Base
from sqlalchemy.orm import Mapped, mapped_column


class Context(Base):
    __tablename__ = "contexts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column()
    label: Mapped[str] = mapped_column()
    context: Mapped[str] = mapped_column()
