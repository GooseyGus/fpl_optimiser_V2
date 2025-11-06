# output_window_updated.py
# Display squad results with transfer information using tabulate for perfect alignment

import pandas as pd
import tkinter as tk
from tkinter import ttk, scrolledtext
from pulp import LpStatus, value
from tabulate import tabulate
import os

def display_in_window(prob, squad, vars=None, df_players=None, my_team=None, analysis_data=None):
    """
    Display squad results in a tkinter window with transfer information using tabulate for perfect alignment
    """
    # Create window
    root = tk.Tk()
    gw_text = f" - Gameweek {squad['gameweek']}" if squad['gameweek'] else ""
    root.title(f"FPL Team Selection Results{gw_text}")
    root.geometry("1200x800")  # Larger window for better table display
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Tab 1: Team Display
    team_frame = ttk.Frame(notebook)
    notebook.add(team_frame, text="Team")
    
    team_text = scrolledtext.ScrolledText(team_frame, wrap=tk.NONE, width=140, height=40, font=("Courier New", 9))
    team_text.pack(fill='both', expand=True)
    
    # Configure text tags for formatting
    team_text.tag_configure("bold", font=("Courier New", 9, "bold"))
    team_text.tag_configure("title", font=("Courier New", 12, "bold"))
    team_text.tag_configure("header", font=("Courier New", 10, "bold"))
    team_text.tag_configure("important", font=("Courier New", 9, "bold"), foreground="dark blue")
    team_text.tag_configure("penalty", font=("Courier New", 9, "bold"), foreground="red")
    
    # Insert content with formatting
    def insert_with_formatting(text_widget, content_list):
        """Insert text with appropriate formatting based on content type"""
        for item in content_list:
            if isinstance(item, tuple):
                text, tag = item
                text_widget.insert(tk.END, text + "\n", tag)
            else:
                text_widget.insert(tk.END, item + "\n")
    
    # Build team output with transfer info (using tuples for formatted text)
    output = []
    output.append(("=" * 100, "bold"))
    output.append((" " * 35 + "FPL TEAM SELECTION", "title"))
    if squad['gameweek']:
        output.append((" " * 38 + f"GAMEWEEK {squad['gameweek']}", "title"))
    output.append(("=" * 100, "bold"))
    output.append("")
    output.append((f"STATUS: {LpStatus[prob.status]}", "important"))
    
    # Calculate and display adjusted expected points
    raw_expected_points = value(prob.objective)
    transfer_penalty = 0
    
    # Get transfer penalty from analysis_data
    if analysis_data and 'transfers' in analysis_data:
        transfer_penalty = analysis_data['transfers']['transfer_penalty']
    
    # Adjust expected points by subtracting transfer penalty
    adjusted_expected_points = raw_expected_points - transfer_penalty  # Add because penalty is already negative in objective
    
    output.append((f"TOTAL EXPECTED POINTS (RAW): {raw_expected_points:.2f}", "important"))
    if transfer_penalty > 0:
        output.append((f"TRANSFER PENALTY: -{transfer_penalty} pts", "penalty"))
        output.append((f"ADJUSTED EXPECTED POINTS: {adjusted_expected_points:.2f}", "important"))

    # Look up captain and vice-captain
    if squad['captain_idx'] is not None and squad['captain_idx'] in squad['starting_df'].index:
        captain_name = squad['starting_df'].loc[squad['captain_idx'], 'name']
        captain_points = squad['starting_df'].loc[squad['captain_idx'], 'expected_points']  
        output.append((f"CAPTAIN: {captain_name} ({captain_points:.1f} x 2 = {captain_points*2:.1f} pts)", "important"))
    else:
        output.append(("CAPTAIN: None selected", "important"))

    if squad['vice_captain_idx'] is not None and squad['vice_captain_idx'] in squad['starting_df'].index:
        vice_captain_name = squad['starting_df'].loc[squad['vice_captain_idx'], 'name']
        vice_captain_points = squad['starting_df'].loc[squad['vice_captain_idx'], 'expected_points']  
        output.append((f"VICE-CAPTAIN: {vice_captain_name} ({vice_captain_points:.1f} pts)", "important"))
    else:
        output.append(("VICE-CAPTAIN: None selected", "important"))

    # Add enhanced transfer summary
    if analysis_data and 'transfers' in analysis_data:
        transfer_info = analysis_data['transfers']
        if transfer_info['paid_transfers'] > 0:
            output.append("")
            output.append(("TRANSFER DETAILS", "header"))
            output.append(("=" * 50, "bold"))
            output.append((f"Paid Transfers Made: {transfer_info['paid_transfers']}", "important"))
            output.append((f"Penalty per Transfer: -{transfer_info['penalty_points']} pts", "penalty"))
            output.append((f"Total Transfer Penalty: -{transfer_info['transfer_penalty']} pts", "penalty"))
    
    # Fallback to old transfer summary if new data not available
    elif vars and df_players is not None:
        transfers_made = get_transfer_summary(vars, df_players)
        if transfers_made['total'] > 0:
            output.append("")
            output.append((f"TRANSFERS MADE: {transfers_made['total']}", "header"))
            output.append(f"  Free: {transfers_made['free']}")
            output.append(f"  Paid (-4 pts each): {transfers_made['paid']}")
            output.append((f"  Points Hit: -{transfers_made['paid'] * 4}", "penalty"))

    output.append("")
    output.append(("=" * 100, "bold"))
    output.append(("STARTING XI", "header"))
    output.append(("=" * 100, "bold"))

    # Prepare Starting XI data for tabulate
    if not squad['starting_df'].empty:
        # Sort by position
        position_order = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
        starting_sorted = squad['starting_df'].sort_values(
            by='position', 
            key=lambda x: x.map({pos: i for i, pos in enumerate(position_order)})
        )
        
        starting_table_data = []
        for _, player in starting_sorted.iterrows():
            role = ""
            if player.get('is_captain', False):
                role = "(C)"
            elif player.get('is_vice_captain', False):
                role = "(VC)"
            
            starting_table_data.append([
                player['name'],
                player['position'],
                player['team'],
                player.get('opponent', 'No fixture'),
                f"£{player['price']:.1f}m",
                f"{player['expected_points']:.1f}",
                player['transfer_type'],
                role
            ])
        
        starting_headers = ['Name', 'Position', 'Team', 'Opponent', 'Price', 'Points', 'Transfer', 'Role']
        starting_table = tabulate(starting_table_data, headers=starting_headers, tablefmt='grid')
        output.append(starting_table)
    
    output.append("")
    output.append(("=" * 100, "bold"))
    output.append(("BENCH", "header"))
    output.append(("=" * 100, "bold"))
    
    # Prepare Bench data for tabulate
    if not squad['bench_df'].empty:
        bench_table_data = []
        for _, player in squad['bench_df'].iterrows():
            bench_table_data.append([
                player['bench_order'],
                player['name'],
                player['position'],
                player['team'],
                player.get('opponent', 'No fixture'),
                f"£{player['price']:.1f}m",
                f"{player['expected_points']:.1f}",
                player['transfer_type']
            ])
        
        bench_headers = ['#', 'Name', 'Position', 'Team', 'Opponent', 'Price', 'Points', 'Transfer']
        bench_table = tabulate(bench_table_data, headers=bench_headers, tablefmt='grid')
        output.append(bench_table)
    
    output.append("")
    output.append(("=" * 100, "bold"))
    output.append(("SUMMARY", "header"))
    output.append(("=" * 100, "bold"))
    
    formation = squad['formation']
    formation_str = f"{formation.get('Goalkeeper', 0)}-{formation.get('Defender', 0)}-{formation.get('Midfielder', 0)}-{formation.get('Forward', 0)}"
    
    summary_data = [
        ['Formation', formation_str],
        ['Total Cost', f"£{squad['total_cost']:.1f}m"],
    ]
    
    if my_team:
        summary_data.extend([
            ['Previous Team Cost', f"£{my_team.team_value:.1f}m"],
            ['Previous Bank', f"£{my_team.budget:.1f}m"]
        ])
    
    # Add transfer summary to the main summary table
    if analysis_data and 'transfers' in analysis_data:
        transfer_info = analysis_data['transfers']
        if transfer_info['paid_transfers'] > 0:
            summary_data.extend([
                ['Paid Transfers', str(transfer_info['paid_transfers'])],
                ['Transfer Penalty', f"-{transfer_info['transfer_penalty']} pts"],
                ['Net Expected Points', f"{adjusted_expected_points:.1f} pts"]
            ])
    
    summary_table = tabulate(summary_data, tablefmt='simple')
    output.append(summary_table)
    
    # OUT TRANSFERS section
    if not squad['out_df'].empty:
        output.append("")
        output.append(("=" * 100, "bold"))
        output.append(("OUT TRANSFERS", "header"))
        output.append(("=" * 100, "bold"))
        
        out_table_data = []
        for _, player in squad['out_df'].iterrows():
            out_table_data.append([
                player['name'],
                player['position'],
                player['team'],
                player.get('opponent', 'No fixture'),
                f"£{player['price']:.1f}m",
                f"{player['expected_points']:.1f}",
                player['transfer_type']
            ])
        
        out_headers = ['Name', 'Position', 'Team', 'Opponent', 'Price', 'Points', 'Transfer Type']
        out_table = tabulate(out_table_data, headers=out_headers, tablefmt='grid')
        output.append(out_table)

    # Insert content with formatting
    insert_with_formatting(team_text, output)
    team_text.config(state='disabled')

    # Tab 2: Previous Gameweek
    prev_frame = ttk.Frame(notebook)
    notebook.add(prev_frame, text="Previous GW")
    
    prev_text = scrolledtext.ScrolledText(prev_frame, wrap=tk.NONE, width=140, height=40, font=("Courier New", 9))
    prev_text.pack(fill='both', expand=True)
    
    prev_output = []
    
    if my_team is not None:
        prev_output.append("=" * 80)
        prev_output.append(" " * 25 + f"PREVIOUS TEAM (GAMEWEEK {squad.get('gameweek', 1) - 1})")
        prev_output.append("=" * 80)
        
        # Get team data from my_team
        team_df = my_team.current_team
        
        # Sort by starting/bench
        prev_starting = team_df[team_df['is_starting'] == True].copy()
        prev_bench = team_df[team_df['is_starting'] == False].copy()
        
        # Starting XI table
        if not prev_starting.empty:
            prev_output.append("\nSTARTING XI")
            prev_output.append("=" * 80)
            
            prev_starting_data = []
            for _, player in prev_starting.iterrows():
                role = "(C)" if player.get('is_captain', False) else "(VC)" if player.get('is_vice_captain', False) else ""
                prev_starting_data.append([
                    player['name'],
                    player['position'],
                    player['team'],
                    player.get('opponent', 'No fixture'),
                    f"£{player['price']:.1f}m",
                    f"{player['expected_points']:.1f}",
                    role
                ])
            
            prev_starting_headers = ['Name', 'Position', 'Team', 'Opponent', 'Price', 'Points', 'Role']
            prev_starting_table = tabulate(prev_starting_data, headers=prev_starting_headers, tablefmt='grid')
            prev_output.append(prev_starting_table)
        
        # Bench table
        if not prev_bench.empty:
            prev_output.append("\nBENCH")
            prev_output.append("=" * 80)
            
            prev_bench_data = []
            for i, (_, player) in enumerate(prev_bench.iterrows(), 1):
                prev_bench_data.append([
                    i,
                    player['name'],
                    player['position'],
                    player['team'],
                    player.get('opponent', 'No fixture'),
                    f"£{player['price']:.1f}m",
                    f"{player['expected_points']:.1f}"
                ])
            
            prev_bench_headers = ['#', 'Name', 'Position', 'Team', 'Opponent', 'Price', 'Points']
            prev_bench_table = tabulate(prev_bench_data, headers=prev_bench_headers, tablefmt='grid')
            prev_output.append(prev_bench_table)
        
        # Summary
        prev_output.append(f"\n{'=' * 80}")
        prev_output.append("PREVIOUS TEAM SUMMARY")
        prev_output.append("=" * 80)
        
        formation_prev = prev_starting['position'].value_counts()
        prev_formation = f"{formation_prev.get('GK', 0)}-{formation_prev.get('DEF', 0)}-{formation_prev.get('MID', 0)}-{formation_prev.get('FWD', 0)}"
        
        prev_summary_data = [
            ['Total Squad Value', f"£{my_team.team_value:.1f}m"],
            ['Bank', f"£{my_team.budget:.1f}m"],
            ['Free Transfers', str(my_team.free_transfers)],
            ['Formation', prev_formation]
        ]
        
        prev_summary_table = tabulate(prev_summary_data, tablefmt='simple')
        prev_output.append(prev_summary_table)
    else:
        prev_output.append("No previous gameweek data available")
        
    prev_text.insert('1.0', '\n'.join(prev_output))
    prev_text.config(state='disabled')
    
    # Tab 3: Analysis
    if analysis_data:
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Analysis")
        
        analysis_text = scrolledtext.ScrolledText(analysis_frame, wrap=tk.NONE, width=140, height=40, font=("Courier New", 9))
        analysis_text.pack(fill='both', expand=True)
        
        # Configure text tags for formatting
        analysis_text.tag_configure("bold", font=("Courier New", 9, "bold"))
        analysis_text.tag_configure("title", font=("Courier New", 12, "bold"))
        analysis_text.tag_configure("header", font=("Courier New", 10, "bold"))
        analysis_text.tag_configure("important", font=("Courier New", 9, "bold"), foreground="dark blue")
        analysis_text.tag_configure("good", font=("Courier New", 9), foreground="green")
        analysis_text.tag_configure("bad", font=("Courier New", 9), foreground="red")
        analysis_text.tag_configure("neutral", font=("Courier New", 9), foreground="orange")
        analysis_text.tag_configure("penalty", font=("Courier New", 9, "bold"), foreground="red")
        
        # Insert analysis content
        analysis_output = []
        
        # Transfer penalty analysis
        if 'transfers' in analysis_data:
            transfer_info = analysis_data['transfers']
            if transfer_info['paid_transfers'] > 0:
                analysis_output.append(("=" * 100, "bold"))
                analysis_output.append((" " * 35 + "TRANSFER PENALTY ANALYSIS", "title"))
                analysis_output.append(("=" * 100, "bold"))
                analysis_output.append("")
                analysis_output.append((f"Number of paid transfers: {transfer_info['paid_transfers']}", "important"))
                analysis_output.append((f"Penalty per transfer: -{transfer_info['penalty_points']} points", "penalty"))
                analysis_output.append((f"Total penalty deduction: -{transfer_info['transfer_penalty']} points", "penalty"))
                analysis_output.append("")
                analysis_output.append("This penalty has been deducted from the displayed expected points.")
                analysis_output.append("")
        
        # Opposing teams analysis
        if 'opposing_teams' in analysis_data:
            analysis_output.append(("=" * 100, "bold"))
            analysis_output.append((" " * 35 + "OPPOSING TEAMS ANALYSIS", "title"))
            analysis_output.append(("=" * 100, "bold"))
            analysis_output.append("")
            analysis_output.append(analysis_data['opposing_teams'])
            analysis_output.append("")
        
        # FDR analysis
        if 'fdr_analysis' in analysis_data:
            analysis_output.append(("=" * 50, "bold"))
            analysis_output.append(("FDR ANALYSIS OF SELECTED SQUAD", "header"))
            analysis_output.append(("=" * 50, "bold"))
            analysis_output.append("")
            
            for fdr_line in analysis_data['fdr_analysis']:
                if isinstance(fdr_line, tuple):
                    text, color = fdr_line
                    analysis_output.append((text, color))
                else:
                    analysis_output.append(fdr_line)
            
            analysis_output.append("")
            if 'fdr_summary' in analysis_data:
                analysis_output.append((analysis_data['fdr_summary'], "important"))
        
        # Insert content with formatting
        insert_with_formatting(analysis_text, analysis_output)
        analysis_text.config(state='disabled')
    
    # Close button
    close_btn = ttk.Button(root, text="Close", command=root.destroy)
    close_btn.pack(pady=5)
    
    root.mainloop()


def check_var(vars, category, subcategory, idx):
    """Helper to check if a variable is set to 1"""
    if category in vars and subcategory in vars[category]:
        var = vars[category][subcategory].get(idx)
        if var and hasattr(var, 'value') and var.value():
            return var.value() == 1
    return False


def get_transfer_summary(vars, df_players):
    """Get summary of transfers made"""
    transfers = {'total': 0, 'free': 0, 'paid': 0}
    
    if vars is None or df_players is None:
        return transfers
    
    # Count transfers (divide by 2 since we count both in and out)
    free_count = 0
    paid_count = 0
    
    for idx in df_players.index:
        # Count free transfers OUT
        if (check_var(vars, 'out', 'starting_free', idx) or 
            check_var(vars, 'out', 'bench_free', idx)):
            free_count += 1
        
        # Count paid transfers OUT
        if (check_var(vars, 'out', 'starting_paid', idx) or 
            check_var(vars, 'out', 'bench_paid', idx)):
            paid_count += 1
    
    transfers['free'] = free_count
    transfers['paid'] = paid_count
    transfers['total'] = free_count + paid_count
    
    return transfers