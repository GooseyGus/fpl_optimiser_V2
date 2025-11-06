import requests
import pandas as pd
from pathlib import Path


def fetch_fpl_fixtures():
    """
    Fetch all fixtures from the FPL API.
    
    Returns:
        list: List of fixture dictionaries
    """
    url = "https://fantasy.premierleague.com/api/fixtures/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        fixtures = response.json()
        print(f"Fetched {len(fixtures)} fixtures")
        return fixtures
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fixtures: {e}")
        return None


def fetch_team_names():
    """
    Fetch team information to map team IDs to team names.
    
    Returns:
        dict: Dictionary mapping team IDs to team names
    """
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        teams = {team['id']: team['name'] for team in data['teams']}
        print(f"Fetched {len(teams)} teams")
        return teams
    except requests.exceptions.RequestException as e:
        print(f"Error fetching team names: {e}")
        return None


def process_fixtures(fixtures, teams):
    """
    Process fixtures data and convert to DataFrame.
    
    Args:
        fixtures (list): List of fixture dictionaries
        teams (dict): Dictionary mapping team IDs to team names
    
    Returns:
        pd.DataFrame: Processed fixtures data
    """
    processed_data = []
    
    for fixture in fixtures:
        processed_data.append({
            'fixture_id': fixture['id'],
            'gameweek': fixture['event'],
            'kickoff_time': fixture['kickoff_time'],
            'team_h': teams.get(fixture['team_h'], 'Unknown'),
            'team_h_id': fixture['team_h'],
            'team_a': teams.get(fixture['team_a'], 'Unknown'),
            'team_a_id': fixture['team_a'],
            'team_h_score': fixture.get('team_h_score'),
            'team_a_score': fixture.get('team_a_score'),
            'finished': fixture['finished'],
            'started': fixture['started'],
            'team_h_difficulty': fixture['team_h_difficulty'],
            'team_a_difficulty': fixture['team_a_difficulty']
        })
    
    df = pd.DataFrame(processed_data)
    return df


def save_to_csv(df, output_path):
    """Save DataFrame to CSV file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")
    print(f"Total fixtures: {len(df)}")


def main():
    """Fetch and save all FPL fixtures for the season."""
    print("=" * 60)
    print("FPL Fixtures Data Collection")
    print("=" * 60)
    
    # Fetch fixtures and team names
    fixtures = fetch_fpl_fixtures()
    teams = fetch_team_names()
    
    if fixtures is None or teams is None:
        print("Failed to fetch required data")
        return
    
    # Process fixtures
    df = process_fixtures(fixtures, teams)
    
    # Display summary
    print(f"\nFixtures by gameweek:")
    print(df.groupby('gameweek').size())
    
    # Save to CSV
    output_path = Path(__file__).parent / "timetable.csv"
    save_to_csv(df, output_path)
    
    print("\nSample fixtures:")
    print(df.head(10))
    print("=" * 60)


if __name__ == "__main__":
    main()
