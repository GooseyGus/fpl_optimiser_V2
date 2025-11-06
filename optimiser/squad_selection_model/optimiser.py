import sys
import io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
from pulp import LpProblem, LpMaximize, PULP_CBC_CMD
from decision_variables import create_decision_variables
from objective_function import add_objective_function
from constraints import *
from squad_creator import *
from team_class import Team
from output_window import display_in_window
from fdr import *

# Check for manual team override file
manual_team_ids = None
override_file = os.path.join(os.path.dirname(__file__), '..', 'my_team_override.txt')
if os.path.exists(override_file):
    with open(override_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        if lines:
            try:
                manual_team_ids = [int(pid) for pid in lines]
                print(f"🔧 Using manual team override with {len(manual_team_ids)} player IDs")
            except ValueError:
                print(f"⚠️  Warning: Invalid player IDs in my_team_override.txt, using API instead")
                manual_team_ids = None

# Initialize team
my_team = Team(team_id=2562804, budget=1.5, free_transfers=1, manual_player_ids=None)

df_players = pd.read_csv('data/fpl_players_gw_9.csv')

# Initialize FDR calculator
fdr_calculator = CSVFDRCalculator('data/fpl_players_gw_9.csv')
print(f"📊 FDR Calculator initialized with {len(fdr_calculator.team_fdr_ratings)} teams")   

# Create optimization problem
prob = LpProblem("FPL_Transfer_Optimisation", LpMaximize)

# Create decision variables
vars = create_decision_variables(df_players)

# Add objective function with FDR penalties
penalty_points = 4  # Store penalty points for later use
prob = add_objective_function(
    prob, df_players, vars, 
    penalty_points=penalty_points, 
    base_opposing_penalty=1,
    fdr_calculator=fdr_calculator,
    fdr_penalty_weight=0.5 # Adjust this to control FDR impact
)

# Add constraints
prob = add_squad_size_constraints(prob, vars, df_players)
prob = add_captain_constraints(prob, vars, df_players)
prob = add_equal_flow_constraints(prob, vars, df_players)
prob = add_status_constraints(prob, vars, df_players, my_team)
prob = add_positional_constraints(prob, vars, df_players)
prob = add_free_transfer_limit_constraint(prob, vars, df_players, my_team)
prob = add_availability_constraints(prob, vars, df_players, my_team)
prob = add_budget_constraint(prob, vars, df_players, my_team.current_team)
prob = add_team_constraints(prob, vars, df_players)

# Example usage with custom parameters:
'''
prob = add_bench_selection_constraints(
    prob, vars, df_players,         
    min_minutes=0,           # Lower minutes requirement
    min_price=0,           # Minimum £4.0m
    max_price=100,           # Maximum £5.5m (tighter budget)
    min_expected_points=7.1,  # Lower points threshold
    max_expected_points=100,  # Avoid premium players
    min_ownership=0,        # No minimum ownership
    max_ownership=100,       # Avoid very popular players
    allow_injured=False,      # No injured players
    min_form=0             # Require some form
)
'''
# Solve the problem
prob.solve(PULP_CBC_CMD(msg=False))

# Count paid transfers
def count_paid_transfers(vars, df_players):
    """Count the number of paid transfers made"""
    paid_transfer_count = 0
    
    for idx in df_players.index:
        if vars['in_to_starting_paid'][idx].value() > 0:
            paid_transfer_count += vars['in_to_starting_paid'][idx].value()
        if vars['in_to_bench_paid'][idx].value() > 0:
            paid_transfer_count += vars['in_to_bench_paid'][idx].value()
    
    return int(paid_transfer_count)

# Count paid transfers
paid_transfers = count_paid_transfers(vars, df_players)
transfer_penalty = paid_transfers * penalty_points

print(f"Paid transfers made: {paid_transfers}")
print(f"Transfer penalty: {transfer_penalty} points")

# Print transfer summary
transfer_types = [
    ('out_starting_paid', 'Sold', ''),
    ('out_bench_paid', 'Sold', ' from bench'),
    ('in_to_starting_paid', 'Bought', ''),
    ('in_to_bench_paid', 'Bought', ''),
    ('in_to_starting_free', 'Bought', ''),
    ('in_to_bench_free', 'Bought', ''),
    ('out_starting_free', 'Sold', ''),
    ('out_bench_free', 'Sold', ' from bench')
]

for idx in df_players.index:
    for var_name, action, location in transfer_types:
        if vars[var_name][idx].value() > 0:
            player = df_players.loc[idx]
            print(f"{action}: {player['name']}{location} for £{player['price']}m ({var_name})")

print(f"Initial bank: £{0}m")

squad = process_optimization_results(vars, df_players, prob)

# Capture analysis data
fdr_lines, fdr_summary = capture_fdr_analysis(squad, fdr_calculator)

# Create transfer analysis data
transfer_analysis = {
    'paid_transfers': paid_transfers,
    'penalty_points': penalty_points,
    'transfer_penalty': transfer_penalty
}

analysis_data = {
    'opposing_teams': capture_opposing_teams_analysis(df_players, squad, base_penalty=1.0),
    'fdr_analysis': fdr_lines,
    'fdr_summary': fdr_summary,
    'transfers': transfer_analysis
}

display_in_window(prob, squad, vars, df_players, my_team, analysis_data)