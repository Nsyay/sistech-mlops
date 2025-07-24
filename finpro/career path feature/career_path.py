from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn

model = joblib.load("career_recommender_tfidf.joblib")
vectorizer = model["vectorizer"]
tfidf_matrix = model["tfidf_matrix"]
career_df = model["dataframe"]

app = FastAPI(title="Career Path Recommender")

class UserProfile(BaseModel):
    educational_background: str
    major: str
    work_experience: Optional[str] = None
    career_interests: List[str]
    soft_skills: List[str]
    hard_skills: List[str]
    preferred_industries: List[str]

@app.post("/recommend")
def recommend_career(profile: UserProfile, top_n: int = 5):
    parts = [
        profile.major,
        profile.work_experience or "",
        " ".join(profile.career_interests),
        " ".join(profile.soft_skills),
        " ".join(profile.hard_skills)
    ]
    query = " ".join(parts).strip()

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    df_copy = career_df.copy()
    df_copy["similarity"] = similarities

    if profile.preferred_industries:
        df_copy = df_copy[df_copy["industry"].isin(profile.preferred_industries)]

    recommended = df_copy.sort_values(by=["similarity", "level"], ascending=[False, True])
    results = recommended[["path_id", "level", "role", "required_skills", "avg_salary", "industry", "similarity"]].head(top_n)
    return results.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run("career_path:app", host="0.0.0.0", port=8000)