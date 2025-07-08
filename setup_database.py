#!/usr/bin/env python3
"""
Database setup script for Walmart Risk Detection System
Creates sample data for hackathon demo
"""

import sqlite3
import os

def create_sqlite_database():
    """Create SQLite database with sample data"""
    db_path = "walmart_risk.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create centers table
    cursor.execute("""
    CREATE TABLE centers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL
    )
    """)
    
    # Create shops table
    cursor.execute("""
    CREATE TABLE shops (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        risk TEXT NOT NULL,
        analysis TEXT NOT NULL
    )
    """)
    
    # Insert sample Walmart centers (major US cities)
    centers_data = [
        (1, "Walmart Supercenter Dallas", 32.7767, -96.7970),
        (2, "Walmart Supercenter Houston", 29.7604, -95.3698),
        (3, "Walmart Supercenter Phoenix", 33.4484, -112.0740),
        (4, "Walmart Supercenter Chicago", 41.8781, -87.6298),
        (5, "Walmart Supercenter Miami", 25.7617, -80.1918)
    ]
    
    cursor.executemany("INSERT INTO centers (id, name, lat, lon) VALUES (?, ?, ?, ?)", centers_data)
    
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
    
    cursor.executemany("INSERT INTO shops (id, name, lat, lon, risk, analysis) VALUES (?, ?, ?, ?, ?, ?)", shops_data)
    
    conn.commit()
    conn.close()
    
    print("✅ SQLite database created successfully!")
    print(f"📍 Database location: {os.path.abspath(db_path)}")
    print("📊 Sample data loaded:")
    print(f"   - {len(centers_data)} Walmart Centers")
    print(f"   - {len(shops_data)} Supplier Shops")
    
def create_postgresql_setup():
    """Create PostgreSQL setup SQL file"""
    sql_content = """
-- Walmart Risk Detection Database Setup
-- Run this in PostgreSQL after creating database

-- Create centers table
CREATE TABLE IF NOT EXISTS centers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lat DECIMAL(10, 6) NOT NULL,
    lon DECIMAL(10, 6) NOT NULL
);

-- Create shops table  
CREATE TABLE IF NOT EXISTS shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lat DECIMAL(10, 6) NOT NULL,
    lon DECIMAL(10, 6) NOT NULL,
    risk VARCHAR(20) NOT NULL CHECK (risk IN ('low', 'medium', 'high')),
    analysis TEXT NOT NULL
);

-- Insert sample Walmart centers
INSERT INTO centers (id, name, lat, lon) VALUES
(1, 'Walmart Supercenter Dallas', 32.7767, -96.7970),
(2, 'Walmart Supercenter Houston', 29.7604, -95.3698),
(3, 'Walmart Supercenter Phoenix', 33.4484, -112.0740),
(4, 'Walmart Supercenter Chicago', 41.8781, -87.6298),
(5, 'Walmart Supercenter Miami', 25.7617, -80.1918);

-- Insert sample shops
INSERT INTO shops (id, name, lat, lon, risk, analysis) VALUES
(1, 'Tech Electronics Store', 32.7850, -96.8000, 'high', 
 'High risk due to inventory discrepancies and frequent supplier delays. Recent audit revealed 15% shortage in electronics inventory. Supplier reliability score: 2.3/10. Recommended actions: Immediate supplier review, enhanced tracking systems, daily inventory audits.'),
 
(2, 'Fresh Grocery Mart', 32.7700, -96.7800, 'low', 
 'Low risk supplier with excellent track record. 99.2% on-time delivery rate, consistent quality standards, and strong financial position. Regular certifications up to date. Recommended for expanded partnership.'),
 
(3, 'Fashion Outlet Center', 32.7900, -96.8100, 'medium', 
 'Medium risk due to seasonal demand fluctuations and occasional quality control issues. 85% delivery performance, some customer complaints about fabric quality. Requires quarterly quality assessments and demand forecasting improvements.'),
 
(4, 'Auto Parts Warehouse', 32.7600, -96.7900, 'high', 
 'High risk supplier with safety compliance concerns. Failed 2 safety inspections, delayed shipments affecting 12% of orders. Financial instability detected. Immediate corrective actions required: safety audit, financial review, alternative supplier sourcing.'),
 
(5, 'Home & Garden Supply', 32.7750, -96.7850, 'low', 
 'Excellent supplier performance with sustainable practices. LEED certified facilities, 98% accuracy rate, strong ESG compliance. Innovation partnership potential in eco-friendly products.'),
 
(6, 'Sports Equipment Co', 32.7820, -96.8050, 'medium', 
 'Moderate risk due to limited production capacity during peak seasons. Good quality standards but struggles with volume demands during holidays. Capacity planning and backup supplier arrangements recommended.'),
 
(7, 'Beauty & Personal Care', 32.7680, -96.7750, 'low', 
 'Reliable supplier with FDA compliance and quality certifications. Strong brand portfolio, consistent delivery, competitive pricing. Suitable for long-term strategic partnership.'),
 
(8, 'Pharmacy Supplies Inc', 32.7880, -96.7980, 'high', 
 'Critical risk due to regulatory compliance issues. DEA license under review, temperature control failures in 3 shipments. Patient safety concerns identified. Immediate suspension recommended pending full compliance audit.'),
 
(9, 'Toys & Games Distributor', 32.7720, -96.8020, 'medium', 
 'Medium risk supplier with seasonal performance variations. Strong Q4 performance but struggles in off-seasons. Safety testing compliance good, but inventory management needs improvement.'),
 
(10, 'Office Supplies Hub', 32.7800, -96.7920, 'low', 
 'Consistent low-risk supplier with B2B specialization. Excellent bulk order handling, digital integration capabilities, competitive pricing. Recommended for expanded office supplies category.');

-- Reset sequences
SELECT setval('centers_id_seq', (SELECT MAX(id) FROM centers));
SELECT setval('shops_id_seq', (SELECT MAX(id) FROM shops));
"""
    
    with open("postgresql_setup.sql", "w") as f:
        f.write(sql_content)
    
    print("📄 PostgreSQL setup file created: postgresql_setup.sql")

if __name__ == "__main__":
    print("🏪 Walmart Risk Detection Database Setup")
    print("=" * 50)
    
    # Create SQLite database (immediate use)
    create_sqlite_database()
    
    print()
    
    # Create PostgreSQL setup file
    create_postgresql_setup()
    
    print("\n🎯 Next Steps:")
    print("1. For immediate testing: Use SQLite (already created)")
    print("2. For PostgreSQL: Run the postgresql_setup.sql file in your PostgreSQL database")
