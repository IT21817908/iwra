# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 01:33:02 2023

@author: Azmarah Rizvi
"""

import streamlit as st
import pandas as pd
import pickle

# Load the models
user_ratings = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project 3/user_ratings.pkl", 'rb'))
item_similarity_df = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project 3/item_similarity.pkl", 'rb'))

def get_similar_movies(movie_name, user_rating):
    similar_score = item_similarity_df[movie_name] * (user_rating - 2.5)
    similar_score = similar_score.sort_values(ascending=False)
    
    # Exclude movies already rated by the user
    user_rated_movies = user_ratings.columns[user_ratings.loc[1] > 0]
    similar_score = similar_score.drop(user_rated_movies, errors='ignore')
    
    return similar_score

def main():
    st.title("Movie Recommendation System")

    # Collect user input
    st.subheader("Enter Your Movie Preferences:")
    user_preferences = []
    
    # Get movies with at least 10 user ratings
    available_movies = user_ratings.columns
    
    for i in range(3):
        movie_name = st.selectbox(f"Select movie {i + 1} from dropdown", available_movies, key=f"selectbox_{i}")
        rating = st.slider(f"Rating for {movie_name} (1-5):", 1, 5, 3, key=f"slider_{i}")

        if movie_name:
            user_preferences.append((movie_name, rating))

    if st.button("Get Recommendations"):
        # Create empty DataFrame to collect similar movies
        similar_movies = pd.DataFrame()

        # Collect similar movies for each input
        for movie, rating in user_preferences:
            similar_movies = similar_movies.append(get_similar_movies(movie, rating), ignore_index=True)

        # Display recommended movies excluding movies already rated by the user
        st.subheader("Recommended Movies:")
        recommended_movies = similar_movies.sum().sort_values(ascending=False).index[:10]
        
        # Exclude movies already rated by the user
        user_rated_movies = user_ratings.columns[user_ratings.loc[1] > 0]
        recommended_movies = recommended_movies.difference(user_rated_movies)
        
        # Display recommended movies with index values
        for idx, movie in enumerate(recommended_movies, start=1):
            st.write(f"{idx}. {movie}")

if __name__ == "__main__":
    main()
