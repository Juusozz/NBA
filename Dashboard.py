import streamlit as st
import requests
import pandas as pd


st.title('NBA Players Scoring Averages')


api_url = "https://api.balldontlie.io/v1/stats"
headers = {
    'Authorization': '92e8729b-7e58-4394-bd2e-06714a46df2a',
    'season': '2023',
    'per_page': '100'
}


def load_data():
    all_stats = []
    page = 1

    while True:

        headers['page'] = str(page)
        response = requests.get(api_url, headers=headers)
        

        if response.status_code != 200:
            st.error(f"Failed to fetch data from API - Status code {response.status_code}")
            break
        
        data = response.json()
        if not data['data']:
            break  
        
        all_stats.extend(data['data'])
        page += 1
 
    return all_stats


all_stats = load_data()


df = pd.DataFrame(all_stats)


players_df = pd.json_normalize(df['player'])
teams_df = pd.json_normalize(df['team'])


df = df.join(players_df.add_prefix('player_'))
df = df.join(teams_df.add_prefix('team_'))


player_scoring_averages = df.groupby(['player_first_name', 'player_last_name'])['pts'].mean().reset_index()
player_scoring_averages.columns = ['First Name', 'Last Name', 'Points Per Game']


st.header('Players Scoring Averages This Season')
st.dataframe(player_scoring_averages)


top_n = st.slider('Select number of top players to display', min_value=5, max_value=50, value=10)
top_players = player_scoring_averages.nlargest(top_n, 'Points Per Game')

st.header(f'Top {top_n} Players by Points Per Game')
st.bar_chart(top_players.set_index(['First Name', 'Last Name'])['Points Per Game'])
