import cv2
import face_recognition
import numpy as np
import os
import csv
import sqlite3
from flask import Flask, render_template, Response, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Load known faces
known_face_encodings = []
known_face_names = []

def load_known_faces():
    images = os.listdir('known_faces')
    for image in images:
        img = face_recognition.load_image_file(f'known_faces/{image}')
        encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(image.split('.')[0])  # Use filename without extension as name

load_known_faces()

# Database setup
def connect_db():
    return sqlite3.connect('users.db')

def create_user_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Write recognized face to CSV
def write_to_csv(name):
    with open('login_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name])  # Write recognized name to CSV

# Face recognition camera stream
def generate_frames():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                write_to_csv(name)  # Update CSV with recognized name

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Routes

# Main route for login page
@app.route('/')
def login():
    return render_template('login.html')

# Handle login POST request
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = username
        return redirect(url_for('findex'))  # Redirect to the main face recognition page
    else:
        return 'Invalid credentials! Please try again.'

# Handle registration POST request
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        return 'Username already exists! Please choose a different username.'

# Page for face recognition (after successful login)
@app.route('/findex')
def findex():
    if 'username' in session:
        return render_template('findex.html')
    return redirect(url_for('login'))

# Video feed route
@app.route('/video_feed')
def video_feed():
    if 'username' in session:  # Ensure user is logged in before accessing camera
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_user_table()  # Run this once to set up the user table
    app.run(debug=True)
