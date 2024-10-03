import streamlit as st
import requests
import pandas as pd
import os

st.title('NBA Teams List')

headers = {
    'per_page': '100',
    'Authorization': '92e8729b-7e58-4394-bd2e-06714a46df2a'
    # 'Authorization': API_key
}
# '92e8729b-7e58-4394-bd2e-06714a46df2a'

@st.cache_data
def load_teams():
    all_teams = []
    page = 1
    while True:
        api_url = "https://api.balldontlie.io/v1/teams"
        headers['page'] = str(page)
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            st.error(f"Failed to fetch data from API - Status code {response.status_code}")
            break

        data = response.json()
        if not data['data']:
            break

        all_teams.extend(data['data'])
        page += 1

    return all_teams

all_teams = load_teams()

if not all_teams:
    st.warning("No teams found")
else:
    
    df = pd.DataFrame(all_teams)
    
    teams_df = df[['full_name', 'abbreviation', 'conference', 'city']]
    teams_df = teams_df.rename(columns={'full_name': 'Koko nimi', 'abbreviation': 'Lyhenne', 'city': 'Kaupunki', 'conference': 'Konferenssi'})

    st.header('List of NBA Teams')
    st.dataframe(teams_df)