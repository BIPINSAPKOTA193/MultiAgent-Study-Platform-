"""Database module for persistent data storage"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import contextmanager
from .logger import logger


def get_db_path() -> Path:
    """Get path to SQLite database file"""
    # Use a persistent location that works on Streamlit Cloud
    db_dir = Path(__file__).parent.parent.parent / "data"
    db_dir.mkdir(exist_ok=True)
    return db_dir / "app_data.db"


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.get_logger().error(f"Database error: {e}")
        raise
    finally:
        conn.close()


def init_database():
    """Initialize database tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # RL State table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rl_state (
                username TEXT PRIMARY KEY,
                mode_alpha TEXT NOT NULL,
                mode_beta TEXT NOT NULL,
                mode_history TEXT NOT NULL,
                chunk_performance TEXT NOT NULL,
                file_mapping TEXT NOT NULL,
                survey_completed INTEGER NOT NULL DEFAULT 0,
                initial_preference TEXT,
                total_sessions INTEGER NOT NULL DEFAULT 0,
                last_updated TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        logger.get_logger().info("Database initialized successfully")


def save_user(username: str, password_hash: str) -> bool:
    """Save user to database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users (username, password_hash, created_at)
                VALUES (?, ?, ?)
            """, (username, password_hash, datetime.now().isoformat()))
            return True
    except Exception as e:
        logger.get_logger().error(f"Error saving user: {e}")
        return False


def get_user(username: str) -> Optional[Dict[str, Any]]:
    """Get user from database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    except Exception as e:
        logger.get_logger().error(f"Error getting user: {e}")
        return None


def get_all_users() -> Dict[str, Dict[str, Any]]:
    """Get all users from database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return {row["username"]: dict(row) for row in rows}
    except Exception as e:
        logger.get_logger().error(f"Error getting users: {e}")
        return {}


def save_rl_state(username: str, state_data: Dict[str, Any]) -> bool:
    """Save RL state to database"""
    try:
        now = datetime.now().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if state exists
            cursor.execute("SELECT username FROM rl_state WHERE username = ?", (username,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing state
                cursor.execute("""
                    UPDATE rl_state SET
                        mode_alpha = ?,
                        mode_beta = ?,
                        mode_history = ?,
                        chunk_performance = ?,
                        file_mapping = ?,
                        survey_completed = ?,
                        initial_preference = ?,
                        total_sessions = ?,
                        last_updated = ?,
                        updated_at = ?
                    WHERE username = ?
                """, (
                    json.dumps(state_data.get("mode_alpha", {})),
                    json.dumps(state_data.get("mode_beta", {})),
                    json.dumps(state_data.get("mode_history", [])),
                    json.dumps(state_data.get("chunk_performance", {})),
                    json.dumps(state_data.get("file_mapping", {})),
                    1 if state_data.get("survey_completed", False) else 0,
                    state_data.get("initial_preference"),
                    state_data.get("total_sessions", 0),
                    state_data.get("last_updated"),
                    now,
                    username
                ))
            else:
                # Insert new state
                cursor.execute("""
                    INSERT INTO rl_state (
                        username, mode_alpha, mode_beta, mode_history,
                        chunk_performance, file_mapping, survey_completed,
                        initial_preference, total_sessions, last_updated,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    username,
                    json.dumps(state_data.get("mode_alpha", {})),
                    json.dumps(state_data.get("mode_beta", {})),
                    json.dumps(state_data.get("mode_history", [])),
                    json.dumps(state_data.get("chunk_performance", {})),
                    json.dumps(state_data.get("file_mapping", {})),
                    1 if state_data.get("survey_completed", False) else 0,
                    state_data.get("initial_preference"),
                    state_data.get("total_sessions", 0),
                    state_data.get("last_updated"),
                    now,
                    now
                ))
            return True
    except Exception as e:
        logger.get_logger().error(f"Error saving RL state: {e}")
        return False


def load_rl_state(username: str) -> Optional[Dict[str, Any]]:
    """Load RL state from database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rl_state WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "mode_alpha": json.loads(row["mode_alpha"]),
                    "mode_beta": json.loads(row["mode_beta"]),
                    "mode_history": json.loads(row["mode_history"]),
                    "chunk_performance": json.loads(row["chunk_performance"]),
                    "file_mapping": json.loads(row["file_mapping"]),
                    "survey_completed": bool(row["survey_completed"]),
                    "initial_preference": row["initial_preference"],
                    "total_sessions": row["total_sessions"],
                    "last_updated": row["last_updated"]
                }
            return None
    except Exception as e:
        logger.get_logger().error(f"Error loading RL state: {e}")
        return None


# Initialize database on import
try:
    init_database()
except Exception as e:
    logger.get_logger().error(f"Failed to initialize database: {e}")

