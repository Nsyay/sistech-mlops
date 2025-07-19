import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(text):
    tokens = text.lower().split()
    return tokens

def average_vector(tokens, w2v_model, vector_size):
    valid = [w2v_model.wv[tok] for tok in tokens if tok in w2v_model.wv]
    if not valid:
        return np.zeros(vector_size)
    return np.mean(valid, axis=0)


# Load model
# Uncomment one of the following sections based on the model you want to use

# Model 1: TF-IDF
# model = joblib.load("models/course_recommender1.joblib")
# vectorizer = model["vectorizer"]
# tfidf_matrix = model["tfidf_matrix"]
# df = model["dataframe"]

# def recommend(query, top_n=5):
#     vec = vectorizer.transform([query])
#     similarities = tfidf_matrix.dot(vec.T).toarray().flatten()
#     top_indices = similarities.argsort()[::-1][:top_n]
#     return df.iloc[top_indices][["Title", "Description", "URL"]]

# Model 2: Word2Vec
model = joblib.load("models/course_recommender2.joblib")
w2v_model = model["word2vec_model"]
doc_vectors = model["document_vectors"]
df = model["dataframe"]

def recommend(query, top_n=5):
    tokens = preprocess(query)
    vec = average_vector(tokens, w2v_model, w2v_model.vector_size).reshape(1, -1)
    similarities = cosine_similarity(doc_vectors, vec).flatten()
    top_indices = similarities.argsort()[::-1][:top_n]
    return df.iloc[top_indices][["Title", "Description", "URL"]]

if __name__ == "__main__":
    print("Enter your dream job or interest:")
    query = input("> ")
    print("\nTop course recommendations:\n")
    results = recommend(query)
    for i, row in results.iterrows():
        print(f"{row['Title']}")
        print(f"  Description: {row['Description']}")
        print(f"  URL: {row['URL']}\n")
