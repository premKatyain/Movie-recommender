import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse

# API setup (optional, not currently used in your code)
url = "https://api.themoviedb.org/3/movie/343611"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/json"
}

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] 

    rec_movies = []
    rec_movie_posters = []

    for i in movie_list:
        rec_movies.append(movies.iloc[i[0]].title)
        rec_movie_posters.append(get_movie_info(movies.iloc[i[0]].title))
    
    return rec_movies, rec_movie_posters

def get_movie_info(title):
    try:
        title_encoded = urllib.parse.quote(title)
        response = requests.get(f"https://search.imdbot.workers.dev/?q={title_encoded}")
        data = response.json()

        if "description" in data and len(data["description"]) > 0:
            return data["description"][0].get("#IMG_POSTER", "")
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Poster+Found"
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")
        return "https://via.placeholder.com/300x450.png?text=Error"

# Load model and data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity_compressed.pkl', 'rb'))

st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    with st.spinner("Finding awesome recommendations for you... 🍿"):
        names, posters = recommend(selected_movie_name)

    # Display recommendations in 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
