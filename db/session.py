import sqlite3
import json

def store_analysis_result(filename, features, emotion, lexical, fluency, personality):
    conn = sqlite3.connect("analytics.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                 filename TEXT, features TEXT, emotion TEXT, lexical TEXT,
                 fluency TEXT, personality TEXT)''')

    c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)", (
        filename,
        json.dumps(features),
        json.dumps(emotion),
        json.dumps(lexical),
        json.dumps(fluency),
        json.dumps(personality)
    ))
    conn.commit()
    conn.close()

    