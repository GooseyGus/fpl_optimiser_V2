import streamlit as st


def apply_custom_css():
    """Apply custom styling with specified color palette and minimal design."""
    st.markdown("""
        <style>
        /* Import clean, modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Color palette variables */
        :root {
            --color-1: #ECF4E8;
            --color-2: #CBF3BB;
            --color-3: #ABE7B2;
            --color-4: #93BFC7;
        }
        
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, var(--color-1) 0%, var(--color-2) 100%);
        }
        
        /* Hide Streamlit branding and header */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp > header {display: none;}
        
        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 2rem;
        }
        
        /* Welcome container */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 70vh;
            text-align: center;
        }
        
        /* Title styling - using darkest color from palette */
        .main-title {
            font-size: 4rem;
            font-weight: 600;
            color: #4A7C5D;
            margin-bottom: 2rem;
            letter-spacing: -0.02em;
        }
        
        /* Override Streamlit button styling */
        .stButton button {
            background: var(--color-4) !important;
            color: white !important;
            padding: 1.5rem 4rem !important;
            border-radius: 50px !important;
            border: none !important;
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(147, 191, 199, 0.3) !important;
            width: 100% !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(147, 191, 199, 0.4) !important;
            background: #7FA9B3 !important;
            border: none !important;
        }
        
        .stButton button:active,
        .stButton button:focus {
            background: var(--color-4) !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(147, 191, 199, 0.3) !important;
        }
        
        /* Metadata corner */
        .metadata {
            position: fixed;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.9);
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            font-size: 0.85rem;
            color: #5A7C65;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .metadata-item {
            margin: 0.25rem 0;
        }
        
        /* Brand indicator */
        .brand-colors {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            justify-content: center;
        }
        
        .color-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)


def show_metadata():
    """Display metadata in top-right corner."""
    st.markdown("""
        <div class="metadata">
            <div class="metadata-item"><strong>v1.0.0</strong></div>
            <div class="metadata-item">Data: FPL API</div>
            <div class="metadata-item">Updated: Live</div>
        </div>
    """, unsafe_allow_html=True)


def show_home_page():
    """Render the home page with welcome screen."""
    apply_custom_css()
    show_metadata()
    
    # Welcome container
    st.markdown("""
        <div class="welcome-container">
            <h1 class="main-title">FPL Optimiser</h1>
            <div class="brand-colors">
                <div class="color-dot" style="background: #ECF4E8;"></div>
                <div class="color-dot" style="background: #CBF3BB;"></div>
                <div class="color-dot" style="background: #ABE7B2;"></div>
                <div class="color-dot" style="background: #93BFC7;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the enter button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Enter", key="enter_button", use_container_width=True):
            st.session_state.entered = True
            st.rerun()


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="FPL Optimiser",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if 'entered' not in st.session_state:
        st.session_state.entered = False
    
    # Route to appropriate page
    if not st.session_state.entered:
        show_home_page()
    else:
        # Placeholder for main app (to be built)
        st.title("FPL Optimiser Dashboard")
        st.write("Main application interface will go here")
        
        if st.button("← Back to Home"):
            st.session_state.entered = False
            st.rerun()


if __name__ == "__main__":
    main()
