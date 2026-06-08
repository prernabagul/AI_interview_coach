import sqlite3

def create_db():

    conn = sqlite3.connect("interviews.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        report TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_interviews(role, report):

    conn = sqlite3.connect("interviews.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interviews(
            role,
            report
        )
        VALUES (?, ?)
        """,
        (role, report)
    )

    conn.commit()
    conn.close()


def get_interviews():

    conn = sqlite3.connect("interviews.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM interviews"
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def total_interviews():

    conn = sqlite3.connect("interviews.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM interviews"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def average_score():

    conn = sqlite3.connect("interviews.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT AVG(overall_score) FROM interviews WHERE overall_score IS NOT NULL"
    )

    avg = cursor.fetchone()[0]

    conn.close()

    if avg is None:
        return 0

    return round(avg, 2)