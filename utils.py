import sqlite3


# Initialize SQLite database and add 10 Walkman records if they don't exist
def init_db():
    conn = sqlite3.connect("walkman.sqlite")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS walkmans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL UNIQUE,
            year INTEGER NOT NULL,
            description TEXT
        )
    """)

    walkman_records = [
        ("WM-D6C", 1984, "High-end recording Walkman"),
        ("WM-EX631", 1999, "Compact and stylish cassette player"),
        ("WM-FX521", 1998, "AM/FM radio and cassette player"),
        ("WM-701C", 1989, "Ultra-slim cassette player with Dolby C"),
        ("WM-R202", 1992, "Recording Walkman with a built-in mic"),
        ("WM-EX655", 2000, "Lightweight and durable with Mega Bass"),
        ("WM-F701C", 1991, "AM/FM Walkman with Dolby C"),
        ("WM-DD9", 1990, "Direct Drive high-fidelity Walkman"),
        ("WM-EX808HG", 1997, "Limited edition high-end Walkman"),
        ("WM-FX290", 2003, "Budget-friendly Walkman with radio"),
    ]

    # Insert only if model does not exist
    for model, year, description in walkman_records:
        cursor.execute("SELECT COUNT(*) FROM walkmans WHERE model = ?", (model,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO walkmans (model, year, description) VALUES (?, ?, ?)",
                           (model, year, description))

    conn.commit()
    conn.close()
