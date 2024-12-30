import streamlit as st
import pandas as pd
import random

# Placeholder for memes loaded from Google Drive
if 'memes' not in st.session_state:
    st.session_state['memes'] = pd.DataFrame([
        {"id": 1, "title": "Meme 1", "url": "https://drive.google.com/uc?export=view&id=example1", "genre": "Humor", "votes": 0},
        {"id": 2, "title": "Meme 2", "url": "https://drive.google.com/uc?export=view&id=example2", "genre": "Satire", "votes": 0},
        {"id": 3, "title": "Meme 3", "url": "https://drive.google.com/uc?export=view&id=example3", "genre": "Animals", "votes": 0}
    ])

# Utility functions
def upvote_meme(meme_id):
    st.session_state['memes'].loc[st.session_state['memes']['id'] == meme_id, 'votes'] += 1

def downvote_meme(meme_id):
    st.session_state['memes'].loc[st.session_state['memes']['id'] == meme_id, 'votes'] -= 1

# App Layout
st.title("SigMem: Meme Rating Application")

menu = st.sidebar.selectbox("Menu", ["Rate Memes", "Leaderboard"])

if menu == "Rate Memes":
    st.header("Rate Memes")
    
    if not st.session_state['memes'].empty:
        meme_index = st.session_state.get('current_meme', 0)

        if meme_index < len(st.session_state['memes']):
            meme = st.session_state['memes'].iloc[meme_index]
            
            # Center the image
            st.markdown(f"<div style='text-align: center;'><img src='{meme['url']}' alt='{meme['title']}' style='max-width: 100%; height: auto;'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{meme['title']}</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👎 Thumbs Down", key=f"downvote_{meme['id']}"):
                    downvote_meme(meme['id'])
                    st.session_state['current_meme'] = meme_index + 1
            with col2:
                if st.button("👍 Thumbs Up", key=f"upvote_{meme['id']}"):
                    upvote_meme(meme['id'])
                    st.session_state['current_meme'] = meme_index + 1

        else:
            st.info("No more memes to rate. Check back later!")
    else:
        st.warning("No memes available.")

elif menu == "Leaderboard":
    st.header("Leaderboard")
    genre_filter = st.selectbox("Filter by Genre", ["All"] + list(st.session_state['memes']['genre'].unique()))
    filtered_memes = st.session_state['memes']
    if genre_filter != "All":
        filtered_memes = filtered_memes[filtered_memes['genre'] == genre_filter]

    leaderboard = filtered_memes.sort_values(by='votes', ascending=False)
    st.table(leaderboard[['title', 'votes', 'genre']])

# Run the app with `streamlit run app.py`
