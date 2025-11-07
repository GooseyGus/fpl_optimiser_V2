import streamlit as st
from modules.data_panel.data_ui import render_data_panel


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="FPL Optimiser",
        page_icon="⚽",
        layout="wide"
    )
    
    # Simple color scheme with CSS
    st.markdown("""
        <style>
        /* Color scheme: Professional blues and grays */
        :root {
            --primary-blue: #2E5C8A;
            --accent-blue: #4A90E2;
            --light-gray: #F5F7FA;
            --border-gray: #E1E8ED;
            --text-dark: #1A1A1A;
            --text-gray: #5F6368;
        }
        
        /* Main background */
        .stApp {
            background-color: var(--light-gray);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: var(--primary-blue);
            font-weight: 600;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: white;
            padding: 0.5rem;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--light-gray);
            color: var(--text-gray);
            border-radius: 6px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-blue);
            color: white;
        }
        
        /* Data table styling */
        .dataframe {
            font-size: 0.9rem;
        }
        
        /* Remove extra padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("⚽ FPL Optimiser")
    
    # Tabs for different panels
    tabs = st.tabs(["📊 Data"])
    
    with tabs[0]:  # Data tab
        render_data_panel()


if __name__ == "__main__":
    main()
