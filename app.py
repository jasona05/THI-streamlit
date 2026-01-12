import streamlit as st
import pandas as pd
import pydeck as pdk

# Page configuration
st.set_page_config(
    page_title="THI Map Demo",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Sample Interactive Map")
st.markdown("---")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Select a page", ["Home", "Map"], index=1)

if page == "Home":
    st.header("Welcome!")
    st.write("This is a sample interactive map application.")
    st.write("Use the sidebar to navigate between different pages.")
    
    st.subheader("Features")
    st.markdown("""
    - **Map Visualization**: Interactive map of THI donations across Australia
    - **Data Display**: Data table showing the data used in the map
    - **Modern UI**: Clean and responsive design
    """)

elif page == "Map":
    # Sample data - Australian cities with donation information
    sample_data = pd.DataFrame({
        'lat': [-33.8688, -37.8136, -27.4698, -31.9505, -34.9285, -35.2809],
        'lon': [151.2093, 144.9631, 153.0251, 115.8605, 138.6007, 149.1300],
        'City': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Canberra'],
        'Donations': [1250, 980, 650, 420, 380, 280],
        'Total Amount': [125000, 98000, 65000, 42000, 38000, 28000]
    })
    
    # Create formatted tooltip text
    sample_data['tooltip'] = sample_data.apply(
        lambda row: f"{row['City']}\nDonations: {row['Donations']:,}\nTotal Amount: ${row['Total Amount']:,}",
        axis=1
    )
    
    st.subheader("Map View")
    
    # Hide info icon in bottom right corner of map and make contributors smaller
    st.markdown("""
        <style>
        /* Hide PyDeck info/attribution icon in bottom right */
        div[data-testid="stPydeckChart"] button[title*="Info"],
        div[data-testid="stPydeckChart"] button[aria-label*="Info"],
        div[data-testid="stPydeckChart"] div[style*="position: absolute"][style*="right"][style*="bottom"] button,
        div[data-testid="stPydeckChart"] iframe ~ div button[style*="position: absolute"],
        div[data-testid="stPydeckChart"] div[class*="info"],
        div[data-testid="stPydeckChart"] button[style*="bottom"][style*="right"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Make contributors/attribution text smaller */
        div[data-testid="stPydeckChart"] a[href*="carto"],
        div[data-testid="stPydeckChart"] a[href*="openstreetmap"],
        div[data-testid="stPydeckChart"] div[class*="attribution"],
        div[data-testid="stPydeckChart"] span[class*="attribution"],
        div[data-testid="stPydeckChart"] div[style*="position: absolute"][style*="bottom"] a,
        div[data-testid="stPydeckChart"] div[style*="position: absolute"][style*="bottom"] span {
            font-size: 8px !important;
            line-height: 1.2 !important;
        }
        </style>
        <script>
        // Hide info icon and make contributors smaller after map loads
        function hideInfoIconAndResizeContributors() {
            const mapContainer = document.querySelector('div[data-testid="stPydeckChart"]');
            if (mapContainer) {
                // Find all buttons in the map container
                const buttons = mapContainer.querySelectorAll('button');
                buttons.forEach(btn => {
                    const style = window.getComputedStyle(btn);
                    const rect = btn.getBoundingClientRect();
                    const containerRect = mapContainer.getBoundingClientRect();
                    // Check if button is in bottom right corner
                    if (rect.bottom > containerRect.bottom - 50 && rect.right > containerRect.right - 50) {
                        btn.style.display = 'none';
                        btn.style.visibility = 'hidden';
                    }
                });
                
                // Make contributors/attribution text smaller
                const attributions = mapContainer.querySelectorAll('a[href*="carto"], a[href*="openstreetmap"], div[class*="attribution"], span[class*="attribution"]');
                attributions.forEach(el => {
                    el.style.fontSize = '8px';
                    el.style.lineHeight = '1.2';
                });
            }
        }
        setTimeout(hideInfoIconAndResizeContributors, 500);
        setTimeout(hideInfoIconAndResizeContributors, 1500);
        </script>
    """, unsafe_allow_html=True)
    
    # State boundaries layer
    state_boundaries_layer = pdk.Layer(
        "GeoJsonLayer",
        data="https://raw.githubusercontent.com/rowanhogan/australian-states/master/states.geojson",
        stroked=True,
        filled=False,
        get_line_color=[100, 100, 100, 200],
        get_line_width=2,
        line_width_min_pixels=1,
    )
    
    # Map layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=sample_data,
        get_position=["lon", "lat"],
        get_fill_color=[30, 100, 200, 160],
        get_radius=50000,
        pickable=True,
    )
    
    # Set the viewport location - centered on Australia with restricted view
    view_state = pdk.ViewState(
        latitude=-28.0,  # Center of Australia (moved slightly lower)
        longitude=133.7751,  # Center of Australia
        zoom=3.4,  # Zoom level to show Australia
        pitch=0,
    )
    
    # Create view with zoom restrictions to keep focus on Australia
    view = pdk.View(type="MapView", controller=True, min_zoom=2.8, max_zoom=10)
    
    # Render with view restrictions
    r = pdk.Deck(
        layers=[state_boundaries_layer, layer],
        initial_view_state=view_state,
        views=[view],
        map_style=None,  # Uses default map style (no API token required)
        tooltip={"text": "{tooltip}"}
    )
    
    st.pydeck_chart(r, height=600)
    
    st.subheader("Data Points")
    # Format the dataframe for display
    display_data = sample_data[['City', 'Donations', 'Total Amount']].copy()
    display_data['Total Amount'] = display_data['Total Amount'].apply(lambda x: f"${x:,}")
    st.dataframe(display_data, width='stretch')

# Footer
st.markdown("---")
st.markdown("Built by RAP Media")
