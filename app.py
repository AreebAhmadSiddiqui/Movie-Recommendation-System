import streamlit as st
import pickle
import pandas as pd
import requests


def recommender(new_movies, movie_name):

    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_index = new_movies[new_movies['title'] == movie_name].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    poster_paths = []
    for i in movies_list:
        recommended_movies.append(new_movies.iloc[i[0]].title)
        response_API = requests.get(
            "https://api.themoviedb.org/3/movie/{}?api_key=8f655507141a5d524fc2024c9f76b6c7&language=en-US".format(new_movies.iloc[i[0]].id)).json()
        poster_paths.append(
            "https://image.tmdb.org/t/p/original"+response_API['poster_path'])

    return recommended_movies, poster_paths


def main():

    movie_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
    st.title('Watch Them')
    selected_movie = st.selectbox(
        'Select your movie', movies['title'].values)
    if st.button('Recommend'):
        recommendations, poster_path = recommender(movies, selected_movie)
        j=0
        for i in range(2):
            cols = st.columns(5)
            k=0
            while k<5 and j<11:
                cols[k].text(recommendations[j])
                cols[k].image(poster_path[j])
                j += 1
                k+=1


if __name__ == "__main__":
    main()

