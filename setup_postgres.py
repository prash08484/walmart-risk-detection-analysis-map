#!/usr/bin/env python3
"""
PostgreSQL setup script for Walmart Risk Detection System
Creates PostgreSQL database and tables with sample data
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (default database)
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "postgres123"),
            database="postgres"  # Connect to default database first
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        db_name = os.getenv("DB_NAME", "walmart_risk_db")
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database '{db_name}' created successfully!")
        else:
            print(f"ℹ️ Database '{db_name}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def setup_tables_and_data():
    """Create tables and insert sample data"""
    try:
        # Connect to the walmart database
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "walmart_risk_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "postgres123")
        )
        cursor = conn.cursor()
        
        # Create centers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS centers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            lat DECIMAL(10, 6) NOT NULL,
            lon DECIMAL(10, 6) NOT NULL
        )
        """)
        
        # Create shops table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            lat DECIMAL(10, 6) NOT NULL,
            lon DECIMAL(10, 6) NOT NULL,
            risk VARCHAR(20) NOT NULL CHECK (risk IN ('low', 'medium', 'high')),
            analysis TEXT NOT NULL
        )
        """)
        
        # Clear existing data (for fresh setup)
        cursor.execute("DELETE FROM shops")
        cursor.execute("DELETE FROM centers")
        
        # Insert sample Walmart centers
        centers_data = [
            (1, "Walmart Supercenter Dallas", 32.7767, -96.7970),
            (2, "Walmart Supercenter Houston", 29.7604, -95.3698),
            (3, "Walmart Supercenter Phoenix", 33.4484, -112.0740),
            (4, "Walmart Supercenter Chicago", 41.8781, -87.6298),
            (5, "Walmart Supercenter Miami", 25.7617, -80.1918)
        ]
        
        cursor.executemany(
            "INSERT INTO centers (id, name, lat, lon) VALUES (%s, %s, %s, %s)",
            centers_data
        )
        
        # Insert sample shops around Dallas (for demo)
        shops_data = [
            (1, "Tech Electronics Store", 32.7850, -96.8000, "high", 
             "High risk due to inventory discrepancies and frequent supplier delays. Recent audit revealed 15% shortage in electronics inventory. Supplier reliability score: 2.3/10. Recommended actions: Immediate supplier review, enhanced tracking systems, daily inventory audits."),
            
            (2, "Fresh Grocery Mart", 32.7700, -96.7800, "low", 
             "Low risk supplier with excellent track record. 99.2% on-time delivery rate, consistent quality standards, and strong financial position. Regular certifications up to date. Recommended for expanded partnership."),
            
            (3, "Fashion Outlet Center", 32.7900, -96.8100, "medium", 
             "Medium risk due to seasonal demand fluctuations and occasional quality control issues. 85% delivery performance, some customer complaints about fabric quality. Requires quarterly quality assessments and demand forecasting improvements."),
            
            (4, "Auto Parts Warehouse", 32.7600, -96.7900, "high", 
             "High risk supplier with safety compliance concerns. Failed 2 safety inspections, delayed shipments affecting 12% of orders. Financial instability detected. Immediate corrective actions required: safety audit, financial review, alternative supplier sourcing."),
            
            (5, "Home & Garden Supply", 32.7750, -96.7850, "low", 
             "Excellent supplier performance with sustainable practices. LEED certified facilities, 98% accuracy rate, strong ESG compliance. Innovation partnership potential in eco-friendly products."),
            
            (6, "Sports Equipment Co", 32.7820, -96.8050, "medium", 
             "Moderate risk due to limited production capacity during peak seasons. Good quality standards but struggles with volume demands during holidays. Capacity planning and backup supplier arrangements recommended."),
            
            (7, "Beauty & Personal Care", 32.7680, -96.7750, "low", 
             "Reliable supplier with FDA compliance and quality certifications. Strong brand portfolio, consistent delivery, competitive pricing. Suitable for long-term strategic partnership."),
            
            (8, "Pharmacy Supplies Inc", 32.7880, -96.7980, "high", 
             "Critical risk due to regulatory compliance issues. DEA license under review, temperature control failures in 3 shipments. Patient safety concerns identified. Immediate suspension recommended pending full compliance audit."),
            
            (9, "Toys & Games Distributor", 32.7720, -96.8020, "medium", 
             "Medium risk supplier with seasonal performance variations. Strong Q4 performance but struggles in off-seasons. Safety testing compliance good, but inventory management needs improvement."),
            
            (10, "Office Supplies Hub", 32.7800, -96.7920, "low", 
             "Consistent low-risk supplier with B2B specialization. Excellent bulk order handling, digital integration capabilities, competitive pricing. Recommended for expanded office supplies category.")
        ]
        
        cursor.executemany(
            "INSERT INTO shops (id, name, lat, lon, risk, analysis) VALUES (%s, %s, %s, %s, %s, %s)",
            shops_data
        )
        
        # Reset sequences
        cursor.execute("SELECT setval('centers_id_seq', (SELECT MAX(id) FROM centers))")
        cursor.execute("SELECT setval('shops_id_seq', (SELECT MAX(id) FROM shops))")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ PostgreSQL tables created and data inserted successfully!")
        print("📊 Sample data loaded:")
        print(f"   - {len(centers_data)} Walmart Centers")
        print(f"   - {len(shops_data)} Supplier Shops")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error setting up tables: {e}")
        return False

def test_connection():
    """Test the database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "walmart_risk_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "postgres123")
        )
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM centers")
        centers_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM shops")
        shops_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"🔗 Database connection successful!")
        print(f"📍 Centers in database: {centers_count}")
        print(f"🏪 Shops in database: {shops_count}")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🏪 Walmart Risk Detection PostgreSQL Setup")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please update your .env file with PostgreSQL credentials")
        exit(1)
    
    print("🔧 Setting up PostgreSQL database...")
    
    # Step 1: Create database
    if create_database():
        # Step 2: Create tables and insert data
        if setup_tables_and_data():
            # Step 3: Test connection
            if test_connection():
                print("\n🎉 PostgreSQL setup completed successfully!")
                print("🚀 You can now run your Streamlit app: streamlit run app.py")
            else:
                print("\n❌ Setup completed but connection test failed")
        else:
            print("\n❌ Failed to create tables and data")
    else:
        print("\n❌ Failed to create database")
