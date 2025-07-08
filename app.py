import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
from db import get_center, get_shops
import json

st.set_page_config(page_title="Walmart Risk Detection Map", layout="wide")

st.title("🏪 Walmart Risk Detection Map")
st.markdown("---")

# Sidebar for controls
with st.sidebar:
    st.header("🎛️ Map Controls")
    center_id = st.text_input("Enter Walmart Center ID:", value="1", help="Enter the ID of the Walmart center to focus on")
    
    # Map style options
    map_style = st.selectbox(
        "Map Style:",
        ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark_Matter"],
        index=1
    )
    
    # Risk filter
    st.subheader("Risk Level Filter")
    show_high = st.checkbox("High Risk", value=True)
    show_medium = st.checkbox("Medium Risk", value=True) 
    show_low = st.checkbox("Low Risk", value=True)
    
    # Legend
    st.subheader("📍 Map Legend")
    st.markdown("""
    - 🏪 **Blue**: Walmart Center
    - 🔴 **Red**: High Risk Shop
    - 🟡 **Yellow**: Medium Risk Shop  
    - 🟢 **Green**: Low Risk Shop
    """)

center = get_center(center_id)

if not center:
    st.error("❌ Walmart Center not found! Please check the Center ID.")
    st.info("💡 Make sure you have entered a valid Walmart Center ID in the sidebar.")
    st.stop()

center_id, center_name, center_lat, center_lon = center
shops = get_shops()

# Filter shops based on risk level selection
filtered_shops = []
risk_filter = {
    'high': show_high,
    'medium': show_medium, 
    'low': show_low
}

for shop in shops:
    shop_risk = shop[4].lower()
    if risk_filter.get(shop_risk, True):
        filtered_shops.append(shop)

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"### 🎯 Focus: **{center_name}** (ID: {center_id})")
    st.markdown(f"📍 **Coordinates:** {center_lat:.4f}, {center_lon:.4f}")
    
    # Map tiles configuration
    tile_mapping = {
        "OpenStreetMap": "OpenStreetMap",
        "CartoDB Positron": "CartoDB positron", 
        "CartoDB Dark_Matter": "CartoDB dark_matter"
    }
    
    # Create the map with enhanced styling
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=13,
        tiles=tile_mapping[map_style]
    )
    
    # Add custom CSS for better styling
    m.get_root().html.add_child(folium.Element("""
    <style>
    .leaflet-popup-content-wrapper {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .leaflet-popup-content {
        font-family: 'Arial', sans-serif;
        line-height: 1.4;
    }
    </style>
    """))
    
    # Add Walmart center marker with custom styling
    walmart_popup = f"""
    <div style='font-family: Arial; width: 200px;'>
        <h4 style='color: #0071ce; margin: 0;'>🏪 {center_name}</h4>
        <hr style='margin: 5px 0;'>
        <p><b>Center ID:</b> {center_id}</p>
        <p><b>Type:</b> Walmart Center</p>
        <p><b>Status:</b> <span style='color: green;'>Active</span></p>
    </div>
    """
    
    folium.Marker(
        [center_lat, center_lon],
        tooltip=f"🏪 Walmart Center: {center_name}",
        popup=folium.Popup(walmart_popup, max_width=250),
        icon=folium.Icon(
            color="blue", 
            icon="shopping-cart", 
            prefix="fa"
        )
    ).add_to(m)    # Enhanced risk color and icon mapping
    RISK_CONFIG = {
        "high": {"color": "red", "icon": "exclamation-triangle", "emoji": "🔴"},
        "medium": {"color": "orange", "icon": "exclamation-circle", "emoji": "🟡"}, 
        "low": {"color": "green", "icon": "check-circle", "emoji": "🟢"}
    }
    
    # Add shop markers with enhanced popups
    for shop_id, shop_name, shop_lat, shop_lon, risk, analysis in filtered_shops:
        risk_lower = risk.lower()
        config = RISK_CONFIG.get(risk_lower, {"color": "gray", "icon": "question", "emoji": "⚪"})
        
        # Create detailed popup
        shop_popup = f"""
        <div style='font-family: Arial; width: 250px;'>
            <h4 style='color: {config["color"]}; margin: 0;'>{config["emoji"]} {shop_name}</h4>
            <hr style='margin: 5px 0;'>
            <p><b>Shop ID:</b> {shop_id}</p>
            <p><b>Risk Level:</b> <span style='color: {config["color"]}; font-weight: bold;'>{risk.upper()}</span></p>
            <p><b>Location:</b> {shop_lat:.4f}, {shop_lon:.4f}</p>
            <div style='background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin-top: 8px;'>
                <b>Analysis Preview:</b><br>
                <small>{analysis[:100]}{"..." if len(analysis) > 100 else ""}</small>
            </div>
            <p style='font-size: 11px; color: #666; margin-top: 8px;'>Click marker for detailed analysis</p>
        </div>
        """
        
        folium.Marker(
            [shop_lat, shop_lon],
            tooltip=f"{config['emoji']} {shop_name} (Risk: {risk})",
            popup=folium.Popup(shop_popup, max_width=300),
            icon=folium.Icon(
                color=config["color"], 
                icon=config["icon"], 
                prefix="fa"
            ),
        ).add_to(m)
    
    # Add a circle around the Walmart center to show coverage area
    folium.Circle(
        location=[center_lat, center_lon],
        radius=2000,  # 2km radius
        popup=f"Coverage Area (2km radius)",
        color="#0071ce",
        fill=True,
        opacity=0.3,
        fillOpacity=0.1
    ).add_to(m)
    
    # Add plugins for better functionality
    plugins.Fullscreen().add_to(m)
    plugins.MeasureControl().add_to(m)
    
    # Display the map
    st.markdown("### 🗺️ Interactive Risk Detection Map")
    map_data = st_folium(m, width=1000, height=600, returned_objects=["last_object_clicked"])

with col2:
    st.markdown("### 📊 Map Statistics")
    
    total_shops = len(shops)
    filtered_count = len(filtered_shops)
    
    st.metric("Total Shops", total_shops)
    st.metric("Visible Shops", filtered_count)
    
    # Risk distribution
    if shops:
        risk_counts = {'high': 0, 'medium': 0, 'low': 0}
        for shop in shops:
            risk_level = shop[4].lower()
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
        
        st.markdown("#### Risk Distribution")
        st.markdown(f"🔴 High: {risk_counts['high']}")
        st.markdown(f"🟡 Medium: {risk_counts['medium']}")
        st.markdown(f"🟢 Low: {risk_counts['low']}")
        
        # Calculate risk percentage
        high_percentage = (risk_counts['high'] / total_shops) * 100 if total_shops > 0 else 0
        if high_percentage > 30:
            st.warning(f"⚠️ High risk shops: {high_percentage:.1f}%")
        elif high_percentage > 15:
            st.info(f"ℹ️ High risk shops: {high_percentage:.1f}%")
        else:
            st.success(f"✅ High risk shops: {high_percentage:.1f}%")# Handle marker clicks for detailed analysis
st.markdown("---")
if map_data and map_data.get("last_object_clicked"):
    popup_content = map_data["last_object_clicked"].get("popup")
    if popup_content and "Shop ID:" in popup_content:
        # Extract shop ID from popup
        try:
            shop_id_line = [line for line in popup_content.split('\n') if 'Shop ID:' in line][0]
            shop_id = int(shop_id_line.split('Shop ID:</b> ')[1].split('<')[0])
            
            # Find the selected shop
            selected_shop = next((s for s in shops if s[0] == shop_id), None)
            if selected_shop:
                _, shop_name, shop_lat, shop_lon, risk, analysis = selected_shop
                
                # Create detailed analysis section
                st.markdown("## 🔍 Detailed Shop Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Shop Name", shop_name)
                with col2:
                    risk_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk.lower(), "⚪")
                    st.metric("Risk Level", f"{risk_color} {risk.upper()}")
                with col3:
                    st.metric("Shop ID", shop_id)
                
                # Analysis details
                st.markdown("### 📋 Risk Analysis Report")
                st.markdown(f"**Location:** {shop_lat:.6f}, {shop_lon:.6f}")
                
                # Analysis in an expandable section
                with st.expander("📊 Full Analysis Details", expanded=True):
                    st.markdown(analysis)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📧 Generate Report"):
                        st.success("Report generation initiated!")
                with col2:
                    if st.button("🚨 Flag for Review"):
                        st.warning("Shop flagged for immediate review!")
                with col3:
                    if st.button("📞 Contact Shop"):
                        st.info("Contact information retrieved!")
                        
        except (IndexError, ValueError):
            st.error("Could not parse shop information from map click.")
            
# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    🏪 Walmart Risk Detection System | Built for Hackathon 2025
</div>
""", unsafe_allow_html=True)