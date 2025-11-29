🎵 TealTune – Music App

A simple and beautiful music web application built using Python Flask, MySQL, HTML, CSS, and the iTunes Music API.
Users can sign up, log in, search for songs, listen to previews, and admins can manage user details.

🚀 Features
👤 User Features

Sign up & log in

Search songs

View album art

Play audio previews

Clean and modern UI

👑 Admin Features

View all registered users

Edit user details

Delete users

Search users by username / email / role
🛠️ Tech Stack
Frontend

HTML

CSS

JavaScript (Vanilla)

Backend

Python

Flask

flask-cors

requests

Database

MySQL (via XAMPP)

API Used

iTunes Music Search API
📁 Project Structure
musicapp/
│
├── app.py                # Flask backend
├── config.py             # DB config (optional)
├── models.py             # Database models (if used)
├── requirements.txt      # Dependencies
├── templates/            # HTML pages
│   ├── login.html
│   ├── signup.html
│   ├── admin.html
│   └── home.html
│
├── static/               # Images/CSS files
└── README.md
⚙️ Installation & Setup
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start XAMPP MySQL

Create a database named:

musicdb


Add a users table with fields:

id

username

email

password

role

(or let your app create it).

3️⃣ Run the Flask server
python app.py


App runs at:
👉 http://localhost:5000
