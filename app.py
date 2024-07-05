import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    response=requests.get(url)
    data=response.json()
    print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended=[]
    recommended_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        recommended.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended,recommended_movies_posters

movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    # Create 5 columns
    cols = st.columns(5)

    # Loop through the columns and populate them with movie names and posters
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])