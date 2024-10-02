import requests
import pandas as pd
import streamlit as st





def get_player_info():
    #Tunnistautuminen
    headers = {
        "Authorization": "92e8729b-7e58-4394-bd2e-06714a46df2a"
    }
    # Määritellään API:n URL
    api_url = "https://api.balldontlie.io/v1/players/237"
    # Pelaaja ID 237 on LeBron James
    # GET kutsu
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        try:
            # Muunna vastaus JSON-muotoon
            data = response.json()
            # Tulosta saatu data
            return data
        except requests.exceptions.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Response content:", response.content)
    else:
        # Ilmoita virheestä, jos pyyntö epäonnistui
        print(f"Request failed with status code {response.status_code}")
        print("Response content:", response.content)

