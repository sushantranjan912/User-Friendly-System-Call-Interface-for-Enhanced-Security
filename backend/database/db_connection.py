import sqlite3
import os
from contextlib import contextmanager

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database directory and initialize schema if needed"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            self._initialize_schema()
    
    def _initialize_schema(self):
        """Initialize database with schema"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema)
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections

        Use check_same_thread=False to allow concurrent access from multiple
        request threads. SQLite's default behavior (True) would cause "database
        is locked" errors under concurrent load. Each thread creates its own
        connection, so thread safety is handled via connection isolation.
        """
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()
    
    def execute_insert(self, query, params=None):
        """Execute insert and return last row id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
    
    def execute_update(self, query, params=None):
        """Execute update and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
