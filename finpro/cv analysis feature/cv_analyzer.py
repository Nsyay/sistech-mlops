import re
import spacy
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    return extract_text(file_path)


def extract_skills(text, skill_set):
    found = []
    for skill in skill_set:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            found.append(skill)
    return found

def analyze_cv(cv_path, job_description, skill_keywords):
    text = extract_text_from_pdf(cv_path).lower()
    cv_skills = extract_skills(text, skill_keywords)
    jd_skills = extract_skills(job_description.lower(), skill_keywords)

    missing_skills = list(set(jd_skills) - set(cv_skills))

    return {
        "skills_found": cv_skills,
        "missing_skills": missing_skills,
        "optimization_tips": generate_tips(missing_skills)
    }

def generate_tips(missing_skills):
    tips = []
    if missing_skills:
        tips.append("Add these relevant skills mentioned in the job description:")
        tips.extend(f"- {skill}" for skill in missing_skills)
    else:
        tips.append("Your CV matches all required skills from the job description. Great work!")

    return tips

if __name__ == "__main__":
    skill_keywords = [
        "python", "sql", "machine learning", "data analysis",
        "communication", "teamwork", "deep learning", "nlp", "tensorflow",
        "project management", "fastapi", "django", "pandas", "numpy"
    ]

    job_description = """
    We are looking for a data scientist skilled in Python, machine learning, deep learning,
    NLP, and experience with FastAPI and SQL. Good communication and teamwork are required.
    """

    result = analyze_cv("AyuSitiNasyaNingrum-CV.pdf", job_description, skill_keywords)

    print(f"Skills Found: {result['skills_found']}")
    print(f"Missing Skills: {result['missing_skills']}")
    print("Suggestions:")
    for tip in result['optimization_tips']:
        print(tip)
