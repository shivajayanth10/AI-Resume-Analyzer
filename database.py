import sqlite3


def create_database():
    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    role TEXT,
    status TEXT,
    date_applied TEXT,
    resume_score INTEGER,
    skill_match INTEGER,
    resume_file TEXT
)
""")
    conn.commit()
    conn.close()


def register_user(username, password):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username, password)
    )

    conn.commit()
    conn.close()


def validate_user(username, password):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_application(
    company,
    role,
    status,
    date_applied,
    skill_match,
    resume_score,
    resume_file
):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO applications
        (
            company,
            role,
            status,
            date_applied,
            skill_match,
            resume_score,
            resume_file
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            company,
            role,
            status,
            date_applied,
            skill_match,
            resume_score,
            resume_file
        )
    )

    conn.commit()
    conn.close()




def get_all_applications():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM applications
        """
    )

    applications = cursor.fetchall()

    conn.close()

    return applications


def get_applied_count():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Applied'"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_interview_count():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Interview'"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_offer_count():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Offer'"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_rejected_count():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Rejected'"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_application_by_id(id):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM applications WHERE id=?",
        (id,)
    )

    application = cursor.fetchone()

    conn.close()

    return application


def update_application(id, company, role, status):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET company=?, role=?, status=?
        WHERE id=?
        """,
        (company, role, status, id)
    )

    conn.commit()
    conn.close()
def delete_application(id):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()
def search_applications(keyword):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM applications
        WHERE company LIKE ? OR role LIKE ?
        """,
        ('%' + keyword + '%',
         '%' + keyword + '%')
    )

    applications = cursor.fetchall()

    conn.close()

    return applications
def filter_applications(status):

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM applications
        WHERE status=?
        """,
        (status,)
    )

    applications = cursor.fetchall()

    conn.close()

    return applications
def sort_newest():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM applications
        ORDER BY date_applied DESC
        """
    )

    applications = cursor.fetchall()

    conn.close()

    return applications


def sort_oldest():

    conn = sqlite3.connect("resume_analyzer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM applications
        ORDER BY date_applied ASC
        """
    )

    applications = cursor.fetchall()

    conn.close()

    return applications