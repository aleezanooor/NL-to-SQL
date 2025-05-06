import re

def parse_query(user_input: str):
    user_input = user_input.lower()

    if "show me all users" in user_input or "list users" in user_input:
        return "SELECT * FROM users"

    elif "signed up last week" in user_input:
        return "SELECT * FROM users WHERE signup_date >= date('now', '-7 day')"

    elif "products in stock" in user_input:
        return "SELECT COUNT(*) as total FROM products WHERE stock > 0"

    elif "add a new user" in user_input:
        match = re.search(r"named (\w+).*email (\S+)", user_input)
        if match:
            name, email = match.groups()
            return ("INSERT INTO users (name, email, signup_date) VALUES (?, ?, date('now'))", (name, email))

    return None