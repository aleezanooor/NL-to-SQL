from fastapi import FastAPI
from models.query import Query
from nlp.nlp_engine import parse_query
from db.db import execute_query
from nlp.summarizer import summarize_response
import ollama



model = ollama.chat(model="gemma2:2b")  # You can change this to the appropriate model name

app = FastAPI()

@app.post("/ask")
def ask_db(query: Query):
    print("🔹 Received question:", query.question)

    result = parse_query(query.question)
    print("🔍 Parsed query:", result)

    if result is None:
        print("❌ Parsing failed.")
        return {"error": "Sorry, I didn't understand that."}

    # Execute the query
    if isinstance(result, tuple):
        sql, params = result
        print("🛠 Executing SQL with params:", sql, params)
        data = execute_query(sql, params)
    else:
        print("🛠 Executing SQL:", result)
        data = execute_query(result)

    print("📦 Query result:", data)

    if isinstance(data, dict) and "error" in data:
        print("❌ Database error:", data["error"])
        return data

    # Summarize the result
    print("💬 Summarizing result...")
    summary = summarize_response(data, query.question)
    print("📝 Summary:", summary)

    return {
        "summary": summary,
        "data": data
    }
