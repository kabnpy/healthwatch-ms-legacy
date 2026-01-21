import logging

from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine, init_db
from app.seed_mock_data import create_mock_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)
    
    if settings.ENVIRONMENT == "local":
        logger.info("Local environment detected, seeding mock data...")
        create_mock_data()


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
