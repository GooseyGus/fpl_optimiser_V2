# FPL Optimiser Project Guidelines

## Communication Style
Keep code suggestions concise and to the point. If you have alternative approaches, ask for clarification on requirements before suggesting them.

## Code Style Standards

### Functional and Professional
- Write concise but readable code
- Include comments that explain the process, not the obvious
- No unnecessary comments or self-congratulatory remarks
- No emojis in production code
- This is a professional working document for collaborative development

### Code Organization
- Use clear, descriptive function and variable names
- Keep functions focused on a single responsibility
- Include docstrings for functions explaining purpose, args, and returns
- Group related functionality logically

### API Usage Best Practices
- The FPL API provides comprehensive data in minimal calls
- Use `bootstrap-static` endpoint for all player/team data (1 call)
- Use `event/{gameweek}/live/` endpoint for gameweek-specific stats (1 call per gameweek)
- Never iterate through individual player endpoints when batch data is available
- Always include timeout parameters on requests

## Project Structure

This repository is organized into three main components:

### 1. Data Collection (`data/`)
Scripts for gathering complete datasets for each gameweek from the FPL API.

**Key Scripts:**
- `gameweek_data/gameweek_data_collection.py`: Fetch all 38 gameweeks (39 API calls total)
- `gameweek_data/update_current_gameweek.py`: Update current gameweek only (2 API calls)
- `timetable_data/timetable_data_collection.py`: Fetch all fixtures for the season

### 2. Optimiser (`optimiser/`)
Squad selection and optimization logic.

### 3. Dashboard (`app/`)
User interface and visualization components.

## Current Focus
Currently working on data collection layer to establish reliable, efficient data pipelines from the FPL API. 