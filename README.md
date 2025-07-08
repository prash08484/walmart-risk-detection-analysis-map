# 🛡️ Walmart Risk Detection App

A professional interactive web application for visualizing and analyzing risk factors associated with Walmart distribution centers and their supplier network. Built with Streamlit and featuring real-time map visualization, this app helps identify potential supply chain vulnerabilities and operational risks.

## 🎯 Project Overview

This application provides a comprehensive risk assessment dashboard for Walmart's supply chain operations, allowing users to:

- **Visualize Distribution Centers**: Interactive map showing Walmart centers with risk-based color coding
- **Monitor Supplier Network**: Track supplier shops and their risk levels
- **Risk Analysis**: Click on locations for detailed risk breakdowns and analytics
- **Real-time Filtering**: Filter locations by risk level and view statistics
- **Professional Dashboard**: Clean, intuitive interface with comprehensive data insights

## 🚀 Tech Stack

### Frontend
- **Streamlit**: Modern web app framework for the dashboard
- **Folium**: Interactive map visualization
- **Streamlit-Folium**: Seamless integration between Streamlit and Folium maps

### Backend & Database
- **PostgreSQL**: Production database (Neon cloud or local)
- **SQLite**: Development/demo database
- **psycopg2**: PostgreSQL adapter for Python
- **python-dotenv**: Environment variable management

### Additional Libraries
- **Pandas**: Data manipulation and analysis
- **Branca**: Enhanced map styling and elements

## 📊 Features

### 🗺️ Interactive Map
- **Risk-based Color Coding**: Green (Low), Yellow (Medium), Red (High)
- **Clickable Markers**: Detailed popups with location information
- **Multiple Map Styles**: OpenStreetMap, CartoDB, Stamen terrain options
- **Zoom Controls**: Navigate and explore different regions

### 📈 Analytics Dashboard
- **Risk Distribution**: Real-time statistics on risk levels
- **Location Filtering**: Filter by risk level (Low, Medium, High)
- **Data Insights**: Total locations, risk breakdowns, and trends
- **Professional UI**: Clean sidebar controls and organized layout

### 🔄 Database Flexibility
- **Dual Database Support**: SQLite for development, PostgreSQL for production
- **Cloud Integration**: Ready for Neon PostgreSQL deployment
- **Sample Data**: Pre-loaded with realistic Walmart and supplier locations

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- PostgreSQL (optional, for production setup)

### 1. Clone or Download the Project
```bash
# Navigate to your project directory
cd "c:\Users\prash\OneDrive\Desktop\Prash08484\Entire-Project"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Quick Start (SQLite)
```bash
python setup_database.py
```
This creates a local SQLite database with sample data for immediate testing.

#### Option B: PostgreSQL Local Setup
```bash
python setup_postgres.py
```
Requires local PostgreSQL installation.

#### Option C: Neon Cloud Setup (Recommended for Production)
1. Create a free account at [Neon.tech](https://neon.tech)
2. Create a new database
3. Update `.env` file with your Neon credentials:
```
DATABASE_URL=postgresql://username:password@hostname/database
DB_HOST=your-hostname
DB_NAME=your-database
DB_USER=your-username
DB_PASSWORD=your-password
DB_PORT=5432
```
4. Run the Neon setup:
```bash
python setup_neon.py
```

### 4. Launch the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📱 Usage Guide

### Getting Started
1. **Launch the app** using the command above
2. **Select database type** (the app will automatically detect your setup)
3. **Use the sidebar** to filter locations by risk level
4. **Choose map style** from the dropdown options
5. **Click on markers** for detailed location information

### Dashboard Features

#### Map Interactions
- **Zoom & Pan**: Navigate the map to explore different regions
- **Marker Clicks**: Click any marker for detailed popup information
- **Legend**: Color-coded legend shows risk levels (Green/Yellow/Red)

#### Sidebar Controls
- **Risk Level Filter**: Show only locations with specific risk levels
- **Map Style Selector**: Choose from multiple map visualization styles
- **Statistics Panel**: Real-time counts and risk distribution

#### Location Details
Each marker popup displays:
- Location name and type (Walmart Center or Supplier)
- Complete address
- Risk level and score
- Additional relevant details

## 🏗️ Project Structure

```
Entire-Project/
├── app.py                 # Main Streamlit application
├── db.py                  # Database connection and operations
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── setup_database.py      # SQLite setup with sample data
├── setup_postgres.py      # Local PostgreSQL setup
├── setup_neon.py         # Neon cloud database setup
├── postgres_setup.py     # Alternative PostgreSQL setup
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database Configuration
DATABASE_URL=your_database_url
DB_HOST=your_host
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
```

### Database Schema
The application uses two main tables:
- **walmart_centers**: Distribution center locations with risk assessments
- **supplier_shops**: Supplier locations with risk evaluations

## 🎨 Customization

### Adding New Locations
1. Connect to your database
2. Insert new records into `walmart_centers` or `supplier_shops` tables
3. Include coordinates (latitude, longitude) and risk assessment data
4. Restart the application to see new locations

### Styling Options
- Modify map styles in `app.py`
- Customize color schemes for risk levels
- Adjust popup content and formatting
- Update sidebar layout and controls

## 🚀 Deployment

### Local Development
- Use SQLite setup for quick local development
- All features available without external dependencies

### Production Deployment
- Use Neon PostgreSQL for cloud database
- Deploy to Streamlit Cloud, Heroku, or other platforms
- Ensure environment variables are properly configured

## 🤝 Contributing

This project was developed for hackathon demonstration purposes. For improvements or modifications:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is available for educational and demonstration purposes. Please respect Walmart's trademarks and use this only for learning and portfolio demonstration.

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Errors
- Verify `.env` file contains correct credentials
- Check if PostgreSQL service is running (for local setup)
- Confirm Neon database is accessible (for cloud setup)

#### Map Not Loading
- Check internet connection
- Verify Folium and Streamlit-Folium are properly installed
- Clear browser cache and restart the application

#### Dependencies Issues
```bash
pip install --upgrade -r requirements.txt
```

#### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Support
For technical issues or questions, review the code comments and error messages. The application includes comprehensive error handling and informative messages.

---

**Built with ❤️ for supply chain risk analysis and hackathon innovation.**
