import pickle
import streamlit as st
import requests

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/600%7B%7D?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
#         movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_patkh = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def fetch_poster(movie_id):
#     # Correct URL format without the misplaced %7B%7D and using the movie_id in the URL
#     url = f"http://www.omdbapi.com/3/movie/{movie_id}?api_key=99daa963&language=en-US"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#
# Add timeout parameter (60 seconds)

    try:
        data = requests.get(url, timeout=30)

        # Check if the request was successful
        if data.status_code == 200:
            data = data.json()
            poster_path = data.get('poster_path')

            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                return "https://via.placeholder.com/300x450?text=No+Poster"
        else:
            # Handle the error in case of failure (e.g., invalid movie_id or network issues)
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except requests.exceptions.RequestException:
        # Handle connection errors like ConnectionResetError(10054)
        return "https://via.placeholder.com/300x450?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

st.header('Movie Recommender System Using Machine Learning')
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_name, recommended_movie_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_name[0])
        st.image(recommended_movie_poster[0])
    with col2:
        st.text(recommended_movie_name[1])
        st.image(recommended_movie_poster[1])
    with col3:
        st.text(recommended_movie_name[2])
        st.image(recommended_movie_poster[2])
    with col4:
        st.text(recommended_movie_name[3])
        st.image(recommended_movie_poster[3])
    with col5:
        st.text(recommended_movie_name[4])
        st.image(recommended_movie_poster[4])