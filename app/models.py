"""

    our application is going to need a commit entity with attributes: repo_name, date,

"""

from sqlalchemy import Column, Integer, String, DateTime # type: ignore
from sqlalchemy.orm import Mapped, mapped_column # type: ignore
from app.database import Base

class Commit(Base):
    __tablename__ = "commits"

    id: Mapped[int] = mapped_column(primary_key=True)
    username = Column(String, nullable = False)
    repo_name = Column(String, nullable = False)
    committed_at = Column(DateTime(timezone=True), nullable = False)
    sha = Column(String, unique=True)