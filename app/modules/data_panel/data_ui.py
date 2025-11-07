import streamlit as st
from .data_service import load_all_gameweek_data, get_data_summary


def render_data_panel():
    """Render the data panel UI."""
    st.header("Gameweek Data")
    
    with st.spinner("Loading data..."):
        df = load_all_gameweek_data()
    
    if df.empty:
        st.warning("No gameweek data found. Run the data collection scripts first.")
        return
    
    # Get summary stats
    summary = get_data_summary(df)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{summary['total_records']:,}")
    with col2:
        st.metric("Gameweeks", summary['gameweeks'])
    with col3:
        st.metric("Players", summary['players'])
    with col4:
        st.metric("Teams", summary['teams'])
    
    st.markdown("---")
    
    # Display the data table
    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="fpl_all_gameweeks.csv",
        mime="text/csv"
    )
