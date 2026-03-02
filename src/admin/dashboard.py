"""Admin dashboard module."""
from flask import request, render_template_string

def admin_dashboard(user):
    # VULNERABLE: No authentication check on admin endpoint
    # Anyone can access this without @require_auth decorator
    search_query = request.args.get("q", "")

    # VULNERABLE: XSS - user input rendered without escaping
    html = f"""
    <h1>Admin Panel</h1>
    <p>Welcome {user.name}</p>
    <p>Search results for: {search_query}</p>
    <div>{render_search_results(search_query)}</div>
    """
    return render_template_string(html)

def render_search_results(query):
    # VULNERABLE: XSS via unescaped query
    return f"<p>Results for: {query}</p>"

def get_all_users():
    """Return all users - handles PII data."""
    import sqlite3
    conn = sqlite3.connect("users.db")
    # Returns names, emails, addresses - PII exposure risk
    return conn.execute("SELECT * FROM users").fetchall()
