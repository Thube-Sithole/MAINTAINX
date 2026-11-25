
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for the duration
    of an API request.

    The session is automatically closed when
    the request finishes.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
