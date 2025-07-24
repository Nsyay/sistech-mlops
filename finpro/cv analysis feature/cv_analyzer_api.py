import re
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pdfminer.high_level import extract_text

app = FastAPI()

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_skills(text, skill_set):
    text = text.replace('\f', ' ')
    text = re.sub(r'\s+', ' ', text).strip().lower()

    found = []
    for skill in skill_set:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.append(skill)
    return found

def generate_tips(missing_skills):
    if missing_skills:
        return  [f"- {skill}" for skill in missing_skills]
    else:
        return ["Your CV matches all required skills from the job description. Great work!"]

@app.post("/analyze_cv/")
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    skill_keywords: str = Form(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        skill_list = [s.strip().lower() for s in skill_keywords.split(",")]
        text = extract_text_from_pdf(tmp_path).lower()

        cv_skills = extract_skills(text, skill_list)
        jd_skills = extract_skills(job_description.lower(), skill_list)
        missing_skills = list(set(jd_skills) - set(cv_skills))
        tips = generate_tips(missing_skills)

        return JSONResponse({
            "skills_found": cv_skills,
            "missing_skills": missing_skills,
            "optimization_tips": tips
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)