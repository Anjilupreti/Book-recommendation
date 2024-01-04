import streamlit as st
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd


# Load your data
popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')

# Flask app initialization
app = Flask(__name__)

# Streamlit app initialization
st.set_page_config(page_title="Book Recommendation App", page_icon="📚", layout="wide")

# Streamlit app routes
@st.cache_data
def load_data():
    return popular_df, pt, books, similarity_scores

@st.cache_data
def recommend_books(user_input):
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return data

def main():
    st.title("Book Recommendation App")

    # Load data
    popular_df, pt, books, similarity_scores = load_data()

    # Display popular books
    st.subheader("Popular Books")
    st.table(popular_df[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'avg_rating']])

    # Recommendation UI
    st.subheader("Recommend a Book")
    user_input = st.text_input("Enter a book title:")
    if st.button("Recommend"):
        if user_input:
            recommended_books = recommend_books(user_input)
            st.subheader("Recommended Books")
            st.table(recommended_books)

if __name__ == '__main__':
    main()

