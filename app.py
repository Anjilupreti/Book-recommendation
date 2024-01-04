from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import os

popular_df = pd.read_pickle('popular.pkl')
print(popular_df.columns)  # Display the first few rows of the DataFrame
pt = pd.read_pickle('pt.pkl')
#print(pt.head()) 
books = pd.read_pickle('books.pkl')
#print(books.head())
similarity_scores = pd.read_pickle('similarity_scores.pkl')
#print(similarity_scores[:5])  # Print the first 5 elements of the array

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
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

    print(data)

    return render_template('recommend.html',data=data)
 

if __name__ == '__main__':
    app.run(debug=True)