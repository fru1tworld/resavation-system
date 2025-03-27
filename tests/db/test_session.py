from sqlalchemy import text
from app.db.session import get_db  

def test_get_db_session():
    db_gen = get_db()
    db = next(db_gen)
    
    assert db is not None

    try:
        result = db.execute(text("SELECT 1")).fetchone()
        assert result[0] == 1
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass
