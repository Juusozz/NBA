import streamlit as st
import requests
import pandas as pd

# Set the title of the Streamlit app
st.title('NBA Players Scoring Averages')

# Define the balldontlie API endpoint for player stats
api_url = "https://www.balldontlie.io/api/v1/stats"
params = {
    'season': 2022,     # Specify the current season
    'per_page': 100    # Specify number of results per page; maximum is 100
}

@st.cache
def load_data():
    # Container for all players' stats
    all_stats = []
    page = 1

    while True:
        # Make the API call with pagination
        params['page'] = page
        response = requests.get(api_url, params=params)
        
        # Check if the response is successful
        if response.status_code != 200:
            st.error(f"Failed to fetch data from API - Status code {response.status_code}")
            break
        
        data = response.json()
        if not data['data']:
            break  # Break the loop if there is no more data
        
        all_stats.extend(data['data'])
        page += 1

    return all_stats

# Load data from the API
all_stats = load_data()

# Convert the data into a pandas DataFrame
df = pd.DataFrame(all_stats)

# Merge nested player and team information into columns
players_df = pd.json_normalize(df['player'])
teams_df = pd.json_normalize(df['team'])

# Combine player stats with corresponding player and team information
df = df.join(players_df.add_prefix('player_'))
df = df.join(teams_df.add_prefix('team_'))

# Calculate scoring averages grouped by player ID
player_scoring_averages = df.groupby(['player_first_name', 'player_last_name'])['pts'].mean().reset_index()
player_scoring_averages.columns = ['First Name', 'Last Name', 'Points Per Game']

# Show the data
st.header('Players Scoring Averages This Season')
st.dataframe(player_scoring_averages)

# Optionally, create a bar chart of the top N players
top_n = st.slider('Select number of top players to display', min_value=5, max_value=50, value=10)
top_players = player_scoring_averages.nlargest(top_n, 'Points Per Game')

st.header(f'Top {top_n} Players by Points Per Game')
st.bar_chart(top_players.set_index(['First Name', 'Last Name'])['Points Per Game'])
