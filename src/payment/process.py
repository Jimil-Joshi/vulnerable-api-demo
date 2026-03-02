"""Payment processing module."""
import sqlite3
from flask import request, jsonify

def process_payment():
    user_id = request.form.get("user_id")
    amount = request.form.get("amount")
    card = request.form.get("card_number")

    # VULNERABLE: SQL injection in payment query
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO transactions (user_id, amount, card) VALUES ({user_id}, {amount}, '{card}')"
    )
    conn.commit()
    return jsonify({"status": "processed", "amount": amount})

def get_transaction_history(user_id):
    # VULNERABLE: SQL injection
    conn = sqlite3.connect("payments.db")
    result = conn.execute(f"SELECT * FROM transactions WHERE user_id = {user_id}").fetchall()
    return result

def refund(transaction_id):
    conn = sqlite3.connect("payments.db")
    conn.execute(f"UPDATE transactions SET status='refunded' WHERE id={transaction_id}")
    conn.commit()
    return {"refunded": True}