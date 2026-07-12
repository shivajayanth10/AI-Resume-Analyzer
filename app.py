from flask import Flask, render_template, request, redirect, Response
import csv
import os
import re
import fitz
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
for m in genai.list_models():  print(m.name)
from werkzeug.utils import secure_filename
from flask import send_from_directory
from PyPDF2 import PdfReader
from database import (
    create_database,
    register_user,
    validate_user,
    add_application,
    get_all_applications,
    get_applied_count,
    get_interview_count,
    get_offer_count,
    get_rejected_count,
    get_application_by_id,
    update_application,
    delete_application,
    search_applications,
    filter_applications,
    sort_newest,
    sort_oldest
)
def clean_ai_response(text):
    text = text.replace("###", "")
    text = text.replace("##", "")
    text = text.replace("**", "")
    text = text.replace("---", "")
    text = text.replace("`", "")

    # Remove extra blank lines (3 or more -> 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
app = Flask(__name__)
model = genai.GenerativeModel("models/gemini-2.5-flash")
latest_skills = []
latest_ai_analysis = ""
analyzed_filename = ""
analyzed_filename = None
latest_ai_analysis = None
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
def calculate_resume_score(text):

    score = 0

    skills = [
        "python",
        "sql",
        "flask",
        "docker",
        "aws",
        "azure",
        "git",
        "kubernetes",
        "terraform",
        "jenkins",
        "linux",
        "mysql",
        "mongodb",
        "devops",
        "ci/cd"
    ]

    text = text.lower()

    matched_skills = []

    for skill in skills:
        if skill in text:
            score += 100 / len(skills)
            matched_skills.append(skill)

    score = min(round(score), 100)

    return score, matched_skills
def extract_skills(text):

    skills_list = [
        "Python",
        "SQL",
        "Flask",
        "Docker",
        "Git",
        "AWS",
        "Azure",
        "Kubernetes",
        "Terraform",
        "CI/CD",
        "Pandas",
        "NumPy",
        "Power BI",
        "Excel",
        "Tableau",
        "Machine Learning",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "MongoDB",
        "MySQL"
         ]
    
   

    
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills

    
create_database()


@app.route("/")
def home():
    return redirect("/dashboard")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        register_user(username, password)

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = validate_user(username, password)

        if user:
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
        global latest_ai_analysis
        global analyzed_filename
        applications = get_all_applications()
        
        applied = get_applied_count()

        interviews = get_interview_count()

        offers = get_offer_count()

        rejected = get_rejected_count()
        avg_applied_score = 0
        avg_interview_score = 0
        avg_offer_score = 0
        avg_rejected_score = 0

        applied_scores = []
        interview_scores = []
        offer_scores = []
        rejected_scores = []

        for app in applications:

            if app[3] == "Applied":
                applied_scores.append(app[5])

            elif app[3] == "Interview":
                interview_scores.append(app[5])

            elif app[3] == "Offer":
                offer_scores.append(app[5])

            elif app[3] == "Rejected":
                rejected_scores.append(app[5])


        if applied_scores:
            avg_applied_score = round(sum(applied_scores) / len(applied_scores))

        if interview_scores:
            avg_interview_score = round(sum(interview_scores) / len(interview_scores))

        if offer_scores:
            avg_offer_score = round(sum(offer_scores) / len(offer_scores))

        if rejected_scores:
            avg_rejected_score = round(sum(rejected_scores) / len(rejected_scores))
            
        career_tips = [
            "Customize your resume for every job application.",
            "Keep your resume to one page as a fresher.",
            "Add GitHub links to your projects.",
            "Use action verbs like Developed, Built, and Implemented.",
            "Tailor your skills section for each role."
        ]           

        recent_apps = list(applications[-3:])
        recent_apps.reverse()
        print("DASHBOARD AI:", latest_ai_analysis)
        ai_analysis = latest_ai_analysis if latest_ai_analysis else None
        current_filename = analyzed_filename
        return render_template(
        "dashboard.html",
        applications=applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        avg_applied_score=avg_applied_score,
        avg_interview_score=avg_interview_score,
        avg_offer_score=avg_offer_score,
        avg_rejected_score=avg_rejected_score,
        rejected=rejected,
        recent_apps=recent_apps,
        ai_analysis=ai_analysis,
        analyzed_filename=current_filename
)

@app.route("/applications", methods=["GET", "POST"])
def applications():

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        date_applied = request.form["date_applied"]

        resume = request.files["resume"]
        filename = secure_filename(resume.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        resume.save(filepath)

        doc = fitz.open(filepath)

        text = ""

        for page in doc:
            text += page.get_text()

        resume_score, matched_skills = calculate_resume_score(text)
        skill_match = len(matched_skills) * 10
        skill_match = min(skill_match, 100)

        if isinstance(resume_score, tuple):
            resume_score = resume_score[0]
        print("RESUME SCORE:", resume_score)
        print(type(resume_score))   
        skills = extract_skills(text)
        print(skills)
        print("EXTRACTED SKILLS:", skills)
        global latest_skills
        latest_skills = skills
        add_application(
    company,
    role,
    status,
    date_applied,
    resume_score,
    skill_match,
    filename
)

        return redirect("/applications")

    return render_template("applications.html")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):

    application = get_application_by_id(id)

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]

        update_application(
            id,
            company,
            role,
            status
        )

        return redirect("/dashboard")

    return render_template(
        "edit_application.html",
        application=application
    )
@app.route("/delete/<int:id>")
def delete(id):

    delete_application(id)

    return redirect("/dashboard")
@app.route("/search")
def search():

    keyword = request.args.get("keyword")

    applications = search_applications(keyword)

    applied = get_applied_count()
    interviews = get_interview_count()
    offers = get_offer_count()
    rejected = get_rejected_count()

    return render_template(
        "dashboard.html",
        applications=applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected
    )
    return redirect("/dashboard")
@app.route("/filter/<status>")
def filter_status(status):

    applications = filter_applications(status)

    applied = get_applied_count()
    interviews = get_interview_count()
    offers = get_offer_count()
    rejected = get_rejected_count()

    return render_template(
        "dashboard.html",
        applications=applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        recent_apps=applications[:3]
    )
@app.route("/newest")
def newest():

    applications = sort_newest()

    applied = get_applied_count()
    interviews = get_interview_count()
    offers = get_offer_count()
    rejected = get_rejected_count()

    return render_template(
        "dashboard.html",
        applications=applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        recent_apps=applications[:3]
    )


@app.route("/oldest")
def oldest():

    applications = sort_oldest()

    applied = get_applied_count()
    interviews = get_interview_count()
    offers = get_offer_count()
    rejected = get_rejected_count()
    recent_apps = applications[-3:]
    recent_apps.reverse()
    return render_template(
        "dashboard.html",
        applications=applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        recent_apps=applications[:3]
    )
@app.route("/export")
def export_csv():

    applications = get_all_applications()

    with open("applications.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Company",
            "Role",
            "Status",
            "Date Applied"
        ])

        for app in applications:

            writer.writerow([
                app[1],
                app[2],
                app[3],
                app[4]
            ])

    return redirect("/dashboard")
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

@app.route("/skill_analysis")
def skill_analysis():

    print("SKILL ANALYSIS FUNCTION CALLED")

    global latest_skills

    skills = latest_skills
    print("LATEST SKILLS:", latest_skills)
    print("CURRENT SKILLS:")
    print(skills)
    prompt = f"""
    Analyze these resume skills:

    {skills}

   Give:
1. Resume Score out of 100
2. Strengths
3. Missing Skills
4. Improvement Suggestions
5. Best Job Roles suitable for this candidate

Keep response short and use bullet points.
    """ 
    response = model.generate_content(prompt)
    ai_analysis = None
    analyzed_filename = None
    print("AI ANALYSIS SAVED:")
    print(latest_ai_analysis)
    return render_template(
        "skill_analysis.html",
        skills=skills,
        ai_analysis=response.text
    )

@app.route("/analytics")
def analytics():

    applied = get_applied_count()
    interview = get_interview_count()
    offer = get_offer_count()
    rejected = get_rejected_count()

    return render_template(
        "analytics.html",
        applied=applied,
        interview=interview,
        offer=offer,
        rejected=rejected
    )
@app.route("/analyze_resume", methods=["POST"])
def analyze_resume():
    print("ANALYZE ROUTE CALLED")
    global latest_ai_analysis
    global analyzed_filename

    
    resume = request.files["resume"]
    filename = secure_filename(resume.filename)

    analyzed_filename = filename

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume.save(filepath)

    doc = fitz.open(filepath)

    text = ""

    for page in doc:
        text += page.get_text()
        ats_score, matched_skills = calculate_resume_score(text)

    
    prompt = f"""
Analyze this resume.

Resume Text:
{text}

ATS Score Calculated: {ats_score}/100

Matched Skills:
{', '.join(matched_skills)}

Give the output in this format:

📊 ATS Score:
(Explain the ATS score briefly)

💪 Strengths:
- Point 1
- Point 2
- Point 3

❌ Missing Skills:
- Point 1
- Point 2

🎯 Recommended Job Roles:
- Role 1
- Role 2

🚀 Improvement Suggestions:
- Point 1
- Point 2

Keep the response concise and well formatted.
"""

    print("========== AI RESPONSE ==========")
    
    try:
        response = model.generate_content(prompt)
        latest_ai_analysis = response.text

    except Exception as e:

        if "429" in str(e):
            latest_ai_analysis = """
⚠ Gemini free quota exceeded.

Please wait a few minutes and try again.
"""

        else:
            latest_ai_analysis = f"⚠ AI service error: {str(e)}"

    analyzed_filename = filename

    print("========== SAVED SUCCESSFULLY ==========")
    print(latest_ai_analysis)
    print(analyzed_filename)

    return redirect("/dashboard")

@app.route("/clear_analysis")
def clear_analysis():
    global latest_ai_analysis
    global analyzed_filename

    latest_ai_analysis = "Upload a resume to see AI analysis here."
    analyzed_filename = None

    return redirect("/dashboard")

@app.route("/job_match", methods=["GET", "POST"])

def job_match():
    result = None
    job_description = ""
    

    if request.method == "POST":

        job_description = request.form.get("job_description", "")

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""


        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        print("RESUME:")
        print(resume_text[:500])

        print("JOB DESCRIPTION:")
        print(job_description)

        prompt = f"""
         Compare this resume with the job description.

        Resume:
         {resume_text}

        Job Description:
        {job_description}

        Give:

        1. ATS Match Score out of 100
        2. Matching Skills
        3. Missing Skills
        4. Suggestions to improve the resume

        Keep the response short and professional.
"""

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
    "job_match.html",
    result=result,
    job_description=job_description
)

@app.route("/resume_improvement", methods=["GET", "POST"])
def resume_improvement():

    result = None

    if request.method == "POST":

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
        You are an expert resume reviewer.

        Analyze this resume and give:

        1. Resume strengths
        2. Weak areas
        3. Missing skills
        4. Improvement suggestions
        5. Resume formatting tips

        Keep the response short and professional.

        Resume:

        {resume_text}
    """
        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "resume_improvement.html",
        result=result
    )
@app.route("/interview_questions", methods=["GET", "POST"])
def interview_questions():

    result = None

    if request.method == "POST":

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
You are an experienced technical interviewer.

Based on this resume, generate:

1. 5 Technical Questions
2. 3 HR Questions
3. 2 Project-Based Questions
4. 1 Scenario-Based Question

Keep questions practical and suitable for a fresher.

Resume:

{resume_text}
"""
        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "interview_questions.html",
        result=result
    )
@app.route("/cover_letter", methods=["GET", "POST"])
def cover_letter():

    result = None

    if request.method == "POST":

        job_description = request.form["job_description"]

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
Generate a professional cover letter based on this resume and job description.

Resume:
{resume_text}

Job Description:
{job_description}

Keep it professional and concise.
"""

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "cover_letter.html",
        result=result
    )
@app.route("/job_recommendation", methods=["GET", "POST"])
def job_recommendation():

    result = None

    if request.method == "POST":

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
Analyze this resume and recommend the top 5 suitable job roles.

Resume:
{resume_text}

For each role, provide:

1. Job Role
2. Why it matches the candidate
3. Skills that support this role

Keep the response clear and concise.
"""

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "job_recommendation.html",
        result=result
    )
@app.route("/resume_chatbot", methods=["GET", "POST"])
def resume_chatbot():

    result = None

    if request.method == "POST":

        question = request.form["question"]

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
You are an AI career assistant.

Answer the user's question based only on the resume below.

Resume:
{resume_text}

Question:
{question}

Give a helpful, professional, and concise answer.
"""

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "resume_chatbot.html",
        result=result
    )
@app.route("/learning_roadmap", methods=["GET", "POST"])
def learning_roadmap():

    result = None

    if request.method == "POST":

        target_role = request.form["target_role"]

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
Analyze this resume and create a learning roadmap to become a successful {target_role}.

Resume:
{resume_text}

Provide:

1. Current Strengths
2. Missing Skills
3. Step-by-Step Learning Plan
4. Recommended Projects
5. Useful Certifications

Keep the roadmap practical and beginner-friendly.
"""

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "learning_roadmap.html",
        result=result
    )
@app.route("/resume_summary", methods=["GET", "POST"])
def resume_summary():

    result = None

    if request.method == "POST":

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
Analyze this resume and generate:

1. Professional Summary (3-4 lines)
2. 30-Second Elevator Pitch
3. LinkedIn About Section
4. One-Line Resume Headline

Resume:
{resume_text}

Keep everything professional and suitable for a fresher candidate.
"""

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "resume_summary.html",
        result=result
    )
@app.route("/skill_gap", methods=["GET", "POST"])
def skill_gap():

    result = None

    if request.method == "POST":

        target_role = request.form["target_role"]

        resume = request.files["resume"]

        pdf_reader = PdfReader(resume)

        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        prompt = f"""
        Analyze the following resume for the role: {target_role}

        Give:

        1. Current Skills
        2. Missing Skills
        3. Skills to Learn First
        4. Final Recommendation

        Resume:

        {resume_text}
        """

        response = model.generate_content(prompt)

        result = clean_ai_response(response.text)

        result = result.replace("###", "")
        result = result.replace("##", "")
        result = result.replace("**", "")
        result = result.replace("---", "")
        result = result.replace("`", "")

    return render_template(
        "skill_gap.html",
        result=result
    )
if __name__ == "__main__":
    app.run(debug=True)