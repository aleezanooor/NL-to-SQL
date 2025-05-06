import ollama

def summarize_response(data: list[dict], question: str) -> str:
    """
    Provide a conversational summary of the data based on the original user question.
    """
    # Convert the result into a readable string table (basic version)
    formatted_data = "\n".join([str(row) for row in data[:5]])  # limit to 5 rows to avoid overloading the model

    prompt = f"""
You are a helpful assistant. A user asked: "{question}"

The following rows were retrieved from the database:
{formatted_data}

Provide a short and clear explanation of what this data means, in a friendly tone. Do not return SQL or technical terms.
"""

    try:
        response = ollama.chat(
            model="gemma2:2b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"(Could not summarize data: {e})"
