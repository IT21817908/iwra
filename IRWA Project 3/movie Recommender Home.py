# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 01:48:14 2023

@author: Azmarah Rizvi
"""

import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

movies = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project/movies_list.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project/similarity.pkl", 'rb'))

movies_list = movies['title'].values

# fetch the posters
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=80321b186ae2ff767c6ef9499a9bae85&language=en-US".format(movie_id)
    data = requests.get(url)

    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

st.header("Movie Recommender System")

imageCarouselComponent = components.declare_component("image-carousel-component", path="C:/Users/Azmarah Rizvi/Desktop/IRWA Project/frontend/public")


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue = st.selectbox("Select movie from dropdown", movies_list)



# recommendation function
def recommend(movie):
    # Get the each index and access the title of each movie
    index = movies[movies['title'] == movie].index[0]
    
    # create a list of similarity
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])

    # store the recommended movies inside a list
    recommend_movie = []
    
    # store the movie posters inside a list
    recommend_poster = []
    
    for i in distance[1:6]:
        
        #for posters
        movies_id = movies.iloc[i[0]].id
        recommend_poster.append(fetch_poster(movies_id))
        
        recommend_movie.append(movies.iloc[i[0]].title)
        
    return recommend_movie, recommend_poster


if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    
    #display
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        if movie_poster[0] is not None:
           st.image(movie_poster[0])
        else:
           st.warning("Poster not available")
    with col2:
        st.text(movie_name[1]) 
        if movie_poster[1] is not None:
           st.image(movie_poster[1])
        else:
           st.warning("Poster not available")
    with col3:
        st.text(movie_name[2])
        if movie_poster[2] is not None:
           st.image(movie_poster[2])
        else:
           st.warning("Poster not available")
    with col4:
        st.text(movie_name[3])
        if movie_poster[3] is not None:
           st.image(movie_poster[3])
        else:
           st.warning("Poster not available")
    with col5:
        st.text(movie_name[4])
        if movie_poster[4] is not None:
           st.image(movie_poster[4])
        else:
           st.warning("Poster not available")