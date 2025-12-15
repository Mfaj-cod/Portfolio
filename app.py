import os
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from src.agent import generate_blog_draft
from src.db import get_db_connection, setup as db_setup
from src.logg import logger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Ensure DB is ready
db_setup()

# decorator function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# routes
@app.route('/')
def home():
    conn = get_db_connection()
    # Fetch all data dynamically
    blogs = conn.execute("SELECT * FROM blogs ORDER BY created_at DESC").fetchall()
    projects = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    profile = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    
    # Fallback if profile is empty
    if not profile:
        profile = {"bio": "Welcome to my portfolio.", "skills": "AI, Python"}

    return render_template('index.html', blogs=blogs, projects=projects, profile=profile)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        flash('Invalid password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



@app.route('/admin')
@login_required
def admin():
    conn = get_db_connection()
    blogs = conn.execute("SELECT * FROM blogs ORDER BY created_at DESC").fetchall()
    projects = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template('admin.html', blogs=blogs, projects=projects)

# API
@app.route('/api/generate', methods=['POST'])
@login_required
def generate_api():
    data = request.json
    draft = generate_blog_draft(data.get('prompt'))
    if draft:
        return jsonify(draft)
    return jsonify({"error": "Agent failed"}), 500


@app.route('/api/save', methods=['POST'])
@login_required
def save_content():
    data = request.json
    content_type = data.get('type', 'blog') # Default to blog

    try:
        with open('data/history.txt', 'a', encoding='utf-8') as file:
            file.write(f"--- NEW ENTRY ({content_type}) ---\n")
            file.write(f"Title: {data.get('title', 'No Title')}\n")
            file.write(f"Tags: {data.get('tags', '')}\n")
            file.write(f"Content:\n{data.get('content', '')}\n")
            file.write("-" * 30 + "\n\n")
    except Exception as e:
        logger.error(f"Warning: Could not save to history.txt: {e}")

    
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        if content_type == 'project':
            cur.execute(
                "INSERT INTO projects (title, description, tech_stack) VALUES (?, ?, ?)",
                (data['title'], data['content'], data['tags'])
            )
        elif content_type == 'about':
            # Create a new profile entry (we always fetch the latest one)
            cur.execute(
                "INSERT INTO profile (bio, skills) VALUES (?, ?)",
                (data['content'], data['tags'])
            )
        else:
            # Blog
            cur.execute(
                "INSERT INTO blogs (title, content, tags) VALUES (?, ?, ?)",
                (data['title'], data['content'], data['tags'])
            )
            
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "type": content_type})
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

# Delete Route
@app.route('/api/delete/<content_type>/<int:item_id>', methods=['POST'])
@login_required
def delete_item(content_type, item_id):
    conn = get_db_connection()
    try:
        if content_type == 'blog':
            conn.execute("DELETE FROM blogs WHERE id = ?", (item_id,))
        elif content_type == 'project':
            conn.execute("DELETE FROM projects WHERE id = ?", (item_id,))
        
        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)