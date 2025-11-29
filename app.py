from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
import requests

app = Flask(__name__)
CORS(app)

# ------------------ DATABASE CONNECTION (for login/admin only) ------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="musicdb"
)
cursor = db.cursor(dictionary=True)

# ------------------ PAGES ------------------
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/home')
def user_page():
    return render_template('home.html')

# ------------------ USERS API ------------------
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
    existing = cursor.fetchone()
    if existing:
        return jsonify({"error": "Username or Email already exists"}), 400
    cursor.execute(
        "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
        (username, email, password, 'user')
    )
    db.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s",
        (username, password, role)
    )
    user = cursor.fetchone()
    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
        })
    else:
        return jsonify({"error": "Invalid username, password, or role"}), 401


# ---------- 🔹 ADMIN USERS API (for /api/users used by admin.html) ----------
@app.route('/api/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()  # list of dicts
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    role = data.get('role', 'user')

    cursor.execute(
        "UPDATE users SET username=%s, email=%s, role=%s WHERE id=%s",
        (username, email, role, user_id)
    )
    db.commit()
    return jsonify({"message": "User updated"})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    return jsonify({"message": "User deleted"})


# ------------------ SEARCH SONG API (using iTunes instead of Deezer) ------------------
@app.route('/api/search-song', methods=['GET'])
def search_song():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    try:
        # iTunes Search API – no auth needed
        url = "https://itunes.apple.com/search"
        params = {
            "term": query,
            "media": "music",
            "limit": 25
        }
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        songs_to_send = []
        for item in data.get("results", []):
            song = {
                "id": item.get("trackId"),
                "title": item.get("trackName"),
                "artist": item.get("artistName"),
                "album": item.get("collectionName"),
                "preview": item.get("previewUrl"),
                "cover": item.get("artworkUrl100"),
                "duration": int(item.get("trackTimeMillis", 0) / 1000)
            }
            songs_to_send.append(song)

        return jsonify(songs_to_send)
    except Exception as e:
        print("Music API error:", e)
        return jsonify({"error": "Music API failed"}), 500

# ------------------ MAIN ------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
