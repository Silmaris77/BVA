"""
Database Connection Management
Zarządzanie połączeniem z bazą danych (SQLite lub PostgreSQL)
"""

import json
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool


# Globalna instancja engine (lazy initialization)
_engine = None
_SessionLocal = None


def load_config():
    """Ładuje konfigurację bazy danych"""
    config_path = Path(__file__).parent.parent / "config" / "migration_config.json"
    
    if config_path.exists():
        with open(config_path, encoding='utf-8') as f:
            config = json.load(f)
            return config.get("database", {})
    
    # Domyślna konfiguracja - SQLite
    return {
        "type": "sqlite",
        "sqlite_path": "database/bva_app.db"
    }


def get_database_url():
    """
    Zwraca connection string dla bazy danych
    
    Returns:
        str: Database URL (SQLite lub PostgreSQL)
    """
    config = load_config()
    db_type = config.get("type", "sqlite")
    
    if db_type == "sqlite":
        # SQLite - prosty plik
        db_path = Path(__file__).parent.parent / config.get("sqlite_path", "database/bva_app.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"
    
    elif db_type == "postgresql":
        # PostgreSQL
        pg_config = config.get("postgresql", {})
        host = pg_config.get("host", "localhost")
        port = pg_config.get("port", 5432)
        database = pg_config.get("database", "bva_app")
        user = pg_config.get("user", "bva_user")
        password = pg_config.get("password", "")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_engine():
    """
    Zwraca SQLAlchemy engine (singleton)
    
    Returns:
        Engine: SQLAlchemy engine
    """
    global _engine
    
    if _engine is None:
        database_url = get_database_url()
        
        # Konfiguracja engine zależna od typu bazy
        if database_url.startswith("sqlite"):
            # SQLite specific configuration
            _engine = create_engine(
                database_url,
                connect_args={
                    "check_same_thread": False,  # Pozwala na multi-threading
                    "timeout": 30  # Timeout 30 sekund
                },
                poolclass=StaticPool,  # Jeden connection dla SQLite
                echo=False  # Set to True for SQL debugging
            )
            
            # Enable foreign keys dla SQLite
            @event.listens_for(_engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        
        else:
            # PostgreSQL configuration
            _engine = create_engine(
                database_url,
                pool_pre_ping=True,  # Verify connections
                pool_size=10,
                max_overflow=20,
                echo=False
            )
    
    return _engine


def get_session() -> Session:
    """
    Zwraca nową sesję SQLAlchemy
    
    Returns:
        Session: SQLAlchemy session
    """
    global _SessionLocal
    
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    
    return _SessionLocal()


@contextmanager
def session_scope():
    """
    Context manager dla sesji bazodanowej z auto-commit/rollback
    
    Usage:
        with session_scope() as session:
            user = session.query(User).first()
            session.commit()
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def init_database():
    """
    Inicjalizuje bazę danych - tworzy tabele jeśli nie istnieją
    """
    try:
        from .models import Base
    except ImportError:
        from models import Base
    
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")


def drop_all_tables():
    """
    UWAGA: Usuwa wszystkie tabele z bazy danych!
    Użyj tylko w testach lub przy resetowaniu.
    """
    try:
        from .models import Base
    except ImportError:
        from models import Base
    
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All database tables dropped")


def get_database_info():
    """
    Zwraca informacje o bazie danych
    
    Returns:
        dict: Informacje o bazie
    """
    config = load_config()
    engine = get_engine()
    
    return {
        "type": config.get("type", "sqlite"),
        "url": get_database_url(),
        "driver": engine.driver,
        "dialect": engine.dialect.name,
        "pool_size": getattr(engine.pool, 'size', lambda: 'N/A')(),
    }


if __name__ == "__main__":
    # Test connection
    print("="*60)
    print("🔌 DATABASE CONNECTION TEST")
    print("="*60)
    
    try:
        info = get_database_info()
        print(f"\nDatabase Type: {info['type']}")
        print(f"Database URL: {info['url']}")
        print(f"Driver: {info['driver']}")
        print(f"Dialect: {info['dialect']}")
        
        # Test connection
        engine = get_engine()
        with engine.connect() as conn:
            print("\n✅ Connection successful!")
        
        # Initialize tables
        init_database()
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
