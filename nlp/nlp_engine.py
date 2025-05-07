import json
import ollama
from db.valid_queries import valid_queries
import re

def parse_query(user_input: str):
    """
    Use LLM to classify intent and extract variables for fine-grained SQL queries.
    """
    prompt = f"""
You are a database assistant. Based on the user question, identify:
1. The intent (only one of these): {list(valid_queries.keys())}
2. The required parameters: table name, column name, condition, or row range

Respond only in compact JSON format like:
{{
  "intent": "...",
  "table": "...",
  "column": "...",
  "condition": "...",
  "start": 1,
  "end": 3
}}

Question: "{user_input}"
"""

    try:
        # Send prompt to Ollama model
        response = ollama.chat(
            model="gemma2:2b",
            messages=[{"role": "user", "content": prompt}]
        )

        # Get raw response message
        message = response['message']['content']
        print("🧠 Raw LLM Output:", message)

        # Clean up markdown-style formatting if present
        cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", message).strip()

        # Parse the cleaned message into JSON
        try:
            parsed = json.loads(cleaned.lower())
        except json.JSONDecodeError:
            print("⚠️ Failed to parse LLM output as JSON:", cleaned)
            return None

        # Extract components safely
        intent = parsed.get("intent")
        table = (parsed.get("table") or "").strip()
        column = (parsed.get("column") or "*").strip()
        condition = (parsed.get("condition") or "1=1").strip()
        start = parsed.get("start", 1)
        end = parsed.get("end", 3)

        # Check for essential fields
        if not table or not intent:
            print(f"❌ Missing table or intent. Parsed response: {parsed}")
            return None

        # Retrieve the query template and build the SQL
        query_template = valid_queries.get(intent)
        if query_template:
            sql = query_template.format(
                column=column,
                table=table,
                condition=condition,
                start=start,
                end=end
            )
            print("✅ Final SQL:", sql)
            return sql
        else:
            print(f"❌ No valid query template found for intent: {intent}")
            return None

    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        return None
