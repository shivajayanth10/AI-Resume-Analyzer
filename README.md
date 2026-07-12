# 🤖 AI Resume Analyzer

An AI-powered web application built using Python and Flask that helps job seekers analyze resumes, identify skill gaps, track job applications, and improve their job search process using AI-powered tools.

## 🌐 Live Demo

🚀 Live Application: https://ai-resume-analyzer-5lu4.onrender.com/dashboard

## 📌 Project Overview

AI Resume Analyzer is a full-stack web application designed to help job seekers manage and improve their job search process.

The application combines resume analysis, job application tracking, analytics, and AI-powered career tools in a single platform.

Users can upload their resumes, analyze skills, track job applications, view application statistics, generate interview questions, create cover letters, receive job recommendations, and interact with an AI resume chatbot.

## ✨ Features

- 📊 Interactive Dashboard
- 📄 Resume Upload and Analysis
- 🧠 Skill Analysis
- 📈 Job Application Analytics
- 🎯 ATS Resume Analyzer
- ✨ AI Resume Improvement Suggestions
- 💬 AI-Generated Interview Questions
- 📝 AI Cover Letter Generator
- 💼 Job Recommendations
- 🤖 AI Resume Chatbot
- 🗺️ Personalized Learning Roadmap
- 📋 AI Resume Summary
- 🔍 Skill Gap Analyzer
- 📁 Job Application Tracker
- 🔎 Search and Filter Applications
- 📥 Export Application Data to CSV
- 📊 Application Status Charts and Resume Score Analytics

## 🛠️ Technologies Used

### Backend

- Python
- Flask
- SQLite
- REST API Integration

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### AI Integration

- Google Gemini API

### Libraries and Tools

- PyMuPDF
- Requests
- Gunicorn
- Git
- GitHub

### Deployment

- Render

## 📊 Dashboard

The interactive dashboard provides an overview of the user's job search progress, including:

- Total job applications
- Applications in progress
- Interviews
- Offers
- Rejections
- Average resume scores
- Application status distribution
- Recent applications
- Career improvement tips

## 🤖 AI-Powered Tools

The application includes several AI-powered features designed to assist job seekers.

### ATS Resume Analyzer

Analyzes a resume against a job description and provides compatibility insights.

### Resume Improvement

Generates AI-powered suggestions to improve resume content and presentation.

### Interview Question Generator

Creates interview questions based on the user's resume and target role.

### Cover Letter Generator

Generates customized cover letters based on resume and job information.

### Job Recommendations

Provides job recommendations based on the user's skills and resume.

### Resume Chatbot

Allows users to ask questions and interact with an AI assistant about their resume.

### Learning Roadmap

Generates a personalized learning roadmap based on the user's career goals and skill gaps.

### Resume Summary

Creates a concise AI-generated professional summary from the uploaded resume.

### Skill Gap Analyzer

Identifies missing skills and provides suggestions for career improvement.

## 📁 Project Structure

AI-Resume-Analyzer/

    static/
        style.css

    templates/
        analytics.html
        applications.html
        cover_letter.html
        dashboard.html
        edit_application.html
        index.html
        interview_questions.html
        job_match.html
        job_recommendation.html
        learning_roadmap.html
        login.html
        register.html
        resume_chatbot.html
        resume_improvement.html
        resume_summary.html
        skill_analysis.html
        skill_gap.html

    uploads/

    app.py
    database.py
    requirements.txt
    .gitignore
    README.md

## ⚙️ Installation and Setup

### 1. Clone the Repository

    git clone https://github.com/shivajayanth10/AI-Resume-Analyzer.git

### 2. Navigate to the Project Directory

    cd AI-Resume-Analyzer

### 3. Create a Virtual Environment

    python -m venv venv

### 4. Activate the Virtual Environment

Windows:

    venv\Scripts\activate

Linux/macOS:

    source venv/bin/activate

### 5. Install Dependencies

    pip install -r requirements.txt

### 6. Configure Environment Variables

Create the required environment variables for the AI API configuration.

Example:

    GEMINI_API_KEY=your_api_key

Never commit API keys or sensitive credentials to GitHub.

### 7. Run the Application

    python app.py

Open the application in your browser.

    http://127.0.0.1:5000

## 🚀 Deployment

The application is deployed using Render.

Deployment configuration:

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

## 🔮 Future Improvements

- User-specific authentication and data management
- PostgreSQL database integration
- Cloud-based resume file storage
- Advanced resume scoring algorithms
- Improved AI recommendations
- Enhanced dashboard analytics
- Automated job matching
- Resume version comparison

## 👨‍💻 Author

**Shiva Jayanth**

B.Tech Computer Science Graduate | Python Developer

## ⭐ Support

If you found this project useful, consider giving the repository a star.