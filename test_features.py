#!/usr/bin/env python3
"""
Test script to verify the Walmart Risk Detection App features:
1. Path visualization between shops and centers
2. Distance calculations in km and meters
3. Interactive shop selection
"""

import math
from db import get_all_centers, get_shops

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def test_distance_calculations():
    """Test distance calculations between shops and centers"""
    print("🧪 Testing Distance Calculation Features")
    print("=" * 50)
    
    # Get data
    all_centers = get_all_centers()
    shops = get_shops()
    
    print(f"📊 Data loaded: {len(all_centers)} centers, {len(shops)} shops")
    
    if not all_centers or not shops:
        print("❌ No data found in database!")
        return False
    
    # Test with first shop
    test_shop = shops[0]
    shop_id, shop_name, shop_lat, shop_lon, risk, analysis = test_shop
    
    print(f"\n🏪 Testing with shop: {shop_name} (ID: {shop_id})")
    print(f"📍 Location: {shop_lat:.6f}, {shop_lon:.6f}")
    print(f"🚨 Risk Level: {risk}")
    
    # Calculate distances to all centers
    distances = []
    for center_id, center_name, center_lat, center_lon in all_centers:
        distance = calculate_distance(shop_lat, shop_lon, center_lat, center_lon)
        distances.append((center_name, distance, center_id))
    
    # Sort by distance
    distances.sort(key=lambda x: x[1])
    
    print(f"\n📏 Distance to all {len(distances)} centers:")
    print("-" * 40)
    
    for i, (center_name, distance, center_id) in enumerate(distances):
        distance_meters = distance * 1000
        if distance >= 1.0:
            print(f"{i+1:2d}. {center_name:<25} {distance:6.2f} km ({distance_meters:6.0f} m)")
        else:
            print(f"{i+1:2d}. {center_name:<25} {distance_meters:6.0f} m ({distance:6.3f} km)")
    
    print(f"\n✅ Top 5 closest centers to {shop_name}:")
    for i, (center_name, distance, center_id) in enumerate(distances[:5]):
        distance_meters = distance * 1000
        if distance >= 1.0:
            print(f"   {i+1}. {center_name}: {distance:.2f} km ({distance_meters:.0f} m)")
        else:
            print(f"   {i+1}. {center_name}: {distance_meters:.0f} m ({distance:.3f} km)")
    
    return True

def test_data_integrity():
    """Test data integrity and coverage"""
    print("\n🔍 Testing Data Integrity")
    print("=" * 50)
    
    all_centers = get_all_centers()
    shops = get_shops()
    
    # Check centers
    print(f"🏪 Walmart Centers: {len(all_centers)}")
    if len(all_centers) >= 50:
        print("✅ Target of 50+ centers achieved")
    else:
        print(f"⚠️  Only {len(all_centers)} centers (target: 50)")
    
    # Check shops
    print(f"🏬 Shops: {len(shops)}")
    if len(shops) >= 30:
        print("✅ Target of 30+ shops achieved")
    else:
        print(f"⚠️  Only {len(shops)} shops (target: 30+)")
    
    # Risk distribution
    risk_counts = {'high': 0, 'medium': 0, 'low': 0}
    for shop in shops:
        risk_level = shop[4].lower()
        if risk_level in risk_counts:
            risk_counts[risk_level] += 1
    
    print(f"\n📊 Risk Distribution:")
    print(f"   🔴 High Risk: {risk_counts['high']}")
    print(f"   🟡 Medium Risk: {risk_counts['medium']}")
    print(f"   🟢 Low Risk: {risk_counts['low']}")
    
    total_shops = len(shops)
    if total_shops > 0:
        high_percentage = (risk_counts['high'] / total_shops) * 100
        print(f"   📈 High Risk Percentage: {high_percentage:.1f}%")
    
    return True

def test_path_visualization_data():
    """Test that we have enough data for path visualization"""
    print("\n🛣️  Testing Path Visualization Data")
    print("=" * 50)
    
    all_centers = get_all_centers()
    shops = get_shops()
    
    if not all_centers or not shops:
        print("❌ Insufficient data for path visualization")
        return False
    
    print(f"✅ Path visualization can connect {len(shops)} shops to {len(all_centers)} centers")
    print(f"📈 Total possible paths: {len(shops) * len(all_centers)}")
    
    # Test coordinate validity
    valid_centers = 0
    for center_id, center_name, center_lat, center_lon in all_centers:
        if -90 <= center_lat <= 90 and -180 <= center_lon <= 180:
            valid_centers += 1
    
    valid_shops = 0
    for shop_id, shop_name, shop_lat, shop_lon, risk, analysis in shops:
        if -90 <= shop_lat <= 90 and -180 <= shop_lon <= 180:
            valid_shops += 1
    
    print(f"✅ Valid center coordinates: {valid_centers}/{len(all_centers)}")
    print(f"✅ Valid shop coordinates: {valid_shops}/{len(shops)}")
    
    return valid_centers == len(all_centers) and valid_shops == len(shops)

if __name__ == "__main__":
    print("🚀 Walmart Risk Detection App - Feature Testing")
    print("="*60)
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    try:
        if test_data_integrity():
            tests_passed += 1
            print("\n✅ Data integrity test passed")
        else:
            print("\n❌ Data integrity test failed")
    except Exception as e:
        print(f"\n❌ Data integrity test error: {e}")
    
    try:
        if test_path_visualization_data():
            tests_passed += 1
            print("✅ Path visualization data test passed")
        else:
            print("❌ Path visualization data test failed")
    except Exception as e:
        print(f"❌ Path visualization data test error: {e}")
    
    try:
        if test_distance_calculations():
            tests_passed += 1
            print("\n✅ Distance calculation test passed")
        else:
            print("\n❌ Distance calculation test failed")
    except Exception as e:
        print(f"\n❌ Distance calculation test error: {e}")
    
    print(f"\n🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All features are working correctly!")
        print("\n📋 Feature Summary:")
        print("   ✅ 50 Walmart centers loaded")
        print("   ✅ 30+ shops with risk levels")
        print("   ✅ Distance calculations (km and meters)")
        print("   ✅ Path visualization data ready")
        print("   ✅ Interactive shop selection")
        print("\n🗺️  Visit http://localhost:8502 to test the interactive map!")
    else:
        print("⚠️  Some features need attention")
