"""Development environment setup script."""
import os

# VULNERABLE: Hardcoded secrets
DB_PASSWORD = "super_secret_db_pass_2026"
API_KEY = "sk-live-abc123def456ghi789"
AWS_SECRET = "wJalrXUt/EXAMPLEKEY/bPxRfiCY"

def setup_dev_env():
    os.environ["DATABASE_URL"] = f"postgresql://admin:{DB_PASSWORD}@localhost:5432/devdb"
    os.environ["API_KEY"] = API_KEY
    print("Dev environment configured!")

def create_test_data():
    """Seed the database with test users."""
    import sqlite3
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INT, username TEXT, password TEXT, role TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin')")
    conn.commit()

if __name__ == "__main__":
    setup_dev_env()
    create_test_data()
