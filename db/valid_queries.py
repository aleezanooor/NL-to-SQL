# db/valid_queries.py

valid_queries = {
    "show_all_users": "SELECT * FROM users;",
    "count_products_in_stock": "SELECT COUNT(*) FROM products WHERE stock > 0;",
    "show_products_in_stock": "SELECT * FROM products WHERE stock > 0;",
    "add_user": (
        "INSERT INTO users (name, email, signup_date) VALUES (?, ?, date('now'))",
        ("John Doe", "john@example.com")  # Default params for example
    ),
}
