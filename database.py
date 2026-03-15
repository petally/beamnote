import sqlite3
from models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    # Handles all SQLite interactions. Uses an in-memory dict cache for notes

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._note_cache: dict[int, Note] = {}

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init(self):
        # Create tables and seed an admin account if one doesnt exist
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user'
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (author) REFERENCES users(username)
                )
            """)
            # Seed default admin
            conn.execute("""
                INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)""",
                ("admin", generate_password_hash("admin"), "admin")
            )
            conn.commit()

    # Users

    def create_user(self, username: str, password: str, role: str = "user"):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), role)
            )
            conn.commit()

    def get_user(self, username: str) -> User | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
        return User(row["username"], row["password"], row["role"]) if row else None

    def get_all_users(self) -> list[User]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM users").fetchall()
        return [User(r["username"], r["password"], r["role"]) for r in rows]

    def delete_user(self, username: str):
        with self._connect() as conn:
            conn.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.execute("DELETE FROM notes WHERE author = ?", (username,))
            conn.commit()
        # Invalidate cache entries belonging to this user
        self._note_cache = {
            pid: p for pid, p in self._note_cache.items() if p.author != username
        }

    # Notes

    def create_note(self, title: str, content: str, author: str):
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO notes (title, content, author) VALUES (?, ?, ?)",
                (title, content, author)
            )
            conn.commit()
            note_id = cursor.lastrowid
        note = self.get_note(note_id)
        self._note_cache[note_id] = note  # cache it
        return note

    def get_note(self, note_id: int) -> Note | None:
        if note_id in self._note_cache:
            return self._note_cache[note_id]
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM notes WHERE id = ?", (note_id,)
            ).fetchone()
        if not row:
            return None
        note = Note(row["id"], row["title"], row["content"], row["author"], row["created_at"])
        self._note_cache[note_id] = note
        return note

    def get_all_notes(self) -> list[Note]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM notes ORDER BY created_at DESC"
            ).fetchall()
        notes = [Note(r["id"], r["title"], r["content"], r["author"], r["created_at"]) for r in rows]
        # Refresh cache
        for n in notes:
            self._note_cache[n.id] = n
        return notes

    def update_note(self, note_id: int, title: str, content: str):
        with self._connect() as conn:
            conn.execute(
                "UPDATE notes SET title = ?, content = ? WHERE id = ?",
                (title, content, note_id)
            )
            conn.commit()
        # invalidate cache entry
        self._note_cache.pop(note_id, None)

    def delete_note(self, note_id: int):
        with self._connect() as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
        self._note_cache.pop(note_id, None)
