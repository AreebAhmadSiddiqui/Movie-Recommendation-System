import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_similarity_matrix():
    new_movies=pd.read_csv('./datasets/cleaned_movies.csv')
    cv=CountVectorizer(max_features=5000,stop_words='english')
    vectors=cv.fit_transform(new_movies['tags']).toarray()
    similarity=cosine_similarity(vectors)
    return similarity

def recommender(new_movies, movie_name):

    similarity = get_similarity_matrix()
    movie_index = new_movies[new_movies['title'] == movie_name].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    poster_paths = []
    for i in movies_list:
        recommended_movies.append(new_movies.iloc[i[0]].title)
        response_API = requests.get(
            "https://api.themoviedb.org/3/movie/{}?api_key={YOUR_API_KEY}&language=en-US".format(new_movies.iloc[i[0]].id)).json()
        poster_paths.append(
            "https://image.tmdb.org/t/p/original"+response_API['poster_path'])

    return recommended_movies, poster_paths


def main():

    movies= pd.read_csv('./datasets/tmdb_5000_movies.csv')
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

