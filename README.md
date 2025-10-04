🧠 Multi-Factor Face & OTP Recognition System
🔐 Secure Login | 👁️ Face Recognition | 📱 OTP Verification | 🧾 Attendance Logging
📘 Overview

This project integrates multiple authentication and recognition layers to build a secure, AI-powered identity verification and attendance system.
It uses:

Flask (Web Interface) — for user registration, login, and face recognition dashboard

Face Recognition (OpenCV + face_recognition) — for real-time face detection and name recognition

Twilio API — for OTP-based verification via SMS

SQLite — for storing user login data

CSV Logging — to maintain attendance or recognition records

Tkinter GUI — for standalone OTP verification interface

This system can be extended for:

Smart attendance systems (colleges, offices)

Secure login portals with face + OTP verification

Multi-factor authentication prototypes

⚙️ Features

✅ User Registration & Login (Flask + SQLite)
✅ Real-time Face Recognition using Webcam
✅ Recognized Users Automatically Logged to CSV
✅ OTP Authentication (Twilio API + Flask)
✅ Desktop OTP GUI (Tkinter)
✅ Attendance Recording (with timestamp)
✅ Session Management for Security

🧩 System Components
1️⃣ app.py — Flask Face Recognition Login System

User authentication (register/login)

Uses face_recognition for identifying known faces

Stores user credentials in users.db

Logs recognized users to login_data.csv

Secured with Flask sessions

Main Routes:

Route	Description
/	Login page
/login	Validate login credentials
/register	Register new user
/findex	Face recognition page
/video_feed	Live webcam feed for face detection
2️⃣ otp_app.py — Flask OTP Verification (Twilio)

Sends OTP via Twilio SMS API

Verifies OTP entered by the user

Grants or denies access based on validation

Main Routes:

Route	Description
/	OTP input page
/index	User login and OTP generation
/validate	Verify OTP input
/success	Access granted message
/face_recognition	Redirects to face recognition page
3️⃣ otp_tkinter.py — Desktop OTP GUI (Tkinter)

Generates and validates OTP locally

Includes resend OTP and countdown timer

Provides feedback for successful or failed verification

Features:

Countdown timer (30 seconds)

Button to resend new OTP

MessageBox alerts for result feedback

4️⃣ face_attendance.py — Attendance Recognition Script

Uses face_recognition and OpenCV to:

Identify known faces (bhushan.jpg, tata.jpg, etc.)

Log attendance to a daily CSV file named with the current date

Display real-time face recognition with bounding boxes

Automatically record timestamp for recognized faces

🧰 Technologies Used
Category	Tools / Libraries
Backend	Flask, SQLite3
Face Recognition	OpenCV, face_recognition, NumPy
OTP & SMS	Twilio API
GUI	Tkinter
File Management	CSV
Authentication	Flask Session
🗂️ Folder Structure
📂 MultiFactorRecognition
│
├── 📁 known_faces/
│   ├── bhushan.jpg
│   ├── tata.jpg
│   ├── sadmona.jpg
│   └── tesla.jpg
│
├── app.py                # Flask app with face recognition
├── otp_app.py            # Flask app for OTP verification
├── otp_tkinter.py        # Tkinter-based OTP GUI
├── face_attendance.py    # Attendance recognition script
├── templates/
│   ├── login.html
│   ├── findex.html
│   ├── index.html
│   └── otp_verification.html
│
├── users.db              # SQLite database (auto-created)
├── login_data.csv        # Face recognition log
└── README.md

🔧 Setup Instructions
🪜 1. Clone the Repository
git clone https://github.com/yourusername/multifactor-recognition.git
cd multifactor-recognition

🪜 2. Install Dependencies
pip install flask opencv-python face_recognition numpy twilio

🪜 3. Set Up Twilio Credentials

Edit your Twilio credentials in otp_app.py:

account_sid = "YOUR_TWILIO_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"
twilio_number = "+1XXXXXXXXXX"

🪜 4. Add Known Faces

Place face images (e.g., bhushan.jpg, tata.jpg) inside the known_faces/ folder.

🪜 5. Initialize Database
python app.py


This will automatically create users.db with a users table.

🪜 6. Run the Application
🧠 For Face Recognition Flask App:
python app.py


Open: http://127.0.0.1:5000

📱 For OTP Verification Flask App:
python otp_app.py


Open: http://127.0.0.1:8098

🖥️ For Desktop OTP GUI:
python otp_tkinter.py

🎥 For Attendance Recognition Script:
python face_attendance.py

🧾 Output Examples

✅ Face recognized:
Displays user name on webcam feed and writes name + timestamp in YYYY-MM-DD.csv

📩 OTP verified successfully:
Grants access via web interface or Tkinter GUI

📜 Login CSV Record:

bhushan
ratan tata
tesla

🔐 Security Notes

Always keep your Twilio credentials private.

Use environment variables (setx TWILIO_SID, etc.) instead of hardcoding.

Use hashed passwords (e.g., bcrypt) in production.

💡 Future Enhancements

Add JWT tokens for API authentication

Integrate email OTP as a backup method

Add role-based access control

Store face encodings in the database instead of reloading every time

Use DeepFace for more robust recognition