from fastapi import FastAPI
from models.query import Query
from nlp.nlp_engine import parse_query
from db.db import execute_query
import ollama

model = ollama.chat(model="gemma-2.2b")  # You can change this to the appropriate model name

app = FastAPI()

@app.post("/ask")
def ask_db(query: Query):
    result = parse_query(query.question)
    if result is None:
        return {"error": "Sorry, I didn't understand that."}
    if isinstance(result, tuple):
        sql, params = result
        return execute_query(sql, params)
    else:
        return execute_query(result)