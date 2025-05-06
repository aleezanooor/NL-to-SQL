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
    result = parse_query(query.question)
    if result is None:
        return {"error": "Sorry, I didn't understand that."}

    if isinstance(result, tuple):
        sql, params = result
        data = execute_query(sql, params)
    else:
        data = execute_query(result)

    if isinstance(data, dict) and "error" in data:
        return data

    summary = summarize_response(data, query.question)
    return {
        "summary": summary,
        "data": data
    }