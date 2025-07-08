import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Get PostgreSQL database connection"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    return conn

def get_center(center_id):
    """Get Walmart center information by ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, lat, lon FROM centers WHERE id = %s", (center_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def get_shops():
    """Get all shops with risk analysis"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, lat, lon, risk, analysis FROM shops")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_shops_by_risk(risk_level):
    """Get shops filtered by risk level"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, lat, lon, risk, analysis FROM shops WHERE risk = %s", (risk_level,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_shop_by_id(shop_id):
    """Get specific shop by ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, lat, lon, risk, analysis FROM shops WHERE id = %s", (shop_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row