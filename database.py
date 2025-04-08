import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database with all required tables and columns"""
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    # User actions tracking table
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_actions (
        session_id TEXT PRIMARY KEY,
        email_clicked INTEGER DEFAULT 0,
        login_submitted INTEGER DEFAULT 0,
        ceo_attempt INTEGER DEFAULT 0,
        tech_support_attempt INTEGER DEFAULT 0,
        vishing_attempt INTEGER DEFAULT 0,
        quishing_attempt INTEGER DEFAULT 0,
        flags_identified INTEGER DEFAULT 0,
        last_active TIMESTAMP
    )
    ''')
    
    # Training scenarios table
    c.execute('''
    CREATE TABLE IF NOT EXISTS scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        difficulty TEXT
    )
    ''')
    
    # Insert default scenarios if they don't exist
    c.execute('''
    INSERT OR IGNORE INTO scenarios (name, description, difficulty)
    VALUES 
        ('Phishing Email', 'Simulated bank phishing email', 'Easy'),
        ('CEO Fraud', 'Fake CEO wire transfer request', 'Medium'),
        ('Tech Support', 'Fake Microsoft support scam', 'Hard'),
        ('Vishing', 'Fake tech support call', 'Medium')
    ''')
    
    conn.commit()
    conn.close()

def log_action(session_id, action_type):
    """
    Log user actions in the database
    Supported action_types:
    - 'email_click'
    - 'form_submit'
    - 'ceo_transfer_attempt'
    - 'tech_support_attempt'
    """
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    # Create record if doesn't exist
    c.execute('''
    INSERT OR IGNORE INTO user_actions (session_id, last_active)
    VALUES (?, ?)
    ''', (session_id, datetime.now()))
    
    # Update based on action type
    update_map = {
        'email_click': ('email_clicked', 1),
        'form_submit': ('login_submitted', 1),
        'ceo_transfer_attempt': ('ceo_attempt', 1),
        'tech_support_attempt': ('tech_support_attempt', 1),
        'vishing_attempt': ('vishing_attempt', 1),
        'quishing_attempt': ('quishing_attempt', 1)
    }
    
    if action_type in update_map:
        column, value = update_map[action_type]
        c.execute(f'''
        UPDATE user_actions 
        SET {column} = ?, last_active = ?
        WHERE session_id = ?
        ''', (value, datetime.now(), session_id))
    
    conn.commit()
    conn.close()

def get_user_stats(session_id):
    """Retrieve statistics for a specific user session"""
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('''
    SELECT 
        email_clicked, 
        login_submitted, 
        ceo_attempt, 
        tech_support_attempt,
        flags_identified
    FROM user_actions 
    WHERE session_id = ?
    ''', (session_id,))
    
    result = c.fetchone()
    conn.close()
    
    if not result:
        return None
    
    return {
        'email_clicked': bool(result[0]),
        'login_submitted': bool(result[1]),
        'ceo_attempt': bool(result[2]),
        'tech_support_attempt': bool(result[3]),
        'flags_identified': result[4]
    }

def reset_user_session(session_id):
    """Clear all actions for a specific session (for testing)"""
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('''
    DELETE FROM user_actions
    WHERE session_id = ?
    ''', (session_id,))
    
    conn.commit()
    conn.close()