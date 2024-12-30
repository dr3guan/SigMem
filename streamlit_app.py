import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Initialize session state for app-wide data
if 'memes' not in st.session_state:
    st.session_state['memes'] = pd.DataFrame(columns=['id', 'title', 'url', 'genre', 'votes', 'uploaded_by', 'timestamp'])

# Utility functions
def add_meme(title, url, genre, uploaded_by):
    new_meme = {
        'id': len(st.session_state['memes']) + 1,
        'title': title,
        'url': url,
        'genre': genre,
        'votes': 0,
        'uploaded_by': uploaded_by,
        'timestamp': datetime.now()
    }
    st.session_state['memes'] = pd.concat([st.session_state['memes'], pd.DataFrame([new_meme])], ignore_index=True)

def upvote_meme(meme_id):
    st.session_state['memes'].loc[st.session_state['memes']['id'] == meme_id, 'votes'] += 1

def downvote_meme(meme_id):
    st.session_state['memes'].loc[st.session_state['memes']['id'] == meme_id, 'votes'] -= 1

# App Layout
st.title("SigMem: Meme Rating Application")

menu = st.sidebar.selectbox("Menu", ["Upload Meme", "Rate Memes", "Leaderboard"])

if menu == "Upload Meme":
    st.header("Upload a Meme")
    title = st.text_input("Meme Title")
    url = st.text_input("Meme URL")
    genre = st.text_input("Meme Genre")
    uploaded_by = st.text_input("Your Username")
    if st.button("Upload"):
        if title and url and genre and uploaded_by:
            add_meme(title, url, genre, uploaded_by)
            st.success("Meme uploaded successfully!")
        else:
            st.error("Please fill in all fields.")

elif menu == "Rate Memes":
    st.header("Rate Memes")
    genre_filter = st.selectbox("Filter by Genre", ["All"] + list(st.session_state['memes']['genre'].unique()))
    filtered_memes = st.session_state['memes']
    if genre_filter != "All":
        filtered_memes = filtered_memes[filtered_memes['genre'] == genre_filter]

    if not filtered_memes.empty:
        for _, meme in filtered_memes.iterrows():
            st.image(meme['url'], caption=meme['title'])
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Upvote {meme['id']}"):
                    upvote_meme(meme['id'])
            with col2:
                if st.button(f"Downvote {meme['id']}"):
                    downvote_meme(meme['id'])
    else:
        st.info("No memes available in this category.")

elif menu == "Leaderboard":
    st.header("Leaderboard")
    genre_filter = st.selectbox("Filter by Genre", ["All"] + list(st.session_state['memes']['genre'].unique()))
    filtered_memes = st.session_state['memes']
    if genre_filter != "All":
        filtered_memes = filtered_memes[filtered_memes['genre'] == genre_filter]

    leaderboard = filtered_memes.sort_values(by='votes', ascending=False)
    st.table(leaderboard[['title', 'votes', 'genre', 'uploaded_by']])

# Run the app with `streamlit run app.py`
