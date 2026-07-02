import pickle
import streamlit as st
import requests
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# CONFIG API
# =========================
API_KEY = os.environ.get("TMDB_API_KEY")

if API_KEY is None:
    st.error("❌ TMDB_API_KEY manquante. Ajoute-la dans les variables d'environnement.")
    st.stop()


# =========================
# LOAD DATA
# =========================
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))


# =========================
# CACHE SIMILARITY
# =========================
@st.cache_data
def load_similarity(data):
    cv = TfidfVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(data['tags'].values.astype('U'))
    return cosine_similarity(vectors)

similarity = load_similarity(movies)


# =========================
# FETCH POSTER TMDB
# =========================
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url).json()

        poster_path = data.get('poster_path')

        if not poster_path:
            return "https://via.placeholder.com/500"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        return "https://via.placeholder.com/500"


# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# =========================
# UI STREAMLIT
# =========================
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.header("🎬 Système de recommandation de films")

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Choisis un film",
    movie_list
)

if st.button("🎥 Voir recommandations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])