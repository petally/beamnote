class User:
    def __init__(self, username: str, password: str, role: str = "user"):
        self.username = username
        self.password = password
        self.role = role  # "user" or "admin"

    def is_admin(self) -> bool:
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.username!r} role={self.role!r}>"


class Note:
    def __init__(self, id: int, title: str, content: str, author: str, created_at: str):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at

    def preview(self, chars: int = 100) -> str:
        # return a short preview of the content
        return self.content[:chars] + ("..." if len(self.content) > chars else "")

    def __repr__(self):
        return f"<Note id={self.id} title={self.title!r} author={self.author!r}>"
