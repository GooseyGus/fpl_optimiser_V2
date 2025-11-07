import requests
import pandas as pd
from pathlib import Path


def fetch_player_history(player_id):
    """
    Fetch complete gameweek history for a specific player.
    
    Args:
        player_id (int): FPL player ID
        
    Returns:
        dict: Player history data
    """
    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_bootstrap_data():
    """Fetch bootstrap data for player names and team info."""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def process_player_gameweek_data(player_id):
    """
    Get all gameweek data for a player.
    
    Args:
        player_id (int): FPL player ID
        
    Returns:
        pd.DataFrame: Complete gameweek history
    """
    # Get bootstrap for player info
    bootstrap = fetch_bootstrap_data()
    players = {p['id']: p for p in bootstrap['elements']}
    teams = {t['id']: t['name'] for t in bootstrap['teams']}
    
    player_info = players[player_id]
    
    # Get player history
    history_data = fetch_player_history(player_id)
    
    # Extract gameweek history
    gameweek_history = history_data['history']
    
    # Process into clean dataframe
    data = []
    for gw in gameweek_history:
        row = {
            'player_id': player_id,
            'player_name': player_info['web_name'],
            'full_name': f"{player_info['first_name']} {player_info['second_name']}",
            'team': teams.get(player_info['team'], 'Unknown'),
            'position': {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}.get(player_info['element_type']),
            'gameweek': gw['round'],
            'kickoff_time': gw['kickoff_time'],
            'opponent_team': teams.get(gw['opponent_team'], 'Unknown'),
            'was_home': gw['was_home'],
            'total_points': gw['total_points'],
            'minutes': gw['minutes'],
            'goals_scored': gw['goals_scored'],
            'assists': gw['assists'],
            'clean_sheets': gw['clean_sheets'],
            'goals_conceded': gw['goals_conceded'],
            'own_goals': gw['own_goals'],
            'penalties_saved': gw['penalties_saved'],
            'penalties_missed': gw['penalties_missed'],
            'yellow_cards': gw['yellow_cards'],
            'red_cards': gw['red_cards'],
            'saves': gw['saves'],
            'bonus': gw['bonus'],
            'bps': gw['bps'],
            'influence': gw['influence'],
            'creativity': gw['creativity'],
            'threat': gw['threat'],
            'ict_index': gw['ict_index'],
            'value': gw['value'] / 10,
            'transfers_balance': gw['transfers_balance'],
            'selected': gw['selected'],
            'transfers_in': gw['transfers_in'],
            'transfers_out': gw['transfers_out'],
            'expected_goals': gw['expected_goals'],
            'expected_assists': gw['expected_assists'],
            'expected_goal_involvements': gw['expected_goal_involvements'],
            'expected_goals_conceded': gw['expected_goals_conceded'],
        }
        data.append(row)
    
    return pd.DataFrame(data)


def main():
    """Test with David Raya (player_id = 1)."""
    print("Fetching David Raya's complete gameweek history...")
    
    df = process_player_gameweek_data(player_id=1)
    
    # Save to CSV
    output_path = Path(__file__).parent / "gameweek_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"\nSaved to: {output_path}")
    print(f"Total gameweeks: {len(df)}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nColumns: {list(df.columns)}")


if __name__ == "__main__":
    main()
