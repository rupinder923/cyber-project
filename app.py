from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
import sqlite3
import uuid
import os
import pytest

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this for production!

# Database setup
def init_db():
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_actions (
        session_id TEXT PRIMARY KEY,
        email_clicked INTEGER DEFAULT 0,
        login_submitted INTEGER DEFAULT 0,
        flags_identified INTEGER DEFAULT 0,
        last_active TIMESTAMP
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        difficulty TEXT
    )
    ''')
    
    # Insert default scenarios
    c.execute('''
    INSERT OR IGNORE INTO scenarios (name, description, difficulty)
    VALUES 
        ('Phishing Email', 'Simulated bank phishing email', 'Easy'),
        ('CEO Fraud', 'Fake CEO wire transfer request', 'Medium'),
        ('Tech Support', 'Fake Microsoft support scam', 'Hard')
    ''')
    
    conn.commit()
    conn.close()

# Stored user logs using log_action
def log_action(session_id, action_type):
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT OR IGNORE INTO user_actions (session_id, last_active)
    VALUES (?, ?)
    ''', (session_id, datetime.now()))
    
    if action_type == 'email_click':
        c.execute('''
        UPDATE user_actions 
        SET email_clicked = 1, last_active = ?
        WHERE session_id = ?
        ''', (datetime.now(), session_id))
    elif action_type == 'form_submit':
        c.execute('''
        UPDATE user_actions 
        SET login_submitted = 1, last_active = ?
        WHERE session_id = ?
        ''', (datetime.now(), session_id))
    
    conn.commit()
    conn.close()

# Initialize database
with app.app_context():
    init_db()

# Ensure templates exist
REQUIRED_TEMPLATES = [
    'index.html',
    'phishing_email.html',
    'fake_login.html',
    'phishing_result.html',
    'email_feedback.html',
    'ceo_fraud.html',
    'ceo_fraud_result.html',
    'tech_support.html',
    'tech_support_result.html',
    'fraud_payment.html',
    'fraud_payment_result.html',
    'social_media.html',
    'social_media_result.html'
]

# Handling Missing template function
for template in REQUIRED_TEMPLATES:
    template_path = os.path.join('templates', template)
    print(template_path)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Missing template: {template_path}")

# Routes
@app.route("/")
def home():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("index.html")

# Email Simulation Flow
@app.route("/email-test")
def show_email_test():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("phishing_email.html")

# handle_email_click function redirect cibc mail user to cibc cridentitals page
@app.route("/email-test/click", methods=['POST'])
def handle_email_click():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    log_action(session['session_id'], 'email_click')
    return redirect(url_for('show_fake_login', source='email'))

# Fake Cibc Cridentials page render
@app.route("/fake-login")
def show_fake_login():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    source = request.args.get("source", "direct")
    return render_template("fake_login.html", source=source)

# Redirect user to the red flag page
@app.route("/email-test/submit", methods=['POST'])
def handle_email_submit():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    log_action(session['session_id'], 'form_submit')
    return redirect(url_for('show_email_result', success=False))

# Render red flag page
@app.route("/email-test/result")
def show_email_result():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    # success = request.args.get("success", "false").lower() == "true"
    source = request.args.get("source", "direct")
    return render_template("phishing_result.html", success=source)



# Render Details red flag overview page for the cibc scenario
@app.route("/email-test/feedback")
def show_email_feedback():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("email_feedback.html")



# Render Tech Support Scam Scenario
@app.route("/tech-support")
def show_tech_support():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("tech_support.html")

# Redirect tech scam page to red flag
@app.route("/tech-support/download", methods=['POST'])
def handle_tech_download():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    log_action(session['session_id'], 'tech_support_attempt')
    return redirect(url_for('tech_support_result'))

# Render red flag for tech scam
@app.route("/tech-support/result")
def tech_support_result():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("tech_support_result.html")


# CEO Fraud Scenario
@app.route("/ceo-fraud")
def show_ceo_fraud():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("ceo_fraud.html")

# Redirect ceo fraud page to red flag
@app.route("/ceo-fraud/transfer", methods=['POST'])
def handle_ceo_transfer():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    log_action(session['session_id'], 'ceo_transfer_attempt')
    return redirect(url_for('ceo_fraud_result'))

# Render red flag page for ceo fraud
@app.route("/ceo-fraud/result")
def ceo_fraud_result():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("ceo_fraud_result.html")


# Fraud Payment scam Scenario
@app.route("/fraud-payment")
def show_fraud_payment():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("fraud_payment.html")

# Redirect Payment scam Scenario to red flag page
@app.route("/fraud-payment/complate", methods=['POST'])
def handle_fraud_payment():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    log_action(session['session_id'], 'tech_support_attempt')
    return redirect(url_for('fraud_payment_result'))

# Render red flag page for Payment scam Scenario 
@app.route("/fraud-payment/result")
def fraud_payment_result():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("fraud_payment_result.html")


# Render Social Media Scenario
@app.route("/social-media")
def show_social_media():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("social_media.html")

# Redirect Social Media Scenario to red flag page
@app.route("/social-media/complate", methods=['POST'])
def handle_social_media():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    log_action(session['session_id'], 'tech_support_attempt')
    return redirect(url_for('social_media_result'))

# Render red flag page for Social Media Scenario
@app.route("/social-media/result")
def social_media_result():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template("social_media_result.html")



# User Statistics
@app.route("/api/stats")
def get_user_stats():
    if 'session_id' not in session:
        return jsonify({"error": "No active session"}), 401
    
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    c.execute('''
    SELECT email_clicked, login_submitted, flags_identified 
    FROM user_actions 
    WHERE session_id = ?
    ''', (session['session_id'],))
    
    result = c.fetchone()
    conn.close()
    
    return jsonify({
        "email_clicked": bool(result[0]) if result else False,
        "login_submitted": bool(result[1]) if result else False,
        "flags_identified": result[2] if result else 0
    })


if __name__ == "__main__":
    app.run(debug=True)




@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, Flask!"}