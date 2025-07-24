from fastapi import FastAPI, Query
import joblib
import numpy as np
import uvicorn

app = FastAPI(title="TF-IDF Course Recommender API")

model = joblib.load("course_recommender1.joblib")
vectorizer = model["vectorizer"]
tfidf_matrix = model["tfidf_matrix"]
df = model["dataframe"]

def recommend(query, top_n=5):
    vec = vectorizer.transform([query])
    similarities = tfidf_matrix.dot(vec.T).toarray().flatten()
    top_indices = similarities.argsort()[::-1][:top_n]
    results = df.iloc[top_indices][["Title", "Description", "URL"]]
    return results.to_dict(orient="records")

@app.get("/recommend")
def get_recommendations(
    query: str = Query(..., description="Your dream job or interest"),
    top_n: int = 5
):
    results = recommend(query, top_n)
    return {"query": query, "recommendations": results}

if __name__ == "__main__":
    uvicorn.run("course_recommendation:app", host="0.0.0.0", port=8000, reload=True)