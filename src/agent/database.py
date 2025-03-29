"""Database operations for the agent."""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import os

class DatabaseManager:
    """Manages database operations for the agent."""
    
    def __init__(self):
        """Initialize database connection."""
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "data", "users.db")
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the database with sample data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            firstname TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        ''')
        
        # Sample data
        sample_users = [
            ("John", "Smith", "john.smith@email.com"),
            ("Emma", "Johnson", "emma.j@email.com"),
            ("Michael", "Williams", "m.williams@email.com"),
            ("Sarah", "Brown", "sarah.brown@email.com"),
            ("David", "Jones", "david.jones@email.com"),
            ("Lisa", "Garcia", "l.garcia@email.com"),
            ("James", "Miller", "james.m@email.com"),
            ("Maria", "Davis", "maria.davis@email.com"),
            ("Robert", "Anderson", "r.anderson@email.com"),
            ("Jennifer", "Taylor", "jen.taylor@email.com")
        ]
        
        # Insert sample data
        try:
            cursor.executemany(
                "INSERT OR REPLACE INTO users (firstname, surname, email) VALUES (?, ?, ?)",
                sample_users
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()
    
    def query_users(self, query: str) -> List[Dict[str, Any]]:
        """Query the users database and return results."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return [{"error": str(e)}]
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from the database."""
        return self.query_users("SELECT * FROM users")

# Create a global instance of the database manager
db_manager = DatabaseManager() 