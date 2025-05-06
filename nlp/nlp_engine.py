import ollama
from db.valid_queries import valid_queries

def parse_query(user_input: str):
    """
    Use the local LLM to classify the user's intent and map it to a valid SQL query.
    """
    # Define the format for prompting the model
    prompt = f"""
You are a helpful assistant that maps user questions to database intents. Only choose from the following intents:

{list(valid_queries.keys())}

User question: "{user_input}"

Respond with only the matching intent name.
"""

    try:
        # Proper call to Ollama chat
        response = ollama.chat(
            model="gemma2:2b",  # make sure the model name matches what Ollama provides locally
            messages=[{"role": "user", "content": prompt}]
        )

        generated_intent = response["message"]["content"].strip().lower()
        print("LLM responded with intent:", generated_intent)

        # Match to one of the valid queries
        for intent, query in valid_queries.items():
            if intent in generated_intent:
                return query

    except Exception as e:
        print(f"Error during parsing: {e}")

    return None  # fallback if no match
