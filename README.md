# FPL Optimiser V2

A professional Fantasy Premier League optimization tool with an intuitive dashboard interface.

## Features

- **Data Collection**: Automated FPL API data fetching with minimal API calls
- **Squad Optimization**: Mathematical optimization for squad selection
- **Interactive Dashboard**: Clean, minimal Streamlit interface

## Installation

```bash
# Clone repository
git clone https://github.com/GooseyGus/fpl_optimiser_V2.git
cd fpl_optimiser_V2

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Data Collection

```bash
# Collect all 38 gameweeks
python data/gameweek_data/gameweek_data_collection.py

# Update current gameweek only
python data/gameweek_data/update_current_gameweek.py

# Fetch fixture timetable
python data/timetable_data/timetable_data_collection.py
```

### Run Dashboard

```bash
streamlit run app/app.py
```

## Project Structure

```
fpl_optimiser_V2/
├── app/                    # Streamlit dashboard
├── data/                   # Data collection scripts
│   ├── gameweek_data/     # Player data per gameweek
│   └── timetable_data/    # Fixture information
├── optimiser/             # Optimization algorithms
└── requirements.txt       # Python dependencies
```

## Development

- **Python Version**: 3.13+
- **Code Style**: Functional, professional, minimal comments
- **API Usage**: Efficient batch calls (39 API calls for full season data)

## Deployment

Deploy to Streamlit Cloud:
1. Push repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository and deploy

## License

MIT
