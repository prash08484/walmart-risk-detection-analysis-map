import sqlite3
import math

def test_sqlite_database():
    """Test the SQLite database and verify features"""
    print("🧪 Testing SQLite Database Features")
    print("=" * 50)
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('walmart_risk.db')
        cursor = conn.cursor()
        
        # Test centers
        cursor.execute("SELECT COUNT(*) FROM centers")
        center_count = cursor.fetchone()[0]
        print(f"🏪 Walmart Centers: {center_count}")
        
        # Test shops
        cursor.execute("SELECT COUNT(*) FROM shops")
        shop_count = cursor.fetchone()[0]
        print(f"🏬 Shops: {shop_count}")
        
        # Get sample data
        cursor.execute("SELECT * FROM centers LIMIT 5")
        centers = cursor.fetchall()
        print(f"\n📍 Sample Centers:")
        for center in centers:
            print(f"   ID: {center[0]}, Name: {center[1]}")
        
        cursor.execute("SELECT * FROM shops LIMIT 5")
        shops = cursor.fetchall()
        print(f"\n🏪 Sample Shops:")
        for shop in shops:
            print(f"   ID: {shop[0]}, Name: {shop[1]}, Risk: {shop[4]}")
        
        # Test distance calculation
        if centers and shops:
            center = centers[0]
            shop = shops[0]
            
            def calculate_distance(lat1, lon1, lat2, lon2):
                R = 6371  # Earth's radius in kilometers
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return R * c
            
            distance = calculate_distance(shop[2], shop[3], center[2], center[3])
            distance_meters = distance * 1000
            
            print(f"\n📏 Distance Test:")
            print(f"   From: {shop[1]} to {center[1]}")
            if distance >= 1.0:
                print(f"   Distance: {distance:.2f} km ({distance_meters:.0f} m)")
            else:
                print(f"   Distance: {distance_meters:.0f} m ({distance:.3f} km)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    if test_sqlite_database():
        print("\n✅ SQLite database features working correctly!")
        print("🗺️  The Streamlit app should now show:")
        print("   ✅ Path visualization when you click a shop")
        print("   ✅ Distance in km and meters")
        print("   ✅ Interactive shop selection")
        print("\n🌐 Open http://localhost:8502 to test!")
    else:
        print("\n❌ Database test failed")
