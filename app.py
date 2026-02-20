import streamlit as st
import pickle
import pandas as pd
import requests

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🍿",
    layout="wide"
)

# 2. Custom CSS to clean up the UI (Optional but recommended for aesthetics)
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    div[data-testid="stImage"] > img {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Function to fetch posters safely
def fetch_posters(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=32b57e4d14c679cb948de3eb512c77c1&language=en-US".format(movie_id)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movie_list:
        # Correctly accessing the ID from the dataframe
        movie_id = movies.iloc[i[0]].id 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
        
    return recommended_movies, recommended_movies_posters

# 3. Load Data
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# 4. App Layout
st.title('🍿 Movie Recommender System')
st.markdown("Select a movie you like, and I'll recommend 5 similar ones!")

selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values
)

# 5. The "Recommend" Button Logic
if st.button('Show Recommendations'):
    
    # Add a spinner so the user knows something is happening
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie_name)
        
        # Create 5 columns for the display
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Display each movie in its own column
        with col1:
            st.image(posters[0], use_container_width=True)
            st.caption(names[0]) # caption is smaller and neater than text()
        with col2:
            st.image(posters[1], use_container_width=True)
            st.caption(names[1])
        with col3:
            st.image(posters[2], use_container_width=True)
            st.caption(names[2])
        with col4:
            st.image(posters[3], use_container_width=True)
            st.caption(names[3])
        with col5:
            st.image(posters[4], use_container_width=True)
            st.caption(names[4])


