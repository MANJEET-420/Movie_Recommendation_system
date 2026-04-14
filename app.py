import streamlit as st
import pickle
import pandas as pd
import requests

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System (50 Movies)")

TMDB_API_KEY = "953672acddee6a9148b5eb43616fc3c9"

# ===============================
# LOAD DATA
# ===============================
movies = pickle.load(open("movie_list.pkl", "rb"))   # DataFrame
similarity = pickle.load(open("similarity.pkl", "rb"))

# ===============================
# POSTER FUNCTION
# ===============================
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"

# ===============================
# RECOMMEND FUNCTION
# ===============================
def recommend(movie, num=50):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )

    movie_names = []
    movie_posters = []

    n = min(num, len(movie_list)-1)

    for i in range(1, n+1):
        movie_id = movies.iloc[movie_list[i][0]].movie_id
        movie_names.append(movies.iloc[movie_list[i][0]].title)
        movie_posters.append(fetch_poster(movie_id))

    return movie_names, movie_posters

# ===============================
# UI
# ===============================
selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie, 50)

    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i % 5]:
            st.image(posters[i])
            st.caption(names[i])