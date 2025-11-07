import pandas as pd
from pathlib import Path


def load_all_gameweek_data():
    """
    Load the single gameweek data CSV.
    
    Returns:
        DataFrame: All gameweek data.
    """
    data_file = Path(__file__).parent.parent.parent.parent / "data" / "gameweek_data" / "gameweek_data.csv"
    
    if not data_file.exists():
        return pd.DataFrame()
    
    try:
        return pd.read_csv(data_file)
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()


def get_data_summary(df):
    """
    Get summary statistics for the data.
    
    Args:
        df: DataFrame to summarize.
        
    Returns:
        dict: Summary statistics.
    """
    if df.empty:
        return {
            'total_records': 0,
            'gameweeks': 0,
            'players': 0,
            'teams': 0
        }
    
    return {
        'total_records': len(df),
        'gameweeks': df['gameweek'].nunique() if 'gameweek' in df.columns else 0,
        'players': df['player_name'].nunique() if 'player_name' in df.columns else 0,
        'teams': df['team'].nunique() if 'team' in df.columns else 0
    }
