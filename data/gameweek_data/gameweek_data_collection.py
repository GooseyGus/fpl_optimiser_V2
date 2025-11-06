import requests
import pandas as pd
from pathlib import Path


def fetch_bootstrap_data():
    """
    Fetch bootstrap-static data containing all player information.
    
    Returns:
        dict: Complete bootstrap data including players, teams, and events
    """
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"Fetched bootstrap data: {len(data['elements'])} players")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bootstrap data: {e}")
        return None


def fetch_live_gameweek_data(gameweek):
    """
    Fetch live gameweek data with player-specific stats.
    
    Args:
        gameweek (int): The gameweek number
    
    Returns:
        dict: Live gameweek data, or None if not available
    """
    url = f"https://fantasy.premierleague.com/api/event/{gameweek}/live/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def create_team_mapping(teams_data):
    """Create mapping of team IDs to team names."""
    return {team['id']: team['name'] for team in teams_data}


def create_position_mapping():
    """Create mapping of position IDs to position names."""
    return {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}


def process_gameweek_data(bootstrap_data, live_data, gameweek):
    """
    Process player data for a specific gameweek.
    
    Args:
        bootstrap_data (dict): Complete bootstrap data
        live_data (dict): Live gameweek data (None for future gameweeks)
        gameweek (int): Gameweek number
    
    Returns:
        pd.DataFrame: Player data for the gameweek
    """
    players = bootstrap_data['elements']
    teams = create_team_mapping(bootstrap_data['teams'])
    positions = create_position_mapping()
    
    # Create lookup for live gameweek stats
    live_stats_lookup = {}
    if live_data and 'elements' in live_data:
        for element in live_data['elements']:
            live_stats_lookup[element['id']] = element['stats']
    
    gameweek_data = []
    
    for player in players:
        player_id = player['id']
        gw_stats = live_stats_lookup.get(player_id, {})
        
        player_data = {
            # Player identifiers
            'player_id': player['id'],
            'player_name': player['web_name'],
            'full_name': f"{player['first_name']} {player['second_name']}",
            'team': teams.get(player['team'], 'Unknown'),
            'team_id': player['team'],
            'position': positions.get(player['element_type'], 'Unknown'),
            'position_id': player['element_type'],
            
            # Current season info
            'now_cost': player['now_cost'] / 10,
            'selected_by_percent': player['selected_by_percent'],
            'total_points': player['total_points'],
            'points_per_game': player['points_per_game'],
            'form': player['form'],
            'ep_next': player['ep_next'],
            'ep_this': player['ep_this'],
            
            # Status
            'status': player['status'],
            'chance_of_playing_next_round': player['chance_of_playing_next_round'],
            'chance_of_playing_this_round': player['chance_of_playing_this_round'],
            'news': player['news'],
            'news_added': player['news_added'],
            
            # Cumulative stats
            'minutes': player['minutes'],
            'goals_scored': player['goals_scored'],
            'assists': player['assists'],
            'clean_sheets': player['clean_sheets'],
            'goals_conceded': player['goals_conceded'],
            'own_goals': player['own_goals'],
            'penalties_saved': player['penalties_saved'],
            'penalties_missed': player['penalties_missed'],
            'yellow_cards': player['yellow_cards'],
            'red_cards': player['red_cards'],
            'saves': player['saves'],
            'bonus': player['bonus'],
            'bps': player['bps'],
            'influence': player['influence'],
            'creativity': player['creativity'],
            'threat': player['threat'],
            'ict_index': player['ict_index'],
            'starts': player['starts'],
            'expected_goals': player['expected_goals'],
            'expected_assists': player['expected_assists'],
            'expected_goal_involvements': player['expected_goal_involvements'],
            'expected_goals_conceded': player['expected_goals_conceded'],
            
            # Gameweek-specific stats
            'gw_minutes': gw_stats.get('minutes') if gw_stats else None,
            'gw_goals_scored': gw_stats.get('goals_scored') if gw_stats else None,
            'gw_assists': gw_stats.get('assists') if gw_stats else None,
            'gw_clean_sheets': gw_stats.get('clean_sheets') if gw_stats else None,
            'gw_goals_conceded': gw_stats.get('goals_conceded') if gw_stats else None,
            'gw_own_goals': gw_stats.get('own_goals') if gw_stats else None,
            'gw_penalties_saved': gw_stats.get('penalties_saved') if gw_stats else None,
            'gw_penalties_missed': gw_stats.get('penalties_missed') if gw_stats else None,
            'gw_yellow_cards': gw_stats.get('yellow_cards') if gw_stats else None,
            'gw_red_cards': gw_stats.get('red_cards') if gw_stats else None,
            'gw_saves': gw_stats.get('saves') if gw_stats else None,
            'gw_bonus': gw_stats.get('bonus') if gw_stats else None,
            'gw_bps': gw_stats.get('bps') if gw_stats else None,
            'gw_influence': gw_stats.get('influence') if gw_stats else None,
            'gw_creativity': gw_stats.get('creativity') if gw_stats else None,
            'gw_threat': gw_stats.get('threat') if gw_stats else None,
            'gw_ict_index': gw_stats.get('ict_index') if gw_stats else None,
            'gw_total_points': gw_stats.get('total_points') if gw_stats else None,
        }
        
        gameweek_data.append(player_data)
    
    return pd.DataFrame(gameweek_data)


def save_gameweek_csv(df, gameweek, output_dir):
    """Save gameweek DataFrame to CSV file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"gameweek{gameweek}.csv"
    df.to_csv(output_path, index=False)
    print(f"  Saved gameweek{gameweek}.csv")


def main():
    """
    Fetch and save data for all 38 gameweeks.
    Uses 1 bootstrap call + 1 live data call per gameweek = 39 total API calls.
    """
    print("=" * 60)
    print("FPL All Gameweeks Data Collection")
    print("=" * 60)
    
    # Fetch bootstrap data (contains all player information)
    bootstrap_data = fetch_bootstrap_data()
    if bootstrap_data is None:
        print("Failed to fetch bootstrap data")
        return
    
    output_dir = Path(__file__).parent
    
    print(f"\nProcessing all 38 gameweeks...")
    print("-" * 60)
    
    # Process each gameweek with one additional API call per gameweek
    for gameweek in range(1, 39):
        live_data = fetch_live_gameweek_data(gameweek)
        status = "Complete" if live_data else "Future"
        print(f"GW{gameweek:2d} ({status:8s}): ", end="", flush=True)
        
        try:
            df = process_gameweek_data(bootstrap_data, live_data, gameweek)
            save_gameweek_csv(df, gameweek, output_dir)
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print("-" * 60)
    print("Data collection complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
