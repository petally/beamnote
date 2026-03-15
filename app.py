from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database
from models import User, Note
from werkzeug.security import check_password_hash

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static/")
app.secret_key = "asdgoiadfvohia4h9038"
db = Database("beamnote.db")
db.init()

# Auth

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.get_user(username):
            flash("This username already taken.")
            return redirect(url_for("register"))
        db.create_user(username, password, role="user")
        flash("Registered! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.get_user(username)
        if not user or not check_password_hash(user.password, password):
            flash("Invalid login details.")
            return redirect(url_for("login"))
        session["username"] = user.username
        session["role"] = user.role
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Notes

@app.route("/")
def index():
    notes = db.get_all_notes()
    return render_template("index.html", notes=notes)

@app.route("/new", methods=["GET", "POST"])
def new_note():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        db.create_note(title, content, session["username"])
        return redirect(url_for("index"))
    return render_template("new_note.html")

@app.route("/note/<int:note_id>")
def view_note(note_id):
    note = db.get_note(note_id)
    if not note:
        flash("Note not found.")
        return redirect(url_for("index"))
    return render_template("view_note.html", note=note)

@app.route("/note/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    note = db.get_note(note_id)
    if not note:
        flash("Note not found.")
        return redirect(url_for("index"))
    if "username" not in session:
        return redirect(url_for("login"))
    # Only owner or admin can edit
    if session["username"] != note.author and session["role"] != "admin":
        flash("This action is not authorized.")
        return redirect(url_for("view_note", note_id=note_id))
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        db.update_note(note_id, title, content)
        return redirect(url_for("view_note", note_id=note_id))
    return render_template("edit_note.html", note=note)

@app.route("/note/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    note = db.get_note(note_id)
    if not note:
        flash("Note not found.")
        return redirect(url_for("index"))
    if "username" not in session:
        return redirect(url_for("login"))
    if session["username"] != note.author and session["role"] != "admin":
        flash("Not allowed.")
        return redirect(url_for("view_note", note_id=note_id))
    db.delete_note(note_id)
    flash("Note deleted.")
    return redirect(url_for("index"))

# Admin 

@app.route("/admin")
def admin_panel():
    if session.get("role") != "admin":
        flash("Admins only.")
        return redirect(url_for("index"))
    users = db.get_all_users()
    return render_template("admin.html", users=users)

@app.route("/admin/delete_user/<username>", methods=["POST"])
def delete_user(username):
    if session.get("role") != "admin":
        flash("This action is not authorized.")
        return redirect(url_for("index"))
    db.delete_user(username)
    flash(f"User {username} deleted.")
    return redirect(url_for("admin_panel"))

if __name__ == "__main__":
    app.run(debug=True)
