# pytest configuration file for setting up test fixtures and database connections

# pytest fixture for test settings
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from test_db_manager import TestSettings, TestDatabaseManager

# Base class for test SQLAlchemy models
Base = declarative_base()
    
# create a fixture for the test database engine
@pytest.fixture(scope="session")
def engine():
    settings = TestSettings()
    db_manager = TestDatabaseManager(settings)
    
    test_branch_url = db_manager.provide_test_branch()
    engine = create_engine(test_branch_url, echo=True, future=True)
    
    yield engine
    
    engine.dispose()
    db_manager.teardown_test_branch()
    
@pytest.fixture(scope="function")
def get_test_session(engine):
    conn = engine.connect()
    # create a new session for the test
    transaction = conn.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=conn)
    session = SessionLocal()
    
    yield session
    
    # rollback the transaction after the test
    session.close()
    transaction.rollback()
    conn.close()